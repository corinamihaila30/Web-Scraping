import re
from bs4 import BeautifulSoup
import requests


def scrape_address(url):
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=custom_headers)
    txt = response.text

    if 'embcmonroe.org' in url:
        addresses = scrape_embcmonroe_address(txt)
    elif 'sk4designs.com' in url:
        addresses = scrape_sk4designs_address(txt)
    elif 'seedsourceag.com' in url:
        addresses = scrape_seedsourceag_address(txt)
    else:
        addresses = []

    return addresses


def scrape_embcmonroe_address(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    address_element = soup.find(class_='contact-text')

    if address_element:
        address = address_element.get_text(strip=True)
        if address:
            return [address]
    return []


def scrape_sk4designs_address(html_text):
    txt2 = html_text.upper()
    addresses = re.findall(r"PO BOX [0-9]+ [A-Z]+,* [A-Z]{2} [0-9]*", txt2)
    return addresses


def scrape_seedsourceag_address(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    address_elements = soup.find_all('p', class_='address')

    addresses = []
    for element in address_elements:
        address = element.get_text(strip=True)
        if address:
            addresses.append(address)

    return addresses


def main():
    urls = ['https://embcmonroe.org/', 'https://sk4designs.com/', 'https://www.seedsourceag.com/']

    for url in urls:
        addresses = scrape_address(url)
        print(f"Addresses found for {url}:")
        if addresses:
            for address in addresses:
                print(address)
        else:
            print("No addresses found")


if __name__ == "__main__":
    main()
