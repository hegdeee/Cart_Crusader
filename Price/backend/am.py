import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
from selenium.webdriver.chrome.options import Options

def get_amazon_link(product_name):
    try:
        encoded_product_name = urllib.parse.quote_plus(product_name)
        amazon_url = f'https://www.amazon.in/s?k={encoded_product_name}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        time.sleep(2)
        response = requests.get(amazon_url, headers=headers)
        
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first search result on Amazon
        first_result = soup.find('div', {'data-component-type': 's-search-result'})
        if first_result:
            # Extract the URL from the first result
            first_result_link = urllib.parse.urljoin('https://www.amazon.in/', first_result.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href'])
            print(first_result_link)
            return first_result_link

    except requests.exceptions.RequestException as e:
        print(f'Error during Amazon search: {e}')

    return None

def get_flipkart_link_selenium(product_name, base_url='https://www.flipkart.com/'):
    try:
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)

        # Navigate to the search page on Flipkart
        encoded_product_name = urllib.parse.quote_plus(product_name)
        full_url = f'{base_url}search?q={encoded_product_name}'
        driver.get(full_url)

        # Wait for the page to load and for the first result to be present on Flipkart
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2kHMtA')))

        # Get the first result link on Flipkart
        first_result_link = driver.find_element(By.CSS_SELECTOR, 'div._2kHMtA a._1fQZEK').get_attribute('href')
        print(first_result_link)
        return first_result_link
    except requests.exceptions.RequestException as e:
        print(f'Error during Amazon search: {e}')
    
    
def get_jiomart_link_selenium(product_name, base_url = "https://www.jiomart.com"):
    try:
        # Set up Chrome WebDriver in headless mode
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Navigate to the search page on JioMart
        encoded_product_name = urllib.parse.quote_plus(product_name)
        full_url = f'{base_url}/search?q={encoded_product_name}'
        driver.get(full_url)

        # Wait for the page to load and for the first result to be present on JioMart
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="algolia_hits"]/div/ol/li[1]')))
        first_result_link = driver.find_element(By.CSS_SELECTOR, 'li.ais-InfiniteHits-item a').get_attribute('href')
        print(first_result_link)
        return first_result_link

    finally:
        # Close the WebDriver
        driver.quit()



#if __name__ == "__main__":
    # Get the product name from the user
    #product_name = input("Enter the product name: ")

    # Get links from Amazon and Flipkart
    #amazon_link = get_amazon_link(product_name)
    #flipkart_link = get_flipkart_link_selenium(product_name)

   # if amazon_link:
   #     print(f'Amazon URL: {amazon_link}')
   # else:
    #    print('No results found on Amazon.')

   # if flipkart_link:
    #    print(f'Flipkart URL: {flipkart_link}')
   # else:
    #    print('No results found on Flipkart.'