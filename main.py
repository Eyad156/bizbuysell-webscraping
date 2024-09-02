from bs4 import BeautifulSoup
import requests
import pandas as pd

# Base URLs without page numbers
BASE_URLS = [
    'https://www.bizbuysell.com/california-businesses-for-sale/?q=bHQ9MzAsNDAsODA%3D',
    'https://www.bizbuysell.com/california-businesses-for-sale/{}/?q=bHQ9MzAsNDAsODA%3D',
    'https://www.bizbuysell.com/illinois/chicago-businesses-for-sale/',
    'https://www.bizbuysell.com/illinois/chicago-metro-area-businesses-for-sale/',
    'https://www.bizbuysell.com/illinois-businesses-for-sale/?q=bHQ9MzAsNDAsODA%3D',
    'https://www.bizbuysell.com/illinois/chicago-ridge-businesses-for-sale/',
    'https://www.bizbuysell.com/new-york/new-york-city-metro-area-businesses-for-sale/'
]

# Function to get page URLs up to 110 pages
def get_page_urls(base_url, total_pages=110):
    page_urls = []
    if '{}' in base_url:
        # If the URL has a placeholder for page numbers
        for i in range(1, total_pages + 1):
            page_urls.append(base_url.format(i))
    else:
        # If there's no placeholder, add the base URL as-is
        page_urls.append(base_url)
    return page_urls

# Initialize a list to store all URLs
all_urls = []

# Populate all URLs for each base URL
for base_url in BASE_URLS:
    all_urls.extend(get_page_urls(base_url))

# List to store the data
data = []

# Loop through all URLs to scrape data
for url in all_urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all business listings on the page (adjust the selector based on actual HTML structure)
        listings = soup.find_all('div', class_='listing')

        # Extract data from each listing
        for listing in listings:
            title = listing.find('h3', class_='listing-title').get_text(strip=True) if listing.find('h3', class_='listing-title') else 'N/A'
            price = listing.find('div', class_='listing-price').get_text(strip=True) if listing.find('div', class_='listing-price') else 'N/A'
            location = listing.find('div', class_='listing-location').get_text(strip=True) if listing.find('div', class_='listing-location') else 'N/A'
            description = listing.find('div', class_='listing-description').get_text(strip=True) if listing.find('div', class_='listing-description') else 'N/A'
            
            # Append the extracted data to the list
            data.append({
                'Title': title,
                'Price': price,
                'Location': location,
                'Description': description
            })

    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save the data to an Excel file
df.to_excel('bizbuysell_listings.xlsx', index=False)
print("Data saved to bizbuysell_listings.xlsx")
