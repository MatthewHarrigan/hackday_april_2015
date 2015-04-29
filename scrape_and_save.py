import bs4
import csv
import re
import requests

# set tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab 

def get_links():
    page = open('google_food_results_page.html', 'r')
    soup = bs4.BeautifulSoup(page)
    return [a.attrs.get('href') for a in soup.select('h3.r a[href^=http://www.bbc]')]

links = get_links()
rows = []
for link in links:
    response = requests.get(link)

    soup  = bs4.BeautifulSoup(response.text)

    str = soup.select('div#description')
    str = str[0].text
    num = '(\d*\.?\dg* kcal|\d*\.?\dg* protein|\d*\.?\dg* carbohydrate|\d*\.?\dg* fat|\d*\.?\dg* sugars|\d*\.?\dg* saturates|\d*\.?\dg* fibre|\d*\.?\dg* salt)'

    nutrients = re.findall(num, str)
    
    # put all the nutrients into a list
    nutrients_list = []
    nutrients_list = [re.findall('\d*\.?\d', nutrient)[0] for nutrient in nutrients ]

    # Insert link name at the start
    nutrients_list.insert(0, link.split("/")[5])
    nutrients_list.insert(1, soup.h1.text.encode('ascii', errors='backslashreplace') + " (%s)" % nutrients[0])

# encode(formatter=None)
    rows.append(nutrients_list)
    print nutrients_list

headers = ['link', 'title', 'kcal', 'protein', 'carbohydrates', 'sugars', 'fat', 'saturates', 'fibre', 'salt']

with open('nutrients.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
