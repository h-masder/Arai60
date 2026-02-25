# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()
        current_node = head
        visited.add(current_node)

        if current_node is None:
            return False
        
        while current_node.next:
            if current_node.next in visited:
                return True
            
            visited.add(current_node.next)
            current_node = current_node.next
        
        return False