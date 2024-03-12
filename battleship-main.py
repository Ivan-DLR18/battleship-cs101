import re

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

class Player:
  def __init__(self, input_name):
    print("Player " + input_name + " created.")
    self.name = input_name
    self.lose = False   # Boolean for if player lost
    self.shot_log = []  # Record of the shots recieved by opponent
    self.turns = 0      # Turns counter
    self.fleet = []     # Ship objects list
  
  def __repr__(self):
    return "The player {name_player} has {ships_player} ships left in {turns_player}.".format(self.name, len(self.fleet), self.turns)

  def attack(self, coordinates_att, other_player):
    coordinates_att = coordinates_game[coordinates_att]['cardinal']
    hit_counter_temp = 0
    for other_ship in other_player.fleet:
      if coordinates_att[0] in other_ship.coordinates[0] and coordinates_att[1] in other_ship.coordinates[1]:
        print('HIT!')
        other_player.shot_log.append(coordinates_att) 
        other_ship.hit_count -= 1
        hit_counter_temp += 1
        other_ship.check_if_sunk()
        if other_player.check_if_lose():
          print(f'Player {other_player.name} has lost!')
        break
      else:
        continue
    if hit_counter_temp == 0:
      print('MISS!')
      other_player.shot_log.append(coordinates_att)
    print('attack finished')
  
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

  

class Ship:
  def __init__(self, owner, dimensions, coordinate, orientation='h'):
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
    if self.hit_count == 0:
      self.is_sunk = True
      print(f"Ship from {self.belongs_to} is sunk!.")
  
  def __repr__(self):
    return f"This ship belongs to {self.belongs_to} its dimensions are {self.size}."

# ∆∇<>◘
   
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
        index = coordinates_game.get(ship_pos[0])['pos']
        self.board_status = self.board_status[:index] + '<' + self.board_status[index+1:]
        index = coordinates_game.get(ship_pos[-1])['pos']
        self.board_status = self.board_status[:index] + '>' + self.board_status[index+1:]
        for i in ship_pos[1:-1]:
          index = coordinates_game.get(i)['pos']
          self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]
      elif ship.orientation == 'v':
        index = coordinates_game.get(ship_pos[0])['pos']
        self.board_status = self.board_status[:index] + '∆' + self.board_status[index+1:]
        index = coordinates_game.get(ship_pos[-1])['pos']
        self.board_status = self.board_status[:index] + '∇' + self.board_status[index+1:]
        for i in ship_pos[1:-1]:
          index = coordinates_game.get(i)['pos']
          self.board_status = self.board_status[:index] + '◘' + self.board_status[index+1:]
  
  def update_board(self):
    for i in self.owner.shot_log:
      for key, value in coordinates_game.items():
        if str(i) in str(value):
          index = coordinates_game[key]['pos']
          self.board_status = self.board_status[:index] + 'X' + self.board_status[index+1:]

  def show_damage(self):
    for i in self.owner.shot_log:
      for key, value in coordinates_game.items():
        if str(i) in str(value):
          index = coordinates_game[key]['pos']
          self.shot_record_board = self.shot_record_board[:index] + 'X' + self.shot_record_board[index+1:]
    print(self.shot_record_board)

  def __repr__(self):
    self.update_board()
    return self.board_status


import sys

def main():
  start_game = input('''
██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ 
██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗
██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝
██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ 
██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     
╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
                                                By: Iván Díaz de León R.

Welcome to battleship, in this game each player will build their own fleet of two ships 
with dimensions between (1,2) to (2,3) and position them in a grid that goes from A1 to D5.
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
    players_list = game_setup()
    player_in_turn, rival = players_list # player_in_turn[0] is player object and [1] is its board
  elif start_game == 'b':
    print('Option b selected')
  
  while True:
    lost_check = [player_in_turn[0], rival[0]]
    if True in lost_check:
      game_end(players_list[lost_check.index(True)].name)
    else:
      for turn in [0,1]:
        
        player_action = input(f"Is {player_in_turn[0].name}'s turn. What would you want to do:\n\
                              \t\ta) Attack!\n\
                              \t\tb) Check my board\n\
                              \t\tc) Check shots made\n")
      if player_action == 'exit':
        sys.exit()
      elif player_action == 'a':
        attack_method()
      elif player_action == 'b':
        print(player_in_turn[1])
      elif player_action == 'c':
        rival[1].show_damage()
  


def game_setup():
  players_list = []
  players_boards = []

  for player_input in [0,1]:
    player_input_name = input(f"Enter player {player_input+1} name and hit enter: ")
    if player_input_name == 'exit':
      sys.exit()
    player = Player(player_input_name)
    players_list.append(player)
    
    while len(players_list[player_input].fleet) < 2:
      try:
        player_input_ship_size = input("Welcome, " + str(player_input_name) + ", please enter the dimensions (width, lenght) with a max size of (2,3) of your next ship: ")
        if player_input_ship_size == 'exit':
          sys.exit()
        values = player_input_ship_size[1:-1].split(',')
        if int(values[0]) > 2 or int(values[1]) > 3:
          print(values[0], values[1])
          raise ValueError("Invalid dimensions. Max size is (2,3)")
        else:
          pass
      except ValueError:
        print("DimensionsError: Invalid dimensions. Max size is (2,3)")
        pass
      
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
              player_input_board = Board(player)
              print(player_input_board)
              players_boards.append(player_input_board)
              break
          except IndexError:
            print("Input doesn't match with classic notation. (e.g: B3 h)")
        except ValueError:
          print("PositionError: Please enter a valid coordinate and orientation.")
  return zip(players_list, players_boards)

def game_end(winner):
  print(f'Game over, player {winner} won!')
  sys.exit()

def attack_method():
  pass

# ivan = Player('Iván')
# ivan.fleet.append(Ship(ivan, (1, 2), 'E2', 'v'))
# ivan.fleet.append(Ship(ivan, (1,2), 'A3', 'v'))


# michelle = Player('Michelle')
# michelle.fleet.append(Ship(michelle, (1, 3), 'C3', 'v'))
# michelle.fleet.append(Ship(michelle, (1,2), 'A2', 'h'))
# print(len(michelle.fleet))

# board_ivan = Board(ivan)
# board_michelle = Board(michelle)
# print(board_ivan)

# ivan.attack('C1', michelle)
# ivan.attack('C2', michelle)
# ivan.attack('C3', michelle)
# michelle.attack('C3', ivan)
# # board_michelle.update_board(michelle) # Esto es para que el jugador vea donde le han disparado
# ## Esto es para que el jugador vea donde ha disparado
# # board_michelle.show_damage()
# board_ivan.show_damage()
# print(board_michelle)
main()
