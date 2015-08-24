## Synopsis
This is a hack to demonstrate:
* Inserting on-the-fly nutritional data into a BBC Food Recipe page and visualising it as part of RDA
* Showing nutritionally similar recipes (using pearson similarity coefficient) based on the nutritional content of the current recipes

## Examples

See ./screenshots

## Motivatation
This work is part of a BBC K&L internal hackday. Nutrional data for recipes is currently manually curated and entered into the page as text only. It would be nice to show this data off in a more visually compelling way. This would require having the data in a format that is easier to access and process like database. Once it is in this form then we can start ask more interesing types of questions about the data, like what recipes have a similar nutritional fingerprint. 

For this demo we use Google to look for Food pages containing nutritional info. These search results are then scraped for links to relevant pages whose pages are further scraped to get nutrional data. This data is then stored in nutrients.csv for processing. The server program uses the Flask framework to proxy the pages and insert the new data into them.

## Installation

Install venv 
http://docs.python-guide.org/en/latest/dev/virtualenvs/

Activate venv
'. venv/bin/activate'

Install dependencies
'pip install -r requirements.txt'

Run the server
'python server.py'

Visit a recipe page i.e:
http://127.0.0.1:5000/page/black_bean_and_avocado_32747

