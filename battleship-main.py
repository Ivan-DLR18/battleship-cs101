coordinates_game = {
  'A1': {'pos': 54, 'cardinal': (1,1)},
  'B1': {'pos': 58, 'cardinal': (1,2)},
  'C1': {'pos': 62, 'cardinal': (1,3)},
  'D1': {'pos': 66, 'cardinal': (1,4)},
  'E1': {'pos': 70, 'cardinal': (1,5)},
  'A2': {'pos': 104, 'cardinal': (2,1)},
  'B2': {'pos': 108, 'cardinal': (2,2)},
  'C2': {'pos': 112, 'cardinal': (2,3)},
  'D2': {'pos': 116, 'cardinal': (2,4)},
  'E2': {'pos': 120, 'cardinal': (2,5)},
  'A3': {'pos': 154, 'cardinal': (3,1)},
  'B3': {'pos': 158, 'cardinal': (3,2)},
  'C3': {'pos': 162, 'cardinal': (3,3)},
  'D3': {'pos': 166, 'cardinal': (3,4)},
  'E3': {'pos': 170, 'cardinal': (3,5)},
  'A4': {'pos': 204, 'cardinal': (4,1)},
  'B4': {'pos': 208, 'cardinal': (4,2)},
  'C4': {'pos': 212, 'cardinal': (4,3)},
  'D4': {'pos': 216, 'cardinal': (4,4)},
  'E4': {'pos': 220, 'cardinal': (4,5)},
  'A5': {'pos': 254, 'cardinal': (5,1)},
  'B5': {'pos': 258, 'cardinal': (5,2)},
  'C5': {'pos': 262, 'cardinal': (5,3)},
  'D5': {'pos': 266, 'cardinal': (5,4)},
  'E5': {'pos': 270, 'cardinal': (5,5)}
}
poss_list_complete = [x for x in coordinates_game.keys()]

# Player class
class Player:
  def __init__(self, input_name):
    print("Player " + input_name + " created.")
    self.name = input_name
    self.lose = False         # Boolean for if player lost
    self.shot_log = []        # Record of the shots recieved by opponent
    self.hits_recieved = []
    self.misses_recieved = []
    self.fleet = []           # Ship objects list
    self.shots_made_ai = []   # For ai player
    self.hits_ai = []         # For ai player
    self.sunken = [x.is_sunk for x in self.fleet].count(True)
  
  def __repr__(self):
    return f"The player {self.name} has {len(self.fleet) - self.sunken} ships left."

  # Player's ability to attack other player and keep track of damage
  def attack(self, coordinates_att, other_player):
    coordinates_att_card = coordinates_game[coordinates_att]['cardinal']
    hit_counter_temp = 0
    for other_ship in other_player.fleet:
      if coordinates_att_card[0] in other_ship.coordinates[0] and coordinates_att_card[1] in other_ship.coordinates[1]:
        other_player.shot_log.append(coordinates_att_card) 
        other_player.hits_recieved.append(coordinates_att) 
        self.hits_ai.append(coordinates_att)
        self.shots_made_ai.append(coordinates_att)
        other_ship.check_if_sunk()
        hit_counter_temp += 1
        if other_player.check_if_lose():
          other_player.lose = True
          return True
        return 'HIT!'
      else:
        continue
    if hit_counter_temp == 0:
      other_player.misses_recieved.append(coordinates_att)
      self.shots_made_ai.append(coordinates_att)
      return 'MISS!'
  
  def check_if_lose(self):
    sunk_ships = 0
    for ship in self.fleet:
      if ship.is_sunk:
        sunk_ships += 1
      else:
        continue
    if sunk_ships == len(self.fleet):
      self.lose = True
      return True
    else:
      return False

  
