# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        
        dummy = ListNode(next=head)
        unique = dummy
        node = head

        while node is not None:
            if node.next is not None and node.val == node.next.val:
                while node.next is not None and node.val == node.next.val:
                    node = node.next
                #whileを抜けると重複の最後にいる
                unique.next = node.next
            else:
                unique = unique.next
            node = node.next

        return dummy.next