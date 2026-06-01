# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None and l2 is None:
            return None
        if l1 is not None and l2 is None:
            return l1
        if l1 is None and l2 is not None:
            return l2
        
        dummy = ListNode()
        node = dummy

        carry = 0
        while l1 is not None and l2 is not None:
            total = l1.val + l2.val + carry
            carry = 0
            if total >= 10:
                carry = 1
                total %= 10
            node.next = ListNode(total)
            node = node.next
            l1 = l1.next
            l2 = l2.next
        
        while l1 is not None:
            total = l1.val + carry
            carry = 0
            if total >= 10:
                carry = 1
                total %= 10
            node.next = ListNode(total)
            node = node.next
            l1 = l1.next
        
        while l2 is not None:
            total = l2.val + carry
            carry = 0
            if total >= 10:
                carry = 1
                total %= 10
            node.next = ListNode(total)
            node = node.next
            l2 = l2.next

        if carry == 1:
            node.next = ListNode(1)

        return dummy.next
