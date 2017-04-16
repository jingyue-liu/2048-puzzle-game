from random import randint
from BaseAI import BaseAI
import math
import Helper
import numpy as np
import time
time1 = 0

class PlayerAI(BaseAI):     
    def miniMax(self, grid,  depth, maxPlayer):
        if time.clock()-time1 > 0.19:
            return -1
        if depth == 0:
            return self.heuristic(grid)
        if not grid.canMove():
            return self.heuristic(grid)
        if maxPlayer:
            bestValue = -np.inf
            moves = Helper.getAvailableMoves(grid)
            for child in zip(*moves)[1]:
                v = self.miniMax(child, depth - 1, False)
                bestValue = max(bestValue,v)
            return bestValue
        else:
            cells = grid.getAvailableCells()
            children = []
            bestValue = np.inf
            alpha = -np.inf
            beta = np.inf
            for cell in cells:
                gridCopy = grid.clone()
                gridCopy.map[cell[0]][cell[1]] = 2
                children.append(gridCopy)
                gridCopy = grid.clone()
                gridCopy.map[cell[0]][cell[1]] = 4
                children.append(gridCopy)
            for child in children:
                v = self.miniMax(child, depth - 1, True)
                bestValue = min(bestValue,v)            
            return bestValue
            
    def miniMaxab(self, grid,  depth, maxPlayer, alpha, beta):
        if time.clock()-time1 > 0.19:
            return -1
        if depth == 0:
            return self.heuristic(grid)
        if not grid.canMove():
            return self.heuristic(grid)
        if maxPlayer:
            bestValue = -np.inf
            moves = Helper.getAvailableMoves(grid)
            for child in zip(*moves)[1]:
                v = self.miniMaxab(child, depth - 1, False, alpha, beta)
                bestValue = max(bestValue,v)
                alpha = max(alpha, bestValue)
                if alpha > beta:
                    break
            return bestValue
        else:
            cells = grid.getAvailableCells()
            children = []
            bestValue = np.inf
            alpha = -np.inf
            beta = np.inf
            for cell in cells:
                gridCopy = grid.clone()
                gridCopy.map[cell[0]][cell[1]] = 2
                children.append(gridCopy)
                gridCopy = grid.clone()
                gridCopy.map[cell[0]][cell[1]] = 4
                children.append(gridCopy)
            for child in children:
                v = self.miniMaxab(child, depth - 1, True, alpha, beta)
                bestValue = min(bestValue,v)
                beta = min(beta, bestValue)
                if alpha > beta:
                    break               
            return bestValue
    
    
    def heuristic(self,grid):
        copygrid = []
        for i in range(4):
            copygrid.extend(grid.map[i])
        maxTile = max(copygrid)
        emptyTiles = len([i for i,x in enumerate(copygrid) if x == 0])
        sum = 0
        #weights = [65536,32768,16384,8192,512,1024,2048,4096,256,128,64,32,2,4,8,16]
        #weights = [10,8,7,6.5,0.5,0.7,1,3,-0.5,-1.5,-1.8,-2,-3.8,-3.7,-3.5,-3]
        weights = [17,16,15,14,9,10,11,12,8,7,6,5,1,2,3,4]
        #weights = [16,15,14,13,9,10,11,12,8,7,6,5,1,2,3,4]
        #weights = [65536,32768,16384,8192,4096,2048,1024,512,256,128,64,32,16,8,4,2]
        if maxTile == copygrid[0]:
            sum += copygrid[0]*weights[0]*2
        #if maxTile == copygrid[0]:
            #sum += (math.log(copygrid[0])/math.log(2))*weights[0]
            #sum += copygrid[0]*weights[0]
        for i in range(16):
            #if copygrid[i]>=8:
                #sum += (math.log(copygrid[i])/math.log(2))*weights[i]
            sum += copygrid[i]*weights[i]
        #if emptyTiles <=8:
            #sum += emptyTiles*512
        smoothness = abs(copygrid[1]-copygrid[0])+abs(copygrid[2]-copygrid[1])+abs(copygrid[3]-copygrid[2])+abs(copygrid[5]-copygrid[4])+abs(copygrid[6]-copygrid[5])+abs(copygrid[7]-copygrid[6])+abs(copygrid[9]-copygrid[8])+abs(copygrid[10]-copygrid[9])+abs(copygrid[11]-copygrid[10])+abs(copygrid[13]-copygrid[12])+abs(copygrid[14]-copygrid[13])+abs(copygrid[15]-copygrid[14])+abs(copygrid[4]-copygrid[0])+abs(copygrid[8]-copygrid[4])+abs(copygrid[12]-copygrid[8])+abs(copygrid[5]-copygrid[1])+abs(copygrid[9]-copygrid[5])+abs(copygrid[13]-copygrid[9])+abs(copygrid[6]-copygrid[2])+abs(copygrid[10]-copygrid[6])+abs(copygrid[14]-copygrid[10])+abs(copygrid[7]-copygrid[3])+abs(copygrid[11]-copygrid[7])+abs(copygrid[15]-copygrid[11])            
        sum = sum + emptyTiles*emptyTiles - smoothness
        #return sum/(16-emptyTiles)
        return sum 
        
    def getMove (self,grid):
        global time1
        time1 = time.clock()
        moves = Helper.getAvailableMoves(grid)
        maxdepth = 3
        flag =1
        highest_value_dict = {0:-1,1:-1,2:-1,3:-1}
        while (flag == 1):
            #print maxdepth
            for i, child in enumerate(zip(*moves)[1]):
                highest_value = self.miniMaxab(child, maxdepth, False, -np.inf, np.inf)
                #highest_value = self.miniMax(child, maxdepth, False)
                direction = zip(*moves)[0][i]
                if highest_value != -1:
                    highest_value_dict[direction] = highest_value
                    #print "direction: ",direction
                    #print "highest_value: ",highest_value
                    #print "dict: ",highest_value_dict
                else:
                    #print "direction: ",direction
                    #print "highest_value: ",highest_value
                    #print "dict: ",highest_value_dict
                    flag = 0
                    break
            maxdepth += 1
        direction_final = max(highest_value_dict, key=highest_value_dict.get)
        
        return direction_final if moves else None