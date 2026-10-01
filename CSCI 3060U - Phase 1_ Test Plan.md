# **CSCI 3060U – Phase 1: Test Plan**

## **Front End Requirements Test Plan**

### **1\. Purpose**

The purpose of this test plan is to organize the requirements tests for the Front End of the Digital Games Distribution System.

The tests are designed from the Front End requirements and will be maintained throughout later phases of the project. Phase 1 focuses on defining and organizing the tests. No Front End program is implemented as part of this phase.

### **2\. Test Organization**

Each test case is assigned a unique identifier from **TC01 through TC46**.

Each test represents a complete Front End test session and is associated with the input files required to establish the test conditions and the expected output files that describe the correct result.

The files are divided into the following directories.

#### **Inputs Directory – tests/inputs/**

The input directory contains the files required for each test.

#### **Transaction Input – TCXX.inp**

Contains the complete sequence of transaction codes and user input for the test session.

For example, a login/logout test input may contain:

login  
admin  
logout

#### **Current User Accounts File – TCXX.user**

Contains the initial Current User Accounts File required for the test.

This file establishes users, user types, and available credit needed for the test case.

#### **Available Games File – TCXX.game**

Contains the initial Available Games File required for the test.

This file establishes the games available for purchase at the beginning of the session.

#### **Game Collection File – TCXX.collection**

When required by a test case, this file identifies games already owned by users. It is particularly useful for tests involving the requirement that a buyer cannot purchase a game already in their collection.

### **3\. Expected Output Organization**

Expected results are stored in:

tests/expected/

#### **Expected Console Behaviour – TCXX.expout**

Describes the expected Front End behaviour for the test session, including whether transactions are accepted or rejected and whether the program continues operating correctly.

Where the requirements do not specify exact wording for terminal messages, the test will verify the required behaviour rather than inventing a specific message.

#### **Expected Daily Transaction File – TCXX.exptf**

Contains the expected Daily Transaction File produced when the session ends.

The expected transaction file follows the formats defined in the Front End requirements, including:

* two-digit transaction codes  
* required field widths  
* left-justified alphabetic fields  
* space padding  
* numeric formatting  
* monetary formatting  
* the 00 end-of-session transaction

### **4\. Directory Structure**

csci3060u-phase1/  
│  
├── documents/  
│   ├── test\_cases.pdf  
│   └── test\_plan.pdf  
│  
├── scripts/  
│   ├── run\_tests.sh  
│   └── run\_tests.bat  
│  
└── tests/  
    │  
    ├── inputs/  
    │   ├── TC01.inp  
    │   ├── TC01.user  
    │   ├── TC01.game  
    │   ├── TC01.collection  
    │   │  
    │   ├── TC02.inp  
    │   ├── TC02.user  
    │   ├── TC02.game  
    │   ├── TC02.collection  
    │   │  
    │   └── ... continues through TC46  
    │  
    ├── expected/  
    │   ├── TC01.expout  
    │   ├── TC01.exptf  
    │   ├── TC02.expout  
    │   ├── TC02.exptf  
    │   └── ... continues through TC46  
    │  
    └── actual/  
        └── Generated during later execution of the requirements tests

Files that are unnecessary for a particular test case may be omitted when they do not affect the test conditions.

### **5\. Running the Tests**

During Phase 1, the tests are being designed and organized. The Front End executable has not yet been implemented.

Once the Front End is available in a later project phase, the requirements tests can be automated using shell scripts or Windows batch files.

Two test-running scripts are planned:

* scripts/run\_tests.sh for Linux/macOS  
* scripts/run\_tests.bat for Windows

For each test case, the test runner will:

1. Prepare the Current User Accounts, Available Games, and Game Collection files required by the test.  
2. Start the Front End using the appropriate test files.  
3. Redirect the corresponding TCXX.inp file to standard input.  
4. Capture the Front End's terminal output.  
5. Store the generated Daily Transaction File.  
6. Compare the generated results against the expected results.  
7. Report whether the test passed or failed.

Each test will be run independently so that the results of one test do not affect another test.

### **6\. Actual Test Results**

When the Front End is implemented and the requirements tests are executed, generated results will be stored in:

tests/actual/

For each test, the directory may contain:

#### **TCXX.out**

The actual terminal output produced during the test.

#### **TCXX.dtf**

The actual Daily Transaction File produced during the test.

These files are generated results rather than Phase 1 requirements-test definitions.

### **7\. Comparing Results**

Generated results will be compared with the expected results.

On Linux/macOS, standard tools such as diff can be used.

On Windows, standard tools such as fc can be used.

A test passes when the observed Front End behaviour and generated files satisfy the expected requirements.

The comparison will consider:

#### **Transaction Behaviour**

The transaction should be accepted or rejected according to the Front End requirements.

#### **Daily Transaction File**

The generated Daily Transaction File should contain the correct transactions and use the required formatting.

This includes:

* correct two-digit transaction codes  
* correct transaction information  
* correct field lengths  
* required space padding  
* correct monetary formatting  
* the 00 end-of-session transaction

#### **Application Stability**

The Front End should not crash or stop unexpectedly when processing valid or invalid input.

### **8\. Requirements Coverage**

The test suite covers each Front End transaction:

* login  
* logout  
* create  
* delete  
* sell  
* buy  
* refund  
* addcredit

The tests include:

* successful transactions  
* unauthorized transactions  
* session restrictions  
* nonexistent users and games  
* duplicate usernames and game names  
* user-type restrictions  
* boundary values  
* invalid input  
* credit limits  
* game ownership restrictions  
* Daily Transaction File generation and formatting  
* general Front End stability

This organization allows the same requirements tests to be maintained and used during later development and testing phases.

