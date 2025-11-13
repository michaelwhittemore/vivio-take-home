
# maybe note down future work that should be done?
# note that I'm commit more than I otherwise would
# should I download the NDC database or use an API? Let's check how big the file is - if I do it with the API should do some cacheing
# also maybe add a run option? for NDC validation I mean
# also note that I would add some parameters to command line for ease of modifying files
# https://open.fda.gov/apis/drug/ndc/
import csv
import json
from datetime import datetime
import sys
import requests
# https://api.fda.gov/drug/ndc.json?search=product_ndc:00002-7510-01
# https://api.fda.gov/drug/ndc.json?search=product_ndc:82757-102 - returns a result
# https://api.fda.gov/drug/ndc.json?search=product_ndc:50580-475 - also valid
# https://api.fda.gov/drug/ndc.json?search=product_ndc:0002-7510 - this is the exmample, it returns insulin
# base_url = 'https://api.fda.gov/drug/ndc.json'


# We assume a consistent data structure
# I don't actually use this dict anywhere, it just makes it easier to reference
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

def convert_ndc(ndc: str) -> tuple[bool, str | list]:
    """NDCs can only be searched by the product ndc (not the package ndc).
    The product ndc is nine digits (labeler code plus product code). The last part of the ndc
    is the package code which doesn't appear to be supported as part of the API endpoint.
    The packed code is separately returned as part of the package field. The 'labeler-product' code can be
    either eight or nine digits. This returns a tuple with a bool indicating if it was a valid ndc, 
    and either the converted searchable value or a failure reason."""
    # it's possible to have multiple possible ndc's as in the 00002-7597-01 case
    # see https://www.fda.gov/media/173715/download page 6 
    # 5-4-1 -> 5-4-2 the zero goes on in front of package
    # 5-3-2 -> 5-4-2 the zero goes in front of product
    # 4-4-2 -> 5-4-2 the zero goes in front of labeler
    if not '-' in ndc:
        return [False, 'NDC does not contain hyphens']
    split_ndc = ndc.split('-')
    if len(split_ndc) != 3:
        return [False, 'NDC not fully formed']
    labeler, product, package = split_ndc
    possible_combinations = [labeler + '-' + product, ]
    if labeler[0] == '0':
        possible_combinations.append(labeler[1:] + '-' + product)
    if product[0] == '0':
        possible_combinations.append(labeler + '-' + product[1:])
    # I guess we just try all possible cases - note that only one zero will ever be added
    print(possible_combinations)
    return [True, possible_combinations]

def query_ndcs(processed_ndcs:str) -> bool:
    '''returns true if at least one of the permutations is true'''
    fda_url = 'https://api.fda.gov/drug/ndc.json?search=product_ndc:'
    for ndc in processed_ndcs:
        response = requests.get(fda_url + ndc)
        if response.status_code == 200:
            return True
    return False

claim_id_list =  []
def validate_claim_id(claim_id) -> tuple[bool, str]:
    """Need to check that it's not a duplicate"""
    if claim_id in claim_id_list: 
        # print('Found a claim dupe!', claim_id)
        return [False, 'Duplicate claim Id']
    claim_id_list.append(claim_id)
    return [True, 'Valid']

def validate_member_id(member_id) -> tuple[bool, str]:
    """Check that it's a number and that it's ten digits"""
    if len(member_id) != 10:
        # print('member is not ten digits', member_id)
        return [False, 'member is not ten digits']
    try:
        int(member_id)
    except ValueError:
        # print('member id is not a number', member_id)
        return [False, 'member id is not a number']
    return [True, 'Valid']

def validate_ndc(ndc) -> tuple[bool, str]:
    """Check that it's a an eleven digit number"""
    # todo use the ndc api or download the database
    stripped_ndc = ndc.replace('-', '')
    if len(stripped_ndc) != 11:
        # print('stripped ndc does not have 11 digits', stripped_ndc)
        return [False, 'stripped ndc does not have 11 digits']
    try:
        int(stripped_ndc)
    except ValueError:
        # print('stripped ndc is not a number', stripped_ndc)
        return [False, 'stripped ndc is not a number']
    if not use_ndc_api:
        # We're not using the api for queries 
        return [True, 'Valid']
    is_valid_ndc, processed_ndcs = convert_ndc(ndc)
    if not is_valid_ndc:
        return [False, processed_ndcs]
    else:
        found_ndc = query_ndcs(processed_ndcs)
        if found_ndc:
            return [True, 'Valid']
        else:
            return [False, 'Could not find ndc in FDA database']
    
        


def validate_date(date) -> tuple[bool, str]:
    """ensure it's a valid date and not future dated"""
    try:
        formatted_data = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        # print('invalid date', date)
        return [False, 'invalid date']
    else:
        if formatted_data > datetime.now():
            # print('future date', date)
            return [False, 'future date']
        else: 
            return [True, 'Valid']
    
