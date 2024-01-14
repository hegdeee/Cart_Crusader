import requests
from bs4 import BeautifulSoup
import json
import re
import ast
import time
import sys

def scrape_amazon_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    try:
        # Add a delay before making the request
        time.sleep(5)

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('span', {'id': 'productTitle'})
        product_price_element = soup.find('span', {'class': 'a-price-whole'})
        rating_element = soup.find('span', {'id': 'acrCustomerReviewText'})
        image_element = soup.find('img', {'id': 'landingImage'})

        if title_element:
            title = title_element.get_text(strip=True)
            product_price = product_price_element.get_text(strip=True) if product_price_element else 'Price not found'
            rating = rating_element.get_text(strip=True) if rating_element else 'Rating not found'

            # Check if the image element is present
            if image_element:
                # Extract the data-a-dynamic-image attribute
                dynamic_image_data = image_element.get('data-a-dynamic-image', '{}')
                # Convert the data attribute string to a dictionary using ast.literal_eval
                image_data_dict = ast.literal_eval(dynamic_image_data)
                # Get the first URL in the dictionary (original resolution)
                image_url = next(iter(image_data_dict))

                print(f'Product Title: {title}')
                print(f'Product Price: {product_price}')
                print(f'Product Rating: {rating}')
                print(f'Image URL: {image_url}')

                # Scrape the first two negative reviews
                negative_reviews = scrape_negative_reviews(soup)
                print('First two negative reviews:')
                for i, review in enumerate(negative_reviews[:2], start=1):
                    print(f'{i}. {review}')

                # Return a dictionary with the scraped data
                return {
                    'title': title,
                    'product_price': product_price,
                    'rating': rating,
                    'image_url': image_url,
                    'negative_reviews': negative_reviews
                }
            else:
                print('Image element not found on the page.')
        else:
            print('Product Title not found on the page.')

    except requests.exceptions.RequestException as e:
        print(f'Error during request: {e}')

def scrape_negative_reviews(soup):
    # Find the review elements
    review_elements = soup.find_all('div', class_='a-section review aok-relative')

    # Extract text from the negative reviews
    negative_reviews = []

    for review in review_elements:
        rating_span = review.find('span', {'data-action': 'review-summary-rating'})
        if rating_span and '2 stars' in rating_span.get_text(strip=True):
            review_text = review.find('span', {'data-action': 'review-body'}).get_text(strip=True)
            negative_reviews.append(review_text)

    return negative_reviews


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python price.py <amazon_url>")
        sys.exit(1)

    amazon_url = sys.argv[1]
    print(sys.argv[1])
    scraped_data = scrape_amazon_product(amazon_url)

    if scraped_data:
        with open('amazon_data.json', 'w') as json_file:
            json.dump(scraped_data, json_file, indent=2)
