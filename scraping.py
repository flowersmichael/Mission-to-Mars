# Import Splinter, BeautifulSoup, Pandas
import sys
sys.path.append("/opt/anaconda3/envs/python37/lib/python3.7/site-packages")
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

    # Set the executable path and initialize the chrome browser in splinter
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    print ('title is')
    print(news_title)
    print('paragraph')
    print(news_paragraph)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
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
    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    