# Ship class
class Ship:
  def __init__(self, owner, dimensions, coordinate, orientation='h'):
    self.owner = owner
    self.belongs_to = owner.name
    self.size = dimensions
    self.orientation = orientation
    self.initial_coordinates = coordinates_game[coordinate]['cardinal']
    self.coordinate = coordinates_game[coordinate]['cardinal']
    self.is_sunk = False
    self.hit_count = dimensions[0]*dimensions[1]
    if orientation == 'h':
      if self.coordinate[1] > 6-dimensions[1]:
        raise ValueError("Invalid positioning. Ship doesn't fit.")
    elif orientation == 'v':
      if dimensions[1] > self.coordinate[0] < 6-dimensions[1]:
        raise ValueError("Invalid positioning. Ship doesn't fit.")
    else:
      raise ValueError("Invalid orientation. Use 'h' or 'v'.")
    if dimensions[0] > 2 or dimensions[1] > 3:
        raise ValueError("Invalid dimensions. Max size is (2,3)")
    if self.coordinate[0] > 5 or dimensions[1] > 5:
        raise ValueError("Invalid coordinate. Ship doesn't fit.")
    
    if orientation == 'h':
      self.coordinates = [list(range(j, j+i)) for i, j in zip(dimensions, self.coordinate)]
    else:
      self.coordinates = []
      if dimensions[0] == 2:
        self.coordinates.append(list(range(self.coordinate[0]-dimensions[1]+1, self.coordinate[0]+1)))
        self.coordinates.append(list(range(self.coordinate[1], self.coordinate[1]+2)))
      else:
        self.coordinates.append(list(range(self.coordinate[0]-dimensions[1]+1, self.coordinate[0]+1)))
        self.coordinates.append(list(range(self.coordinate[1], self.coordinate[1]+1)))

    self.all_coordinates = []
    for i in self.coordinates[0]:
      for j in self.coordinates[1]:
        self.all_coordinates.append((i,j))
    
    for ship_owner in owner.fleet:
      for ship_owner_coord in ship_owner.all_coordinates:
        if ship_owner_coord in self.all_coordinates:
          print("Invalid coordinate. Ship doesn't fit.")
          raise ValueError("Invalid coordinate. Ship doesn't fit.")
        else:
          pass
    
  
  def check_if_sunk(self):
    # print('Checking if sunk')
    coord_hits = 0
    for x in self.all_coordinates:
      # print('All coordinates: ', self.all_coordinates)
      # print('Shot log by opponent: ', self.owner.shot_log)
      if x in self.owner.shot_log:
        coord_hits += 1
    # print('Final coord hits: ', coord_hits)
    # print('Ship size hit count: ', self.hit_count_extra)
    if self.hit_count == coord_hits:
      self.is_sunk = True
      # print(f"Ship from {self.belongs_to} is sunk!.")
      return True
    else:
      return False
  
  def __repr__(self):
    return f"This ship belongs to {self.belongs_to} its dimensions are {self.size}."

