from flask import Flask, render_template, request, jsonify
from am import get_amazon_link, get_flipkart_link_selenium,get_jiomart_link_selenium
import json
import os

import subprocess

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search():
    data = request.json  # Get the JSON data from the request
    product_name = data.get('productName', '')

    
    amazon_link = get_amazon_link(product_name)

    flipkart_link = get_flipkart_link_selenium(product_name)
    
    jiomart_link=get_jiomart_link_selenium(product_name)
    
    if amazon_link:
        os.system(f'python price.py {amazon_link}')
    if flipkart_link:
        os.system(f'python flip.py {flipkart_link}')
    if jiomart_link:
        os.system(f'python jiomart.py {jiomart_link}')
    
    
    return jsonify({'amazonLink': amazon_link, 'flipkartLink': flipkart_link , 'jiomartLink':jiomart_link})

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/12")

def home():
    try:
        # Run the price.py script to scrape the data and create the JSON files
        # os.system('python price.py')
        # os.system('python flip.py')

        # Load the scraped data from the JSON files
        with open('amazon_data.json', 'r') as amazon_file, open('flipkart_data.json', 'r') as flipkart_file, \
                open('jiomart_data.json', 'r') as jiomart_file:
            amazon_data = json.load(amazon_file)
            flipkart_data = json.load(flipkart_file)
            jiomart_data = json.load(jiomart_file)

        # Calculate the smallest price and platform
        smallest_platform = None
        smallest_price = None

        # Check if the prices exist and find the smallest one
        if 'product_price' in amazon_data:
            # Remove currency symbol and commas before converting
            amazon_price = float(amazon_data['product_price'].replace('₹', '').replace(',', ''))
            smallest_platform = 'Amazon'
            smallest_price = amazon_price

        if 'product_price' in flipkart_data:
            # Remove currency symbol and commas before converting
            flipkart_price = float(flipkart_data['product_price'].replace('₹', '').replace(',', ''))
            if smallest_price is None or flipkart_price < smallest_price:
                smallest_platform = 'Flipkart'
                smallest_price = flipkart_price

        if 'product_price' in jiomart_data:
            # Remove currency symbol and commas before converting
            jiomart_price = float(jiomart_data['product_price'].replace('₹', '').replace(',', ''))
            if smallest_price is None or jiomart_price < smallest_price:
                smallest_platform = 'JioMart'
                smallest_price = jiomart_price

        # Render the template with both sets of scraped data
        return render_template('content.html', amazon_data=amazon_data, flipkart_data=flipkart_data,
                               jiomart_data=jiomart_data, smallestPlatform=smallest_platform, smallestPrice=smallest_price)

    except FileNotFoundError:
        # Handle the case where one or both JSON files are not found
        return render_template('content.html', amazon_data=None, flipkart_data=None, jiomart_data=None)


if __name__ == '__main__':
    app.run(debug=True)
