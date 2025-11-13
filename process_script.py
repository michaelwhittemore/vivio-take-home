
# maybe note down future work that should be done?
# note that I'm commit more than I otherwise would
# should I download the NDC database or use an API? Let's check how big the file is - if I do it with the API should do some cacheing
# also maybe add a run option? for NDC validation I mean
# https://open.fda.gov/apis/drug/ndc/
import csv
import json
from datetime import datetime


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
    return [True, 'Valid']

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
            return 5 if row[2][0] == '0' else 15
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

if __name__ == "__main__":
    main()