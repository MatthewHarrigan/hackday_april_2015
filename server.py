import bs4
import re
import requests
import csv
import scipy
import numpy
from scipy.stats.stats import pearsonr
from flask import render_template

from flask import Flask
app = Flask(__name__)

def insert_into_description(text, insert):
    tag = '<div id="description" class="module padded summary">'
    replaced = re.sub(tag, tag + str(insert), text)
    return replaced

def remove_cookies_banner(text):
    tag = '<div id="bbccookies"'
    replace = '<div '
    replaced = re.sub(tag, replace, text)
    return replaced

def extract_nutrients(response):
    soup = bs4.BeautifulSoup(response.text)
    str = soup.select('div#description')
    str = str[0].text
    num = '(\d*\.?\dg* kcal|\d*\.?\dg* protein|\d*\.?\dg* carbohydrate|\d*\.?\dg* fat|\d*\.?\dg* sugars|\d*\.?\dg* saturates|\d*\.?\dg* fibre|\d*\.?\dg* salt)'
    nutrients = re.findall(num, str)
    return nutrients

def nutrient_values_list(nutrients):
    return [float(re.findall('\d*\.?\d', nutrient)[0]) for nutrient in nutrients]

def get_related(current):
    # current = [487.0, 40.0, 43.0, 5.0, 17.5, 4.0, 12.0, 0.9]
    with open('nutrients.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()

        results = []

        for row in reader:
            link = row.pop(0)
            title = row.pop(0)

            if len(row) == 8:
                vals = [float(v) for v in row]
                correl = scipy.stats.pearsonr(current, vals)[0]
                results.append([link, title, correl])
    return results

@app.route('/page/<page>')
def show_user_profile(page):

    link = 'http://www.bbc.co.uk/food/recipes/%s' % page
    response = requests.get(link)

    # response = remove_cookies_banner(response)

    nutrients = extract_nutrients(response)

    nutrient_vals = nutrient_values_list(nutrients)
    results =  get_related(nutrient_vals)

    results.sort(key = lambda x: x[2], reverse=True)

    if results[0][2] == 1:
        results.pop(0)

    # top_results = results[:20]
    top_results = results

    top_results = render_template('link.html', links=top_results)
    return insert_into_description(response.text, top_results)

if __name__ == '__main__':
    app.debug = True
    app.run()

