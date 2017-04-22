'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import signal
import inspect
import socket
from main_level import MainLevel

# ***************** Constants used to configure the controller *****************
OPTIONS = {
    'GOAL_LOCATIONS': [(2, 1), (2, 2), (2, 3)], # The locations of the goal states.
    'DUMP_MSGS_TO_MAIN': False, # Show all messages in main log output
    'RAISE_ERRORS_AFTER_CATCH': True, # Raises errors after catching
    'NUMBER_OF_DEVICES': 3, # Number of devices that the controller expects to use
    'CAMERA_ID': 0, # The location of the camera as viewed by openCV. Built-in webcam is always 0.
    'BAUD': 115200, # Baud rate used by the COM ports
    'TCP_LISTENER_IP': socket.gethostbyname(socket.gethostname()), # Hostname the TCP listener uses
    'TCP_LISTENER_PORT': 5000, # Port the TCP listener uses
    'TCP_LISTENER_START_PORT': 10000, # Starting port for TCP bots to use
    'BOT_LOOP_SLEEP_INTERVAL': .001, # Number of seconds between bot event loop iterations
    'BOT_SLEEP_INTERVALS_PER_PING': 5000, # Number of bot sleep intervals before a ping is sent
    'COM_PORT_TIMEOUT': 10, # Number of seconds that a COM port will wait for a response
    'TCP_PORT_TIMEOUT': 10, # Number of seconds that a TCP port will wait for a response
    'MAIN_LOOP_SLEEP_INTERVAL': .001, # Number of seconds that between main event loop iterations
    'COM_LOOP_SLEEP_INTERVAL': .001, # Number of seconds that between com event loop iterations
    'MOV_LOOP_SLEEP_INTERVAL': .001, # Number of seconds that between mov event loop iterations
    'AI_LOOP_SLEEP_INTERVAL': .001, # Number of seconds that between AI event loop iterations
    'ARENA_SIZE': 5, # The number of tiles on one side of the arena
    'ARENA_SIZE_CM': 82.55, # The square wall size of the arena
    'MAX_CNTR_MISALIGNMENT': 3, # The distance from a centerpoint that is acceptable error for robot
    'MAX_NORTH_MISALIGNMENT': 5, # The degrees off of north that is acceptable error for robot
    'FREAKOUT_ITERATIONS': 1, # The number of actions a robot should take when freaking out
    'colors': ['Orange', 'smores3', 'smores2', 'smores1', 'Light Blue'], #colors that will be searched for in blob detection of camera process
    'minColors': [[0, 67, 122], [48, 37, 1], [113, 85, 153], [108, 119, 170], [90, 102, 228]], #minimum value for corresponding colors [0] arena (orange) [1] smores3 (green) [2] smores2 (purple) [3] smores1 (blue) [3] available (light blue)
    'maxColors': [[20, 255, 255], [83, 255, 255], [134, 149, 202], [116, 183, 218], [114, 181, 255]], #maximum value for corresponding colors [0] arena (orange) [1] smores3 (green) [2] smores2 (purple) [3] smores1 (blue) [3] available (light blue)
    'CAMERA_ITERATIONS': 50
}
# ******************************************************************************

def signal_handler(sig, frame):
    """
    Handles the SIGINT when shutting down the controller.  Ensures that all processes exit
    gracefully.

    Args:
        signal (int): The number indicating the signal that was given.
        frame (frame): The object representing the frame where the signal originated.
    """
    # Get the origin of the SIGINT
    origin = inspect.getouterframes(frame)[0].function

    # Initilize shutdown only once, if the signal is from the main frame
    if __name__ == "__main__" and origin == "main_loop" and sig == 2:
        print("Initiating shutdown")

        MAIN_CONTROLLER.shutdown()

    # Don't do anything for the other frames

# Reigister the SIGINT signal handler
# This captures a ctrl+c and causes the controller to shutdown.
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    MAIN_CONTROLLER = MainLevel(OPTIONS)
    MAIN_CONTROLLER.main_loop()
