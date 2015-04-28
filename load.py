import csv
import scipy
import numpy
from scipy.stats.stats import pearsonr

current = [487.0, 40.0, 43.0, 5.0, 17.5, 4.0, 12.0, 0.9]

with open('nutrients.csv') as csvfile:
    reader = csv.reader(csvfile, 'utf-8')
    headers = reader.next()
    for row in reader:
        link = row.pop(0)

        if len(row) == 8:
            vals = [float(v) for v in row]

            correl = scipy.stats.pearsonr(current, vals)[0]
            print link, correl

