# Setup and Usage
This is a fairly simple python script which takes in a csv file of claims and outputs a JSON file with the status of the claims. The claim will either be approved or rejected. If it is approved it will also include the copay amount
1. `git clone` and `cd` into the repo
2. Verify that python3 is properly installed with `python3 --version`
4. Run `pip3 install -r requirements.txt` to ensure that requests is installed 
3. Provide a data.csv file with claims (or use the existing one that covers all cases). The csv file expects the following format: `claim_id,member_id,ndc,date_of_service,quantity,days_supply,drug_cost,plan_type`. An example of a valid row is `CLM001,1234567890,00002-7510-01,2025-10-15,30,30,150.00,commercial` which will return approved and a copay value of $30
4. Run the script with `python3 process_script.py`. The output will be found in the processed_claims.json file. If the file does not currently exist one will be created
5. Run the script with the `query` parameter to `python3 process_script.py query` use the https://open.fda.gov/ API to validate NDCs. The processed_claims.json file will now have more claims rejected due to the database being unable to match the ndc.

# Unit Testing
* Run `python3 unit_tests.py` in terminal
* We expect to see `Ran 10 tests in 0.004s. OK`(we use unittest.py)
* All validator functions are calculators are tested

# A note on NDC validation  
I was attempting to use the FDA API endpoints to validate if the NDC's were valid. From my research, it appears that NDCs should be ten digits and may be in the form 4-4-2 – 5-3-2 – 5-4-1 (see https://www.fda.gov/media/173715/download) which may then be converted to an eleven digit format by adding an appropriate zero. The FDA API endpoint only supports a eight or nine digit *product* + *labeler* ndc query parameter. I'm in the process of appropriately updating the validator. We will search by *product* + *labeler* ndc, and then check that the full *package* ndc is supported in the API response. 

I've discovered some issues when attempting to get the 10 digit ndc from the 11 digit version. 00002-7597-01 is a valid eleven digit code for one vial of Olanzapine. Looking at this code, there's no way to immediately know if the leading zero was added to the labeler or the package section. It could have either been constructed from 0002-7597-01 (4-4-2) or from 00002-7597-1 (5-4-1). In this particular case, the query https://api.fda.gov/drug/ndc.json?search=product_ndc:0002-7597  
will correctly find the drug while https://api.fda.gov/drug/ndc.json?search=product_ndc:00002-7597 will not. To the best of my knowledge there's no way to know which one is correct other than trying both. 

# Future improvements    
* Code dryness - Especially in the test script there's a fair bit of copy-paste. This could be improved with some helper functions
* terminal parameters - it would be nice to allow the user to specify the input and output file names from within the terminal when running the script
* robustness for differently formatted data - Currently the script will reject fields with spaces or capitalization differences for plan types. This could be improved with some simple trimming and string manipulation
* improve some clarity when directly accessing row properties - it can make it difficult to read when I'm just accessing a seemingly arbitrary row property. Some clarity, presumably by using well named local, variables would help
