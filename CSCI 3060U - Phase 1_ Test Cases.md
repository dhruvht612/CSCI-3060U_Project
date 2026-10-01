# **CSCI 3060U – Phase 1: Test Cases**

## **Front End Requirements Test Cases**

### **Test Cases**

| Test | What It Tests |
| ----- | ----- |
| **TC01 – Valid Login** | An existing user can successfully log in and begin a Front End session. |
| **TC02 – Invalid Login** | A login attempt using a nonexistent username is rejected. |
| **TC03 – Transaction Before Login** | A transaction other than login is rejected before a user has logged in. |
| **TC04 – Second Login During Session** | A second login transaction is rejected while a user is already logged in. |
| **TC05 – Valid Logout** | A logged-in user can log out, ending the session and producing the Daily Transaction File. |
| **TC06 – Logout Before Login** | A logout transaction is rejected when no user is logged in. |
| **TC07 – Transaction After Logout** | Transactions other than login are rejected after logout. |
| **TC08 – Valid Create User** | An admin can create a new user using a unique username of no more than 15 characters and a valid user type. |
| **TC09 – Unauthorized Create User** | A non-admin user cannot create a new user. |
| **TC10 – Duplicate Username** | A new user cannot be created using a username that already belongs to a current user. |
| **TC11 – Username Over 15 Characters** | A username longer than 15 characters is rejected during user creation. |
| **TC12 – Username Exactly 15 Characters** | A username containing exactly 15 characters is accepted when the other create requirements are satisfied. |
| **TC13 – Valid Delete User** | An admin can delete an existing user other than the currently logged-in user. |
| **TC14 – Unauthorized Delete User** | A non-admin user cannot delete another user. |
| **TC15 – Delete Nonexistent User** | An admin cannot delete a username that does not belong to a current user. |
| **TC16 – Delete Current User** | An admin cannot delete the account currently being used for the session. |
| **TC17 – Valid Sell** | A permitted user can place a uniquely named game up for sale at a valid price. |
| **TC18 – Buy-Standard User Attempts Sell** | A buy-standard user cannot perform a sell transaction. |
| **TC19 – Maximum Game Price** | A game priced at exactly \$999.99 is accepted when all other sell requirements are satisfied. |
| **TC20 – Price Above Maximum** | A game price greater than \$999.99 is rejected. |
| **TC21 – Game Name Exactly 25 Characters** | A game name containing exactly 25 characters is accepted when all other sell requirements are satisfied. |
| **TC22 – Game Name Over 25 Characters** | A game name longer than 25 characters is rejected. |
| **TC23 – Duplicate Game Name** | A game cannot be placed for sale using a name that is already used by another game. |
| **TC24 – Invalid Sell Input** | Invalid sell input, such as a non-numeric price, is handled without the Front End crashing. |
| **TC25 – Transaction on Newly Listed Game** | A newly listed game cannot be used in further transactions until the next session. |
| **TC26 – Valid Buy** | A permitted user with sufficient credit can purchase an existing available game they do not already own. |
| **TC27 – Sell-Standard User Attempts Buy** | A sell-standard user cannot perform a buy transaction. |
| **TC28 – Buy Nonexistent Game** | A purchase is rejected when the requested game does not exist. |
| **TC29 – Insufficient Credit** | A purchase is rejected when the buyer does not have enough credit to purchase the game. |
| **TC30 – Exact Credit Purchase** | A purchase succeeds when the buyer's available credit exactly equals the game's price. |
| **TC31 – Already-Owned Game** | A user cannot purchase a game they already own. |
| **TC32 – Valid Refund** | An admin can transfer a specified amount of credit from an existing seller to an existing buyer. |
| **TC33 – Unauthorized Refund** | A non-admin user cannot perform a refund transaction. |
| **TC34 – Refund to Nonexistent Buyer** | A refund is rejected when the specified buyer is not a current user. |
| **TC35 – Refund from Nonexistent Seller** | A refund is rejected when the specified seller is not a current user. |
| **TC36 – Valid Add Credit – Standard User** | A standard user can add a valid amount of credit to their own account. |
| **TC37 – Valid Add Credit – Admin** | An admin can add credit to an existing user's account. |
| **TC38 – Admin Adds Credit to Nonexistent User** | An admin cannot add credit to a username that does not exist. |
| **TC39 – Add Exactly \$1000** | A total of exactly \$1000.00 can be added to an account during one session. |
| **TC40 – Add More Than \$1000** | An attempt to add more than \$1000.00 to an account during one session is rejected. |
| **TC41 – Multiple Credit Additions to \$1000** | Multiple credit additions that total exactly \$1000.00 during one session are accepted. |
| **TC42 – Multiple Credit Additions Over \$1000** | An addition that would cause the total credit added during the session to exceed \$1000.00 is rejected. |
| **TC43 – Invalid Credit Amount** | Invalid credit input is handled without the Front End crashing. |
| **TC44 – Invalid Transaction Code** | An invalid transaction code is handled gracefully without the Front End crashing. |
| **TC45 – Daily Transaction File End Code** | The Daily Transaction File ends with the required 00 end-of-session transaction code. |
| **TC46 – Daily Transaction File Formatting** | Transactions written to the Daily Transaction File follow the required transaction codes, field widths, spacing, padding, and monetary formatting. |

### **Coverage Summary**

The test cases cover the Front End transaction types:

* login  
* logout  
* create  
* delete  
* sell  
* buy  
* refund  
* addcredit

The test suite includes successful transactions, unauthorized transactions, invalid inputs, boundary values, session restrictions, and Daily Transaction File requirements.

The suite also tests the general requirement that the Front End must handle bad input gracefully and should not crash or stop unexpectedly.