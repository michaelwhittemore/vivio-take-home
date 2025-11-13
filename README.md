# Setup and Usage
This is a fairly simple python script which takes in a csv file of claims and outputs a JSON file with the status of the claims. The claim will either be approved or rejected. If it is approved it will also include the copay amount
1. `git clone` and `cd` into the repo
2. Verify that python3 is properly installed with `python3 --version`
3. Provide a data.csv file with claims (or use the existing one that covers all cases). The csv file expects the following format: `claim_id,member_id,ndc,date_of_service,quantity,days_supply,drug_cost,plan_type`. An example of a valid row is `CLM001,1234567890,00002-7510-01,2025-10-15,30,30,150.00,commercial` which will return approved and a copay value of $30
4. Run the script with `python3 process_script.py`. The output will be found in the processed_claims.json file. If the file does not currently exist one will be created

# Unit Testing
* Run `python3 unit_tests.py` in terminal
* We expect to see `Ran 10 tests in 0.004s. OK`(we use unittest.py)
* All validator functions are calculators are tested

# Future improvements    
* Code dryness - Especially in the test script there's a fair bit of copy-paste. This could be improved with some helper functions
* terminal parameters - it would be nice to allow the user to specify the input and output file names from within the terminal when running the script
* robustness for differently formatted data - Currently the script will reject fields with spaces or capitalization differences for plan types. This could be improved with some simple trimming and string manipulation
* improve some clarity when directly accessing row properties - it can make it difficult to read when I'm just accessing a seemingly arbitrary row property. Some clarity, presumably by using well named local, variables would help
