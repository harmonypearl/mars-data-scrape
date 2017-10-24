#dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import html5lib


#create a function that will run mars data scrape and return dictionary of scraped data
def scrape():

    #create an empty dictionary to store all mars scraped data
    mars_data_dict = {}



        # NASA Mars News

    #retrieve page to be scraped
    with Browser() as browser:
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        news_html = browser.html
        
        #create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(news_html, 'html.parser')

        #examine the results, then determine element that contains desired info
        #results are returned as an iterable list
        results = soup.find_all('div', class_ = 'list_text')

    #create empty lists for article title and article teaser
    news_titles = []
    news_paras = []

    #loop through results to scrape desired info
    for result in results:
        
        #error handling
        try:
            
            #retrieve article title and add to titles list
            title = result.find('a').text
            news_titles.append(title)

            #retrieve article teaser and add to teasers list
            para = result.find('div', class_ = 'article_teaser_body').text
            news_paras.append(para)

        except:
            print('error')

    #store latest article scraped data in variables and add to mars data dict
    news_t = news_titles[0]
    news_p = news_paras[0]
    mars_data_dict['news_title'] = news_t
    mars_data_dict['news_para'] = news_p



        # JPL Mars Space Images - Featured Image

    #url for jpl main site
    jpl_url = 'https://www.jpl.nasa.gov'

    #retrieve page to be scraped
    with Browser() as browser:
        url = jpl_url + '/spaceimages/?search=&category=Mars'
        browser.visit(url)
        image_html = browser.html
        
        #create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(image_html, 'html.parser')

        #examine the results, then determine element that contains desired info
        #results are returned as an iterable list
        results = soup.find_all('div', class_ = 'carousel_items')

    #loop through results to scrape featured image data
    for result in results:

        #error handling
        try:
            
            #retrieve and print image title & description
            image_title = result.find('h1', class_ = 'media_feature_title').text  
            image_descript = result.a['data-description']

            #retrieve image link and print full image url
            image_link = result.a['data-fancybox-href']
            featured_image_url = jpl_url + image_link
        
        except:
            print('error')

    #add featured image data to mars data dict
    mars_data_dict['featured_image_title'] = image_title
    mars_data_dict['featured_image_descript'] = image_descript
    mars_data_dict['featured_image_url'] = featured_image_url



        # Mars Weather

    #retreive page to be scraped
    with Browser() as browser:
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        weather_html = browser.html
        
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(weather_html, 'html.parser')

    #examine the results, then determine element that contains desired info
    #results are returned as an iterable list
    results = soup.find('div', class_='js-tweet-text-container')

    #retrieve weather tweet and add to mars data dict
    mars_weather = results.find('p').text
    mars_data_dict['mars_weather'] = mars_weather



        # Mars Facts

    #url for page to be scraped
    fact_url = 'https://space-facts.com/mars/'

    #read the table from the page
    fact_table = pd.read_html(fact_url)

    #create a dataframe from the first (and in this case,only) table
    fact_df = fact_table[0]
    fact_df.columns = ['Quantity', 'Value']

    #generate HTML table from dataframe and strip newlines
    fact_html = fact_df.to_html().replace('\n', '')

    #add fact data HTML to mars data dict
    mars_data_dict['mars_facts'] = fact_html



        # Mars Hemispheres

    #create a list of urls for pages to be scraped
    hemi_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
                ]

    #create dict key list and empty list for dict values
    dict_keys = ['title', 'img_url']
    dict_values = []

    #create an empty list to add dicts of each title & image url 
    hemisphere_image_urls = []

    #url for usgs main site
    usgs_url = 'https://astrogeology.usgs.gov'

    #loop through each url to retrieve individual pages to scrape
    for item in hemi_urls:

        #error handling
        try:
            
            #retireive page to be scraped
            with Browser() as browser:
                url = item
                browser.visit(url)
                hemi_html = browser.html

            #create BeautifulSoup object; parse with 'html.parser'
            soup = BeautifulSoup(hemi_html, 'html.parser')

            #examine the results, then determine element that contains image title
            #results are returned as an iterable list
            title_results = soup.find('h2', class_ = 'title')

            #loop through results to retrieve title data, add to values list 
            for result in title_results:
                
                #error handling
                try:
                
                    hemi_title = title_results.text
                    dict_values.append(hemi_title)

                except:
                    print('error')
                    
            #examine the results, then determine element that contains image link
            #results are returned as an iterable list
            link_results = soup.find_all('img', class_ = 'wide-image')

            #loop through results to retrieve image link, add to values list
            for result in link_results:
                
                #error handling
                try:
                
                    hemi_link = result['src']
                    hemi_image_url = usgs_url + hemi_link
                    dict_values.append(hemi_image_url)  
                
                except:
                    print('error')
                    
            #create a dict for each title/url pair and add to list     
            hemi_dict = dict(zip(dict_keys, dict_values))
            hemisphere_image_urls.append(hemi_dict)
            
            
        except:
            print('error')   
            
    #add hemisphere image data to mars data dict
    mars_data_dict['hemisphere_image_data'] = hemisphere_image_urls

    return mars_data_dict