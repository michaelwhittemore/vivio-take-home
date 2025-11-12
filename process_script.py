# First pass notes
# Should go through each field and validate that they match the correct pattern - maybe regex?

# maybe i should write out my thought process to present to the company? 
# need to double check on best naming conventions
# maybe note down future work that should be done?

import csv

import csv
with open('data.csv') as csvfile:
    data_reader = csv.reader(csvfile)
    for row in data_reader:
        print(', '.join(row))
