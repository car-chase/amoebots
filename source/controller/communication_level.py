'''
Created on Nov 1, 2016

@author: Trevor
'''
from multiprocessing import Process, Queue, Array
from bot_listener import listener_main
from time import sleep

def com_level_main(TO_MAIN, FROM_MAIN, TO_COM_LEVEL, FROM_COM_LEVEL):

    #stores the ports 
    ports = Array()

    q_list = []

    q = Queue()
    #create bot_listener process
    bot_listener = Process(target=listener_main, args=(q,ports))

    #start bot_listener process
    bot_listener.start()

    #infinite loop to keep checking the queue for information
    while(True):
        
        print('Communication_level is running')
        
        #get items from q until it's empty
        while not q.empty():
            
            #print item to console
            p = q.get()
            if type(p) is list:
                if p[1] == '0':
        
                    #adds the port to the port list if it doesn't already exist
                    ports.append(p[0])
                    q_list.addpend(p[3])
                    print('\t\t' + p[0] + ' added')
                
                elif p[1] == '1':
                    if exists(p[0]):
                        ports.remove(p[0])
                        q_list.remove(p[3])
                        print('\t\t' + p[0] + ' removed')
                    else:
                        print('\t\t' + p[0] + ' failed to start')
                    
                elif p[1] == '-1':
                    t = '\t\t[' + ', '.join(p) + ']'
                    print(t)
                    
                else:
                    t = '\t\t[' + ', '.join(p) + ']'
                    print(t)
                
            else:
                print('\t' + p)
            
        #sleep so that this is not constantly eating processing time
        sleep(5)

#checks that a port isn't already open
def exists(addr):
    
    #checks for the current port in the port list
    if addr in ports:
        return True;
    else:
        return False;
    
def port_list(f):
    print('Com-level:\t' + ', '.join(ports))
    f(ports)