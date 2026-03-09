# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):

#         self.val = val
#         self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def helper(node: Optional[ListNode]) -> None:
            if node.next is not None:
                if node.val == node.next.val:
                    node.next = node.next.next
                    helper(node)
                else:
                    helper(node.next)
            return None
        
        if head is None:
            return None
        node = head
        helper(node)
        
        return head