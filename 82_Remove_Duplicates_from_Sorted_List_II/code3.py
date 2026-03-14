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

        while unique.next is not None and unique.next.next is not None:
            if unique.next.val == unique.next.next.val:
                #重複がある最後のnodeを見つける
                ptr = unique.next
                while ptr.next is not None and ptr.val == ptr.next.val:
                    ptr = ptr.next
                unique.next = ptr.next
            else:
                unique = unique.next
        return dummy.next