"""
Problem: https://leetcode.com/problems/coupon-code-validator/description/

"""

from typing import List


class Coupon:
    def __init__(self, code, bussinessLine, isActive):
        self.code = code
        self.bussinessLine = bussinessLine
        self.isActive = isActive


def ValidateCoupons(
    code: List[str], bussinessLine: List[str], isActive: List[bool]) -> List[str]:
    
    valid_buissinessLines = ["electronics", "grocery", "pharmacy", "restaurant"]
    valid_coupons: List[Coupon] = []

    n = len(code)

    coupons: List[Coupon] = [
        Coupon(code[i], bussinessLine[i], isActive[i]) for i in range(n)
    ]

    for coupon in coupons:
        if not coupon.code or not all(c.isalnum() or c == "_" for c in coupon.code):
            continue

        if coupon.bussinessLine not in valid_buissinessLines:
            continue

        if not coupon.isActive:
            continue

        valid_coupons.append(coupon)

    # Sort by businessLine order, then by code lexicographically within each category
    valid_coupons.sort(
        key=lambda x: (valid_buissinessLines.index(x.bussinessLine), x.code)
    )

    return [coupon.code for coupon in valid_coupons]


code = ["SAVE20", "", "PHARMA5", "SAVE@20"]
businessLine = ["restaurant", "grocery", "pharmacy", "restaurant"]
isActive = [True, True, True, True]
print(ValidateCoupons(code, businessLine, isActive))  # output: ["SAVE20","PHARMA5"]

code = ["GROCERY15", "ELECTRONICS_50", "DISCOUNT10"]
businessLine = ["grocery", "electronics", "invalid"]
isActive = [False, True, True]
print(ValidateCoupons(code, businessLine, isActive))  # Output: ["ELECTRONICS_50"]
