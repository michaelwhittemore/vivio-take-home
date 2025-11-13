import unittest
import process_script

#validator_function_tuple = (validate_claim_id, validate_member_id, validate_ndc, validate_date, validate_quantity,
#                            validate_days_supply,validate_drug_cost, validate_plan_type)

class TestClaimsProcessing(unittest.TestCase):

    # def test_validate_claim_id(self):
    #     validate_claim_id()

    def test_validate_member_id(self):
        valid_row = ['CLM001', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
        short_id_row = ['CLM001', '123', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
        long_id_row = ['CLM001', '123456789123123', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
        non_init_id_row = ['CLM001', '123456789123123', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']


    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

"""
['claim_id', 'member_id', 'ndc', 'date_of_service', 'quantity', 'days_supply', 'drug_cost', 'plan_type']
['CLM001', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
['CLM002', '9876543210', '12345678901', '2025-10-20', '90', '30', '200.00', 'medicare']
['CLM003', '1111111111', '98765432109', '2025-11-01', '60', '90', '75.00', 'medicaid']
['CLM004', '999', '00001-2345-67', '2025-10-10', '120', '30', '300.00', 'commercial']
['notNumberMemID', 'a123456789', '00001-2345-67', '2025-10-10', '120', '30', '300.00', 'commercial']
['duplicate', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
['duplicate', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
['shortNDC', ' 1234567890', '0002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
['longNDC', ' 1234567890', '000021-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
['badNDC', ' 1234567890', '0000A-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
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