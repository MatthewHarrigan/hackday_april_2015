# Dataset is too small
# The results aren't statistically significant

import bs4
import re
import requests
import csv
import scipy
import numpy
from scipy.stats.stats import pearsonr
from flask import render_template
from flask import request

from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

assets = Environment(app)

js = Bundle('jquery.easypiechart.js')
assets.register('js_all', js)

def insert_into_description(text, insert):
    tag = '<div id="description" class="module padded summary">'
    replaced = re.sub(tag, tag + str(insert), text)
    return replaced

def insert_into_editorpick(text, insert):
    tag = '<div id="subcolumn-1" class="subcolumn">'
    replaced = re.sub(tag, tag + str(insert), text)
    return replaced

def remove_cookies_banner(text):
    tag = '<div id="bbccookies"'
    replace = '<div style="display:none"'
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

def get_recommended(age, gender, weight, height, intake):
    baseIntake = 1200
    suggestedIntake = baseIntake + getAgeOffset(age) + getWeightOffset(weight) + getGenderOffset(gender)
    print suggestedIntake
    with open('nutrients.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()

        results = []

        for row in reader:
            link = row.pop(0)
            title = row.pop(0)

            if len(row) > 3:
                kcal =  row.pop(0)

                if int(intake) + int(kcal) < int(suggestedIntake):
                    results.append([link, title])

    return results

def getAgeOffset(ageArg):
    age  = int(ageArg)
    if(age < 13):
        return 200
    if(age <18):
        return 400
    if(age<30):
        return 600

    return 400

def getWeightOffset(weightArg):
    weight  = int(weightArg)
    if(weight < 50):
        return 600
    if(weight < 75):
        return 400
    if(weight<85):
        return 200

    return 0

def getGenderOffset(gender):
    if(gender == 'female'):
        return 0

    return 200

@app.route('/page/<page>')
def show_user_profile(page):

    link = 'http://www.bbc.co.uk/food/recipes/%s' % page
    response = requests.get(link)

    nutrients = extract_nutrients(response)

    nutrient_vals = nutrient_values_list(nutrients)
    results = get_related(nutrient_vals)

    results.sort(key = lambda x: x[2], reverse=True)

    if results[0][2] == 1:
        results.pop(0)

    top_results = results[:5]
    # bottom_results = results
    #
    bottom_results = results[-5:]
    bottom_results.sort(key = lambda x: x[2])

    healthIndicator = 2000 - nutrient_vals[0]
    healthIndicatorVerb = 'Highly Unhealthy'

    if healthIndicator < 200:
        healthIndicatorVerb = 'Highly Healthy'
    if healthIndicator > 200 and  healthIndicator < 500:
        healthIndicatorVerb = 'Moderately Healthy'
    if healthIndicator > 500 and  healthIndicator < 1000:
        healthIndicatorVerb = 'Unhealthy'



    res = render_template(
        'link.html',
        most_links = top_results,
        least_links = bottom_results,
        full_links = results,
        kcal = nutrient_vals[0],
        protein = nutrient_vals[1],
        carbohydrates = nutrient_vals[2],
        sugar = nutrient_vals[3],
        fat = nutrient_vals[4],
        saturates = nutrient_vals[5],
        fibre = nutrient_vals[6],
        salt = nutrient_vals[7],
        healthIndicator = healthIndicator,
        healthIndicatorVerb = healthIndicatorVerb,
    )

    response = remove_cookies_banner(response.text)

    return insert_into_description(response, res)

@app.route('/userdata', methods=['GET', 'POST'])
def get_user_profile():
      response = requests.get('http://www.bbc.co.uk/food/')
      age = request.args.get('age')
      gender = request.args.get('gender')
      weight = request.args.get('weight')
      height = request.args.get('height')
      intake = request.args.get('intake')

      recommended_recipes = get_recommended(age, gender, weight, height, intake)
      res = render_template(
            'link_recommended.html',
            recommended_links = recommended_recipes
      )
      print response
      return insert_into_editorpick(response.text, res)

@app.route('/user/')
def show_user_form():
    return render_template('user.html')







if __name__ == '__main__':
    app.debug = True
    app.run()

