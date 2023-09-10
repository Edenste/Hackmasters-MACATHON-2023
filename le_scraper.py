import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_ozbargain():
    #URL of the OzBargain deals page url
    url = 'https://www.ozbargain.com.au/deals'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # \elements containing deal information
        deal_elements = soup.find_all('div', class_='node-ozbdeal')

        # dictionary to store the deals by category
        deals_data = {}

        # Iterate through deal elements and extract relevant information
        for deal_element in deal_elements:
            title = deal_element.find('h2').text.strip()
            link = 'https://www.ozbargain.com.au' + deal_element.find('a')['href']
            
            #'price' element is present
            price_element = deal_element.find('span', class_='price')
            price = price_element.text.strip() if price_element else 'Price not available'
            
            #'submitted' element is present
            submitted_element = deal_element.find('span', class_='submitted')
            posted_by = submitted_element.text.strip() if submitted_element else 'Posted by unknown'

            # Extract description 
            description_element = deal_element.find('p')
            description = description_element.text.strip() if description_element else ''

            # Extract upvotes
            upvote_element = deal_element.find('span', class_='voteup')
            upvotes = int(upvote_element.text.strip()) if upvote_element else 0

            # Ge current date
            current_date = datetime.now().strftime('%Y-%m-%d')

            #dictionary
            deal = {
                'title': title,
                'description': description, 
                'upvotes': upvotes,   
                'link': link,
                'date': current_date,
            }

            # Determine the category (how???)
            category = 'Other'  # Default category 
            if 'Groceries' in title:
                category = 'Groceries'
            elif 'Gaming' in title:
                category = 'Gaming'

            # Append the deal dictionary to the corresponding category
            if category not in deals_data:
                deals_data[category] = []
            deals_data[category].append(deal)

        # Save the deals_data dictionary as a JSON file with the current date in the name
        json_file_name = f'{datetime.now().strftime("%Y-%m-%d")}.json'
        json_directory = "./json_files/" + json_file_name
        with open(json_directory, 'w', encoding='utf-8') as json_file:
            json.dump(deals_data, json_file, ensure_ascii=False, indent=4)

        print(f'Scraped and saved deals to {json_file_name}')
        return json_file_name
    else:
        print('Failed to retrieve the web page.')

scrape_ozbargain()