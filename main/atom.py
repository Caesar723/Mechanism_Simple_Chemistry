import random
import math

import pygame




ALL_ELECTRON=[]
ALL_ELEMENT=[]

SCREENSIZE=(1160, 800)

MAXSPEED=1
MAXFORCE=3

ELEMENT_REPUL=0.001
ELEMENT_POWER=-5

SUPERSCRIPT="⁰¹²³⁴⁵⁶⁷⁸⁹"
SYMBOL={'+':'⁺',
        '-':'⁻'}


def color_generate(ele):# random create color
    seed=int("{}{}{}".format(ele.Proton,ele.Electron,ele.Neutron))
    random.seed(seed)
    return [random.randint(0,255) for i in range(3)]

def oppositeColor(color:list)->list:
    return [ 255 - col for col in color]

def adjustPosition(font:pygame.font.Font,text:str,position:list)->None:#calculate offset
    
    getPam=font.size(text)
    
    position[0]-=getPam[0]/2
    position[1]-=getPam[1]/2
    return position


def Force(self,other,attract=-1,power=2):# return force of x and y   attrct 1  repulsion -1
    diff_x,diff_y=other.x-self.x,other.y-self.y
    
    #print(360*angle/(2*math.pi))
    r=((diff_x)**2+(diff_y)**2)**0.5
    F=attract*self.Charge*other.Charge/((r/100)**power+1e-7)
    


    return ((diff_x/(r+1e-7))*F,(diff_y/(r+1e-7))*F)
    
        

    
class micro:

    _x=0
    _y=0
    OverAllForce=[0]*2#x,y
    State=1#1: in elemrnt 0: move out
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,value):
        self._x=value

    @property
    def y(self):
        return SCREENSIZE[1]-self._y
    @y.setter
    def y(self,value):
        self._y=SCREENSIZE[1]-value

    def distance(self,other):
        return ((other.x-self.x)**2+(other.y-self.y)**2)**0.5
    


