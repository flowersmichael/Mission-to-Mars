# Import Sys, Splinter, BeautifulSoup, Pandas, Datetime
import sys
sys.path.append("/opt/anaconda3/envs/python37/lib/python3.7/site-packages")
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# Create scrape_all function
def scrape_all():

    # Set the executable path and initialize the chrome browser in splinter
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# Scrape Mars News

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'


# ### Mars Facts

def mars_facts():
    #Add try/except for error handling
    try:
        # Use 'read_html' to scrape facts table from space-facts.com/mars as DataFrame
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert DataFrame to HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# ### Scrape hemisphere
    
def mars_hemispheres(browser):
    # Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        # Create empty dictionary
        hemispheres = {}
        # Click on hemisphere link
        browser.find_by_css('a.product-item h3')[i].click()
        # Navigate to full-resolution image page
        element = browser.links.find_by_text('Sample').first
        # Navigate to full-res image
        img_url = element['href']
        # Navigate to image title
        title = browser.find_by_css("h2.title").text
        # Save full-resolution image URL string as value for img_url key
        hemispheres["img_url"] = img_url
        # Save hemisphere image title as value for title key
        hemispheres["title"] = title
        # Before getting the next image URL and title, add the dictionary with the image URL string and
        # the hemisphere image title
        hemisphere_image_urls.append(hemispheres)
        # Go back on browser
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    