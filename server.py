import bs4
import re
import requests

from flask import Flask
app = Flask(__name__)

def insert_in_page(text):
    tag = '<div id="description" class="module padded summary">'
    replace = '<strong>HELLO Matthew</strong>'

    replaced = re.sub(tag, tag + replace, text)
    return replaced


@app.route('/page/<page>')
def show_user_profile(page):

    link = 'http://www.bbc.co.uk/food/recipes/%s' % page
    response = requests.get(link)

    return insert_in_page(response.text)

if __name__ == '__main__':
    app.debug = True
    app.run()

