from GameObject import GameObject
from GameDefs import Pos
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals
from Game import Pill
from collections import deque

pillInstance = Pill(Pos(15, 3))


class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.state = "findPill"

    def updateState(self, new_state):
        self.state = new_state

    def move(self):

        if self.state == "chase":
            return self.chase()
        elif self.state == "findPill":
            return self.findPill()
        elif self.state == "collectDots":
            return self.collectDots()
        
        #if the pill is eaten, chase the ghost 
        if globals.game.pill.eaten() == True: 
            return self.updateState("chase")
        elif globals.game.ghost.checkCollision(globals.game.self):
           return self.updateState("collectDots")
        else: 
            return self.updateState("findPill")
    
    def findPill(self):
        direction = Direction.NONE
        

        # If no direction to avoid ghost, move towards the pill
        if direction == Direction.NONE:
            if globals.pill.position.y > self.position.y:
                direction = direction | Direction.DOWN
            if globals.pill.position.y < self.position.y:
                direction = direction | Direction.UP
            if globals.pill.position.x > self.position.x:
                direction = direction | Direction.RIGHT
            if globals.pill.position.x < self.position.x:
                direction = direction | Direction.LEFT


        newPosR = Pos(self.position.x + 1, self.position.y)  
        newPosL = Pos(self.position.x -1 , self.position.y)
        newPosU = Pos(self.position.x , self.position.y + 1)
        newPosD = Pos(self.position.x , self.position.y - 1)
        ghostPos = globals.game.ghost.position 

    
        if globals.game.check_position(newPosR) == SpriteType.WALL:
            if ghostPos.y > self.position.y:
                return Direction.DOWN
            else:
                return Direction.UP
            
        if globals.game.check_position(newPosL) == SpriteType.WALL:
            if ghostPos.y < self.position.y:
                return Direction.UP
            else:
                return Direction.DOWN
            
        if globals.game.check_position(newPosU) == SpriteType.WALL:
            if ghostPos.x < self.position.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT
            
        if globals.game.check_position(newPosD) == SpriteType.WALL:
            if ghostPos.x < self.position.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        
        return direction
                


    def chase(self):
        direction = Direction.NONE

        direction = self.wallChaseGhost()
        
        if globals.ghost.position.y > self.position.y:
            direction = direction | Direction.DOWN

        if globals.ghost.position.y < self.position.y:
            direction = direction | Direction.UP
        if globals.ghost.position.x > self.position.x:
            direction = direction | Direction.RIGHT
        if globals.ghost.position.x < self.position.x:
            direction = direction | Direction.LEFT
    

    def wallChaseGhost(self):
        direction = Direction.NONE
        newPosR = Pos(self.position.x + 1, self.position.y)  
        newPosL = Pos(self.position.x -1 , self.position.y)
        newPosU = Pos(self.position.x , self.position.y + 1)
        newPosD = Pos(self.position.x , self.position.y - 1)
        ghostPos = globals.game.ghost.position 

        if globals.game.check_position(newPosR) == SpriteType.WALL:
            if ghostPos.y > self.position.y:
                return Direction.DOWN
            else:
                return Direction.UP
            
        if globals.game.check_position(newPosL) == SpriteType.WALL:
            if ghostPos.y > self.position.y:
                return Direction.UP
            else:
                return Direction.DOWN
            
        if globals.game.check_position(newPosU) == SpriteType.WALL:
            if ghostPos.x > self.position.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT
            
        if globals.game.check_position(newPosD) == SpriteType.WALL:
            if ghostPos.x > self.position.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT


        return direction

    def collectDots(self):
        queue = deque([self.position])
        visited = set([self.position])

        while queue:
            position = queue.popleft()

            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                new_position = self.get_new_position(position, direction)

                if new_position not in visited and self.is_valid_position(new_position):
                    queue.append(new_position)
                    visited.add(new_position)


    def get_new_position(self, position, direction):
        if direction == Direction.UP:
            return Pos(position.x, position.y + 1)
        elif direction == Direction.DOWN:
            return Pos(position.x, position.y - 1)
        elif direction == Direction.LEFT:
            return Pos(position.x - 1, position.y)
        else:  # direction == Direction.RIGHT
            return Pos(position.x + 1, position.y)
    
    def is_valid_position(self, position):
        invalid_directions = set()
        positions_to_check = [
        (Pos(self.position.x + 1, self.position.y), Direction.RIGHT),
        (Pos(self.position.x - 1, self.position.y), Direction.LEFT),
        (Pos(self.position.x, self.position.y + 1), Direction.DOWN),
        (Pos(self.position.x, self.position.y - 1), Direction.UP),]

        for pos, dir in positions_to_check:
            if globals.game.check_position(pos) == SpriteType.WALL:
                invalid_directions.add(dir)
        
        for invalid_dir in invalid_directions:
            direction = direction & ~invalid_dir
            