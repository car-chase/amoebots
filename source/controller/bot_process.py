'''
This file contains the code for the bot processes.  This process communicates with 
a bot and funnels the messages to the controller.

Created on Nov 1, 2016
View the full repository here https://github.com/car-chase/amoebots
'''
from time import sleep
import serial

reps = 100

def process_main(addr, q, q2, l, baud):
    for i in range(10):
        sleep(.5)
        with serial.Serial(addr, baud) as port:
            print(port)
#    header = "Is it writing to file?\n"
#    outf.write(header)
            for j in range(reps):
                x = port.readline()
                s = bytes.decode(x)
                '''print('before lock on ' + add)'''
                l.acquire()
                q.put(s)
                l.release()
                '''print('after lock on ' + add)'''
                port.write(str.encode(addr + " hello"))
    return 0