# Board class
class Board:
  def __init__(self, player):
    self.owner = player
    self.owner_name = player.name
    self.board_status = '''
     A   B   C   D   E
   +---+---+---+---+---+
 1 |   |   |   |   |   |
   +---+---+---+---+---+
 2 |   |   |   |   |   |
   +---+---+---+---+---+
 3 |   |   |   |   |   |
   +---+---+---+---+---+
 4 |   |   |   |   |   |
   +---+---+---+---+---+
 5 |   |   |   |   |   |
   +---+---+---+---+---+

'''
    self.shot_record_board = self.board_status
    self.set_board(player)

  def set_board(self, player):
    for ship in player.fleet:
      ship_pos = []
      for key, values in coordinates_game.items():
        if values.get('cardinal') == ship.all_coordinates[0]:
          ship_pos.append(key)
        elif values.get('cardinal') == ship.all_coordinates[-1]:
          ship_pos.append(key)
        elif values.get('cardinal') in ship.all_coordinates[1:]:
          ship_pos.append(key)

      if ship.orientation == 'h':
        if ship.size[0] == 2:
          if ship.size[1] == 2:
            index = coordinates_game.get(ship_pos[0])['pos']
            self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[2])['pos']
            self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[-1])['pos']
            self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[-3])['pos']
            self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
          else:
            index = coordinates_game.get(ship_pos[0])['pos']
            self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[3])['pos']
            self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[-1])['pos']
            self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
            index = coordinates_game.get(ship_pos[2])['pos']
            self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
            for i in [1, 4]:
              index = coordinates_game.get(ship_pos[i])['pos']
              self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]
        else:
          index = coordinates_game.get(ship_pos[0])['pos']
          self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
          index = coordinates_game.get(ship_pos[-1])['pos']
          self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
          for i in ship_pos[1:-1]:
            index = coordinates_game.get(i)['pos']
            self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]

      elif ship.orientation == 'v':
        if ship.size[0] == 2:
          index = coordinates_game.get(ship_pos[0])['pos']
          self.board_status = self.board_status[:index] + '∆' + self.board_status[index+1:]
          index = coordinates_game.get(ship_pos[1])['pos']
          self.board_status = self.board_status[:index] + '∆' + self.board_status[index+1:]
          index = coordinates_game.get(ship_pos[-1])['pos']
          self.board_status = self.board_status[:index] + '∇' + self.board_status[index+1:]
          index = coordinates_game.get(ship_pos[-2])['pos']
          self.board_status = self.board_status[:index] + '∇' + self.board_status[index+1:]
          for i in ship_pos[2:-2]:
            index = coordinates_game.get(i)['pos']
            self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]
        else:
          index = coordinates_game.get(ship_pos[0])['pos']
          self.board_status = self.board_status[:index] + '∆' + self.board_status[index+1:]
          index = coordinates_game.get(ship_pos[-1])['pos']
          self.board_status = self.board_status[:index] + '∇' + self.board_status[index+1:]
          for i in ship_pos[1:-1]:
            index = coordinates_game.get(i)['pos']
            self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]
  
  def update_board(self):
    for i in self.owner.hits_recieved:
      index = coordinates_game[i]['pos']
      self.board_status = self.board_status[:index] + '⨀' + self.board_status[index+1:]
    for i in self.owner.misses_recieved:
      index = coordinates_game[i]['pos']
      self.board_status = self.board_status[:index] + 'X' + self.board_status[index+1:]

  def show_damage(self):
    # print('shots_made_ai: ', self.owner.shots_made_ai)
    # print('hits_ai: ', self.owner.hits_ai)
    misses = [x for x in self.owner.shots_made_ai if x not in self.owner.hits_ai]
    # print('misses: ', misses)
    # print('shot_log: ', self.owner.shot_log)
    for i in self.owner.shots_made_ai:
      if i in self.owner.hits_ai:
        index = coordinates_game[i]['pos']
        self.shot_record_board = self.shot_record_board[:index] + '⨀' + self.shot_record_board[index+1:]
      
      elif i in misses:
        index = coordinates_game[i]['pos']
        self.shot_record_board = self.shot_record_board[:index] + 'X' + self.shot_record_board[index+1:]

      else:
        pass      
    print(self.shot_record_board)

  def __repr__(self):
    self.update_board()
    return self.board_status


import sys
import os
import time
import random

