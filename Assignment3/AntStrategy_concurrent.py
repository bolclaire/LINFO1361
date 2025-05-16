import random
from math import sqrt
from environment import TerrainType, AntPerception
from ant import AntAction, AntStrategy, Direction
from collections import deque
import heapq

class AntMemory:
    def __init__(self):
        self.is_searching = True
        self.last_move = None
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
            if terrain != TerrainType.WALL:
                self.current_memory.map[(self.current_memory.pos[0]+x, self.current_memory.pos[1]+y)] = terrain

        if self.current_memory.is_searching:
            if not perception.has_food and perception.can_see_food():
                if perception.visible_cells.get((0,0), None) == TerrainType.FOOD:
                    self.current_memory.is_searching = False
                    self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.COLONY))
                    return AntAction.PICK_UP_FOOD

                action = self.goto(perception, is_food=True)
                return self.update(action, perception)
            
            return self.update(self.random_move(), perception)
            
        
        elif perception.has_food:
            
            if perception.can_see_colony():

                if perception.visible_cells.get((0,0), None) == TerrainType.COLONY:
                    self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.FOOD))
                    self.current_memory.is_searching = self.current_memory.actions == deque()
                    return AntAction.DROP_FOOD
            
                action = self.goto(perception, is_food=False)
                return self.update_nockeck(action, perception)
            
            if len(self.current_memory.actions) != 0:
                return self.update_nockeck(self.current_memory.actions.popleft(), perception)
            
            self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.COLONY))
            return self.update_nockeck(self.current_memory.actions.popleft(), perception)
        
        else:
            if perception.can_see_food():

                if perception.visible_cells.get((0,0), None) == TerrainType.FOOD:
                    self.current_memory.actions = self.parse_astar(perception, self.astar(self.current_memory.map, TerrainType.COLONY))
                    return AntAction.PICK_UP_FOOD
            
                action = self.goto(perception, is_food=True)
                return self.update_nockeck(action, perception)
            
            if len(self.current_memory.actions) != 0:
                return self.update_nockeck(self.current_memory.actions.popleft(), perception)
            
            self.current_memory.is_searching = True
            return self.update(self.random_move(), perception)
        
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

    def get_dir(self, dx, dy):
        if dx == 0 and dy < 0:
            return Direction.NORTH
        elif dx > 0 and dy < 0:
            return Direction.NORTHEAST
        elif dx > 0 and dy == 0:
            return Direction.EAST
        elif dx > 0 and dy > 0:
            return Direction.SOUTHEAST
        elif dx == 0 and dy > 0:
            return Direction.SOUTH
        elif dx < 0 and dy > 0:
            return Direction.SOUTHWEST
        elif dx < 0 and dy == 0:
            return Direction.WEST
        elif dx < 0 and dy < 0:
            return Direction.NORTHWEST
        return Direction.NORTH

    def astar(self, map_dict, obj: TerrainType):
        def heuristic(a, b):
            # Manhattan distance
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

        def neighbors(pos):
            x, y = pos
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (1,-1), (-1,1)]:
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
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            for neighbor in neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, current)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None  # No path found

    def parse_astar(self, perception: AntPerception, list: list[tuple[int, int]]|None):
        if list == None:
            return deque()
        def get_turn_diff(start: Direction, end: Direction):
            t = (end.value - start.value) % 8
            return t if t < 4 else t-8 
        
        result = deque()

        dir = perception.direction
        pos1 = list[0]
        for pos2 in list[1:]:
            new_dir = self.get_dir(pos2[0]-pos1[0], pos2[1]-pos1[1])
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

    def update_nockeck(self, action, perception: AntPerception):
        dir = Direction.get_delta(perception.direction)
        if action == AntAction.MOVE_FORWARD and perception.visible_cells.get(dir, TerrainType.WALL) != TerrainType.WALL:
            self.current_memory.pos = (self.current_memory.pos[0] + dir[0], self.current_memory.pos[1] + dir[1])
        return action

    def update(self, action, perception: AntPerception) -> AntAction:
        dir = Direction.get_delta(perception.direction)
        if action == AntAction.MOVE_FORWARD:
            if perception.visible_cells.get(dir, TerrainType.WALL) != TerrainType.WALL:
                self.current_memory.pos = (self.current_memory.pos[0] + dir[0], self.current_memory.pos[1] + dir[1])
            else:
                if (
                    self.current_memory.last_move == AntAction.TURN_RIGHT 
                    or perception.visible_cells.get(Direction.get_delta(Direction.get_right(perception.direction)), TerrainType.WALL) != TerrainType.WALL
                ):
                    action = AntAction.TURN_RIGHT
                elif (
                    self.current_memory.last_move == AntAction.TURN_LEFT 
                    or perception.visible_cells.get(Direction.get_delta(Direction.get_left(perception.direction)), TerrainType.WALL) != TerrainType.WALL
                ):
                    action = AntAction.TURN_LEFT
                else:
                    action = random.choice([AntAction.TURN_LEFT, AntAction.TURN_RIGHT])
        
        self.current_memory.last_move = action
        return action
