import unittest
import process_script

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

    def test_validate_quantity(self):
        valid_quantity = '150'
        zero_quantity = '0'
        negative_quantity = '-20'
        float_quantity = '23.1'
        # Happy path
        tested_bool, tested_reason = process_script.validate_quantity(valid_quantity)
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        # Zero Quantity 
        tested_bool, tested_reason = process_script.validate_quantity(zero_quantity)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'quantity not positive int')
        # Negative Quantity 
        tested_bool, tested_reason = process_script.validate_quantity(negative_quantity)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'quantity not positive int')
        # Float Quantity 
        tested_bool, tested_reason = process_script.validate_quantity(float_quantity)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'non-int quantity')

    def test_validate_days_supply(self):
        valid_supply = '30'
        float_supply = '30.5'
        large_supply = '99'
        negative_supply = '-30'
        # Happy path
        tested_bool, tested_reason = process_script.validate_days_supply(valid_supply)
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        # large supply
        tested_bool, tested_reason = process_script.validate_days_supply(large_supply)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'supply not between 1 and 90')
        # negative supply
        tested_bool, tested_reason = process_script.validate_days_supply(negative_supply)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'supply not between 1 and 90')
        # invalid supply 
        tested_bool, tested_reason = process_script.validate_days_supply(float_supply)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'non-int supply')

    def test_validate_drug_cost(self):

        valid_cost = '30'
        non_number_cost = '3a0.5'
        negative_cost = '-30'
        # Happy path
        tested_bool, tested_reason = process_script.validate_drug_cost(valid_cost)
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        # negative cost
        tested_bool, tested_reason = process_script.validate_drug_cost(negative_cost)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'cost not positive')
        # bad cost
        tested_bool, tested_reason = process_script.validate_drug_cost(non_number_cost)
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'non-number cost')
    
    def test_validate_plan_type(self):
        # Happy paths
        tested_bool, tested_reason = process_script.validate_plan_type('commercial')
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        tested_bool, tested_reason = process_script.validate_plan_type('medicare')
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')
        tested_bool, tested_reason = process_script.validate_plan_type('medicaid')
        self.assertTrue(tested_bool)
        self.assertEqual(tested_reason, 'Valid')       
        # Invalid plan
        tested_bool, tested_reason = process_script.validate_plan_type('michael-care')
        self.assertFalse(tested_bool)
        self.assertEqual(tested_reason, 'invalid plan type')       

    def test_validate_pills_per_day(self):
        valid_row = ['CLM001', '1234567890', '00002-7510-01', '2025-10-15', '30', '30', '150.00', 'commercial']
        invalid_row = ['tooManyPills', '1234567890', '00002-7510-01', '2025-10-15', '40', '10', '150.00', 'commercial']
        # Happy path
        tested_bool= process_script.validate_pills_per_day(valid_row)
        self.assertTrue(tested_bool)
        # Four pills per day
        tested_bool = process_script.validate_pills_per_day(invalid_row)
        self.assertFalse(tested_bool)

class TestCopayCalculator(unittest.TestCase):
    def test_calculate_copay_from_row(self):
        medicaid = ['medicaid', '9876543210', '12345678901', '2025-10-20', '90', '30', '200.00', 'medicaid']
        medicare_brand =  ['medicareBrand', '9876543210', '02345678901', '2025-10-20', '90', '30', '200.00', 'medicare']
        medicare_generic = ['medicareGeneric', '9876543210', '12345678901', '2025-10-20', '90', '30', '200.00', 'medicare']
        commercial_min = ['commercialCheap', '9876543210', '02345678901', '2025-10-20', '90', '30', '10.00', 'commercial']
        commercial_max = ['commercialExpensive', '9876543210', '02345678901', '2025-10-20', '90', '30', '2000.00', 'commercial']
        commercial_calculated = ['commercialMidrange', '9876543210', '02345678901', '2025-10-20', '90', '30', '425.58', 'commercial']
        # medicaid always $0
        self.assertEqual(process_script.calculate_copay_from_row(medicaid), 0)
        # medicare brand is $15
        self.assertEqual(process_script.calculate_copay_from_row(medicare_brand), 15)
        # medicare generic is $15
        self.assertEqual(process_script.calculate_copay_from_row(medicare_generic), 5)
        # commercial maxes out at $100 and has a minimum of $0
        self.assertEqual(process_script.calculate_copay_from_row(commercial_min), 10)
        self.assertEqual(process_script.calculate_copay_from_row(commercial_max), 100)
        # otherwise cost 20% (rounded to two decimals)
        self.assertEqual(process_script.calculate_copay_from_row(commercial_calculated), 85.12)
        

if __name__ == '__main__':
    unittest.main()