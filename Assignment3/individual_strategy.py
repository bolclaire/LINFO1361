import random
from math import sqrt
from environment import TerrainType, AntPerception, PheromoneMap
from ant import AntAction, AntStrategy, Direction
from collections import deque
import heapq

class AntMemory:
    def __init__(self):
        self.is_last_pheromone = False
        self.is_searching = True
        self.map = {}
        self.actions = deque()
        self.pos = (0,0)

class PheromoneStrategy(AntStrategy):
    def __init__(self):
        self.ant_memories = {}
        self.current_memory = None
        # Track the last action to alternate between movement and pheromone deposit

    def decide_action(self, perception: AntPerception) -> AntAction:
        ant_id = perception.ant_id

        self.current_memory = self.ant_memories.get(ant_id, None)
        if self.current_memory == None:
            self.current_memory = AntMemory()
            self.ant_memories[ant_id] = self.current_memory
        

        for (x, y), terrain in perception.visible_cells.items():
            self.current_memory.map[(self.current_memory.pos[0]+x, self.current_memory.pos[1]+y)] = terrain

        if self.current_memory.is_searching:
            if not perception.has_food and perception.can_see_food():
                if perception.visible_cells.get((0,0), None) == TerrainType.FOOD:
                    self.current_memory.is_searching = False
                    self.current_memory.is_last_pheromone = True
                    self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.COLONY))
                    return AntAction.PICK_UP_FOOD
                action = self.goto(perception, is_food=True)
                self.current_memory.is_last_pheromone = False
                return self.update(action, perception.direction)
            
            return self.update(self.random_move(), perception.direction)
        else:
            if not self.current_memory.is_last_pheromone:
                self.current_memory.is_last_pheromone = not self.current_memory.is_last_pheromone
                return AntAction.DEPOSIT_FOOD_PHEROMONE
            
            self.current_memory.is_last_pheromone = not self.current_memory.is_last_pheromone
            if len(self.current_memory.actions) != 0:
                return self.update(self.current_memory.actions.popleft(), perception.direction)
            
            if perception.visible_cells.get((0,0), None) == TerrainType.FOOD:
                self.current_memory.is_searching = False
                self.current_memory.is_last_pheromone = True
                self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.FOOD))
                print(1)
                return AntAction.DROP_FOOD
        
        
    def random_move(self):
        movement_choice = random.random()

        if movement_choice < 0.8:  # 80% chance to move forward
            return AntAction.MOVE_FORWARD
        elif movement_choice < 0.9:  # 10% chance to turn left
            return AntAction.TURN_LEFT
        else:  # 10% chance to turn right
            return AntAction.TURN_RIGHT
    
    def goto(self, perception: AntPerception, is_food= True):
        dir = perception.get_food_direction() if is_food else perception.get_colony_direction()
        # print(dir, perception.direction)
        if dir == Direction.get_left(perception.direction).value:
            return AntAction.TURN_LEFT
        elif dir == perception.direction.value:
            return AntAction.MOVE_FORWARD
        else:
            return AntAction.TURN_RIGHT

    def get_dir(self, pos):
        match pos:
            case (1,0): return Direction.EAST
            case (1,1): return Direction.SOUTHEAST
            case (0,1): return Direction.SOUTH
            case (-1,1): return Direction.SOUTHWEST
            case (-1,0): return Direction.WEST
            case (-1,-1): return Direction.NORTHWEST
            case (0,-1): return Direction.NORTH
            case (1,-1): return Direction.NORTHEAST

    def astar(self, map_dict, obj: TerrainType):
        def heuristic(a, b):
            # Manhattan distance
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

        def neighbors(pos):
            x, y = pos
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (1,-1), (-1,1)]:  # 8-directional
                neighbor = (x + dx, y + dy)
                if neighbor in map_dict:
                    yield neighbor

        open_set = []
        heapq.heappush(open_set, (0, self.current_memory.pos))
        came_from = {}
        g_score = {self.current_memory.pos: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if map_dict[current] == obj:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            for neighbor in neighbors(current):
                tentative_g_score = g_score[current] + 1  # all edges have cost 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, current)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None  # No path found

    def parse_astar(self, perception: AntPerception, list: list[tuple[int, int]]):
        def get_turn_diff(start: Direction, end: Direction):
            t = (end.value - start.value) % 8
            return t if t < 4 else t-8 
        
        result = deque()

        dir = perception.direction
        pos1 = list[0]
        for pos2 in list[1:]:
            new_dir = self.get_dir((pos2[0]-pos1[0], pos2[1]-pos1[1]))
            t = get_turn_diff(new_dir, dir)

            if t > 0:
                for _ in range(t):
                    result.append(AntAction.TURN_LEFT)

            elif t < 0:
                for _ in range(-t):
                    result.append(AntAction.TURN_RIGHT)

            result.append(AntAction.MOVE_FORWARD)

            dir = new_dir
            pos1 = pos2
        
        return result

    def update(self, action, direction: Direction) -> AntAction:
        if action == AntAction.MOVE_FORWARD:
            dir = Direction.get_delta(direction)
            self.current_memory.pos = (self.current_memory.pos[0] + dir[0], self.current_memory.pos[1] + dir[1])
        return action
