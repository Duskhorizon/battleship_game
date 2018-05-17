from random import randint
import os
import settings
import sys

# printing board
def print_board(board):
  print ("======= BATTLESHIPS =======")
  print ("\n" *1)
  for row in board:
    print("            " + " ".join(row))
  print ("\n" *1)  



# function for getting random ship location
def random_row(board):
  return randint(0, settings.board_size - 1)
def random_col(board):
  return randint(0, settings.board_size - 1)

# defining coordinates that are restricted from ship placement
def restricted_coordinates(temp_coordinates):
  returned_coords = []
  returned_coords.append(temp_coordinates)
  returned_coords.append([temp_coordinates[0] + 1,temp_coordinates[1] + 1])
  returned_coords.append([temp_coordinates[0] - 1,temp_coordinates[1] - 1])
  returned_coords.append([temp_coordinates[0] + 1,temp_coordinates[1] - 1])
  returned_coords.append([temp_coordinates[0] - 1,temp_coordinates[1] + 1])
  returned_coords.append([temp_coordinates[0],temp_coordinates[1] - 1])
  returned_coords.append([temp_coordinates[0],temp_coordinates[1] + 1])
  returned_coords.append([temp_coordinates[0] + 1,temp_coordinates[1]])
  returned_coords.append([temp_coordinates[0] - 1,temp_coordinates[1]])
  return returned_coords

#checking if score is high score and writing it to the file if so
def high_score(passed_score):
  with open("highscores.txt","r+") as score:
    score_lines = score.read().split("#")
    if os.stat("highscores.txt").st_size == 0:
      score_lines = []
    temp_points_table = []
    #extracting only points to determine if score is high
    for x in range(1,len(score_lines),2):
      temp_points_table.append(int(score_lines[x]))
    if any(i > passed_score for i in temp_points_table) or len(score_lines) < 20:
      print('\nHEY YOU HAVE A HIGH SCORE\n')
      temp_name = input("What is your name: ")
    if len(score_lines) == 0:
      score_lines.insert(0,str(passed_score))
      score_lines.insert(0,temp_name)
    else:  
      for i in range(1,len(score_lines),2):
        if passed_score < int(score_lines[i]):
          score_lines.insert(i - 1,str(passed_score))
          score_lines.insert(i - 1,temp_name)
          break
        if i == len(score_lines) - 1:
          score_lines.append(temp_name)
          score_lines.append(str(passed_score))
    score.seek(0)
    score.write('#'.join(score_lines[:20]))
    score.truncate()    
    high_scores_menu()


#main game
def play_game():
  import settings
  # initial settings
  board = []
  ships_coordinates = []
  forbiden_coordinates = []
  player_shot = []
  ships_remaining = settings.ships
  place_attempt = 0
  # filling board with "0"'s
  for x in range(0,settings.board_size):
    board.append(["O"] * settings.board_size)
  # filling ship_coordinates table with random coordinates * ship amount   
  while len(ships_coordinates) < settings.ships and place_attempt < 100:
    temp_coordinates = [random_row(board),random_col(board)]
    place_attempt += 1
    # checking if randomed coordinate is valid for ship placement
    while temp_coordinates not in forbiden_coordinates:
      ships_coordinates.append(temp_coordinates)
      forbiden_coordinates += restricted_coordinates(temp_coordinates)
      break
  # program will stop placing ships after 100 attempts and will inform user how many ships was able to place on board   
  if place_attempt == 100:
    os.system('cls' if os.name == 'nt' else 'clear')  
    print('WARNING : game failed to place all ships on board, amount of ships : ',len(ships_coordinates))
    ships_remaining = len(ships_coordinates)
    input("Press Enter to continue")      
  # loop with printing board, turn, asking for input
  for turn in range(1,settings.shots + 1): 
    os.system('cls' if os.name == 'nt' else 'clear')     
    print("Turn", turn)
    print("Max turn ",settings.shots)
    print(' ')
    print (ships_coordinates)
    print (forbiden_coordinates)
    guess_row = int(input("Guess Row: ")) - 1
    guess_col = int(input("Guess Col: ")) - 1
    player_shot = [guess_row,guess_col]
    # win condition
    if player_shot in ships_coordinates:
      print("\nCongratulations! You sank my battleship!")
      input("Press Enter to continue")
      board[guess_row][guess_col] = "S"
      ships_remaining -= 1
      if ships_remaining == 0:
        print("\nCONGRATULATIONS!!THAT WAS THE LAST SHIP")
        input("Press Enter to continue")
        high_score(turn)
    # loose condition
    else:
      if turn == settings.shots:
        print("Game Over")
        input("Press Enter to continue")
        main_menu()
      else:
        # checking if shot was in board coordinates or was tried before  
        if guess_row not in list(range(settings.board_size)) or guess_col not in list(range(settings.board_size)):
          print("Oops, that's not even in the ocean.")
          input("Press Enter to continue")
        elif board[guess_row][guess_col] == "X":
          print( "You guessed that one already." )
          input("Press Enter to continue")
        elif board[guess_row][guess_col] == "S":
          print( "You guessed that one already." )
          input("Press Enter to continue")  
        else:
          print("You missed my battleship!")
          input("Press Enter to continue")
          board[guess_row][guess_col] = "X"

