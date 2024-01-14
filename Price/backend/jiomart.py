from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import sys
def scrape_jiomart_product(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Wait for the dynamic content to load (adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'largeimage')))

        # Extract data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_element = soup.find('div', {'class': 'product-header-name jm-mb-xs jm-body-m-bold'})
        product_price_element = soup.find('span', {'class': 'jm-heading-xs jm-ml-xxs'})
        rating_element = soup.find('span', {'class': 'review-count jm-body-m-bold jm-fc-primary-60 jm-pl-xs'})
        image_element = soup.find('img', {'class': 'largeimage swiper-slide-img lazyautosizes lazyloaded'})

        if title_element:
            title = title_element.get_text(strip=True)
            product_price = product_price_element.get_text(strip=True) if product_price_element else 'Price not found'
            rating = rating_element.get_text(strip=True) if rating_element else 'Rating not found'

            # Check if the image element is present
            if image_element:
                image_url = image_element.get('src', '')

                print(f'Product Title: {title}')
                print(f'Product Price: {product_price}')
                print(f'Product Rating: {rating}')
                print(f'Image URL: {image_url}')

                # Return a dictionary with the scraped data
                return {
                    'title': title,
                    'product_price': product_price,
                    'rating': rating,
                    'image_url': image_url
                }
            else:
                print('Image element not found on the page.')
        else:
            print('Product Title not found on the page.')

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python flip.py <jiomart_url>")
        sys.exit(1)

    jiomart_url = sys.argv[1]
    scraped_data = scrape_jiomart_product(jiomart_url)

    if scraped_data:
        # Open the file in write mode with the 'w' flag to overwrite
        with open('jiomart_data.json', 'w') as json_file:
            # Use the indent parameter for better readability
            json.dump(scraped_data, json_file, indent=2)