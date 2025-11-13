import unittest
import process_script

#validator_function_tuple = (validate_claim_id, , validate_quantity,
#                            validate_days_supply,validate_drug_cost, validate_plan_type)

class TestValidators(unittest.TestCase):
    def test_validate_claim_id(self):
        # Happy path
        tested_bool, tested_reason = process_script.validate_claim_id('aDuplicateName')
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        # invalid when reusing the claim id
        tested_bool, tested_reason = process_script.validate_claim_id('aDuplicateName')
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'Duplicate claim Id')

    def test_validate_member_id(self):
        valid_id =  '1234567890'
        short_id = '123'
        long_id = '12345678902132131'
        non_int_id = '123456789a'
        # Happy path
        valid_bool, valid_reason = process_script.validate_member_id(valid_id)
        self.assertTrue(valid_bool)
        self.assertEqual(valid_reason, 'Valid')
        # Too short
        short_bool, short_reason = process_script.validate_member_id(short_id)
        self.assertFalse(short_bool)
        self.assertEqual(short_reason, 'member is not ten digits')
        # Too long
        long_bool, long_reason = process_script.validate_member_id(long_id)
        self.assertFalse(long_bool)
        self.assertEqual(long_reason, 'member is not ten digits')
        # Not an int
        not_int_bool, not_int_reason = process_script.validate_member_id(non_int_id)
        self.assertFalse(not_int_bool)
        self.assertEqual(not_int_reason, 'member id is not a number')

    def test_validate_ndc(self):
        valid_dnc =  '00002-7510-01'
        short_dnc = '002-7510-01'
        long_dnc = '000102-7510-01'
        non_int_dnc = '0000A-7510-01'
        # Happy path
        valid_bool, valid_reason = process_script.validate_ndc(valid_dnc)
        self.assertTrue(valid_bool)
        self.assertEqual(valid_reason, 'Valid')
        # Too short
        short_bool, short_reason = process_script.validate_ndc(short_dnc)
        self.assertFalse(short_bool)
        self.assertEqual(short_reason, 'stripped ndc does not have 11 digits')
        # Too long
        long_bool, long_reason = process_script.validate_ndc(long_dnc)
        self.assertFalse(long_bool)
        self.assertEqual(long_reason, 'stripped ndc does not have 11 digits')
        # Not an int
        not_int_bool, not_int_reason = process_script.validate_ndc(non_int_dnc)
        self.assertFalse(not_int_bool)
        self.assertEqual(not_int_reason, 'stripped ndc is not a number')

    def test_validate_date(self):
        valid_date = '2025-10-15'
        invalid_date = '2025-99-15'
        future_date = '2030-10-15'
        # Happy path
        valid_bool, valid_reason = process_script.validate_date(valid_date)
        self.assertTrue(valid_bool)
        self.assertEqual(valid_reason, 'Valid')
        # Badly formatted date
        tested_bool, tested_reason = process_script.validate_date(invalid_date)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'invalid date')
        # Future Date
        tested_bool, tested_reason = process_script.validate_date(future_date)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'future date')

if __name__ == '__main__':
    unittest.main()

"""
['claim_id', 'member_id', 'ndc', 'date_of_service', 'quantity', 'days_supply', 'drug_cost', 'plan_type']
['CLM001', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']

['badDateFormat', '1234567890', '00002-7510-01', '2025-13-15', '30', '30', '150.00', 'commercial']
['futureDate', '1234567890', '00002-7510-01', '2030-10-15', '30', '30', '150.00', 'commercial']
['zeroQuantity', '1234567890', '00002-7510-01', '2030-10-15', '0', '30', '150.00', 'commercial']
['negativeQuantity', '1234567890', '00002-7510-01', '2030-10-15', '-30', '30', '150.00', 'commercial']
['floatQuantity', '1234567890', '00002-7510-01', '2030-10-15', '30.5', '30', '150.00', 'commercial']
['floatSupply', '1234567890', '00002-7510-01', '2025-10-15', '30', '30.4', '150.00', 'commercial']
['largeSupply', '1234567890', '00002-7510-01', '2025-10-15', '30', '99', '150.00', 'commercial']
['negativeCost', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '-150.00', 'commercial']
['badCost', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '15a0.00', 'commercial']
['invalidPlan', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'badPlanString']
['medicareBrand', '9876543210', '02345678901', '2025-10-20', '90', '30', '200.00', 'medicare']
['medicareGeneric', '9876543210', '12345678901', '2025-10-20', '90', '30', '200.00', 'medicare']
['commercialCheap', '9876543210', '02345678901', '2025-10-20', '90', '30', '10.00', 'commercial']
['commercialExpensive', '9876543210', '02345678901', '2025-10-20', '90', '30', '2000.00', 'commercial']
['commercialMidrange', '9876543210', '02345678901', '2025-10-20', '90', '30', '425.50', 'commercial']
['tooManyPills', '1234567890', '00002-7510-01', '2025-10-15', '40', '10', '150.00', 'commercial']
"""