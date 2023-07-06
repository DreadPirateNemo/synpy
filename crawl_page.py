import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Function to extract email addresses from a text
def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

# Function to crawl a webpage and its subdirectories
def crawl_page(url, base_url, file):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the text on the webpage
    text = soup.get_text()

    # Extract email addresses from the text
    emails = extract_emails(text)

    # Write the extracted email addresses to the file
    for email in emails:
        file.write(email + '\n')

    # Find all the links on the webpage
    links = soup.find_all('a')

    # Visit each link recursively
    for link in links:
        href = link.get('href')
        absolute_url = urljoin(base_url, href)
        if absolute_url.startswith(base_url) and not href.startswith('#'):
            crawl_page(absolute_url, base_url, file)

# URL of the main page to start crawling
main_page_url = input('Enter a URL: ')

# Send a GET request to the main page
main_page_response = requests.get(main_page_url)

# Create a BeautifulSoup object to parse the HTML content
main_page_soup = BeautifulSoup(main_page_response.content, 'html.parser')

# Find the base URL of the main page
base_url = main_page_response.url

# Open a file to write the extracted email addresses
output_file = open('email_addresses.txt', 'w')

# Crawl the main page and its subdirectories
crawl_page(main_page_url, base_url, output_file)

# Close the output file
output_file.close()
