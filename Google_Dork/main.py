import time

import requests
from datetime import datetime, timedelta
import isHacked

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("dictionary.txt", 'r', encoding='utf-8') as dict:
         keywords = dict.read().splitlines()

import re
import requests
import time

def google_search(query):
    base_url = "https://www.google.com/search"
    params = {
        "q": query
    }

    israeli_urls = []
    response = requests.get(base_url, params=params, headers=isHacked.headers, verify=False)


    if response.status_code == 200:
        # Extract and print search results using regular expressions
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)

        for url in urls:
            if "co.il" in url and "http" in url and "google" not in url:
                print(url)
                if url not in israeli_urls:
                    url = isHacked.process_url(url,response)
                    if url is not None:
                        with open("israeli_urls.txt", 'a', encoding='utf-8') as file:
                            file.write(str(url) + "\n")
                time.sleep(1)
    else:
        print(f"Error: Unable to perform the search for {query} status: {response.status_code}")

if __name__ == "__main__":
    for keyword in keywords:
        query = f"{keyword} intext:hack"
        # Set the desired date in MM/DD/YYYY format
        google_search(query)
        print(f"Search for keyword: {keyword} is DONE!")
