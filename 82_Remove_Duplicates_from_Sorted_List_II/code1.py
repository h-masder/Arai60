# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        #スキップ
        if head.val == head.next.val:
            val = head.val
            while head is not None and val == head.val:
                head = head.next
            return self.deleteDuplicates(head)
        
        head.next = self.deleteDuplicates(head.next)
        return head