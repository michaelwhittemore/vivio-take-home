# First pass notes
# Should go through each field and validate that they match the correct pattern - maybe regex?

# maybe i should write out my thought process to present to the company? 
# need to double check on best naming conventions
# maybe note down future work that should be done?

import csv
# We assume a consistent data structure
column_number_to_field = {
    0 : 'claim_id', # (string, unique identifier)
    1: 'member_id', # (string, 10 digits)
    2: 'ndc', # (string, 11-digit National Drug Code)
    3: 'date_of_service', # (YYYY-MM-DD)
    4: 'quantity', # (integer, pills dispensed)
    5: 'days_supply', # (integer, days medication should last)
    6: 'drug_cost', # (float, wholesale cost)
    7: 'plan_type' # (string: "commercial", "medicare", "medicaid")
}
with open('data.csv') as csvfile:
    data_reader = csv.reader(csvfile)
    line_number = 0
    for row in data_reader:
        if line_number == 0:
            print('these are the labels;', row)
        print(', '.join(row))
        line_number += 1
