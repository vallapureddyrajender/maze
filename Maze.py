import sys
import os
import numpy as np
# this program is successfully execute using Python 3.10.6 version
# please install numpy library to execute this program.
# pip3 install numpy 
class Mirror:
    direction = None
    leftSide = False
    rightSide = False

    def __init__(self, *args):
        if len(args) == 0:
            raise Exception("No parameters passed.")
        
        if args[0] != "R" and args[0] != "L":
            raise Exception("The" + args[0] + "directions of mirror is not supported.")

        self.direction = args[0]

        if len(args) == 1:
            self.leftSide = True
            self.rightSide = True
        else:
            if args[1] != "R" and args[1] != "L":
                raise Exception("The" + args[1] + "of a mirror is not supported.")

            if args[1] == "R":
                self.rightSide = True
            else:
                self.leftSide = True
            
class Position:
    col = None
    row = None
    axis = None
    direction = None

    def __init__(self, col, row, axis, direction):
        self.row = row
        self.col = col
        if axis != "H" and axis != "V":
            raise Exception("The " + axis + " direction of mirror is not supported.")
        self.axis = axis
        if direction != "+" and direction != "-":
            raise Exception("The " + direction + " direction of movement is not supported.")
        self.direction = direction

    def __str__(self):
        return "position: " + str(self.col) + "x" + str(self.row) + " (" + self.axis + self.direction + ") "

class MirrorMaze:
    def main(self):
        filePath = input("Please enter the file name with path: ")
        if not os.path.isfile(filePath):
           print("File path {} does not exist. Exiting...".format(filePath))
           sys.exit()

        if not filePath.lower().endswith('.txt'):
            print("Not a valid file. Please enter a valid ascii text file..")
            sys.exit()
        
        fileCounter = 0
        laserAxis = None
        mirrors = []
        mazeRows = 0
        mazeCols = 0
        laserRow = -1
        laserCol = -1
        
        with open(filePath) as fp:
            for line in fp:
                curLine = line.strip()
                if curLine == "-1":
                    fileCounter += 1
                else:
                    if fileCounter == 0:
                        mazeSize = curLine
                        mazeCols = int(mazeSize.strip().split(",")[0])
                        mazeRows = int(mazeSize.strip().split(",")[1])
                    elif fileCounter == 1:
                        mirrors.append(curLine)
                    elif fileCounter == 2:
                        laser = curLine.strip().split(",")
                        laserCol = int(laser[0])
                        laserRow = int(laser[1][:len(laser[1])-1])
                        laserAxis = laser[1][-1]
            fp.close()
            
        mirrorMaze = np.ndarray((mazeCols, mazeRows), dtype=np.object_)
        for m in mirrors:
            tempList = m.strip().split(",")
            col = int(tempList[0])
            digitCount = 0
            for i, v in enumerate(tempList[1]):
                if v.isdigit():
                    digitCount += 1
            
            row = int(tempList[1][0:digitCount])
            sd = tempList[1][digitCount:]
            if len(sd) > 1:
                d = sd[0:1]
                s = sd[1:]
                tmpMirror = Mirror(d, s)
            else:
                d = sd
                tmpMirror = Mirror(d)

            mirrorMaze[col][row] = tmpMirror

        self.mazePath(mirrorMaze, laserCol, laserRow, laserAxis)

    def mazePath(self, board, col, row, axis):
        if col < 0 or row < 0 or col >= board.shape[0] or row >= board.shape[1] or (axis != "H" and axis != "V"):
            print("incorrect input")
            return

        print("the dimensions of board: " + str(board.shape[0]) + " x " + str(board.shape[1]))

        path = []
        direction = "+"
        path.append(Position(col, row, axis, direction))

        last = path[len(path) - 1]
        while (0 <= last.col < board.shape[0]) and (0 <= last.row < board.shape[1]):
            self.findNextPosition(board, path)
            last = path[len(path) - 1]
        
        print("the path of the laser: ")
        for i in range(len(path)-1):
            print(path[i])

    @staticmethod
    def findNextPosition(board, path):
        prev = path[len(path) - 1]
        prevCol = prev.col
        prevRow = prev.row
        prevAxis = prev.axis
        prevDirection = prev.direction
        nextCol = -1
        nextRow = -1
        nextAxis = prevAxis
        nextDirection = prevDirection

        if prevAxis == "H":
            nextCol = prevCol
            if prevDirection == "+":
                nextCol += 1
            else:
                nextCol += -1
            nextRow = prevRow

        if prevAxis == "V":
            nextRow = prevRow
            if prevDirection == "+":
                nextRow += 1
            else:
                nextRow += -1
            nextCol = prevCol

        if (0 <= nextCol < board.shape[0]) and (0 <= nextRow < board.shape[1]):
            mirror = board[nextCol][nextRow]
            if mirror is not None:

                if mirror.direction == "R":
                    if mirror.rightSide:
                        if prevAxis == "V" and prevDirection == "+":
                            nextAxis = "H"
                            nextDirection = "+"
                        if prevAxis == "H" and prevDirection == "-":
                            nextAxis = "V"
                            nextDirection = "-"

                    if mirror.leftSide:
                        if prevAxis == "V" and prevDirection == "-":
                            nextAxis = "H"
                            nextDirection = "-"
                        if prevAxis == "H" and prevDirection == "+":
                            nextAxis = "V"
                            nextDirection = "+"

                if mirror.direction == "L":
                    if mirror.rightSide:
                        if prevAxis == "V" and prevDirection == "-":
                            nextAxis = "H"
                            nextDirection = "+"
                        if prevAxis == "H" and prevDirection == "-":
                            nextAxis = "V"
                            nextDirection = "+"

                    if mirror.leftSide:
                        if prevAxis == "V" and prevDirection == "+":
                            nextAxis = "H"
                            nextDirection = "-"
                        if prevAxis == "H" and prevDirection == "+":
                            nextAxis = "V"
                            nextDirection = "-"

        nextTemp = Position(nextCol, nextRow, nextAxis, nextDirection)
        for p in path:
            if p == nextTemp:
                Exception("the laser is trapped in the maze.")

        path.append(nextTemp)

           
if __name__ == '__main__':
    MirrorMaze().main()