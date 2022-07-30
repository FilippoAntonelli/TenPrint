import numpy as np
import cv2
import random
import time
from PIL import ImageFont, ImageDraw, Image  

MAZE_SIZE=(640,1280)
PIXEL_SIZE=40

class Maze ():
    def __init__(self,maze_size, pixel_size):
        self.canvas=np.zeros(maze_size,dtype=np.uint8)
        self.maze_size=maze_size
        self.pixel_size=pixel_size
        self.width_in_px=int(self.maze_size[0]/self.pixel_size)
        self.height_in_px=int(self.maze_size[1]/self.pixel_size)
        self.maze=[]
        print('Generated maze with size: ',self.width_in_px, 'x', self.height_in_px)
    def generateMaze(self):
        out = cv2.VideoWriter('maze.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, self.maze_size)
        try:
            for y in range(self.pixel_size,self.maze_size[0]+self.pixel_size,self.pixel_size):
                for x in range(0,self.maze_size[1],self.pixel_size):
                    angle=0 if random.randint(0,1)%2==0 else 90
                    line = Line(self.pixel_size,(x,y), angle,thickness=4)
                    self.maze.append(line)
                    line.draw(self.canvas)
                    self.refreshCanvas()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        raise StopIteration
        except StopIteration: pass
    def rotate(self,angle=0,step=1):
        try:
            print('rotating maze')
            for delta in range(0,angle,step):
                self.canvas=np.zeros(self.maze_size,dtype=np.uint8)
                for line in self.maze:
                    line.rotate(step)    
                    line.draw(self.canvas)
                self.refreshCanvas()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise StopIteration
        except StopIteration: pass
    def scrollV(self,rows_to_scroll=1):
        print('scrolling maze')
        try:
            for _ in range(rows_to_scroll):
                time.sleep(0.2)
                self.canvas=np.zeros(self.maze_size,dtype=np.uint8)
                row=self.maze[0:self.width_in_px]
                for line in row:
                    line.pixel_bl_corner=(line.pixel_bl_corner[0],self.maze_size[1])
                    line.draw(self.canvas)

                self.maze=self.maze[self.width_in_px:]
                for line in self.maze:
                    line.pixel_bl_corner=(line.pixel_bl_corner[0],line.pixel_bl_corner[1]-line.pixel_size)
                    line.draw(self.canvas)

                self.maze=[*self.maze,*row]
                
                self.refreshCanvas()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise StopIteration
        except StopIteration: pass

    def scrollH(self,cols_to_scroll):
        print('scrolling maze')
        try:
            for _ in range(cols_to_scroll):
                time.sleep(0.2)
                self.canvas=np.zeros(self.maze_size,dtype=np.uint8)
                for row in range (self.height_in_px):
                    row_first_el_index=row*self.width_in_px
                    temp_angle=self.maze[row_first_el_index].angle
                    for index in range(row_first_el_index,row_first_el_index + self.width_in_px-1):
                        self.maze[index].angle=self.maze[index+1].angle
                    self.maze[row_first_el_index+self.width_in_px-1].angle=temp_angle
                for line in self.maze:
                    line.draw(self.canvas)
                self.refreshCanvas()    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise StopIteration
        except StopIteration: pass

    def strobe(self,reps=10):
        try:
            for _ in range(reps):
                time.sleep(0.05)
                self.canvas=255-self.canvas
                self.refreshCanvas()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        raise StopIteration
        except StopIteration: pass
    
    def wave(self,step=20,delay=0.02):
        try:
            self.canvas=np.zeros(self.maze_size,dtype=np.uint8)
            for focus in range (0-int(255/step),self.height_in_px+int(255/step)):
                for index in range(self.width_in_px*self.height_in_px):
                    line_row = int(index/self.height_in_px)
                    distance_from_focus=abs(line_row-focus)
                    color=int(step*distance_from_focus)
                    self.maze[index].color=color if color<255 else 255
                time.sleep(delay)
                for line in self.maze:
                    line.draw(self.canvas)
                self.refreshCanvas()    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise StopIteration
        except StopIteration: pass
    

    def vibrate(self,reps=10,intensity=10, delay=0.0008):
        try:
            self.rotate(intensity,2)
            time.sleep(delay)
            for _ in range(reps):
                self.rotate(-2*intensity,-2)
                time.sleep(delay)
                self.rotate(2*intensity,2)
                time.sleep(delay)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise StopIteration
            self.rotate(-intensity,-2)
        except StopIteration: pass



    def refreshCanvas(self):
        cv2.imshow('Maze',self.canvas)

    def deleteMaze(self):
        cv2.destroyWindow('Maze')
        del(self)


# \: angle= 0
# |: angle= 45
# /: angle= 90
# -: angle= 135
class Line():
    def __init__(self, pixel_size, pixel_bl_corner, angle, thickness=1, color=255):
        self.pixel_size=pixel_size
        self.pixel_bl_corner=pixel_bl_corner
        self.thickness=thickness
        self.angle=angle
        self.color=color

    def getStartStopFull(self):
        self.angle=self.angle%180
        starting_point_x=0
        starting_point_y=0
        ending_point_x=0
        ending_point_y=0
        if(self.angle<90):
            starting_point_x=int(self.pixel_bl_corner[0]+(self.angle*(self.pixel_size/90)))
            starting_point_y=int(self.pixel_bl_corner[1]-self.pixel_size)

            ending_point_x=int((self.pixel_bl_corner[0]+self.pixel_size)-(self.angle*(self.pixel_size/90)))
            ending_point_y=int(self.pixel_bl_corner[1])
        else:
            starting_point_x=int(self.pixel_bl_corner[0]+self.pixel_size)
            starting_point_y=int(self.pixel_bl_corner[1]-self.pixel_size+((self.angle-90)*(self.pixel_size/90)))

            ending_point_x=int(self.pixel_bl_corner[0])
            ending_point_y=int(self.pixel_bl_corner[1]-((self.angle-90)*(self.pixel_size/90)))
        
        return ((starting_point_x,starting_point_y),(ending_point_x,ending_point_y))

    def draw(self, canvas):
        start_position , stop_position=self.getStartStopFull()
        cv2.line(canvas, start_position, stop_position, self.color, self.thickness)
    
    def erase(self,canvas):
        start_position , stop_position=self.getStartStopFull()
        cv2.line(canvas, start_position, stop_position, 0, self.thickness)
    
    def rotate(self,angle):
        self.angle=self.angle+angle


maze= Maze(MAZE_SIZE, PIXEL_SIZE)
maze.refreshCanvas()
cv2.waitKey(0)
maze.generateMaze()
cv2.imwrite("Maze.png",maze.canvas)
maze.rotate(180,1)
#maze.scrollV(10)
maze.strobe(10)
maze.scrollH(10)
maze.wave(delay=0.005)
maze.wave(delay=0.001)
maze.vibrate(3)
cv2.waitKey(0)
maze.deleteMaze()