def main():

  while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    start_game = input('''
██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ 
██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗
██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝
██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ 
██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     
╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
                                                By: Iván Díaz de León R.

Welcome to battleship, this version inspired by the popular battleship game is a project for the
CS101 Codecademy Computer Science career path. In this game each player will build their own fleet 
of two ships with dimensions between (1,2) to (2,3) and position them in a grid that goes from A1 to D5.

Players will take turns to try to hit an enemy ship until they sink all their fleet.
Good luck and have fun!
(At any moment, if you want to hard exit the game, whenever you're asked to input something 
write 'exit' and the program will end).
        
How would you like to play? (only write the letter):
    a) Player vs Player
    b) Player vs Computer
        
''').lower()
    if start_game == 'exit':
      sys.exit()

    elif start_game == 'a':
      print('Option a selected')
      game_mode = input('''Now select the type of game:
a) Quick game (1 ship per player)
b) Standard game (2 ships per player)

''')
      if start_game == 'exit':
        sys.exit()

      elif game_mode == 'a':
        print('Quick game selected')
        players_list = game_setup(ships_per_player=1)
        players = [0,1]
        break

      elif game_mode == 'b':
        print('Standard game selected')
        players_list = game_setup()
        players = [0,1]
        break

    elif start_game == 'b':
      print('Option b selected')
      game_mode = input('''Now select the type of game:
a) Quick game (1 ship per player)
b) Standard game (2 ships per player)

''')
      if start_game == 'exit':
        sys.exit()
      
      elif game_mode == 'a':
        print('Quick game selected')
        players_list = game_setup(1, False)
        players = [0, 2]
        ai_player = players_list[0][1]
        break

      elif game_mode == 'b':
        print('Standard game selected')
        players_list = game_setup(pvp=False)
        players = [0, 2]
        ai_player = players_list[0][1]
        break

    else:
      print('Invalid input, try again')
      time.sleep(1)
      pass

  
  while True:
    for turn in players:
      if turn != 2:
        player_in_turn = players_list[0][turn]
        player_in_turn_board = players_list[1][turn]
        rival = players_list[0][turn-1] # player_in_turn[0] is player object and [1] is its board
        rival_board = players_list[1][turn-1] # player_in_turn[0] is player object and [1] is its board
        turn_taken = False

        while not turn_taken:
          player_action = input(f"Is {player_in_turn.name}'s turn. What would you want to do:\n\ta) Attack!\n\tb) Check my board\n\tc) Check shots made\n")
          if player_action == 'exit':
            sys.exit()

          elif player_action == 'a':
            outcome = attack_method(player_in_turn, rival)
            if outcome == None:
              pass
            elif outcome == True:
              lost_check = [players_list[0][0].lose, players_list[0][1].lose]
              if True in lost_check:
                game_end(players_list[0][lost_check.index(False)], players_list[1][0], players_list[1][1])
            else:
              print('\n')
              print(outcome)
              print('\n')
              turn_taken = True

          elif player_action == 'b':
            print(player_in_turn_board, end='', flush=True)

            for i in range(5,0,-1):
              print(f'This board will be erased to avoid cheating in: {i} seconds', end='\r')
              time.sleep(1)
            # Erase board to avoid cheating 
            for _ in range(15):
              sys.stdout.write("\033[K")  # Clear the current line
              sys.stdout.write("\033[F")  # Move cursor to the beginning of the previous line
            print('\n')
          elif player_action == 'c':
            player_in_turn_board.show_damage()
            print('\n')
          else:
            pass

      else:
        past_fleet_status = [x.is_sunk for x in players_list[0][0].fleet]
        print(f"Now is {ai_player.name}'s turn. Get ready to get attacked!")
        shot = ai_attack(ai_player)
        outcome = ai_player.attack(shot, players_list[0][0])
        actual_fleet_status = [x.is_sunk for x in players_list[0][0].fleet]
        if past_fleet_status != actual_fleet_status:
          players_list[0][1].hits_ai = []
        else:
          pass
        if outcome == True:
          if players_list[0][0].lose:
            game_end(players_list[0][1], players_list[1][0], players_list[1][1])
        else:
          print('\n')
          print(outcome)
          print('\n')
        time.sleep(3)
    


def game_setup(ships_per_player=2, pvp=True):
  players_list = []
  players_boards = []
  if pvp:
    players = [0,1]
  else:
    players = [0]

  for player_input in players:
    player_input_name = input(f"Enter player {player_input+1} name and hit enter: ")
    if player_input_name == 'exit':
      sys.exit()
    player = Player(player_input_name)
    players_list.append(player)
    
    while len(players_list[player_input].fleet) < ships_per_player:
      try:
        player_input_ship_size = input("Welcome, " + str(player_input_name) + ", please enter the dimensions (width, lenght) with a from the list [(1,2), (1,3), (2,3)] of your next ship: ")
        for i in range(3,0,-1):
          print(f'Your input will be erased to avoid cheating in: {i} seconds'.upper(), end='\r')
          time.sleep(1)
        sys.stdout.write("\033[K")  # Clear the current line
        sys.stdout.write("\033[F")  # Move cursor to the beginning of the previous line
        sys.stdout.write("\033[K")  # Clear the current line
        print("Welcome, " + str(player_input_name) + ", please enter the dimensions (width, lenght) with a from the list [(1,2), (1,3), (2,2), (2,3)] of your next ship: (?,?)")
        print('\n')
        
        if player_input_ship_size == 'exit':
          sys.exit()
        values = player_input_ship_size[1:-1].split(',')
        
        if int(values[0]) > 2 or int(values[1]) > 3:
          raise ValueError("Invalid dimensions. Max size is (2,3)")
        else:
          pass
      except ValueError:
        print("DimensionsError: Invalid dimensions. Max size is (2,3)")
        continue
      
      player_input_board = Board(player)
      while True:
        try:
          print('Now please enter the position and orientation in the following board using the classic notation (e.g: B3 h):')
          print(player_input_board)
          player_input_ship_pos = input('Position and orientation: ')
          if player_input_ship_pos == 'exit':
            sys.exit()
          try:
            if player_input_ship_pos[0] not in 'ABCDE' or player_input_ship_pos[1] not in '12345' or player_input_ship_pos[3] not in 'hv':
              raise ValueError("Invalid position")
            else:
              # Here creates a Ship object to check if its a valid instance with the parameters the user input
              player_ship = Ship(players_list[player_input], (int(values[0]), int(values[1])), player_input_ship_pos[:2], player_input_ship_pos[-1])
              players_list[player_input].fleet.append(player_ship)
              time.sleep(0.5)
              player_input_board = Board(player)
              print(player_input_board)

              for i in range(2,0,-1):
                print(f'This board will be erased to avoid cheating in: {i} seconds', end='\r')
                time.sleep(1)
              # Erase board to avoid cheating 
              for _ in range(17):
                sys.stdout.write("\033[K")  # Clear the current line
                sys.stdout.write("\033[F")  # Move cursor to the beginning of the previous line
              print('Position and orientation: ?? ?')
              print('\n')
              break
          except IndexError:
            print("Input doesn't match with classic notation. (e.g: B3 h)")
        except ValueError:
          print("PositionError: Please enter a valid coordinate and orientation.")
    players_boards.append(player_input_board)
  if pvp:
    return [[players_list[0], players_list[1]],[players_boards[0], players_boards[1]]]
  else:
    ai_player = generate_AI(ships_per_player)
    return [[players_list[0], ai_player[0]],[players_boards[0], ai_player[1]]]
  


