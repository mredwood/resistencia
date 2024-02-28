#!/usr/bin/env python3


import time
import random
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:
    def __init__(self, name, index):
        self.name = name
        self.is_spy = False
        self.index = index


class Intro:
    def __init__(self):
        self.number_players = 0
        self.number_spies = 0
        self.players = []

    def set_players(self):
        while True:
            clear_screen()
            command = input("¿Cuántos jugadores? (Ej. 5)\n>> ")
            try:
                self.number_players = int(command)
                if self.number_players >= 5 and self.number_players <= 10:
                    break
            except:
                pass

        while True:
            for p in range(self.number_players):
                while True:
                    clear_screen()
                    command = input(f"Introduce el nombre del jugador {p+1}\n>> ")
                    if command != "":
                        break
                player = Player(command,p)
                self.players.append(player)

            clear_screen()
            print("Jugadores:\n\n----------")
            for p in self.players:
                print(p.name)
            command = input("----------\n\n¿Correcto? (S/n)\n>> ")

            if command.lower() == "s" or command.lower() == "":
                break
            self.players = []

    def calculate_spies(self):
        if self.number_players in [5,6]:
            self.number_spies = 2
        elif self.number_players in [7,8,9]:
            self.number_spies = 3
        elif self.number_players in [10]:
            self.number_spies = 4
        else:
            self.number_spies = 1

    def give_identities(self):
        clear_screen()
        spy_indices = random.sample(range(self.number_players), self.number_spies)
        for p in self.players:
            if p.index in spy_indices:
                p.is_spy = True

        for p in self.players:
            clear_screen()
            input(f"{p.name}, para revelar tu identidad pulsa Intro.")
            clear_screen()
            if p.is_spy:
                print("Espía")
            else:
                print("Resistencia")
            input("[Pulsa Intro]")

    def reveal_spies(self):
        clear_screen()
        print("Hora de cerrar los ojos. Los espías deberán abrirlos para conocerse entre ellos.")
        input("[Pulsa Intro]")


    def run(self):
        self.set_players()
        self.calculate_spies()
        self.give_identities()
        self.reveal_spies()


class Game:
    def __init__(self, players):
        self.mission = 0
        self.players = players
        self.number_spies = 0
        self.number_players = len(self.players)
        self.current_leader = None
        self.is_game_finished = False
        self.players_mission_table = [
            [2, 2, 2, 3, 3, 3],
            [3, 3, 3, 4, 4, 4],
            [2, 4, 3, 4, 4, 4],
            [3, 3, 4, 5, 5, 5],
            [3, 4, 4, 5, 5, 5]
            ]
        self.how_many_players_go = 0
        self.spy_score = 0
        self.resistance_score = 0
        self.does_resistance_win = None
        self.chosen_players = []
        self.mission_boxes = ["[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]

    def set_leader(self):
        if self.mission == 1:
            self.current_leader = random.choice(self.players)
        else:
            self.current_leader = self.players[(self.current_leader.index + 1) % self.number_players]

    def set_mission(self):
        self.mission+=1

    def calulate_how_many_players_go(self):
        mission_row = self.mission - 1
        player_col = self.number_players - 5
        self.how_many_players_go = self.players_mission_table[mission_row][player_col]

    def choose_players(self):
        while True:
            clear_screen()
            for p in self.players:
                if p.index != self.current_leader.index:
                    print(f"{p.index+1} - {p.name}")

            command = input(f"¿Qué {self.how_many_players_go - 1} jugadores irán a la misión junto con {self.current_leader.name}? (Ej. 1,2,4)\n>> ")
            try:
                indices = [int(i.strip())-1 for i in command.split(",") if int(i.strip())-1 != self.current_leader.index and int(i.strip())-1 >= 0 and int(i.strip())-1 < self.number_players]

                if len(list(set(indices))) != self.how_many_players_go - 1:
                    continue

                for i in indices:
                    print(i)
                self.chosen_players = [p for p in self.players if p.index in indices] + [self.current_leader]
                clear_screen()

                print("Irán a la misión estas personas:\n\n----------")
                for p in self.chosen_players:
                    print(p.name)
                command = input("----------\n\n¿Correcto? (S/n)\n>> ")
                if command.lower() == "s" or command.lower() == "":
                    break
            except:
                pass

    def secret_vote(self):
        spy_votes = 0
        options_for_spy = ["1 - Éxito","2 - Fracaso"]
        options_for_resistance = ["1 - Éxito","2 - Éxito"]
        for p in self.chosen_players:
            clear_screen()
            print(f"{p.name}, hora de votar:")
            input("[Pulsa Intro]")
            while True:
                try:
                    if p.is_spy:
                        clear_screen()
                        for o in options_for_spy:
                            print(o)
                        command = input("Número de opción:\n>> ")
                        print(int(command))
                        if int(command) != 1 and int(command) !=2:
                            continue
                        if int(command) == 2:
                            spy_votes+=1
                    else:
                        clear_screen()
                        for o in options_for_resistance:
                            print(o)
                        command = input("Número de opción:\n>> ")
                        print(int(command))
                        if int(command) != 1 and int(command) !=2:
                            continue
                    break
                except:
                    pass

        clear_screen()
        counter = 5

        while counter > 0:
            print(counter)
            time.sleep(1)
            counter = counter-1
            clear_screen()

        if spy_votes > 0:
            self.spy_score+=1
            self.mission_boxes[self.mission-1] = "[X]"
            print("FRACASO")
            print("):")
            print(f"Han saboteado la misión {spy_votes} veces.")
            input("[Pulsa Intro]")

        if spy_votes == 0:
            self.resistance_score+=1
            self.mission_boxes[self.mission-1] = "[V]"
            print("ÉXITO")
            print("(:")
            print(f"Nadie ha saboteado la misión.")
            input("[Pulsa Intro]")




    def show(self):
        clear_screen()
        print(f"Líder: {self.current_leader.name}")
        print(f"Número de espías: {self.number_spies}")
        print(f"Misión: {self.mission}")
        for box in self.mission_boxes:
            print(box, end=" ")
        print()
        print(f"\nPara esta misión, hay que elegir a {self.how_many_players_go} jugadores.")
        print(f"El líder propone a {self.how_many_players_go - 1} jugadores.\nEsto será sometido a votación hasta 5 veces.")
        input("[Pulsa Intro]")


    def end_game(self):
        clear_screen()
        for box in self.mission_boxes:
            print(box, end=" ")
        print()

        if self.does_resistance_win:
            print("*****")
            print("¡Enhorabuena! ¡La resistencia ha ganado!")
            print("*****")
        else:
            print("*****")
            print("Lamentablemente, la resistencia pierde. ¡En otra ocasión será!")
            print("*****")

        print("\nFin del juego.")
        input("[Pulsa Intro]")

    def check_if_finished(self):
        if self.mission == 5:
            self.is_game_finished = True
        if self.spy_score == 3:
            self.does_resistance_win = False
            self.is_game_finished = True
        elif self.resistance_score == 3:
            self.does_resistance_win = True
            self.is_game_finished = True


    def run(self):
        while not self.is_game_finished:
            self.set_mission()
            self.set_leader()
            self.calulate_how_many_players_go()

            self.show()
            self.choose_players()
            self.secret_vote()

            self.check_if_finished()

        self.end_game()

if __name__ == "__main__":
    intro = Intro()
    intro.run()
    game = Game(intro.players)
    game.number_spies = intro.number_spies
    game.run()

