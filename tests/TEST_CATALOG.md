# Test catalog

Every test is one transaction input file, `inputs/TCxx.txt`, run against the shared
data files in `data/`. The expected terminal output is `expected/TCxx.out` and the
expected daily transaction file is `expected/TCxx.etf`.

The "Records written" column lists the transaction codes in the expected daily
transaction file, apart from the `00` end-of-session record, which every file ends with.

| Test | Name | What it tests | Records written |
|---|---|---|---|
| TC01 | Valid Login | Login for the existing user ‘admin’ is accepted. The session begins. Logout is accepted and ends the session. | none |
| TC02 | Invalid Login | The nonexistent username ‘ghostuser’ is rejected. The Front End remains able to accept a valid login. The later admin login and logout are accepted. | none |
| TC03 | Transaction Before Login | The sell transaction before login is rejected. Login is then accepted normally. | none |
| TC04 | Second Login During Session | The first login is accepted. The second login is rejected because a user is already logged in. Logout ends the original session. | none |
| TC05 | Valid Logout | Logout is accepted while logged in. The Daily Transaction File is written and the session ends. | none |
| TC06 | Logout Before Login | The first logout is rejected because no user is logged in. The later login and logout are accepted. | none |
| TC07 | Transaction After Logout | After logout, sell is rejected because only login may be accepted. A new login can then begin another session. | none |
| TC08 | Valid Create User | The admin login is accepted. The new unique user ‘newuser’ is created as full-standard and the create transaction is saved for the Daily Transaction File. | 01 |
| TC09 | Unauthorized Create User | Create is rejected because the logged-in user is not an admin. | none |
| TC10 | Duplicate Username | Create is rejected because ‘buyer1’ is already a current username. | none |
| TC11 | Username Over 15 Characters | Create is rejected because the new username contains more than 15 characters. | none |
| TC12 | Username Exactly 15 Characters | The 15-character unique username is accepted when the other create requirements are satisfied. | 01 |
| TC13 | Valid Delete User | The existing user ‘delete1’ is deleted. Any games they have for sale are cancelled. The delete transaction is saved for the Daily Transaction File. | 02 |
| TC14 | Unauthorized Delete User | Delete is rejected because the logged-in user is not an admin. | none |
| TC15 | Delete Nonexistent User | Delete is rejected because ‘ghostuser’ is not a current user. | none |
| TC16 | Delete Current User | Delete is rejected because the username is the current logged-in user. | none |
| TC17 | Valid Sell | The sell transaction is accepted because the user may sell, the game name is unique and within 25 characters, and the price is within the maximum. | 03 |
| TC18 | Buy-Standard User Attempts Sell | Sell is rejected because a buy-standard account cannot perform sell transactions. | none |
| TC19 | Maximum Game Price | The sell transaction is accepted because $999.99 is the maximum permitted game price. | 03 |
| TC20 | Price Above Maximum | The sell transaction is rejected because the price exceeds $999.99. | none |
| TC21 | Game Name Exactly 25 Characters | The sell transaction is accepted because the unique game name is exactly 25 characters. | 03 |
| TC22 | Game Name Over 25 Characters | The sell transaction is rejected because the game name is longer than 25 characters. | none |
| TC23 | Duplicate Game Name | The sell transaction is rejected because all game names must be unique and ‘ExistingGame’ already exists. | none |
| TC24 | Invalid Sell Input | The invalid price is handled gracefully. The Front End does not crash or stop unexpectedly. | none |
| TC25 | Transaction on Newly Listed Game | The sell is accepted, but no further transaction on the newly listed game is accepted until the next session. | 03 |
| TC26 | Valid Buy | The purchase is accepted when the game exists, the account may buy, the buyer has enough credit, and the buyer does not already own the game. | 04 |
| TC27 | Sell-Standard User Attempts Buy | Buy is rejected because a sell-standard account cannot perform buy transactions. | none |
| TC28 | Buy Nonexistent Game | The purchase is rejected because the requested game does not exist. | none |
| TC29 | Insufficient Credit | The purchase is rejected because the buyer does not have enough credit. | none |
| TC30 | Exact Credit Purchase | The purchase is accepted when the buyer’s available credit exactly equals the game’s price. | 04 |
| TC31 | Already-Owned Game | The purchase is rejected because the buyer already owns the game. | none |
| TC32 | Valid Refund | The refund is accepted because both buyer and seller are current users. The specified credit is transferred from seller to buyer. | 05 |
| TC33 | Unauthorized Refund | Refund is rejected because it is a privileged transaction and the logged-in user is not an admin. | none |
| TC34 | Refund to Nonexistent Buyer | Refund is rejected because the buyer is not a current user. | none |
| TC35 | Refund from Nonexistent Seller | Refund is rejected because the seller is not a current user. | none |
| TC36 | Valid Add Credit - Standard User | The standard user adds $100.00 to their own account and the add-credit transaction is saved for the Daily Transaction File. | 06 |
| TC37 | Valid Add Credit - Admin | The admin adds $100.00 to the existing user ‘buyer1’. | 06 |
| TC38 | Admin Adds Credit to Nonexistent User | The add-credit transaction is rejected because the admin specified a username that does not exist. | none |
| TC39 | Add Exactly $1000 | Exactly $1000.00 is accepted because it is the maximum credit that may be added to an account in one session. | 06 |
| TC40 | Add More Than $1000 | The credit addition is rejected because it exceeds the $1000.00 per-session limit. | none |
| TC41 | Multiple Credit Additions to $1000 | Both additions are accepted because the total added to the account during the session is exactly $1000.00. | 06 |
| TC42 | Multiple Credit Additions Over $1000 | The first addition is accepted. The second is rejected because it would make the session total exceed $1000.00. | 06 |
| TC43 | Invalid Credit Amount | The invalid credit input is handled gracefully and the Front End does not crash. | none |
| TC44 | Invalid Transaction Code | The invalid transaction code is handled gracefully. The Front End remains running and can process the later logout. | none |
| TC45 | Daily Transaction File End Code | The Daily Transaction File produced at logout ends with the required 00 end-of-session transaction code. | none |
| TC46 | Daily Transaction File Formatting | The generated Daily Transaction File uses the required transaction code and field formatting for the create transaction and ends with 00. | 01 |
| TC47 | Search by Admin - Games and Users | An admin searches for "admin". The game AdminQuest and the users admin, selleradmin and adminfan are all shown, because an admin sees every matching account. Search writes nothing to the Daily Transaction File. | none |
| TC48 | Search by Standard User Hides Non-Selling Admins | A buy-standard user searches for "admin". The admin account "admin" has no games for sale, so it is not shown. selleradmin (an admin who is selling AdminQuest) and adminfan are shown, and so is the game AdminQuest. | none |
| TC49 | Search Is Case-Insensitive for a Sell-Standard User | A sell-standard user searches for "STAR". The game Star Seller matches even though the case differs. No user name contains "star". | none |
| TC50 | Search With No Matches | A full-standard user searches for "zzz". Nothing matches, so the Front End reports no games and no users and keeps running until logout. | none |
| TC51 | Search Before Login | search is entered before anyone logs in. It is rejected without prompting for a query, and the following login and logout work normally. | none |
| TC52 | Blank Search Query | An admin enters a blank search query. It is rejected with an error and no results are printed; the session continues to logout. | none |
| TC53 | Search After Deleting a User | An admin deletes seller1 and then searches for "seller". seller1 and the game Star Seller (which seller1 was selling) are gone, so only the users selleradmin and seller2 are shown. The delete is saved for the Daily Transaction File. | 02 |
| TC54 | Newly Listed Game Not Found by Search | seller1 lists the new game Star Shooter and then searches for "star". A game sold this session is not available until the next session, so only Star Seller is shown. The sell is saved for the Daily Transaction File. | 03 |
