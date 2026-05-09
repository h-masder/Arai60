class UnionFind:
    def __init__(self, number_of_cells: int):
        self.representative = list(range(number_of_cells))
        self. size = [1] * number_of_cells
    
    def find_root(self, cell: int) -> int:
        if self.representative[cell] != cell:
            self.representative[cell] = self.find_root(self.representative[cell])
        return self.representative[cell]

    def try_merge_cells(self, cell_a: int, cell_b: int) -> bool:
        root_a = self.find_root(cell_a)
        root_b = self.find_root(cell_b)

        if root_a == root_b:
            return False
        
        #小さいほうを大きいほうにマージする
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.representative[root_b] = root_a
        self.size[root_a] += self.size[root_b]

        return True
    
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        LAND = '1'
        WATER = '0'

        if not grid or not grid[0]:
            return 0
        
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])
        island_groups = UnionFind(number_of_rows * number_of_cols)
        number_of_islands = 0

        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] != LAND:
                    continue
                number_of_islands += 1
        
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] != LAND:
                    continue
                
                cell = row * number_of_cols + col
                if row + 1 < number_of_rows and grid[row + 1][col] == LAND:
                    if island_groups.try_merge_cells(cell, cell + number_of_cols):
                        number_of_islands -= 1
                if col + 1 < number_of_cols and grid[row][col + 1] == LAND:
                    if island_groups.try_merge_cells(cell, cell + 1):
                        number_of_islands -= 1
        
        return number_of_islands
