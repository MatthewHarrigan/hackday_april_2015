import requests
import bs4

def get_links():
    page = open('google_food_results_page.html', 'r')
    soup = bs4.BeautifulSoup(page)
    return [a.attrs.get('href') for a in soup.select('h3.r a[href^=http://www.bbc]')]

links = get_links()

for link in links:
    response = requests.get(link);
    soup  = bs4.BeautifulSoup(response.text)
    print soup.select('div#description')

