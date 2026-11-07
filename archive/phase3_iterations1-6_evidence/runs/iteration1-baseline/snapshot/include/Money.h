#pragma once

#include <cctype>
#include <string>

// Parsing of money text shared by FileManager (file records) and FrontEnd
// (typed amounts). Money is handled everywhere as integer cents so that limit
// checks such as 600.00 + 400.01 > 1000.00 are exact.
namespace money {

// True if `text` is non-empty and contains only decimal digits.
inline bool isDigits(const std::string& text) {
    if (text.empty()) return false;
    for (unsigned char c : text) {
        if (!std::isdigit(c)) return false;
    }
    return true;
}

// Parses digits-dot-two-digits money text (e.g. "005000.00" or "15.00") into
// cents. Returns false and leaves `cents` unchanged if the text is not in that form.
inline bool parseCents(const std::string& text, long long& cents) {
    if (text.size() < 4 || text[text.size() - 3] != '.') return false;
    const std::string whole = text.substr(0, text.size() - 3);
    const std::string fraction = text.substr(text.size() - 2);
    if (!isDigits(whole) || !isDigits(fraction)) return false;
    cents = std::stoll(whole) * 100 + std::stoll(fraction);
    return true;
}

}  // namespace money