def game_end(winner, winner_board, loser_board):
  def cartel_print(name):
    import math

    string = 'WINNER: ' + name
    leng = len(string)
    cartel = f"""

 _____                                    _____ 
( ___ )----------------------------------( ___ )
 |   | ░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄ |   | 
 |   | ░█░█░█▀█░█░█░█▀▀░░░█░█░█░█░█▀▀░█▀▄ |   | 
 |   | ░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀ |   | 
 |   |                                    |   |
 |___|                                    |___| 
(_____)----------------------------------(_____)


"""

    string = ' ' * math.floor((36-leng)/2) + string + ' ' * math.ceil((36-leng)/2)
    leng = len(string)
    cartel = cartel[:301] + string + cartel[337:]
    return cartel
  print(winner_board, loser_board)
  print(cartel_print(winner.name))

  sys.exit()

def attack_method(player, rival):
  while True:
    shot = input(f"Okay, {player.name} get ready to attack {rival.name}.\nPlease write the coordinates of your attack (e.g: A1):\n(Write 'back' to go back)\n")
    if shot == 'exit':
      sys.exit()
    elif shot == 'back':
      return
    elif shot[0] in 'ABCDE' and shot[1] in '12345':
      return player.attack(shot, rival)
    else:
      continue

def ai_attack(ai_player):
  global shot_select
  shot_select = ''
  shots_made = ai_player.shots_made_ai
  # print('Shots made: ', shots_made)
  try:
    last_shot = shots_made[-1]
  except IndexError:
    last_shot = 'F6'
  hits = ai_player.hits_ai
  # print('Hits: ', hits)
  poss_shots = [x for x in poss_list_complete if x not in shots_made]
  best_shots = []

  def search_nearby():
    # print('Search nearby process')
    nearby_hits = []
    for i in hits:
      for x in get_next_shots(i):
        nearby_hits.append(x)
    # print('Nearby hits: ', nearby_hits)
    return nearby_hits
  
  def neighbor():
    if len(hits) <= 1:
      hits_neigh = hits
      # print('Neighbot process without modification')
    else:
      hits_neigh = hits[:-1]
      # print('Neighbot process modified')
    try:
      for sh in [x for x in get_next_shots(hits_neigh[0]) if x not in hits_neigh and x not in shots_made]:
        best_shots.append(sh)
      return random.choice(best_shots)
    except IndexError:
      # print('Process failed, calling search_nearby')
      nearby_list = search_nearby()
      nearby_list = [x for x in search_nearby() if x not in hits_neigh and x not in shots_made]
      for sh in nearby_list:
        best_shots.append(sh)
      return random.choice(best_shots)
  
  if len(hits) == 1 or shot_select == last_shot:
    # print('Hit list is 1 or last shot equal to shot select, calling Neighbor')
    shot_select = neighbor()
    # print('Neighbor selected: ', shot_select)

  elif len(hits) > 1:
    # print('Hit list over 1, looking for sequence')
    if len(hits) <= 3:
      # print('Hit less o equal to 3')
      common_coord = hits[0][0] if hits[0][0] == hits[1][0] else hits[0][1]
      # print('Sequence detected: ', common_coord)
    else:
      # print('Hit over 3')
      common_coord = hits[-2][0] if hits[-2][0] == hits[-1][0] else hits[-2][1]
      # print('Sequence detected: ', common_coord)
    try:
      if common_coord in 'ABCDE':
        next_shots = []
        for i in hits:
          for x in get_next_shots(i, 'h'):
            next_shots.append(x)
        for sh in [x for x in next_shots if x not in hits and x not in shots_made]:
          best_shots.append(sh)
        shot_select = random.choice(best_shots)
        # print('Possible shots after vertical sequence detection: ', best_shots)
        # print('Shot selected after vertical sequence detection: ', shot_select)
      else:
        next_shots = []
        for i in hits:
          for x in get_next_shots(i, 'v'):
            next_shots.append(x)
        for sh in [x for x in next_shots if x not in hits and x not in shots_made]:
          best_shots.append(sh)
        shot_select = random.choice(best_shots)
        # print('Possible shots after horizontal sequence detection: ', best_shots)
        # print('Shot selected after horizontal sequence detection: ', shot_select)
    except IndexError:
      # print('Process of sequence finding failed, calling neighbor')
      shot_select = neighbor()

  else:
    # print('Selecting random shot')
    shot_select = random.choice(poss_shots)
  
  # print('best shots', best_shots)
  # print('Shot select: ', shot_select)
  return shot_select
      

