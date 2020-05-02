# encoding: utf-8
"""
@author: dawinia
@time: 2020/5/1 上午10:01
@file: test.py
@desc: 
"""
import collections
from collections import defaultdict


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


from collections import defaultdict
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        d = defaultdict(int)

        ans = left = 0
        for i, ch in enumerate(s):
            if d[ch] == 0 or d[ch] < left:
                ans = max(ans, i - left + 1)
            else:
                left = d[ch]
            d[ch] = i + 1
        return ans


solution = Solution()
l1 = ListNode(1)
l1.next = ListNode(2)
l1.next.next = ListNode(4)
l2 = ListNode(1)
l2.next = ListNode(3)
l2.next.next = ListNode(4)
a = "DRRD"
print(solution.lengthOfLongestSubstring("abcABcbb"))
