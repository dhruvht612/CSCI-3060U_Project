#pragma once

#include <string>

// A game for sale, as stored in one line of the Available Games File.
struct Game {
    std::string name;          // at most 25 characters
    std::string seller;        // username of the seller
    long long priceCents = 0;  // price, in cents
};

// One line of the Games Collection File: a game owned by a user.
struct CollectionEntry {
    std::string gameName;
    std::string owner;
};
