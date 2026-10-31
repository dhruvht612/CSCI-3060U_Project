#pragma once

#include <string>

// Phase 1 compatibility profile, pending TA clarification of handout conflicts.
// See docs/Phase3_Format_Decisions.md. Never truncate a valid name to fit a record.
namespace record {
constexpr long long maxCreditCents = 99999900;

inline bool validName(const std::string& name, std::size_t maximum) {
    if (name.empty() || name.size() > maximum || name == "END" ||
        name.front() == ' ' || name.back() == ' ') return false;
    for (unsigned char character : name) {
        if (character < 32 || character > 126) return false;
    }
    return true;
}

inline std::string field(const std::string& text, std::size_t width) {
    return text + std::string(width - text.size(), ' ');
}

inline std::string money(long long cents, std::size_t width) {
    std::string text = std::to_string(cents / 100) + '.' +
                       (cents % 100 < 10 ? "0" : "") + std::to_string(cents % 100);
    return std::string(width - text.size(), '0') + text;
}

inline std::string account(const std::string& code, const std::string& username,
                           const std::string& type, long long cents) {
    return code + ' ' + field(username, 15) + ' ' + field(type, 2) + ' ' + money(cents, 9);
}
}  // namespace record
