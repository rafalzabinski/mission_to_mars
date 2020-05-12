

#Imports

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#driver = Browser('chrome', **executable_path, headless=False)
driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')


def scrape():

    dict = {}

#News_title and Paragraph

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    title = soup.find('div', class_='content_title').get_text(strip=True)
    paragraph = soup.find('div', class_='rollover_description_inner').get_text(strip=True)
    dict['title'] = title
    dict['paragraph'] = paragraph

    #Scraping the Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    fancybox = soup.select('li.slide a.fancybox')
    links =[]
    for i in fancybox:
        links.append(i.get('data-fancybox-href'))

    main_url = "https://www.jpl.nasa.gov"

    mars_img_url = main_url + links[14]
    #driver.close()
    dict['mars_img_url'] = mars_img_url

    #Scraping last weather tweet

    #driver = webdriver.Chrome()
    url = 'https://twitter.com/MarsWxReport'
    driver.get(url)
    html = driver.page_source
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    tweet = soup.find('span', {'class':"css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})
    text = soup.find(class_='tweet-text').get_text()
    tweet = text.replace("\n"," ")
    #driver.close()
    dict['weather_tweet'] = tweet

    #Mars Facts - Table scraping

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table.to_html("mars.html",index=False, header= False)
    #dict["html_table"] = mars_table

    #Mars Hemispheres

    hemisphere_image_urls = []
    main_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/"
    hemispheres = ["cerberus", "schiaparelli","syrtis_major","valles_marineris"]

    for hemisphere in hemispheres:
        url = main_url + hemisphere + "_enhanced"
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a',target="_blank",href=True):
            if a.text: 
                links.append(a['href'])
            img_url = links[-1]
        title = soup.find('h2', class_="title").text
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    dict['hemisphere_image_urls'] = hemisphere_image_urls
    driver.close()
    return dict


#driver.close()
#print("yep")
#print(title)
#print(paragraph)
#print(mars_img_url)
#print(tweet)
#print(hemisphere_image_urls)
#print("that's all folks!")