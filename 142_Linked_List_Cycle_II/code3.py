# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


class Solution:
    def detectCycle(self, head: Option[ListNode]) -> ListNode:
        if not isinstance(head, ListNode):
            return None
        
        slow = head
        fast = head

        # detect if the linked list has a cycle
        while True:
            if fast.next is None:
                return None
            if fast.next.next is None:
                return None
            
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                break
        
        # find at the start of the cycle
        slow = head
        while True:
            if slow is fast:
                return slow
            slow = slow.next
            fast = fast.next