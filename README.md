## Synopsis
This is a hack to demonstrate:
* Inserting on-the-fly nutritional data into a BBC Food Recipe page and visualising it as part of RDA
* Showing nutritionally similar recipes (using pearson similarity coefficient) based on the nutritional content of the current recipes

## Examples

See ./screenshots

## Motivatation
This work is part of a BBC K&L internal hackday.

## Installation

Install venv 
Install flask http://flask.pocoo.org/docs/0.10/installation/

Activate
. venv/bin/activate

Run the server
python server.py

Visit a recipe page i.e:
http://127.0.0.1:5000/page/black_bean_and_avocado_32747