class Element(micro):
    Name=""
    Proton=0
    Electron=0
    Neutron=0
    symbol=""
    atomic_radius=0
    ionic_radius=0
    
    
    def __init__(self,x:int,y:int,charge:int=0) -> None:
        
        self.color=color_generate(self)
        self.x,self.y=x,y
        self.Electron-=charge

        self.electronPairs=self.initinalElectronPair()# 4 electron pair
        self.bonds=[]# store the bonded electron
        ALL_ELEMENT.append(self)
        self.font=pygame.font.SysFont('Helvetica', int(self.Size/2))
        
        

    @property
    def Charge(self):
        return self.Proton-self.Electron

    @property
    def Size(self):
        getSize=self.ionic_radius if self.Charge  else self.atomic_radius
        return getSize*80

    @property
    def Mini(self):# limit of electron range
        return self.Size-5

    @property
    def outerElectron(self)->int:
        outerElectron=self.Electron-2
        if outerElectron<=0:
            return self.Electron
        if self.Proton>30:
            delete=outerElectron-16-1
            num=(delete//18)+1
            outerElectron=(outerElectron-(num*10))%8
        else:
            outerElectron=outerElectron%8

        if outerElectron:
            return outerElectron
        return 8
    
    
    

    def initinalElectronPair(self)->set:
        pairs=set()
        outerElectron=self.outerElectron
        turn=outerElectron//4
        exce=outerElectron%4
        
        for pair in range(4):
            getPair=Electron_Pair(self,*[ Electron(pair,e,self) for e in range(turn+int(exce-(pair)>0))])
            pairs.add(getPair)
        return pairs

    def move(self):
        pass

    

    def bond_from(self):
        pass

    def bond_borken(self):
        pass

    def display(self,screen:pygame.Surface):
        res_str=''
        
        pygame.draw.circle(screen,self.color,(self._x,self._y),self.Size)
        getCharge=self.Charge
        res_str=sym=''
        if getCharge:
            if getCharge<0:
                sym=SYMBOL['-']
                getCharge=str(getCharge)[1:]
            else:
                sym=SYMBOL['+']
                getCharge=str(getCharge)
            for chr in getCharge:
                res_str+=SUPERSCRIPT[int(chr)]
        
        screen.blit(self.font.render(self.symbol+res_str+sym, True, oppositeColor(self.color)),adjustPosition(self.font,self.symbol,[self._x,self._y]))
        
        
    def __repr__(self) -> str:
        return self.symbol
    

class Electron(micro):
    DIRECTION=[{'x':0,'y':1},{'x':0,'y':-1},{'x':1,'y':0},{'x':-1,'y':0}]
    Pair=None
    element_target=None
    Charge=-1
    
    Size=5
    

    def __init__(self,direct:int,num_e:int,element:Element=None) -> None:
        self.element=element# Main element
        self.shared=[]# two element
        offsetAngle=math.asin(self.Size/(element.Size-self.Size))*2
        offset_1,offset_2= (math.sin(offsetAngle)*(element.Size-self.Size))*num_e ,((element.Size-self.Size)-math.cos(offsetAngle)*(element.Size-self.Size))*num_e 
        SecondElectron=[{'x':-offset_1,'y':-offset_2},{'x':offset_1,'y':offset_2},{'x':-offset_2,'y':offset_1},{'x':offset_2,'y':-offset_1}]
        self.x=element.x+(element.Size-self.Size)*self.DIRECTION[direct]['x'] +SecondElectron[direct]['x']
        self.y=element.y+(element.Size-self.Size)*self.DIRECTION[direct]['y'] +SecondElectron[direct]['y']
        self.font=pygame.font.SysFont('Helvetica', 15)
        ALL_ELECTRON.append(self)

    

    def in_limit(self,diff_x,diff_y,K,R,limit,out=1)->list:

        self.x,self.y=self.element.x+(limit*diff_x/(R+1e-7)),self.element.y+(limit*diff_y/(R+1e-7))
                
        Kd=-1/(K+1e-7)
        assR=(Kd**2+1)**0.5#assume R
        Y_x=self.OverAllForce[1]*Kd/assR#force y out x
        X_x=self.OverAllForce[0]*1/assR#force x out x
        sumX=Y_x+X_x

        end_x,end_y=sumX*1/assR,sumX*Kd/assR
        return [end_x*out,end_y*out]
       

    def move(self):
        out_x=out_y=0

        diff_x,diff_y=-self.element.x+self.x,-self.element.y+self.y
        maxR,R=self.element.Size-self.Size,self.distance(self.element)
        minR=self.element.Size/1.5
        
        K=diff_y/(diff_x+1e-7)#slope
        #self.checkClick()
        if self.State:
            #print(self.OverAllForce)
            end_x,end_y=self.OverAllForce
            self.changePosition(end_x,end_y)
            #self.checkClick()
            if self.distance(self.element)>maxR:
                out_x,out_y=self.in_limit(diff_x,diff_y,K,R,maxR)
            if self.distance(self.element)<minR:
                out_x,out_y=self.in_limit(diff_x,diff_y,K,R,minR)
                #print(end_x,end_y)
            self.changePosition(out_x,out_y)
            self.checkClick()
            
    
    def checkClick(self):
        for e in ALL_ELECTRON:
            disDifferent=self.distance(e)
            
            if disDifferent<=self.Size*2 and e!=self:
                
                moveDis=(self.Size*2-disDifferent)
                diff_x,diff_y=-e.x+self.x,-e.y+self.y

                self.x+=moveDis*diff_x/(disDifferent+1e-7)
                self.y+=moveDis*diff_y/(disDifferent+1e-7)
                

            
            
    def changePosition(self,offset_x,offset_y):
        #print(self.x,self.y,offset_x,offset_y)
        r=(offset_x**2+offset_y**2)**0.5
        if abs(offset_x)>MAXSPEED:
            offset_x=MAXSPEED*offset_x/r
        if abs(offset_y)>MAXSPEED:
            offset_y=MAXSPEED*offset_y/r
        self.x+=round(offset_x)
        self.y+=round(offset_y)
        

    

    # def bond(self):
    #     pass

    @property
    def sumForce(self):
        return ((self.OverAllForce[0])**2+(self.OverAllForce[1])**2)**0.5

    
    
    

    def display(self,screen:pygame.Surface):
        
        pygame.draw.circle(screen,[0]*3,(self._x,self._y),self.Size)
        screen.blit(self.font.render("-", True, [255]*3),adjustPosition(self.font,'-',[self._x,self._y]))

    def __repr__(self) -> str:
        return "Electron form {}".format(self.element.symbol)


class Electron_Pair:
    Bonded=0
    OverAllForce=[[0,0],[0,0]]#[x,y]e1,e2
    def __init__(self,element:Element,*arg) -> None:
        self.element=element
        self.pair=list(arg)#electron pair
        for ele in self.pair:
            ele.Pair=self
        

    @property
    def Charge(self)->int:

        return sum([e.Charge for e in self.pair])

    @property
    def x(self):
        if len(self.pair):
            
            sumx=0
            for each in self.pair:
                sumx+=each.x
            return sumx/len(self.pair)
        return 0
    

    @property
    def y(self):
        if len(self.pair):
            
            sumy=0
            for each in self.pair:
                sumy+=each.y
            return sumy/len(self.pair)
        return 0

    

    def calculateOverallForce(self):
        self.OverAllForce=[[0,0],[0,0]]
        
        #self.calculate_pair()
        self.calculate_single()
        
        for i in range(len(self)):
           # print(self.pair[i].OverAllForce)
            self[i].OverAllForce=self.OverAllForce[i].copy()

        if self.Bonded:

            x,y=Force(self.pair[0],self.pair[1],10)
            self.pair[0].OverAllForce[0]+=x
            self.pair[0].OverAllForce[1]+=y

            x,y=Force(self.pair[1],self.pair[0],10)
            self.pair[1].OverAllForce[0]+=x
            self.pair[1].OverAllForce[1]+=y

    def calculate_pair(self):
        for element in ALL_ELEMENT:
            if element!=self:
                x,y=Force(self,element)
                rup_x,rup_y=Force(self,element,ELEMENT_REPUL)
                self.addOverallForce(x+rup_x,y+rup_y)
            for pair in element.electronPairs:
                if len(pair) and  self!=pair:
                    x,y=Force(self,pair)
                    self.addOverallForce(x,y)
                    

    def calculate_single(self):

        for element in ALL_ELEMENT:
            
            for i in range(len(self)):

                x,y=Force(self[i],element,ELEMENT_POWER)
                rup_x,rup_y=Force(self[i],element,ELEMENT_REPUL)
                self.OverAllForce[i][0]+=x+rup_x
                self.OverAllForce[i][1]+=y+rup_y
                for pair in element.electronPairs:
                    for ele in pair.pair:
                        if not(ele in self):
                            
                            x,y=Force(self[i],ele)
                            self.OverAllForce[i][0]+=x
                            self.OverAllForce[i][1]+=y
                        
            

    def addOverallForce(self,x:int,y:int):
        for each in self.OverAllForce:
            each[0]+=x
            each[1]+=y

    def addEachForce(self,x_1:int,y_1:int,x_2:int,y_2:int):
        self.OverAllForce[0][0]+=x_1
        self.OverAllForce[0][1]+=y_1
        self.OverAllForce[1][0]+=x_2
        self.OverAllForce[1][1]+=y_2
    # def belong(self,other):#mix the Electron_Pair
    #     pass

    # def bond(self,Other):
    #     if len(self)==len(Other)==1:
    #         Bond(self,Other)

    def __getitem__(self,key:int)->Electron:
        return self.pair[key]

    def __len__(self)->int:
        return len(self.pair)

    def __repr__(self) -> str:
        return " ".join([str(i) for i in self.pair])

    
class Covalent_Bond:

    Type=None
    def __init__(self,pair_1:Electron_Pair,pair_2:Electron_Pair) -> None:
        if len(pair_1)==1 and len(pair_2)==1:
            self.sharePair(pair_1,pair_2)
            self.Type="SHARE"
        elif len(pair_1)==2 :
            self.gainPair(pair_1,pair_2)
            self.Type="COORDINATE"
        elif len(pair_2)==2:
            self.gainPair(pair_2,pair_1)
            self.Type="COORDINATE"

        #print(pair_2[0].element.electronPairs,pair_1[0].element.electronPairs)
        
    def sharePair(self,pair_1:Electron_Pair,pair_2:Electron_Pair):# share pair
        self.pair_dict={pair_1:pair_1[0],pair_2:pair_2[0]}

        pair_1[0].element.bonds.append(self)
        pair_2[0].element.bonds.append(self)

        
        pair_1.Bonded=1
        pair_2[0].element.electronPairs.remove(pair_2)
        pair_1.pair.append(pair_2.pair.pop())

        self.pair_1,self.pair_2=pair_1,pair_2

    def gainPair(self,pair_1:Electron_Pair,pair_2:Electron_Pair):# pair_1 lose pair,pair_2 gain pair
        self.pair_dict={pair_1:pair_1[0],pair_2:pair_1[1]}

        

        pair_1.element.bonds.append(self)
        pair_2.element.bonds.append(self)

        pair_1.element.Electron-=1
        pair_2.element.Electron+=1
        
        pair_2.element.electronPairs.remove(pair_2)
        

        pair_1.Bonded=1
        self.pair_1,self.pair_2=pair_1,pair_2

        self.adjustPair()

    def Break(self):
        for pair in self.pair_dict:
            self.pair_dict[pair].element.bonds.remove(self)
            self.pair_dict[pair].element.electronPairs.add(pair)
            pair.Bonded=0
        self.pair_dict[self.pair_2].element.electronPairs.add(self.pair_2)
        self.pair_1.pair.remove(self.pair_dict[self.pair_2])
        self.pair_2.pair.append(self.pair_dict[self.pair_2])

        self.adjustPair()


    def Transfer(self,element:Element,lose:Element):#element gain pair
        element.Electron+=1
        lose.Electron-=1
        targetPair=None
        transferPair=None
        self.pair_dict[self.pair_2].element.electronPairs.add(self.pair_2)
        self.pair_2.element=self.pair_dict[self.pair_2].element
        for pair in self.pair_dict:
            pair.Bonded=0
            self.pair_dict[pair].element.bonds.remove(self)
            if pair.element==element:
                transferPair=pair
                
            else:
                targetPair=pair
                
                #pair.element=element
            self.pair_dict[pair].element=element
        
        if len(targetPair):
            for i in range(len(targetPair.pair)):
                transferPair.pair.append(targetPair.pair.pop())
        
    def adjustPair(self):
        self.pair_dict[self.pair_1].element=self.pair_1.element
        self.pair_dict[self.pair_2].element=self.pair_2.element

        
        

        
    

def search_Elec_pairs(element:Element,num_ele:int)->list:
    prepare=[]
    for pair in element.electronPairs:
        if len(pair)==num_ele and not(pair.Bonded):
            prepare.append(pair)
    return prepare


def covalent_bond(element1:Element,element2:Element,num:int):
    prepare=[search_Elec_pairs(element1,1),
            search_Elec_pairs(element2,1)]
    for i in range(num):
        Covalent_Bond(prepare[0][i],prepare[1][i])

def findSameBond(element1:Element,element2:Element)->set:
    result=set()
    for bond1 in element1.bonds:
        for bond2 in element2.bonds:
            if bond1==bond2:
                result.add(bond1)
    return result

def covalent_bond_break(element1:Element,element2:Element,num_break:int):# element return to orginal
    sameBond=findSameBond(element1,element2)
    count=0
    for bond in sameBond:
        count+=1
        if count>num_break:
            break
        bond.Break()
     
        


def covalent_bond_transfer(element1:Element,element2:Element,num_pair:int):# element1:lose electron,element2:gain electron
    sameBond=findSameBond(element1,element2)
    count=0
    for bond in sameBond:
        count+=1
        if count>num_pair:
            break
        bond.Transfer(element2,element1)

def coordinate_bond_transfer(element1:Element,element2:Element,num_pair:int):# element1:lose pair(charge +1),element2:gain pair(charge -1)
    prepare=[search_Elec_pairs(element1,2),
            search_Elec_pairs(element2,0)]
    for i in range(num_pair):
        Covalent_Bond(prepare[0][i],prepare[1][i])