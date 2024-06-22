#%% Import Dependencies
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  

def replace_none(value, default='NA'):
    try:
        value = value[0]
        result = value if value is not None and value != '' else default
        return result
    except:
        return default

def get_source_after_render(url):
    '''
    This function gets the webpage's source html but opens the webpage first so all JavaScript
    renders correctly, unlike when using the requests library. It is slower.
    '''
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  

        page_source = driver.page_source 
    finally:
        driver.quit()

    return page_source

def get_list_of_element_texts(soup, id):
    tags = soup.select(id)
    if tags:
        extracted_texts = [tag.get_text() for tag in tags]
        return extracted_texts


def get_cat_list(url):
    '''
    This function obtains the list of cats up for adoption right now at the Boulder 
    Humane Society.
    '''
    page_source = get_source_after_render(url)

    if page_source:
        soup = BeautifulSoup(page_source, 'html.parser')
        
        cat_ids = get_list_of_element_texts(soup, 'p.agr-field-id')

        return cat_ids

    

def get_cat_data(cat_id):
    '''
    This function gets the individual cat data and returns a dict
    '''
    url = f'https://boulderhumane.org/animals/?animalid={cat_id[5:]}'

    response = get_source_after_render(url)

    if response:
        soup = BeautifulSoup(response, 'html.parser')

        # Get each list of cat data
        cat_names = get_list_of_element_texts(soup, 'td.ad-field-AnimalName')
        cat_weights = get_list_of_element_texts(soup, 'td.ad-field-BodyWeight')
        cat_breeds = get_list_of_element_texts(soup, 'td.ad-field-PrimaryBreed')
        cat_ages = get_list_of_element_texts(soup, 'td.ad-field-Age')
        cat_sexes = get_list_of_element_texts(soup, 'td.ad-field-Sex')
        cat_description = get_list_of_element_texts(soup, 'td.ad-field-description')
        page_urls = [url]

        images = soup.find_all('img', id='animal-picture')
        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        
        try:
            availabilty = get_list_of_element_texts(soup, 'p.animal-banner-adoptme-view')
        except:
            availabilty = get_list_of_element_texts(soup, 'p.animal-banner-onhold-view')
        
        try:
            dict = {'name': replace_none(cat_names), 
                    'availability': replace_none(availabilty),
                    'weight': replace_none(cat_weights), 
                    'breed': replace_none(cat_breeds), 
                    'age': replace_none(cat_ages), 
                    'sex': replace_none(cat_sexes), 
                    'desc': replace_none(cat_description), 
                    'img': replace_none(image_urls),
                    'url': replace_none(page_urls),}

            return dict
        except Exception as e:
            print(f'Error for {cat_id}:{e}')
            return None



def run_get_cat_data(url):
    '''
    This function runs get_cat_list on each Animal ID we obtained concurrently and returns 
    a list of dicts
    '''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cat_ids = get_cat_list(url)
        cat_data = executor.map(get_cat_data, cat_ids)
        cat_data = [cat for cat in cat_data if cat is not None]
        return cat_data
    

def html_widget_generator(df_row, widget_title):
    '''
    This function builds the html that makes up the cat widgets
    '''
    html = f"""
        <a href="{df_row['url']}" style="text-decoration: none; color: black;" target="_blank">
            <div style="display: flex; align-items: center; padding: 10px; border: 1px solid #ddd; margin-bottom: 10px; border-radius: 10px; background-color: #f0f2f6;">
                <div>
                    <h3 style="margin: 0; padding: 2px; font-size: 1.2em;">{widget_title}</h3>
                    <p style="margin: 0; color: #333333;"><b>Name:</b> {df_row['name']}</p>
                    <p style="margin: 0; color: #333333;"><b>Breed:</b> {df_row['breed']}</p>
                    <p style="margin: 0; color: #333333;"><b>Age:</b> {df_row['age']}</p>
                    <p style="margin: 0; color: #333333;"><b>Weight:</b> {df_row['weight']}</p>
                    <br>
                    <p style="margin: 0; color: #333333;">{df_row['desc']}</p>
                </div>
                <img src="{df_row['img']}" alt="News Image" style="width: auto; height: 300px; margin-left: 20px; border-radius: 8px;">
            </div>
        </a>
    """
    return html
