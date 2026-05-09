#bfs, 再帰
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        LAND = '1'
        WATER = '0'

        if not grid or not grid[0]:
            return 0
        
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])
        visited = set()
        def explore_island(frontier: List[int]) -> None:
            if not frontier:
                return
            next_frontier = []
            for row, col in frontier:
                for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
                    if not(0 <= neighbor_row < number_of_rows):
                        continue
                    if not(0 <= neighbor_col < number_of_cols):
                        continue
                    if not(grid[neighbor_row][neighbor_col] == LAND and (neighbor_row, neighbor_col) not in visited):
                        continue
                    visited.add((neighbor_row, neighbor_col))
                    next_frontier.append((neighbor_row, neighbor_col))
            return explore_island(next_frontier)
        
        number_of_islands = 0
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] == LAND and (row, col) not in visited:
                    number_of_islands += 1
                    visited.add((row, col))
                    explore_island([(row, col)])
        return number_of_islands


#bfs, 再帰なしバージョン
#dfs, 再帰なしとの違いはfrontierのポップの方法だけ
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        LAND = '1'
        WATER = '0'

        if not grid or not grid[0]:
            return 0
        
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])
        visited = set()
        def explore_island(row: int, col: int) -> None:
            frontier = deque([(row, col)])
            while frontier:
                row, col = frontier.popleft()
                for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
                    if not(0 <= neighbor_row < number_of_rows):
                        continue
                    if not(0 <= neighbor_col < number_of_cols):
                        continue
                    if not(grid[neighbor_row][neighbor_col] == LAND and (neighbor_row, neighbor_col) not in visited):
                        continue
                    visited.add((neighbor_row, neighbor_col))
                    frontier.append((neighbor_row, neighbor_col))
        
        number_of_islands = 0
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] == LAND and (row, col) not in visited:
                    number_of_islands += 1
                    visited.add((row, col))
                    explore_island(row, col)
        return number_of_islands
