class Solution:
    def isValid(self, s: str) -> bool:
        marker = "marker"
        stack = [marker]
        bracket_pairs = {
            "(": ")",
            "{": "}",
            "[": "]"
        }

        for c in s:
            if c in bracket_pairs:
                stack.append(bracket_pairs[c])
                continue       
            expected = stack.pop()
            if c != expected or c == marker:
                return False

        last = stack.pop()
        return last == marker
