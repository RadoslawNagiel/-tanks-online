import socket
import pickle
import pygame
from _thread import *
from game import Game

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")
game = Game()

commands_sets = []


def game_loop():
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        while not len(commands_sets) == 0:
            (player_id, commands) = commands_sets.pop()

            while not len(commands) == 0:
                command = commands.pop()
                game.use_command((player_id, command))

        game.loop()


def threaded_client(conn, player_id):
    conn.send(pickle.dumps(game.tanks[player_id]))
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            commands_sets.append((player_id, data))

            if not data:
                print("Disconnected")
                break
            else:
                reply = game

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    game.remove_tank(player_id)

    conn.close()


start_new_thread(game_loop, ())

idForNextPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    game.add_tank(idForNextPlayer)

    start_new_thread(threaded_client, (conn, idForNextPlayer))
    idForNextPlayer += 1
