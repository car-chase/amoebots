# File:          TCPIPControl.py
# Date:
# Description:   
# Author:        Ben Smith
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import Robot
import socket
import SocketServer
from time import sleep
from threading import Thread
from multiprocessing import Process, Queue
# queue is where the commands are going to be pushed to and accessed between threads.
# Currently trying out a global instead of passing the queue to the threads for now.
queue = Queue()
# queue_free is a boolean that will be letting hte program know when the queue is accessible
# for pushing or pulling of commands.
queue_free = True

# variables for the motors
top_motor = None
left_motor = None
right_motor = None
top_conn = None
left_conn = None
right_conn = None
back_conn = None

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions

class TCPIPControl(Robot):
    # The following variables are all
    # top_motor = None
    # left_motor = None
    # right_motor = None
    # top_conn = None
    # left_conn = None
    # right_conn = None
    # back_conn = None
    # tcp_received = False
    #
    # tcp_command = None
    # tcp_velocity = None

    # User defined function for initializing and running
    # the TCPIPControl class
    def handle_input(self, cmd, vel, delay):
        global top_motor
        global left_motor
        global right_motor

        top_motor = self.getMotor("Bending Motor")
        # top_motor.setPosition(float('inf'))
        left_motor = self.getMotor("Left Wheel Motor")
        # left_motor.setPosition(float('inf'))
        right_motor = self.getMotor("Right Wheel Motor")
        # right_motor.setPosition(float('inf'))

        top_conn = self.getConnector("top conn")
        top_conn.enablePresence(64)
        left_conn = self.getConnector("left conn")
        left_conn.enablePresence(64)
        right_conn = self.getConnector("right conn")
        right_conn.enablePresence(64)
        back_conn = self.getConnector("back conn")
        back_conn.enablePresence(64)

        whichStop = 0

        if cmd == 1:
            self.move(left_motor, vel, 1)
            self.move(right_motor, vel, 1)
            message = 'Moving forward for ' + str(delay)
        elif cmd == 2:
            self.move(left_motor, vel, -1)
            self.move(right_motor, vel, -1)
            message = 'Moving backward for ' + str(delay)
        elif cmd == 3:
            self.move(left_motor, vel, 1)
            self.move(right_motor, vel, -1)
            message = 'Turning left for ' + str(delay)
        elif cmd == 4:
            self.move(left_motor, vel, -1)
            self.move(right_motor, vel, 1)
            message = 'Turning right for ' + str(delay)
        elif cmd == 5:
            self.move(top_motor, vel, 1)
            message = 'Moving the arm down ' + str(delay)
            whichStop = 1
        elif cmd == 6:
            self.move(top_motor, vel, -1)
            message = 'Moving the arm up ' + str(delay)
            whichStop = 1
        elif cmd == 7:
            message = 'Move key out'
            whichStop = 2
        elif cmd == 8:
            message = 'Move key in'
            whichStop = 2
        else:
            message = 'Invalid command ' + str(cmd)

        # delay is used to allow the motor to move for a predetermined
        # amount of time before it's turned off
        self.step(delay)

        # indicates which stop function is called
        if whichStop == 0:
            right_motor.setVelocity(0)
            left_motor.setVelocity(0)
        elif whichStop == 1:
            top_motor.setVelocity(0)

        return message

    def move(self, motor, speed, direction):
        # move motor specific speed and direction
        # speed: 0 is off, 255 is full speed
        # direction: 1 clockwise, -1 counter-clockwise
        motor.setPosition(float('inf'))
        motor.setVelocity(direction * speed)

    # def move_wheels(self, left, right, delay):
    #     self.left_motor.setVelocity(left)
    #     self.right_motor.setVelocity(right)
    #     if delay:
    #         if right != 0 and left != 0:
    #             self.step(2000)
    #         else:
    #             self.step(1000)
    #         self.move_wheels(0, 0, False)
    #     else:
    #         self.tcp_received = False
    #
    # def move_arm(self, velocity, delay):
    #     self.top_motor.setPosition(velocity / 2.0)
    #     if delay:
    #         self.step(500)
    #         self.move_arm(0, False)
    #     else:
    #         self.tcp_received = False

    def setup_new_host_port(self, hostport):
        host = hostport[0]
        port = int(hostport[1])
        return host, port

    def run(self):
        print 'Inside the run method.'
        # The host gethostbyname method is only working on my (Ben Smith's) computer because the
        # host that it's connecting to is my own computer. This will need to change if the connection
        # is external.
        host, port = socket.gethostbyname(socket.gethostname()), 5000
        # data = 'My ID is: 1'.join(sys.argv[1:])
        data = (b'{\"type\": \"SMORES\",\"id\": \"1\", \"ip\": \"' + bytes(socket.gethostbyname(socket.gethostname())) + b'\"}')
        # data = 'My ID is: 1'

        # create a socket (SOCK_STREAM means a TCP socket)
        print 'before socket connection'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'after socket connection'
        # connect to the server and send data
        sock.connect((host, port))
        sock.send(data + '\n')

        # receive data from the server and shut down.
        received = str(sock.recv(1024)).split()

        print 'Sent:        {}'.format(data)
        print 'Received:    {}'.format(received[0] + ', ' + received[1])

        hostport = self.setup_new_host_port(received)
        server = SocketServer.TCPServer((hostport[0], hostport[-1]), TCPHandler)

        print 'Opening Port on: ', hostport[1], '...\n'
        # Spinning the server up in a new thread. The messages sent over TCP will be stored in the
        # global queue that's initiated up at the top.
        thread_server = Thread(target=server.serve_forever)
        thread_server.start()

        # You should insert a getDevice-like function in order to get the
        # instance of a device of the robot. Something like:
        #  led = self.getLed('ledname')

        # So, the way this is handled here is stupid, but I have no choice because this is
        # how the devs of Webots decided to make their controller. Anyway, here is the list
        # of commands that will control the different motors on the robot.
        # self.top_motor = self.getMotor("Bending Motor")
        # # self.top_motor.setPosition(float('0'))
        # self.left_motor = self.getMotor("Left Wheel Motor")
        # # self.left_motor.setPosition(float('inf'))
        # self.right_motor = self.getMotor("Right Wheel Motor")
        # # self.right_motor.setPosition(float('inf'))
        #
        # self.top_conn = self.getConnector("top conn")
        # self.top_conn.enablePresence(64)
        # self.left_conn = self.getConnector("left conn")
        # self.left_conn.enablePresence(64)
        # self.right_conn = self.getConnector("right conn")
        # self.right_conn.enablePresence(64)
        # self.back_conn = self.getConnector("back conn")
        # self.back_conn.enablePresence(64)
        #
        # self.left_motor.setVelocity(0)
        # self.right_motor.setVelocity(0)
        # The queue is where all the commands will be stored and accessed over TCP and in the Simulator.
        # The queue_free is a boolean that lets the program know when the queue is accessible.
        global queue
        global queue_free

        # Main loop
        while True:
            # Perform a simulation step of 64 milliseconds
            # and leave the loop when the simulation is over
            if self.step(64) == -1:
                break
            # If the queue is free, lock the queue, get the command from the queue
            # lock the queue, and then handle the command.
            if (queue_free == True) and not queue.empty():
                queue_free = False
                command = queue.get()
                queue_free = True
                # The first two commands are sent to the command function using the command
                # type and then the velocity.
                self.handle_input(int(command[0]), int(command[1])/100, int(command[2]))
                # The command will execute for the specified duration of time.
                self.step(int(command[2]))
            print 'loop executed'

class TCPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            print 'we are in the tcp handler.'
            # global tcp_command
            # global tcp_velocity
            global queue
            global queue_free
            # Receives the command from the TCP socket.
            self.data = self.request.recv(1024).strip()
            # Splits the string into the individual parts of the command.
            # There are three parts:
            #     1. The command number
            #     2. The velocity for the motors
            #     3. The duraction of the command to execute
            self.data = self.data.split(' ')
            # Sends a response back to the server to confirm reception of the command.
            self.request.send(b'Got it')
            # And finally closes the connection.
            self.request.close()
            # puts the data into the Queue so that information can be passed between threads.
            # If the queue is free, then lock the queue, put the command into the queue,
            # and then lock the queue when finished.
            if queue_free == True:
                print 'Putting command into the queue.'
                queue_free = False
                queue.put(self.data)
                queue_free = True

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.

controller = TCPIPControl()
controller.run()
# creates the threads that is going to run the program here.
# network_thread in this instance starts the connection to the controller in a thread.
# network_thread = Thread(target=controller.connect_to_controller(), args=(self,queue))
# controller_thread = Thread(target=controller.run(), args=(self,queue))
# network_thread.start()
# controller_thread.start()
