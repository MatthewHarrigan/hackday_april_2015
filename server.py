import bs4
import re
import requests

from flask import Flask
app = Flask(__name__)

def insert_into_description(text, insert):
    tag = '<div id="description" class="module padded summary">'

    replaced = re.sub(tag, tag + str(insert), text)
    return replaced

def extract_nutrients(response):
    soup = bs4.BeautifulSoup(response.text)
    str = soup.select('div#description')
    str = str[0].text
    num = '(\d*\.?\dg* kcal|\d*\.?\dg* protein|\d*\.?\dg* carbohydrate|\d*\.?\dg* fat|\d*\.?\dg* sugars|\d*\.?\dg* saturates|\d*\.?\dg* fibre|\d*\.?\dg* salt)'
    nutrients = re.findall(num, str)
    return nutrients

def nutrient_values_list(nutrients):
    return [re.findall('\d*\.?\d', nutrient)[0] for nutrient in nutrients]

@app.route('/page/<page>')
def show_user_profile(page):

    link = 'http://www.bbc.co.uk/food/recipes/%s' % page
    response = requests.get(link)

    nutrients = extract_nutrients(response)

    nutrient_vals = nutrient_values_list(nutrients)

    print nutrient_vals

    return insert_into_description(response.text, nutrient_vals)

if __name__ == '__main__':
    app.debug = True
    app.run()

