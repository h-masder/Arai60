# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    # output: the last node in the cycle
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = set()
        node = head
        prev = None

        while node is not None:
            if node in visited:
                return prev
            
            visited.add(node)
            prev = node
            node = node.next

        return None