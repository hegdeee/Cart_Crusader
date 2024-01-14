# flip.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import sys

def scrape_flipkart(url):
    driver = None
    try:
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        options.add_argument('--no-sandbox')
        service = ChromeService()

        # Use ChromeDriverManager to automatically download and manage the WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        # Add a delay to allow the page to load (adjust as needed)
        time.sleep(5)

        title_element = driver.find_element(By.XPATH, '//h1[@class="yhB1nd"]')
        product_price_element = driver.find_element(By.XPATH, '//div[@class="_30jeq3 _16Jk6d"]')
        rating_element = driver.find_element(By.XPATH, '//span[@class="_2_R_DZ"]')
        image_element = driver.find_element(By.XPATH, '//img[@class="_396cs4 _2amPTt _3qGmMb"]')
        
        title = title_element.text.strip()
        product_price = product_price_element.text.strip() if product_price_element else 'Price not found'
        rating = rating_element.text.strip() if rating_element else 'Rating not found'
        image_url = image_element.get_attribute('src')

        print(f'Product Title: {title}')
        print(f'Product Price: {product_price}')
        print(f'Product Rating: {rating}')
        print(f'Image URL: {image_url}')

        return {
            'title': title,
            'product_price': product_price,
            'rating': rating,
            'image_url': image_url
        }

    except Exception as e:
        print(f'Error during scraping: {e}')

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Check if a command-line argument (URL) is provided
    if len(sys.argv) != 2:
        print("Usage: python flip.py <flipkart_url>")
        sys.exit(1)

    # Get the Flipkart URL from the command-line argument
    flipkart_url = sys.argv[1]

    scraped_data_flipkart_selenium = scrape_flipkart(flipkart_url)

    if scraped_data_flipkart_selenium:
        # Open the file in write mode with the 'w' flag to overwrite
        with open('flipkart_data.json', 'w') as json_file:
            json.dump(scraped_data_flipkart_selenium, json_file)
