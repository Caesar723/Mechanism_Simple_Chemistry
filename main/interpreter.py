
import os
from atom import *
from element import *
import threading 
import time

BASEDIR=os.path.dirname(os.path.abspath(__file__))
PATH=f'{BASEDIR}/script/'


def getFilesName()->list:
    get=os.listdir(PATH)
    
    try:
        get.remove('.DS_Store')
    except:pass
    return get

class file_Interpreter:
    POINTER=-1
    MAXPOINTER=POINTER
    State=1#1:can execute code 0 is executing code
    
    def __init__(self,file_Name:str) -> None:
        self.State_Storer=state_Storer(self)
        self.move_threads=[]
        file_path=PATH+file_Name
        self.VARIABLE={}
        self.LEVEL_1={
            '=':self.Assgnment,
            '(':self.Function,
            ':':self.Coordinate,
            '&':self.PairTranfer,
            '-':self.Bond,
            '#':self.Immediately,
            '!':self.Break,
        }

        self.LEVEL_2={
            '+':self.Add,
            '*':self.Multiply,
            '/':self.Divide,
        }
        self.LEVEL_3={
            '"':self.String,
            '[':self.GetItem,

            
            }

        self.FUNCTION={
            'create':self.Create,
            'move':self.Move,
            'pos':self.Position
        }
        self.codes=self.file_process(file_path)
        self.lenCode=len(self.codes)

    @property
    def current_code(self):#show current code
        if self.POINTER!=-1:
            return self.codes[self.POINTER]
        else:
            return ""

    def next(self):
        
        self.POINTER+=1
        
        if self.lenCode>self.POINTER:
            self.State_Storer.NewLine()
            get=self.lineCheck(self.codes[self.POINTER])
            self.MAXPOINTER=max(self.MAXPOINTER,self.POINTER)
            return get
        else:
            print("over")
            self.POINTER-=1
        
            
    
    def file_process(self,file_path:str)->list:#get each code
        result=[]
        with open(file_path,'r') as f:
            gettext=f.read()
            getlist=gettext.split('\n')
            

        for line in getlist:
            if line:
                result.append(line.split('//')[0].strip(' '))
        return result

    def lineCheck(self,line:str):
        if line in self.VARIABLE:
            return self.VARIABLE[line]
        try:
            return int(line)
        except:pass
        
        get=self.FindChar(self.LEVEL_1,line)
        if get[1]:
            return get[0]
        get=self.FindChar(self.LEVEL_2,line)
        if get[1]:
            return get[0]
        get=self.FindChar(self.LEVEL_3,line)
        if get[1]:
            return get[0]
        
        
    def FindChar(self,dic:dict,line):
        for i in range(len(line)):
            
            if line[i] in dic:
                return (dic[line[i]](line,i),1)
        return (None,0)

    def Assgnment(self,line:str,index:int):
        variable=line[:index]
        self.VARIABLE[variable]=self.lineCheck(line[index+1:])
        return self.VARIABLE[variable]

    def String(self,line:str,index:int):
        
        return line[index+1:-1]

    def Function(self,line:str,index:int):
        func=self.FUNCTION[line[:index]]
        args=line[index+1:-1].split(',')
        
        args=[self.lineCheck(each) for each in args]
        
        return func(*args)

    def Immediately(self,line:str,index:int):
        self.lineCheck(line[index+1:])
        return self.next()

    def Coordinate(self,line:str,index:int):
        pair=line[:index]
        given=line[index+3:]
        element_1,element_2=self.lineCheck(pair),self.lineCheck(given)
        coordinate_bond_transfer(element_1,element_2,1)
        self.State_Storer.Coordinate_Transfer(element_1,element_2)
        
    def Bond(self,line:str,index:int):
        pair=line[:index]
        given=line[index+1:]
        element_1,element_2=self.lineCheck(pair),self.lineCheck(given)
        covalent_bond(element_1,element_2,1)
        self.State_Storer.Bond(element_1,element_2)

    def Break(self,line:str,index:int):
        pair=line[:index]
        given=line[index+1:]
        element_1,element_2=self.lineCheck(pair),self.lineCheck(given)
        covalent_bond_break(element_1,element_2,1)
        self.State_Storer.Break(element_1,element_2)

    def Add(self,line:str,index:int):
        print(line[:index],line,index,'add')
        left_val=self.lineCheck(line[:index])
        right_val=self.lineCheck(line[index+1:])
        return left_val+right_val

    

    def Multiply(self,line:str,index:int):
        left_val=self.lineCheck(line[:index])
        right_val=self.lineCheck(line[index+1:])
        return left_val*right_val

    def Divide(self,line:str,index:int):
        left_val=self.lineCheck(line[:index])
        right_val=self.lineCheck(line[index+1:])
        return left_val/right_val

    def GetItem(self,line:str,index:int):# return item in list
        ind=self.lineCheck(line[index+1:-1])
        arr=self.lineCheck(line[:index])
        return arr[ind]

    def PairTranfer(self,line:str,index:int):
        pair=line[:index]
        given=line[index+3:]
        element_1,element_2=self.lineCheck(pair),self.lineCheck(given)
        covalent_bond_transfer(element_1,element_2,1)
        self.State_Storer.Covalent_Transfer(element_1,element_2)

    def Create(self,name:str,x:int,y:int,charge:int=0):
        if self.MAXPOINTER<self.POINTER:
            element= eval(name)(x,y,charge)
            element.ID=self.POINTER
            return element
        else:
            for element in ALL_ELEMENT:
                if element.ID==self.POINTER:
                    return element

    def Move(self,element:Element,x:int,y:int):
        th=threading.Thread(target=self.Move_step,args=(element,x,y))
        self.State_Storer.Move(element,0,element._x,element._y)
        th.start()
        self.move_threads.append(th)

    def Position(self,element:Element):
        return (element.x,element.y)
        
    def Move_step(self,element:Element,x:int,y:int):
        speed=1.5
        r=lambda :((element.x-x)**2+(element.y-y)**2)**0.5
        t=time.time()
        while r()>2:
            if time.time()-t>0.02:
                t=time.time()
                element.x+=speed*(-element.x+x)/r()
                element.y+=speed*(-element.y+y)/r()

    def Check_next(self)->bool:
        for thread in self.move_threads:
            if thread.is_alive():
                return False
        return True

    
