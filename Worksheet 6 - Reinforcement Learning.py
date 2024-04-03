import random


class Node:
    def __init__(self, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.up = None
        self.down = None
        self.label = None


class Agent:
    def __init__(self, initialNode):
        self.currentNode = initialNode
        self.currentNode.label = "agent"
        self.goalFound = False
        self.foodFound = False
        self.foodCount = 0



    def eatFood(self):
        if self.currentNode.label == "food":
            self.currentNode.label = None
            self.foodCount += 1




    def moveNorth(self):
        print("Moving North")
        if self.currentNode.up:
            self.currentNode.label = None
            self.currentNode = self.currentNode.up
            self.currentNode.label == "agent"
        else:
             print("Wall Ahead")
             self.currentNode = self.currentNode.down
    

    def moveSouth(self):
        print("Moving South")
        if self.currentNode.down:
            self.currentNode.label = None 
            self.currentNode = self.currentNode.down
            self.currentNode.label == "agent"
        else:
            print("Wall Ahead")
            self.currentNode = self.currentNode.up

  


    def moveEast(self):
        print("Moving East")
        if self.currentNode.next:
            self.currentNode.label = None
            self.currentNode = self.currentNode.next
            self.currentNode.label == "agent"
        else:
            print("Wall Ahead")
            self.currentNode = self.currentNode.prev



    def moveWest(self):
        print("Moving West")
        if self.currentNode.prev:
            self.currentNode.label = None
            self.currentNode = self.currentNode.prev
            self.currentNode.label == "agent"
        else:
            print("Wall Ahead")
            self.currentNode = self.currentNode.next
  



    def percieveLabel(self):
        return self.currentNode.label





    def moveTowardsGoal(self):
        label = self.percieveLabel()
        if label == "goal":
            self.goalFound = True
            print("Goal Found Agent Can Rest :)")
            return


        if label == "north":
            self.moveNorth()
        elif label == "south":
            self.moveSouth()
        elif label == "east":
            self.moveEast()
        elif label == "west":
            self.moveWest()




    def moveRandomAndEat(self,grid):
        label = self.percieveLabel()
        if label == "food":
            self.foodFound = True
            self.eatFood()
        else:
            self.moveRandom()



    def moveTowardsFoodOrGoal(self):
        if not self.foodFound:
            self.moveRandomAndEat()
        elif not self.goalFound:
            self.moveTowadsGoal()
        



    def moveRandom(self):
        directions = [self.moveNorth, self.moveSouth, self.moveEast, self.moveWest]
        randomDirection = random.choice(directions)
        randomDirection()
        
        
    

class Goal:
    def __init__(self, initialNode):
        self.currentNode = initialNode
        self.currentNode.label = "goal"

class Food:
    def __init__(self, initialNode):
        self.currentNode = initialNode
        self.currentNode.label = "food"



class GridWorld:
    def __init__(self, rows, columns,numFoods, agentPosition, goalPosition):
        self.rows = rows
        self.columns = columns
        self.agent = None
        self.foods = []
        self.goal = None
        self.grid = self.createGrid(numFoods, agentPosition, goalPosition)



    def createGrid(self, numFoods, agentPosition , goalPosition):
        grid = [[Node() for _ in range(self.columns)]for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                if i > 0:
                    grid[i][j].up = grid[i - 1][j]
                if i < self.rows - 1:
                    grid[i][j].down = grid[i + 1][j]
                if j > 0:
                    grid[i][j].prev = grid[i][j - 1]
                if j < self.columns - 1:
                    grid[i][j].next = grid[i][j + 1]

        agentX, agentY = agentPosition
        goalX, goalY = goalPosition
        
        goalX = max(0,min(goalX, self.rows - 1))
        goalY = max(0,min(goalY, self.columns - 1))
        
        agentX = max(0,min(agentX, self.rows - 1))
        agentY = max(0,min(agentY, self.columns - 1))
        
        #Min, Max used to clamp initial Positions to valid indicies
        #TLDR make sures that they are in the right place despite grid size
        #else you get a index Error

        agentPos = grid[agentX][agentY]
        goalPos = grid[goalX][goalY]
        self.agent = Agent(agentPos)
        self.goal = Goal(goalPos)
        goalPos.label = "goal"

        occupiedCells = {(goalX, goalY),(agentX, agentY)}
        
        for _ in range(numFoods):
            foodI,foodJ = random.randint(0, self.rows - 1), random.randint(0, self.columns - 1)
            while(foodI,foodJ) in occupiedCells:
                foodI,foodJ = random.randint(0, self.rows - 1), random.randint(0, self.columns - 1)
            occupiedCells.add((foodI, foodJ))
            foodPos = grid[foodI][foodJ]
            self.foods.append(Food(foodPos))


        for x in range(self.rows):
            for y in range(self.columns):
                if x > goalX:
                    grid[x][y].label = "north"
                elif x < goalX:
                    grid[x][y].label = "south"
                elif x == goalX and y < goalY:
                    grid[x][y].label = "east"
                elif x == goalX and y > goalY:
                    grid[x][y].label = "west"
        
        return grid





    def displayGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == self.agent.currentNode:
                    print("--[X]--",end="|")
                elif self.grid[i][j] == self.goal.currentNode:
                    print("--[G]--",end="|")
                elif any(self.grid[i][j] == food.currentNode for food in self.foods):
                    print("--[F]--",end="|")

                else:
                    print("--[-]--", end="|")
            print("\n" + '-' *(self.columns * 8-1))





##    def allFoodEaten(self):
##        return len(self.foods) == 0
##
##
##
##
##
##    def moveTowardsFood(self):
##        while not self.allFoodEaten() and not self.agent.goalFound:
##            previousFoodCount = self.agent.foodCount
##            self.agent.moveRandom()
##            if self.agent.foodCount > previousFoodCount:
##                print("Food Count: ",self.agent.foodCount)
##            self.updateFood(self.agent.currentNode)
##            self.displayGrid()
##            print("Food Count:", self.agent.foodCount)
##            print()
##        if self.allFoodEaten():
##            print("All Food Eaten, Moving To Goal")
##            self.agent.moveTowardsGoal()
##            self.displayGrid()
##
##
##
##    def checkFood(self,data):
##        return any(data == food.currentNode for food in self.foods)
##
##
##
    def updateFood(self, data):
        self.foods = [food for food in self.foods if food.currentNode != data]
            







  





    
                    








if __name__ == "__main__":
    rows, columns = 6, 4
    goalPosition = (5,3)
    agentPosition = (2,2)
    numFoods = 10
    moves = 0
    grid = GridWorld(rows,columns, numFoods, agentPosition ,goalPosition)
    a = grid.agent
    grid.displayGrid()
    while not(a.goalFound):
        a.moveRandomAndEat(grid)
        grid.displayGrid()
        print()
    





                    

