import random
from math import sqrt
from environment import TerrainType, AntPerception, PheromoneMap
from ant import AntAction, AntStrategy, Direction


class PheromoneStrategy(AntStrategy):
    """
    A simple random strategy for ants.

    This strategy has minimal intelligence:
    - Picks up food when it sees it
    - Drops food at the colony
    - Tries to move towards food/colony when visible
    - Otherwise moves randomly
    - Always deposits pheromones after each step (home when searching, food when returning)
    """

    def __init__(self):
        """Initialize the strategy with last action tracking"""
        # Track the last action to alternate between movement and pheromone deposit
        self.ants_last_action = {}  # ant_id -> last_action
        self.ants_last_movement = {}
        self.ants_u_turn = {}

    def decide_action(self, perception: AntPerception) -> AntAction:
        """Decide an action based on current perception"""

        # Get ant's ID to track its actions
        ant_id = perception.ant_id
        last_action = self.ants_last_action.get(ant_id, None)

        if self.ants_u_turn.get(ant_id, 0) > 0:
            self.ants_u_turn[ant_id] -= 1
            self.ants_last_action[ant_id] = AntAction.TURN_RIGHT
            return AntAction.TURN_RIGHT

        # Priority 1: Pick up food if standing on it
        if (not perception.has_food) and perception.can_see_food():
            if perception.visible_cells.get((0, 0), None) == TerrainType.FOOD:
                self.ants_u_turn[ant_id] = 4
                self.ants_last_action[ant_id] = AntAction.PICK_UP_FOOD
                return AntAction.PICK_UP_FOOD
            
            # Alternate between movement and dropping pheromones
            # If last action was not a pheromone drop, drop pheromone
            if last_action != AntAction.DEPOSIT_HOME_PHEROMONE:
                self.ants_last_action[ant_id] = AntAction.DEPOSIT_HOME_PHEROMONE
                return AntAction.DEPOSIT_HOME_PHEROMONE
            
            dir = perception.get_food_direction()
            if perception.direction.value == dir:
                self.ants_last_action[ant_id] = AntAction.MOVE_FORWARD
                return AntAction.MOVE_FORWARD
            elif Direction.get_left(perception.direction).value == dir:
                self.ants_last_action[ant_id] = AntAction.TURN_LEFT
                return AntAction.TURN_LEFT
            else:
                self.ants_last_action[ant_id] = AntAction.TURN_RIGHT
                return AntAction.TURN_RIGHT

        # Priority 2: Drop food if at colony and carrying food
        if perception.has_food and perception.can_see_colony():
            if perception.visible_cells.get((0, 0), None) == TerrainType.COLONY:
                self.ants_u_turn[ant_id] = 4
                self.ants_last_action[ant_id] = AntAction.DROP_FOOD
                return AntAction.DROP_FOOD
            
            # Alternate between movement and dropping pheromones
            # If last action was not a pheromone drop, drop pheromone
            if last_action != AntAction.DEPOSIT_FOOD_PHEROMONE:
                self.ants_last_action[ant_id] = AntAction.DEPOSIT_FOOD_PHEROMONE
                return AntAction.DEPOSIT_FOOD_PHEROMONE
            
            dir = perception.get_colony_direction()
            if perception.direction.value == dir:
                self.ants_last_action[ant_id] = AntAction.MOVE_FORWARD
                return AntAction.MOVE_FORWARD
            elif Direction.get_left(perception.direction).value == dir:
                self.ants_last_action[ant_id] = AntAction.TURN_LEFT
                return AntAction.TURN_LEFT
            else:
                self.ants_last_action[ant_id] = AntAction.TURN_RIGHT
                return AntAction.TURN_RIGHT

        # Alternate between movement and dropping pheromones
        # If last action was not a pheromone drop, drop pheromone
        if last_action not in [
            AntAction.DEPOSIT_HOME_PHEROMONE,
            AntAction.DEPOSIT_FOOD_PHEROMONE,
        ]:
            if perception.has_food:
                self.ants_last_action[ant_id] = AntAction.DEPOSIT_FOOD_PHEROMONE
                return AntAction.DEPOSIT_FOOD_PHEROMONE
            else:
                self.ants_last_action[ant_id] = AntAction.DEPOSIT_HOME_PHEROMONE
                return AntAction.DEPOSIT_HOME_PHEROMONE
            
        # Otherwise, perform movement
        action = self._decide_movement(perception)
        self.ants_last_action[ant_id] = action
        self.ants_last_movement[ant_id] = action
        return action

    def _decide_movement(self, perception: AntPerception) -> AntAction:
        """Decide which direction to move based on current state"""

        dir = Direction.get_delta(perception.direction)
        l_dir = Direction.get_delta(Direction.get_left(perception.direction))
        l_dir_n = sqrt(l_dir[0]*l_dir[0] + l_dir[1]*l_dir[1])
        r_dir = Direction.get_delta(Direction.get_right(perception.direction))
        r_dir_n = sqrt(r_dir[0]*r_dir[0] + r_dir[1]*r_dir[1])

        # If has food, try to move toward colony if visible
        if perception.has_food:
            for (x,y), terrain in perception.visible_cells.items():
                if terrain == TerrainType.COLONY:
                    norme = sqrt(x*x + y*y)
                    if x*l_dir[0] + y*l_dir[1] > .9 * norme * l_dir_n and self.ants_last_movement[perception.ant_id] != AntAction.TURN_RIGHT:
                        # Colony is on the left
                        return AntAction.TURN_LEFT
                    elif x*r_dir[0] + y*r_dir[1] > .9 * norme * r_dir_n and self.ants_last_movement[perception.ant_id] != AntAction.TURN_LEFT:
                        # Colony is on the right
                        return AntAction.TURN_RIGHT
                    else: # Colony is ahead
                        return AntAction.MOVE_FORWARD
            action = self.pheromone_gradient(perception.home_pheromone, dir, l_dir, r_dir)
            # print(perception.ant_id)
            # print(dir, perception.home_pheromone)
            # print(action)
            if action != None :
                if action == AntAction.TURN_LEFT and self.ants_last_movement[perception.ant_id] == AntAction.TURN_RIGHT \
                    or action == AntAction.TURN_RIGHT and self.ants_last_movement[perception.ant_id] == AntAction.TURN_LEFT:
                    pass
                else:
                    if random.random() < 0.01:
                        return random.choice([AntAction.MOVE_FORWARD, AntAction.TURN_LEFT, AntAction.TURN_RIGHT])
                    return action
        # If doesn't have food, try to move toward food if visible
        else:
            for (x, y), terrain in perception.visible_cells.items():
                if terrain == TerrainType.FOOD:
                    norme = sqrt(x*x + y*y)
                    if x*l_dir[0] + y*l_dir[1] > .9 * norme * l_dir_n and self.ants_last_movement[perception.ant_id] != AntAction.TURN_RIGHT:
                        # Food is on the left
                        return AntAction.TURN_LEFT
                    elif x*r_dir[0] + y*r_dir[1] > .9 * norme * r_dir_n and self.ants_last_movement[perception.ant_id] != AntAction.TURN_LEFT:
                        # Food is on the right
                        return AntAction.TURN_RIGHT
                    else:
                        # Food is ahead
                        return AntAction.MOVE_FORWARD
            action = self.pheromone_gradient(perception.food_pheromone, dir, l_dir, r_dir)

            if action != None :
                if not (
                    action == AntAction.TURN_LEFT and self.ants_last_movement[perception.ant_id] == AntAction.TURN_RIGHT
                    or action == AntAction.TURN_RIGHT and self.ants_last_movement[perception.ant_id] == AntAction.TURN_LEFT
                ):
                    if random.random() < 0.01:
                        return random.choice([AntAction.MOVE_FORWARD, AntAction.TURN_LEFT, AntAction.TURN_RIGHT])
                    return action

        if dir not in perception.visible_cells: # if agaisnt wall
            if l_dir in perception.visible_cells:
                return AntAction.TURN_LEFT
            elif r_dir in perception.visible_cells:
                return AntAction.TURN_RIGHT
            else:
                return random.choice((AntAction.TURN_LEFT, AntAction.TURN_RIGHT))

        # Random movement if no specific goal
        movement_choice = random.random()

        if movement_choice < 0.8:  # 80% chance to move forward
            return AntAction.MOVE_FORWARD
        elif movement_choice < 0.9:  # 10% chance to turn left
            return AntAction.TURN_LEFT
        else:  # 10% chance to turn right
            return AntAction.TURN_RIGHT
    
    def pheromone_gradient(self, pheromone: dict[tuple[int, int], float], dir: tuple[int, int], l_dir: tuple[int, int], r_dir: tuple[int, int]) -> AntAction|None:
        action = None

        if dir[0] and dir[1]:
            left_acc = 0
            right_acc = 0
            straight_acc = 0
            for (x,y), power in pheromone.items():
                norm = sqrt(x*x+y*y)
                if x*l_dir[0] + y*l_dir[1] > .85 * norm:
                    left_acc += power
                elif x*r_dir[0] + y*r_dir[1] > .85 * norm:
                    right_acc += power
                if x*dir[0] + y*dir[1] > 1.20 * norm:
                    straight_acc += power

        else:
            left_acc = 0
            right_acc = 0
            straight_acc = 0
            for (x,y), power in pheromone.items():
                norm = sqrt(x*x+y*y)
                if x*l_dir[0] + y*l_dir[1] > 1.31 * norm:
                    left_acc += power
                elif x*r_dir[0] + y*r_dir[1] > 1.31 * norm:
                    right_acc += power
                if x*dir[0] + y*dir[1] > .85 * norm:
                    straight_acc += power
            left_acc *= 4
            right_acc *= 4
            straight_acc *= 3

        if straight_acc > left_acc and straight_acc > right_acc:
            action = AntAction.MOVE_FORWARD
        elif left_acc > straight_acc and left_acc > right_acc:
            action = AntAction.TURN_LEFT
        elif right_acc > straight_acc and right_acc > left_acc:
            action = AntAction.TURN_RIGHT

        return action

