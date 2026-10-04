"""
Coupon Code Validator
Source: https://leetcode.com/problems/coupon-code-validator/

Given parallel arrays code, businessLine, and isActive describing coupons,
return the codes of all valid coupons. A coupon is valid when:
  - its code is non-empty and contains only letters, digits, or underscores;
  - its businessLine is one of electronics, grocery, pharmacy, restaurant;
  - it is active.
Results are sorted by business-line category order, then by code lexicographically.

Example:
    Input:  code = ["SAVE20", "", "PHARMA5", "SAVE@20"]
            businessLine = ["restaurant", "grocery", "pharmacy", "restaurant"]
            isActive = [True, True, True, True]
    Output: ["PHARMA5", "SAVE20"]

Approach:
    Filter each coupon against the three rules, then sort the survivors with a
    composite key: (index of its business line, code).

Complexity: Time O(n log n) | Space O(n)
"""

from typing import List

VALID_BUSINESS_LINES = ["electronics", "grocery", "pharmacy", "restaurant"]


class Solution:
    def validateCoupons(
        self, code: List[str], businessLine: List[str], isActive: List[bool]
    ) -> List[str]:
        valid = []
        for c, line, active in zip(code, businessLine, isActive):
            if not c or not all(ch.isalnum() or ch == "_" for ch in c):
                continue
            if line not in VALID_BUSINESS_LINES:
                continue
            if not active:
                continue
            valid.append((c, line))

        valid.sort(key=lambda item: (VALID_BUSINESS_LINES.index(item[1]), item[0]))
        return [c for c, _ in valid]


if __name__ == "__main__":
    s = Solution()
    print(s.validateCoupons(
        ["SAVE20", "", "PHARMA5", "SAVE@20"],
        ["restaurant", "grocery", "pharmacy", "restaurant"],
        [True, True, True, True],
    ))  # ['PHARMA5', 'SAVE20']
    print(s.validateCoupons(
        ["GROCERY15", "ELECTRONICS_50", "DISCOUNT10"],
        ["grocery", "electronics", "invalid"],
        [False, True, True],
    ))  # ['ELECTRONICS_50']
