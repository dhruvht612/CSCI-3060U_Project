# CSCI 3060U – Phase 1: Test Plan

## Front End Requirements Test Plan

The purpose of our test plan is to outline how we will organize, run, and compare the requirements tests for the Front End of the Digital Games Distribution System. For Phase 1, we have created 46 test cases, labelled TC01 through TC46. These tests cover the main Front End transactions, including login, logout, create, delete, sell, buy, refund, and addcredit. The tests include both successful and unsuccessful situations, such as invalid input, unauthorized transactions, session restrictions, boundary values, and incorrect transaction information. For example, our tests check valid and invalid logins, username and game-name limits, maximum game prices, credit limits, and whether users are allowed to perform certain transactions. 

The test files will be organized into separate directories so that the files for each test case can easily be identified. The tests/inputs/ directory will contain the input files needed to set up and run each test case, such as transaction input, user account information, available games, and game collections. The tests/expected/ directory will contain the expected results for each test. Once the Front End has been implemented and the tests can be executed, the results produced by the program will be stored separately in the tests/actual/ directory. Each file will use its test case number, such as TC01 or TC02, so that the input, expected output, and actual output for the same test can easily be matched and compared.

Once the Front End is implemented, the tests will be run using a shell script for Linux/macOS or a batch file for Windows. The script will prepare the files needed for each test case, provide the test input to the Front End, capture the program's output, and save the generated Daily Transaction File. Each test will be run independently so that the results of one test do not affect another test.

After a test is run, its actual results will be compared with the expected results that were created during Phase 1. The comparison will check whether transactions were correctly accepted or rejected and whether the generated Daily Transaction File contains the correct transaction codes, field widths, spacing, padding, and monetary formatting. Our final test cases specifically check that the Daily Transaction File ends with the required 00 transaction code and follows the required formatting. The actual results will remain stored separately from the expected results so they can also be used for reporting and comparison with later test runs.
This structure allows our 46 requirements tests to remain organized and reusable throughout later phases of the project. As the Front End is developed, the same tests can be run again and the new results can be compared with the expected results to determine whether the program continues to satisfy the original requirements.

## Directory Structure Printout

```text
CSCI-3060U_Project/
│
├── inputs/
│   ├── TC01.inp.txt
│   ├── TC01.user.txt
│   ├── TC01.game.txt
│   ├── TC01.collection.txt
│   ├── TC02.inp.txt
│   └── ... continues through TC46
│
├── expected/
│   ├── TC01.expout.txt
│   ├── TC01.exptf.txt
│   ├── TC02.expout.txt
│   ├── TC02.exptf.txt
│   └── ... continues through TC46
│
├── CSCI 3060U - Phase 1_ Test Cases.md
├── CSCI 3060U - Phase 1_ Test Plan.md
├── README.md
└── README.txt
```

## Script File Printouts

The following scripts are planned to automate the requirements tests once the Front End has been implemented. A shell script (run_tests.sh) can be used on Linux/macOS, while a batch file (run_tests.bat) can be used on Windows.

The scripts will run each test case independently using the appropriate files from the inputs/ directory. They will capture the Front End's output and generated Daily Transaction File and store these results separately from the test inputs and expected outputs. The actual results can then be compared with the corresponding files in the expected/ directory to determine whether the test passed or failed.




