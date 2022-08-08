from event import *
from element import *
from display import *
from interpreter import *
import pygame




def enterFile(file_name:str,surface):
    surface.Interpreter=file_Interpreter(file_name)
    surface.event_process.STATE[2]=1
    surface.event_process.Interpreter=surface.Interpreter
    print(file_name)

class event_processor:
    STATE=[1,0,0]# 0:run 1:control atom 2 whether read file 3 move screen
    Surface=None
    Catched_Atom=None
    Interpreter:file_Interpreter=None

    def __init__(self) -> None:
        self.eachEvent={pygame.QUIT:self.Quit,
                pygame.MOUSEBUTTONDOWN:self.Touch_in,
                pygame.MOUSEBUTTONUP:self.Touch_out
                }
        
        
            


    def Touch_in(self,eve:pygame.event.Event):# process touch event
        getPos=pygame.mouse.get_pos()
        

        if self.STATE[2]:
            if eve.button==1:
                getButton=self.findClickedButton(getPos)
                if getButton:
                    self.buttonEvent(getButton)
                    return

                getAtom=self.findClickedAtom(getPos)
                if getAtom:
                    self.InitinalMouPos=pygame.mouse.get_pos()
                    self.InitinalAtomPos=(getAtom._x,getAtom._y)
                    self.Catched_Atom=getAtom
                    self.STATE[1]=1
                    
                    if type(getAtom).__base__==Element:
                        print('elemnt')
                        self.Interpreter.State_Storer.Move(getAtom,2,*self.InitinalAtomPos)
           
            
        else:
            getFiles=getFilesName()
            for i in range(len(getFiles)):
                if (100+200*(i%5))<getPos[0]and getPos[0]<(100+200*(i%5))+100 \
                    and  (200+200*(i//5))<getPos[1] and getPos[1]<(200+200*(i//5))+30:
                    enterFile(getFiles[i],self.Surface)
                    return
        


    def Touch_out(self,eve:pygame.event.Event):
        if eve.button==1 and self.STATE[1]:
            self.Catched_Atom=None
            self.STATE[1]=0
        


    def findClickedAtom(self,position)->micro:
        
        distance=lambda atom:((position[0]-atom._x)**2+(position[1]-atom._y)**2) **0.5
        for electron in ALL_ELECTRON:
            if distance(electron)<electron.Size:
                return electron
        for element in ALL_ELEMENT:
            if distance(element)<element.Size:
                return element
        return 0

    def findClickedButton(self,position)->int:#-1 left, 0 no, 1right 2 adjust
        if position[0]>1000 and position[0]<1050 and position[1]>30 and position[1]<70:
            return 1
        if position[0]>840 and position[0]<890 and position[1]>30 and position[1]<70:
            return -1
        if position[0]>175 and position[0]<175+100 and position[1]>35 and position[1]<35+40:
            return 2
        return 0
        

    def buttonEvent(self,getButton):
        if getButton==1:
            self.Interpreter.next()
        if getButton==2:
            
            self.Adjust()
        if getButton==-1:
            self.Interpreter.State_Storer.Back()

    def Quit(self,eve:pygame.event.Event):
        self.STATE[0]=0

    def Adjust(self):
        for element in ALL_ELEMENT:
            for bond in element.bonds:
                e_1:Electron=bond.pair_dict[bond.pair_1]
                e_2:Electron=bond.pair_dict[bond.pair_2]
                
                diff_x=e_1.element.x-e_2.element.x
                diff_y=e_1.element.y-e_2.element.y
                r=(diff_x**2+diff_y**2)**0.5

                e_1.x=e_1.element.x-e_1.element.Size*diff_x/r
                e_1.y=e_1.element.y-e_1.element.Size*diff_y/r

                e_2.x=e_2.element.x+e_2.element.Size*diff_x/r
                e_2.y=e_2.element.y+e_2.element.Size*diff_y/r

    def moveAtom(self):
        if self.STATE[1]:
            nowPos=pygame.mouse.get_pos()
            #self.InitinalAtomPos
            self.Catched_Atom._x=nowPos[0]-self.InitinalMouPos[0]+self.InitinalAtomPos[0]
            self.Catched_Atom._y=nowPos[1]-self.InitinalMouPos[1]+self.InitinalAtomPos[1]
            #self.Catched_Atom._x,self.Catched_Atom._y=pygame.mouse.get_pos()

    

    def step(self):# each loop will call it
        self.moveAtom()
        



    
