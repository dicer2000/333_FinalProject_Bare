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
import colorsys
import select

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
        self.font = pg.font.SysFont('Arial', 20, bold=True)
        self.new_game()

    def new_game(self):
        # Start the listener
        t = Thread(target=self.start_comms, args=[self]) #, daemon=True
        t.start() #Create a thread that runs the function 

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'Simple Server - {self.clock.get_fps():.1f}')

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')

        strData = current_frame.get()
        # Display it all if we have good data
        if strData is not None and len(strData) == (HEIGHT/PIXEL_HEIGHT) * (WIDTH/PIXEL_WIDTH):

            vert_chars = int(HEIGHT/PIXEL_HEIGHT)
            horz_chars = int(WIDTH/PIXEL_WIDTH)
            for i in range(vert_chars):
                for j in range(horz_chars):
                    self.text_display(strData[i*vert_chars+j], j*PIXEL_WIDTH, i*PIXEL_HEIGHT)

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
        pg.quit()
        sys.exit()

    def text_display(self, char, x, y):
        text = self.font.render(str(char), True, WHITE)
        #self.hsv2rgb(self.hue, 1, 1))
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def start_comms(self, main):
        global current_frame # global video image
        global exiting # global exit program signal

        # Create a socket to listen on the specified port.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", LISTENING_PORT))
        server_socket.listen(1)
        read_list = [server_socket]

        # Close the server socket when the program closes.
        atexit.register(server_socket.close)

        while not exiting.get():
            
                # Check for a socket connecting via the 'select', if available
                # then go ahead and accept(), otherwise recycle after 2 seconds
                # (last parameter)
                readable, writable, errored = select.select(read_list, [], [], 2)
                for s in readable:
                    if s is server_socket:

                        try:
                            # Accept a connection from a client.
                            client_socket, client_address = server_socket.accept()

                            # Read the request from the client.
                            request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                            while not exiting.get() and len(request) > 0:
                                # Parse the request.
                                request_line = request.splitlines()[0]
                                request_method, request_data = request_line.split(':')

                                if request_method == 'frame':
                                    current_frame.set(request_data)
                                elif request_method == 'quit':
                                    break
                                else:
                                    break
                                # Get next frame of data
                                request = client_socket.recv(BUFFER_SIZE).decode("utf-8")

                        except Exception as e:
                            print("Comms Error: {}".format(e))
                        finally:
                            # Close the sockets.
                            client_socket.close()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()