class state_Storer:
    
    
    def __init__(self,interpreter:file_Interpreter) -> None:
        self.storage=[]#((0 continue,1 stop and reduce ,2 stop but not reduce),func,args)
        self.interpreter=interpreter


    def Move(self,element:Element,reduce:int,_x:int,_y:int):#reduce:1 reduce pointer        initinal position
        self.storage.append((reduce,self.Return_pos,(element,_x,_y)))

    def Bond(self,element_1:Element,element_2:Element):
        self.storage.append((0,covalent_bond_break,(element_1,element_2,1)))

    def Break(self,element_1:Element,element_2:Element):
        self.storage.append((0,covalent_bond,(element_1,element_2,1)))
        

    def Covalent_Transfer(self,element_1:Element,element_2:Element):# element1:lose electron,element2:gain electron
        self.storage.append((0,coordinate_bond_transfer,(element_2,element_1,1)))
    
    def Coordinate_Transfer(self,element_1:Element,element_2:Element):# element1:lose pair(charge +1),element2:gain pair(charge -1)
        self.storage.append((0,covalent_bond_transfer,(element_2,element_1,1)))

    def Return_pos(self,element:Element,_x:int,_y:int):
        element._x=_x
        element._y=_y

    def NewLine(self):
        self.storage.append((1,0,0))

    def Back(self):
        if len(self.storage):
            reduce,func,args=self.storage.pop()
            if reduce :
                if reduce==1:
                    self.interpreter.POINTER-=1
                else:
                    func(*args)
            else:
                func(*args)
                self.Back()


if __name__=="__main__":
    pygame.init()
    get=file_Interpreter('test.txt')
    print(get.next())
    print(get.current_code)
    print(get.next())
    print(get.current_code)
    print(get.next())
    print(get.current_code)
    print(get.next())
    print(get.current_code)
    print(get.VARIABLE)