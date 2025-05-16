import heapq
from collections import deque

# Directions (8-connected grid)
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)]

class GridEnvironment:
    def __init__(self, grid, start, vision_radius=1):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = start
        self.vision_radius = vision_radius
        self.agent_pos = start
        self.seen = set()
        self.known_grid = [['?' for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_vision()

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def update_vision(self):
        r, c = self.agent_pos
        for dr in range(-self.vision_radius, self.vision_radius + 1):
            for dc in range(-self.vision_radius, self.vision_radius + 1):
                nr, nc = r + dr, c + dc
                if self.is_valid(nr, nc):
                    self.known_grid[nr][nc] = self.grid[nr][nc]
                    self.seen.add((nr, nc))

    def move(self, new_pos):
        self.agent_pos = new_pos
        self.update_vision()

    def get_neighbors(self, pos):
        neighbors = []
        for dr, dc in DIRS:
            nr, nc = pos[0] + dr, pos[1] + dc
            if self.is_valid(nr, nc) and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def is_goal(self, pos):
        return self.grid[pos[0]][pos[1]] == 'G'

def bfs_to_target(env: GridEnvironment, target_char='G'):
    queue = deque()
    queue.append((env.start, [env.start]))
    visited = set()
    visited.add(env.start)

    while queue:
        current, path = queue.popleft()
        env.move(current)

        if env.is_goal(current):
            print("Goal found at", current)
            return path

        for neighbor in env.get_neighbors(current):
            if neighbor not in visited and neighbor in env.seen:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    print("Goal not reachable.")
    return None

def a_star(env: GridEnvironment, start, goal):
    def heuristic(a, b):
        return max(abs(a[0]-b[0]), abs(a[1]-b[1]))  # Chebyshev distance for 8 directions

    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    g_cost = {start: 0}

    while open_set:
        _, current, path = heapq.heappop(open_set)
        if current == goal:
            return path

        for neighbor in env.get_neighbors(current):
            tentative_g = g_cost[current] + 1
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor, path + [neighbor]))

    return None

def explore_and_return(env: GridEnvironment):
    path_to_goal = bfs_to_target(env)
    if not path_to_goal:
        print("Exploration failed.")
        return

    goal = path_to_goal[-1]
    path_back = a_star(env, goal, env.start)

    full_path = path_to_goal + path_back[1:]  # Avoid repeating goal
    print("Full path (to goal and back):")
    for p in full_path:
        print(p)

# Example Grid
# '.' = empty space
# '#' = obstacle
# 'G' = goal
grid = [
    ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '.', '#', '.', '#', '#', '#', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
    ['#', '.', '#', '#', '#', '.', '#', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '#', '.', '#', 'G'],
]

start = (0, 0)
env = GridEnvironment(grid, start, vision_radius=1)
explore_and_return(env)
