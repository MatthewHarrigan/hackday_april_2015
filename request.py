import requests
import bs4
import re

def get_links():
    page = open('google_food_results_page.html', 'r')
    soup = bs4.BeautifulSoup(page)
    return [a.attrs.get('href') for a in soup.select('h3.r a[href^=http://www.bbc]')]

links = get_links()

for link in links:
    response = requests.get(link);
    soup  = bs4.BeautifulSoup(response.text)
    str = soup.select('div#description')
    str = str[0].text
    print str
    num = '(\d*\.?\dg* kcal|\d*\.?\dg* protein|\d*\.?\dg* carbohydrate|\d*\.?\dg* fat|\d*\.?\dg* sugars|\d*\.?\dg* saturates|\d*\.?\dg* fibre|\d*\.?\dg* salt)'
    print re.findall(num ,str)