def validate_quantity(quantity) -> tuple[bool, str]:
    """ensure it's a positive integer"""
    try:
        int_quantity = int(quantity)
    except ValueError:
        # print('non-int quantity', quantity)
        return [False, 'non-int quantity']
    else:
        if int_quantity <= 0:
            # print('quantity not positive int', quantity)
            return [False, 'quantity not positive int']
        else: 
            return [True, 'Valid']
        
def validate_days_supply(supply) -> tuple[bool, str]:
    """ensure it's an integer between 1-90"""
    try:
        int_supply = int(supply)
    except ValueError:
        # print('non-int supply', supply)
        return [False, 'non-int supply']
    else:
        if  not (1 <= int_supply <= 90):
            # print('supply not positive int', supply)
            return [False, 'supply not between 1 and 90']
        else: 
            return [True, 'Valid']
        
def validate_drug_cost(cost) -> tuple[bool, str]:
    """ensure it's positive"""
    try:
        numeric_cost = float(cost)
    except ValueError:
        # print('non-int cost', cost)
        return [False, 'non-number cost']
    else:
        if  numeric_cost <= 0:
            # print('cost not positive', cost)
            return [False, 'cost not positive']
        else: 
            return [True, 'Valid']

def validate_plan_type(plan) -> tuple[bool, str]:
    """ensure it's one of "commercial", "medicare", or "medicaid" """
    if not plan in ("commercial", "medicare", "medicaid"):
        # print('invalid plan type', plan)
        return [False, 'invalid plan type']
    else:
        return [True, 'Valid']


# The validators are just listed numerically so they can share the index, if it was more inconsistent we'd want to 
# use a dictionary to map the functions to field names
validator_function_tuple = (validate_claim_id, validate_member_id, validate_ndc, validate_date, validate_quantity,
                            validate_days_supply,validate_drug_cost, validate_plan_type)

def validate_pills_per_day(row: list) -> bool:
    """returns false if quantity / days_supply > 3 and assumes correct integer input"""
    quantity = int(row[4])
    days = int(row[5])
    return quantity / days <= 3

def validate_row(row: list) -> tuple[bool, str]:
    """Calls all the validator methods on each field, returns false if anything is wrong"""
    for index, validator_function in enumerate(validator_function_tuple):
        # print('index', index, row)
        validator_output_tuple = validator_function(row[index]) # should fail if there's a false value in the return tuple
        if not validator_output_tuple[0]:
            return validator_output_tuple
    # validate pills per day after each individual field is completed
    if not validate_pills_per_day(row):
        # print('Invalid pills per day', row)
        return [False, 'Invalid pills per day']
    else:
        return [True, 'null']

def calculate_copay_from_row(row: list) -> float:
    """calculates using the plan type, NDC, and cost"""
    # it might make more sense to pass in specific values and not the whole row
    match row[7]:
        case 'medicaid':
            # Medicaid: $0 copay
            return 0
        case 'medicare':
            # Medicare: $5 flat copay for generic, $15 for brand (if NDC starts with "0")
            return 15 if row[2][0] == '0' else 5
        case 'commercial':
            # Commercial: 20% coinsurance, minimum $10, maximum $100
            cost = float(row[6])
            rounded_cost = round(0.2 * cost, 2) 
            if rounded_cost < 10:
                return 10
            elif rounded_cost > 100:
                return 100
            else:
                return rounded_cost
        case _:
             # we validate before using this so it should never slip through
            print('invalid plan type, we should never reach here')
            return -1

output_for_json = {}

def main():
    with open('data.csv') as csvfile:
        data_reader = csv.reader(csvfile)
        for line_number, row in enumerate(data_reader):
            if line_number != 0:
                validator_output_bool, rejection_reason = validate_row(row)
                processed_at = datetime.now().isoformat()
                if not validator_output_bool:
                    output_for_json[line_number] = {
                        "claim_id": row[0],
                        "status": "REJECT",
                        "copay_amount": 'N/A',
                        "rejection_reason": rejection_reason,
                        "processed_at": processed_at,
                    }
                else:
                    output_for_json[line_number] = {
                        "claim_id": row[0],
                        "status": "APPROVED",
                        "copay_amount": calculate_copay_from_row(row), # only do calculation if everything passes
                        "rejection_reason": 'null',
                        "processed_at": processed_at,
                    }
    with open('processed_claims.json', 'w') as outfile:
        json.dump(output_for_json, outfile, indent=4)

use_ndc_api = 'query' in sys.argv
if __name__ == "__main__":
    main()

query_ndcs(['50242-0040', '50242-040'])