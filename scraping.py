# import required libraries 
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# prepare lists to store the extracted data
productName = [] # to store product names
productPrice = [] # to store product prices
seller = [] # to store seller names
city = [] # to store the city of the seller
unitSold = [] # to store the number of units sold
rating = [] # to store product ratings

# create driver variable filled with webdriver class
# since I'm using Edge, we need initialize a web driver for Microsoft Edge
driver = webdriver.Edge()

# loop through pages 2 to 13 to scrape data
for page in range(2, 13):
    # load the webpage for the current page number
    driver.get(f"https://www.tokopedia.com/search?navsource=&page={page}&q=seblak&search_id=202412110649080230A2C77D199C23EDP5&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=")

    # pause for 2 seconds to allow the page to load completely
    time.sleep(2)

    # get the page's HTML content
    html = driver.page_source

    # parse the HTML content using BeautifulSoup package
    page = BeautifulSoup(html, "html.parser")

    # find all product-related elements on the page
    rows = page.find_all("div", {"class": "WABnq4pXOYQihv0hUfQwOg=="})

    # loop through each product element to extract details
    for row in rows:
        # extract specific details for each product
        namaProduk = row.find("span", {"class": "_0T8-iGxMpV6NEsYEhwkqEg=="})
        hargaProduk = row.find("div", {"class": "_67d6E1xDKIzw+i2D2L0tjw=="})
        penjual = row.find("span", {"class": "T0rpy-LEwYNQifsgB-3SQw=="})
        kotaToko = row.find("span", {"class": "pC8DMVkBZGW7-egObcWMFQ== flip"})
        banyakTerjual = row.find("span", {"class": "se8WAnkjbVXZNA8mT+Veuw=="})
        ratingProduk = row.find("span", {"class": "_9jWGz3C-GX7Myq-32zWG9w=="})

        # check if each detail exists. if it does, then extract its text content or add 'None' if unavailable
        if namaProduk != None:
            # macthing content to condition
            # create a new variable filled with whitespace-removed content using .strip() method
            content = namaProduk.get_text().strip()

            # if available, append to list
            productName.append(content)
        else:
            productName.append(None)

        if hargaProduk != None:
            productPrice.append(hargaProduk.get_text().strip())
        else:
            productPrice.append(None)

        if penjual != None:
            seller.append(penjual.get_text().strip())
        else:
            seller.append(None)

        if kotaToko != None:
            city.append(kotaToko.get_text().strip())
        else:
            city.append(None)

        if banyakTerjual != None:
            unitSold.append(banyakTerjual.get_text().strip())
        else:
            unitSold.append(None)

        if ratingProduk != None:
            rating.append(ratingProduk.get_text().strip())
        else:
            rating.append(None)

# create a DataFrame to organize the extracted data
df = pd.DataFrame()

# populate the DataFrame with extracted data
df['productName'] = productName
df['productPrice'] = productPrice
df['seller'] = seller
df['city'] = city
df['unitSold'] = unitSold
df['rating'] = rating

# save the extracted data to a CSV file
df.to_csv('result.csv', index=False)
