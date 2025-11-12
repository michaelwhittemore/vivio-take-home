# First pass notes
# Should go through each field and validate that they match the correct pattern - maybe regex?
# Let's create a 'validator' function for and use it for each row when we iterate over the non 0 ones

# maybe i should write out my thought process to present to the company? 
# need to double check on best naming conventions
# maybe note down future work that should be done?
# note that I'm commit more than I otherwise would
# should I download the NDC database or use an API? Let's check how big the file is - if I do it with the API should do some cacheing
# also maybe add a run option? for NDV validation I mean
import csv
# We assume a consistent data structure
column_number_to_field = {
    0: 'claim_id', # (string, unique identifier)
    1: 'member_id', # (string, 10 digits) - member_id must be exactly 10 digits
    2: 'ndc', # (string, 11-digit National Drug Code) - ndc must be exactly 11 digits - Validate that the NDC is valid via open data sources (extra credit)
    3: 'date_of_service', # (YYYY-MM-DD) - date_of_service cannot be future-dated
    4: 'quantity', # (integer, pills dispensed)  - quantity must be positive
    5: 'days_supply', # (integer, days medication should last) - days_supply must be between 1-90
    6: 'drug_cost', # (float, wholesale cost) - drug_cost must be positive
    7: 'plan_type' # (string: "commercial", "medicare", "medicaid") - should be one of these
}

claim_id_list =  []
def validate_claim_id(claim_id) -> tuple[bool, str]:
    """Need to check that it's not a duplicate"""
    if claim_id in claim_id_list: 
        print('Found a claim dupe!', claim_id)
        return [False, 'Duplicate claim Id']
    claim_id_list.append(claim_id)
    return [True, 'Valid']

# will probably want an array of the validator functions
def validate_row(row: list):
    validate_claim_id(row[0])
    """Calls all the validator methods on each field"""

with open('data.csv') as csvfile:
    data_reader = csv.reader(csvfile)
    for line_number, row in enumerate(data_reader):
        if line_number == 0:
            print('these are the labels;', row)
        # if line_number == 1:
        #     for index, value in enumerate(row):
        #         print (column_number_to_field[index], value)  
        elif line_number != 0:
            validate_row(row)
print(claim_id_list)