#main menu
def main_menu():
  os.system('cls' if os.name == 'nt' else 'clear')
  print ("======= BATTLESHIPS =======")
  print ("\n" *4)
  print('1. Play Game \n2. Options \n3. High Scores \n4. Quit')
  main_menu_choice = int(input('Choose: '))
  if main_menu_choice == 1:
    play_game()
  elif main_menu_choice == 2:  
    options_menu()
  elif main_menu_choice == 3:  
    high_scores_menu()
  elif main_menu_choice == 4:  
    sys.exit(0)

#high scores menu
def high_scores_menu():
  with open("highscores.txt","r") as score:
    score_lines = score.read().split("#")
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("======= HIGH SCORES =======")
    print ("\n" *4)
    if os.stat("highscores.txt").st_size == 0:
      print('NO HIGH SCORES YET, GO PLAY BE THE FIRST!')
    else:  
      for x in range(0,len(score_lines),2):
        print("\nNAME :",score_lines[x],"\nWON IN ROUND: ",score_lines[x+1])
    print ("\n" *2)
    input("Press Enter to continue")
  main_menu()

 
#options menu
def options_menu():
  import re
  import settings
  # using regex
  pattern = r"[0-9]+"
  os.system('cls' if os.name == 'nt' else 'clear')
  print ("======= BATTLESHIPS =======")
  print ("\n" *4)
  ranked_temp = input("Enter 1 to enable IRONMAN_RANKED_PRO_MODE_GODLIKE (scoreboard enabled) or press 0 to disable it and adjust setting manually : ")
  while ranked_temp != "1" and ranked_temp != "0":
    ranked_temp = input("Enter 1 to enable IRONMAN_RANKED_PRO_MODE_GODLIKE (scoreboard enabled) or press 0 to disable it and adjust setting manually : ")
  if ranked_temp == "1":
    settings.ranked = 1
    main_menu()
  #board_size
  temp_board_size = input('Choose board size or enter 0 for default (5): ')
  while re.match(pattern,temp_board_size) == None:
    temp_board_size = input('Choose board size or enter 0 for default (5): ')
  if temp_board_size == "0":
    settings.board_size = 5
  else:
    settings.board_size = int(temp_board_size)
  #shots
  temp_shots = input('Choose available shots amount or enter 0 for default (4): ')
  while re.match(pattern,temp_shots) == None:
    temp_shots = input('Choose available shots amount or enter 0 for default (4): ')
  if temp_shots == "0":
    settings.shots = 4
  else:
    settings.shots = int(temp_shots)
  #ships    
  temp_ships = input('Choose ships amount or enter 0 for default (10): ')
  while re.match(pattern,temp_ships) == None:
    temp_ships = input('Choose ships amount or enter 0 for default (10):  ')
  if temp_ships == "10":
    settings.ships = 2
  else:
    settings.ships = int(temp_ships)
  main_menu()

main_menu()

