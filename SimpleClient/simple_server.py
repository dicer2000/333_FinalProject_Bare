#  /\_/\  Simple Server
# ( o o ) Programming Project
#  =( )=  Fall 2023
#   ~*~   (Cat by ChatGPT)

import pygame as pg
import sys
import socket
import atexit
from threading import Event, Thread, Lock
import copy
from common import SafeFrame, SafeExiting
from serversettings import *

# Objects for Multi-thread use
current_frame = SafeFrame()
exiting = SafeExiting(False)

# Main game object
class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        # Start the listener
        Thread(target=self.start_comms, args=[self]).start() #Create a thread that runs the function frame_grab while main runs in the current thread

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'Simple Server - {self.clock.get_fps():.1f}')

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')

        k = 0
        for i in range(screen_height):
            y_pixel += pixel_height
            for j in range(screen_width):
                x_pixel += pixel_width
                text_display(output[k], x_pixel, y_pixel)

        # Drawn screen to forefront
        pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exiting.set(True)

    def run(self):
        # Called once to manage whole game
        while not exiting.get():
            self.check_events()
            self.update()
            self.draw()
        # Shut down correctly
        pg.quit()
        sys.exit()

    def start_comms(self, main):
        global current_frame # global video image
        global exiting # global exit program signal

        # Create a socket to listen on the specified port.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", LISTENING_PORT))
        server_socket.listen(1)
        # Close the server socket when the program closes.
        atexit.register(server_socket.close)

        while not exiting.get():
            # Any errors immediately close connection and
            # recycle connection
            try:
                # Accept a connection from a client.
                client_socket, client_address = server_socket.accept()

                # Read the request from the client.
                request = client_socket.recv(BUFFER_SIZE)
                while not exiting.get() and len(request) > 0:
                    # Parse the request.
                    request_line = request.splitlines()[0]
                    request_method, request_data = request_line.decode("utf-8").split(':')

                    if request_method == 'frame':
                        current_frame.set(request_data)
                    elif request_method == 'quit':
                        break
                    else:
                        break
                    # Get next frame of data
                    request = client_socket.recv(BUFFER_SIZE)

            except Exception as e:
                print("ERROR: {}".format(e))
            finally:
                # Close the sockets.
                client_socket.close()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()


