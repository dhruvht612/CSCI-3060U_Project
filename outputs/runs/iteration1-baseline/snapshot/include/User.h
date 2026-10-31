#pragma once

#include <string>

// A user account, as stored in one line of the Current User Accounts File.
struct User {
    std::string username;       // at most 15 characters
    std::string type;           // AA (admin), FS (full-standard), BS (buy-standard) or SS (sell-standard)
    long long creditCents = 0;  // available credit, in cents
};
