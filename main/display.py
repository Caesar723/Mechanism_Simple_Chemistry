import pygame
from event import *
from atom import *
from interpreter import *



class map:

    def __init__(self) -> None:
        self.screen=pygame.Surface(SCREENSIZE) #pygame.display.set_mode((800, 800))
        self.Position=[0,0]
        

    
    @property
    def x(self):
        return self.Position[0]
    @x.setter
    def x(self,value):
        self.Position[0]=value

    @property
    def y(self):
        return self.Position[1]
    @y.setter
    def y(self,value):
        self.Position[1]=value

    def Update(self):# refresh all atom
        self.screen.fill((255 ,240 ,245))  # fill the screen

        for element in ALL_ELEMENT:
            element.display(self.screen)

        for electron in ALL_ELECTRON:
            electron.display(self.screen)

class MainSurface:

    Interpreter:file_Interpreter=None
    

    def __init__(self,ma:map,event) -> None:
        self.map=ma
        self.screen=pygame.display.set_mode((1160, 800))
        self.font=pygame.font.SysFont('Helvetica', 12)
        self.event_process=event
        

    def Update(self):#mao and button
        self.screen.fill((0 ,0 ,0))
        self.map.Update()

        self.screen.blit(self.map.screen,(self.map.x,self.map.y))
        

        self.Display()
        

    def Display(self):
        if self.event_process.STATE[2]:
            self.Display_button()
            self.Display_code()
        else:
            self.Display_fileName()


    def Display_code(self):
        self.screen.blit(self.font.render(self.Interpreter.current_code, True, (81,151,186)),(50,700))
        
        
    def Display_fileName(self):
        
        getNameList=getFilesName()
        
        for i in range(len(getNameList)):
            
            self.screen.blit(self.font.render(getNameList[i], True, (51,51,51)),(100+200*(i%5),200+200*(i//5)))

    def Display_button(self):
        pos_R=lambda x,y:[(x+50,y),(x,y-20),(x,y+20)]
        pos_L=lambda x,y:[(x-50,y),(x,y-20),(x,y+20)]
        pygame.draw.polygon(self.screen,(100,100,100),pos_R(1000,50))
        pygame.draw.polygon(self.screen,(150,150,150),pos_R(995,45))

        pygame.draw.polygon(self.screen,(100,100,100),pos_L(890,50))
        pygame.draw.polygon(self.screen,(150,150,150),pos_L(895,45))

        pygame.draw.rect(self.screen, [150,150,150], [175,35, 100, 40], 0)
        self.screen.blit(self.font.render("ADJUST", True, (10,10,10)),(195,50))



    