def generate_AI(ships_per_player=2):
  ai = Player('dAIvid Jones')
  poss_list = [x for x in coordinates_game.keys() if 'E' not in x]
  orient = random.choice(['h', 'v'])
  if orient == 'h':
    poss_list = [x for x in coordinates_game.keys() if 'E' not in x]
  else:
    poss_list = [x for x in coordinates_game.keys() if '1' not in x]
  
  while len(ai.fleet) < ships_per_player:
    values = random.choice([(1,2), (1,3), (2,2), (2,3)])
    ai_board = Board(ai)
    while True:
      try:
        ai_ship_poss = random.choice(poss_list)
        # Here creates a Ship object to check if its a valid instance with the parameters the user input
        ai_ship = Ship(ai, values, ai_ship_poss, orient)
        ai.fleet.append(ai_ship)
        break
      except ValueError:
        print("PositionError: Please enter a valid coordinate and orientation.")
    
  ai_board = Board(ai)
  return [ai, ai_board]

def get_next_shots(coordinate, straight=None):
  col = coordinate[0]
  row = coordinate[1]
  columns = ['A', 'B', 'C', 'D', 'E']
  rows = ['1', '2', '3', '4', '5']

  poss_shots = []
  poss_cols = []
  poss_rows = []
  if straight == 'h':
    if rows.index(row) == 0:
      poss_rows.append(rows[rows.index(row)+1])
    elif rows.index(row) == 4:
      poss_rows.append(rows[rows.index(row)-1])
    else:
      poss_rows.append(rows[rows.index(row)-1])
      poss_rows.append(rows[rows.index(row)+1])
    
    for x in poss_rows:
      poss_shots.append(col+x)
    return poss_shots
      

  elif straight == 'v':
    if columns.index(col) == 0:
      poss_cols.append(columns[columns.index(col)+1])
    elif columns.index(col) == 4:
      poss_cols.append(columns[columns.index(col)-1])
    else:
      poss_cols.append(columns[columns.index(col)-1])
      poss_cols.append(columns[columns.index(col)+1])

    for x in poss_cols:
      poss_shots.append(x+row)
    return poss_shots

  else:
    if columns.index(col) == 0:
      poss_cols.append(columns[columns.index(col)+1])
    elif columns.index(col) == 4:
      poss_cols.append(columns[columns.index(col)-1])
    else:
      poss_cols.append(columns[columns.index(col)-1])
      poss_cols.append(columns[columns.index(col)+1])

    if rows.index(row) == 0:
      poss_rows.append(rows[rows.index(row)+1])
    elif rows.index(row) == 4:
      poss_rows.append(rows[rows.index(row)-1])
    else:
      poss_rows.append(rows[rows.index(row)-1])
      poss_rows.append(rows[rows.index(row)+1])

    for x in poss_cols:
      poss_shots.append(x+row)
    for y in poss_rows:
      poss_shots.append(col+y)
    return poss_shots


main()