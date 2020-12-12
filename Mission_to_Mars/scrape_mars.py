# Dependencies

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setting ChromeDriveManager to visit the site and get the code
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)


    news_tit = ""
    news_par = ""
    browser.visit("https://mars.nasa.gov/news")

    #Looping loading the page and getting the title and paragraph until get some result.
    while news_tit == "" or news_par == "":
        html = browser.html
        soup = bs(html, "html.parser")
        try:
            #Set the second element of the list becuase the first isn´t a new
            news_tit = soup.find_all("div",class_="content_title")[1].text.strip()
            news_par =  soup.find("div",class_="article_teaser_body").text.strip()
        except:
            news_tit = ""
            news_par = ""
    #     except:
    #         news_paragraph = ""


    # In[5]:


    #Printing results
    print(news_tit)
    print(news_par)


    # # Scraping for JPL Mars Space Images - Featured Image

    # In[6]:


    # Set site to be scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(images_url)

    html = browser.html
    images_soup = bs(html, 'html.parser')




    # Retrieve image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path
    print(featured_image_url)


    # # Scraping for Mars Facts


    # Set link to be scraped with pandas
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    tables



    # Build a two columns table with the table scraped and set into a df
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df


    # In[13]:


    # Get the html code for the table and clean the \n
    mars_html_table = mars_facts_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')
    mars_html_table


    # # Scrap por Mars hemispheres data

    # In[21]:


    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    hemispheres_soup = bs(hemispheres_html, 'html.parser')


    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

    print(mars_hemispheres)
    print(hemisphere_image_urls)


    mars_dict = {
            "news_title": news_tit,
            "news_p": news_par,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }
    mars_dict



    return mars_dict