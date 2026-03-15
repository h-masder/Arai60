class Solution:
    def isValid(self, s: str) -> bool:
        stack = ['marker']
        for c in s:
            if c == '(':
                stack.append(')')
            if c == '{':
                stack.append('}')
            if c == '[':
                stack.append(']')

            if c in [')', '}', ']']:
                if c == stack.pop():
                    continue
                else: #一致しない場合(markerである場合も含む)
                    return False
        
        if 'marker' == stack.pop():
            return True
            
        return False
            