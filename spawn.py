from random import randint
import os
import sys
import json

sys.setrecursionlimit(100000)

def cls():
    os.system(['clear','cls'][os.name == 'nt'])


#MapWidth = 50
#MapHeight = 200
MapWidth = 100
MapHeight = 100
PercentAreWalls = 50
VerticalThreshold = 1	# how far from top or bottom the body of water must reach
Map = [[0 for x in range(MapHeight)] for x in range(MapWidth)]

mapMiddle = 0

def RandomPercent(percent):
	if percent >= randint(1,101):
		return 1
	else: 
		return 0

def IsOutOfBounds(x,y):
	if x < 0 or y < 0:
		return True
	elif x > MapWidth-1 or y > MapHeight -1:
		return True
	else:
		return False

def IsWall (x,y):
	if IsOutOfBounds(x,y):
		return True

	if Map[x][y] == 1:
		return True

	if Map[x][y] == 0:
		return False

	return False

def GetAdjacentWalls(x,y,scopeX,scopeY):
	startX = x - scopeX
	startY = y - scopeY
	endX = x + scopeX
	endY = y + scopeY

	iX = startX
	iY = startY

	wallCounter = 0


	for iY in range(startY, endY+1):
		for iX in range(startX, endX+1):
			if not (iX == x and iY==y):
				if IsWall(iX,iY):
					wallCounter = wallCounter + 1
	return wallCounter

def PlaceWallLogic(x,y):
	numWalls = GetAdjacentWalls(x,y,1,1)

	if Map[x][y] == 1:
		if numWalls >= 4:
			return 1
		if numWalls < 2:
			return 0
	else:
			if numWalls >= 5:
				return 1
	return 0


def MakeCaverns():
	for row in range(MapHeight):
		for column in range(MapWidth):
			Map[column][row] = PlaceWallLogic(column,row)

def RandomFillMap():
	for row in range(MapHeight):
		for column in range(MapWidth):
			daGrid = Map[column][row]
			if column == 0:
				Map[column][row] = 1
			elif row == 0:
				Map[column][row] = 1
			elif column == MapWidth - 1:
				Map[column][row] = 1
			elif row == MapHeight -1:
				Map[column][row] = 1
			else:
				mapMiddle = MapHeight / 2
				if row == mapMiddle:
					Map[column][row] = 0
				else:
					Map[column][row] = RandomPercent(PercentAreWalls)
					pass


def PrintMap(mapToPrint):
	for row in range(MapHeight):
		for column in range(MapWidth):
			daGrid = mapToPrint[column][row]
			if daGrid	== 0:
				print " ",
			elif daGrid	== 1:
				print "X",
			else:
				print "?",
		print ""

def TrackFill(x,y,targetMark,counter,gridList):

	if Map[x][y] != targetMark: return 0, None	# base case
	Map[x][y] = 3 						# mark current grid
	counter = counter + 1 				# increase counter
	gridList.append((x,y))				# add to list

	upCount, upList = TrackFill(x,y-1,targetMark,0,[]) 		# iterate UP
	rightCount, rightList = TrackFill(x+1,y,targetMark,0,[]) 	# iterate RIGHT
	downCount, downList = TrackFill(x,y+1,targetMark,0,[]) 	# iterate DOWN
	leftCount, leftList = TrackFill(x-1,y,targetMark,0,[]) 	# iterate LEFT

	if upList != None: gridList = gridList + upList			# tally up coordinates
	if rightList != None: gridList = gridList + rightList
	if downList != None: gridList = gridList + downList
	if leftList != None: gridList = gridList + leftList

	totalCount = counter + upCount + rightCount + downCount + leftCount
	return totalCount,gridList

######################################################################################
# look for bodies of water. compare to the last body found. fill up the smaller body #
######################################################################################
def CompileMap():
	bodyList = None
	largestBodyCount = 0
	for row in range(0,MapHeight-1):		# for each row
		for column in range(0,MapWidth-1):	# for each column
			daGrid = Map[column][row]
			if daGrid == 0:											# if see a grid is water
				fillCount, fillList = TrackFill(column,row,0,0,[])	# do flood fill to get size and coordinate of water
				if fillCount >= largestBodyCount:					# if the new fill count is larger than the last body
					if bodyList != None and largestBodyCount != 0:	# and if it isnt the first body found
						for x,y in bodyList: Map[x][y] = 1 			# fill the smaller body with land
					bodyList = fillList
					largestBodyCount = fillCount
				else:												# else if the body found is smaller
					for x,y in fillList: Map[x][y] = 1 				# fill the smaller body with land
	for x,y in bodyList: Map[x][y] = 0

def IsGoodQuality():
	upperOkay = False
	lowerOkay = False
	for column in range (1,MapWidth-1):
		if Map[column][VerticalThreshold] == 0: upperOkay = True
		if Map[column][MapHeight - VerticalThreshold-1] == 0: lowerOkay = True
	return upperOkay and lowerOkay

def SeedEnterance(columns):
	for column in columns:
		Map[column][MapHeight-2] = 0
		Map[column][MapHeight-3] = 0
		Map[column][MapHeight-4] = 0

		Map[column-1][MapHeight-2] = 0
		Map[column-1][MapHeight-3] = 0
		Map[column-1][MapHeight-4] = 0

		Map[column+1][MapHeight-2] = 0
		Map[column+1][MapHeight-3] = 0
		Map[column+1][MapHeight-4] = 0

	return

def FindExitIndex(map):
	exitList = []
	for column in range (1,MapWidth-1):
		if map[column][1] == 0: exitList.append(column)
	return exitList

def FindEnteranceIndex(map):
	enteranceList = []
	for column in range (1,MapWidth-1):
		if map[column][MapHeight-2] == 0: enteranceList.append(column)
	return enteranceList

def GetInternalBoundary(map):
	newMap = [[0 for x in range(MapHeight)] for x in range(MapWidth)]
	for column in range (0,MapWidth-1):
		for row in range (0,MapHeight-1):
			counter = 0
			if map[column][row-1] == 0: counter = counter + 1
			if map[column+1][row] == 0: counter = counter + 1
			if map[column][row+1] == 0: counter = counter + 1
			if map[column-1][row] == 0: counter = counter + 1

			if counter == 1 or counter == 2 or counter == 4: newMap[column][row] = 1
			else : newMap[column][row] = 0
	return newMap

tempSeeds = None
map1 = None
map2 = None


while True:
	while True:
		RandomFillMap()
		SeedEnterance([5])
		#PrintMap(Map)
		MakeCaverns()
		CompileMap()
		if IsGoodQuality():
			#PrintMap(Map)
			tempSeeds = FindExitIndex(Map)
			#anyKey = raw_input()
			map1 = Map
			break
	#print " ======================================================================== \n"
	while True:
		RandomFillMap()
		SeedEnterance(tempSeeds)
		MakeCaverns() 
		CompileMap()
		if IsGoodQuality():
			tempEnt = FindEnteranceIndex(Map)
			if all(x in tempEnt for x in tempSeeds):
				#PrintMap(map1)

				#PrintMap(GetInternalBoundary(Map))
				#PrintMap(Map)
				print Map


				#print " YAY "
				#anyKey = raw_input()
				#cls()

				break
	break