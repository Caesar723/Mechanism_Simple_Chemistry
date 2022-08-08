from element import *
from display import *
from event import *
from interpreter import *
import threading
import time



def move():
    for element in ALL_ELEMENT:
        for each in element.electronPairs:
                each.calculateOverallForce()
                
    for e in ALL_ELECTRON:
        e.move()

def main():
    
    pygame.init()
    eve_process=event_processor()
    Map=map()
    mainSurface=MainSurface(Map,eve_process)
    eve_process.Surface=mainSurface
    while eve_process.STATE[0]:
        mainSurface.Update()
        move()
        eve_process.step()
        for eve in pygame.event.get():
            if eve.type in eve_process.eachEvent:
                eve_process.eachEvent[eve.type](eve)
        pygame.display.flip()
    pygame.quit()
    
    

if __name__=="__main__":
    
    main()