import queue
from GameObject import GameObject
from GameDefs import Pos
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals
from Game import Pill
import math 

# Define the PacMan class, which inherits from GameObject
class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)

    # Method to get the new position based on the current position and direction
    def getPosition(self, x, y, direction):
        # Update x and y coordinates based on the direction
        if direction & Direction.LEFT:
            x -= 1 
        if direction & Direction.DOWN:
            x += 1 
        if direction & Direction.UP:
            y -= 1
        if direction & Direction.RIGHT:
             y += 1
        return x, y

    # Method to get all possible directions
    def getDirections(self):
        directions=  [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        directions.extend (Direction.UP | Direction.RIGHT, 
                           Direction.UP | Direction.LEFT,
                           Direction.DOWN | Direction.RIGHT,
                           Direction.DOWN | Direction.LEFT)

        return directions

    # Dijkstra's algorithm to find the shortest path from start to end
    def dijkstras(self, start, end=None, positionType = {}, ghostPos=None):
        if positionType == None:
            positionType = {}

        # Initialize priority queue and distance dictionary
        pq = queue.PriorityQueue()
        pq.put((0, start.x, start.y))
        distance, pre = {(start.x, start.y): 0},{}
        directions = self.getDirections()

        # While there are still nodes to visit
        while not pq.empty():
            # Get the node with the smallest distance
            dist, x, y = pq.get()
            currDist = distance[(x, y)]
            posType = positionType.get((x, y), None)

            # If we've reached the end, break
            if end and x == end.x and y == end.y: 
                break

            # If we've found a dot or the end, return the distance and direction
            if (end == None and posType == SpriteType.DOT) or (end != None and x == end.x and y == end.y):
                firstDir = direction
                while (x, y) != start:
                    firstDir = pre[(x, y)][1]
                    x, y = pre[(x, y)][0]
                return currDist, firstDir

            # For each possible direction
            for direction in directions:
                # Get the next position and set the cost to 1
                nextX, nextY = self.getPosition(x, y, direction)
                cost = 1 

                # If there's a ghost nearby, increase the cost
                if ghostPos and math.dist([nextX, nextY], [ghostPos.x, ghostPos.y]) <= 10:
                    cost = 10 - math.dist([nextX, nextY], [ghostPos.x, ghostPos.y])

                # If we've already visited this node and the new path isn't shorter, skip it
                if (nextX, nextY) in distance and distance[(nextX, nextY)] <= currDist + cost:
                    continue

                posType = positionType.get((nextX, nextY), None)

                # If the node isn't a wall, add it to the queue and update the distance and previous node
                if positionType == None or positionType != SpriteType.WALL:
                    pq.put((currDist + cost, nextX, nextY))
                    distance[(nextX, nextY)] = currDist + cost
                    pre[(nextX, nextY)] = [(x, y), direction]

        # If we haven't found a path, return infinity and the last direction
        return float("inf"), firstDir

    def move(self):
    # Dictionary to store position types (e.g., walls, dots)
        pos_Type = {}
        
        # Populate the position type dictionary with objects on the game board
        for object in GameObject.gameObjects:
            pos_Type[(object.position.x, object.position.y)] = object.type

        # Check if there is an active pill in the game
        if globals.game.pill.isActive():
            # If there's an active pill and no ghost, find the shortest path to any position
            if globals.game.ghost.position == -1: 
                length, direction = self.dijkstras(self.position, None, pos_Type, None)
            else: 
                # If there's an active pill and a ghost, find the shortest path to the ghost
                length, direction = self.dijkstras(self.position, globals.game.ghost.position, pos_Type, None)
        else: 
            # If there's no active pill

            if globals.game.pill.position == -1:
                # If there's no pill on the board and a ghost, find the shortest path to the ghost
                length, direction = self.dijkstras(self.position, None, pos_Type, globals.game.ghost.position)
            else: 
                # If there's a pill on the board, find the shortest path to the pill while avoiding the ghost
                length, direction = self.dijkstras(self.position, globals.game.pill.position, pos_Type, globals.game.ghost.position)

        # Return the direction to move
        return direction
