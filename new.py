from copy import deepcopy
from test import *

# Tic Tac Toe board class
class Board():
    # create constructor (init board class instance)
    def __init__(self, board=None):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        self.number_of_move=0
        # define board position
        self.position = {}
        
        # init (reset) board
        self.init_board()
        
        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
    
    # init (reset) board
    def init_board(self):
        # loop over board rows
        for row in range(10):
            # loop over board columns
            for col in range(10):
                # set every board square to empty square
                self.position[row, col] = self.empty_square
    
    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = Board(self)
        
        # make move
        board.position[row, col] = self.player_1
        
        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        # return new board state
        return board
    
    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                # this is not a draw
                return False
        
        # by default we return a draw
        return True
    
    # get whether the game is won
    def is_win(self):
        ##################################
        # vertical sequence detection

        # loop over board columns
        for col in range(10):
            # define winning sequence list
            winning_sequence = []
            winning_sequence_h = []
            # loop over board rows
            for row in range(10):
                # if found same next element in the row               
                if self.position[row, col] == self.player_2:
                # update winning sequence
                 winning_sequence.append((row, col))
                else:
                    winning_sequence=[]
                if self.position[col, row] == self.player_2:
                    # update winning sequence
                    winning_sequence_h.append((col, row))
                else:
                    winning_sequence_h=[]
                              
                # if we have 3 elements in the row
                if len(winning_sequence) == 3 or len(winning_sequence_h) == 3:
                    # return the game is won state
                    return True
        

    
        ##################################
        # 1st diagonal sequence detection
        ##################################
        
        # define winning sequence list
        # Check diagonals from top-left to bottom-right
        for i in range(8):
            for j in range(8):
                if self.position[i,j] == self.position[i + 1,j + 1] == self.position[i + 2,j + 2]==self.player_2:
                    return True
        # Check diagonals from top-right to bottom-left
        for i in range(8):
            for j in range(2,10):
                if self.position[i,j] == self.position[i + 1,j - 1] == self.position[i + 2,j - 2]==self.player_2:
                    return True
        return False
    
    # generate legal moves to play in the current position
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
      actions = []
      if lastrow<2:
          rangerow1=0
          rangerow2=4
      elif lastrow>8:
          rangerow1=lastrow-2
          rangerow2=10
      else:
          rangerow1=lastrow-2
          rangerow2=lastrow+2
      if lastcol<2:
          rangecol1=0
          rangecol2=4
      elif lastcol>8:
          rangecol1=lastcol-2
          rangecol2=10
      else:
          rangecol1=lastcol-2
          rangecol2=lastcol+2
          
      for row in range(rangerow1,rangerow2):
            # loop over board columns
            for col in range(rangecol1,rangecol2):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/board state to action list
                    actions.append(self.make_move(row, col))
    
        
        # return the list of available actions (board class instances)
      return actions
    
    # main game loop
    def game_loop(self):
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        # print board
        print(self)
        
        # create MCTS instance
        mcts = MCTS()
                
        # game loop
        while True:
            # get user input
            user_input = input('> ')
        
            # escape condition
            if user_input == 'exit': break
            
            # skip empty input
            if user_input == '': continue
            
            try:
                # parse user input (move format [col, row]: 1,2) 
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1
                global lastrow,lastcol
                lastrow=row
                lastcol=col
                print(lastrow,lastcol)
                # check move legality
                if self.position[row, col] != self.empty_square:
                    print(' Illegal move!')
                    continue

                # make move on board
                self = self.make_move(row, col)
                # print board
                print(self)
                
                
                # search for the best move
                best_move = mcts.search(self)
                # legal moves available
                try:
                    # make AI move here
                    self = best_move.board
                    global comp_move
                # game over
                except:
                    pass
                
                # print board
                print(self)
                
                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                
                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
            
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        
    # print board state
    def __str__(self):
        # define board string representation
        board_string = ''
        
        # loop over board rows
        for row in range(10):
            # loop over board columns
            for col in range(10):
                board_string += ' %s' % self.position[row, col]
            
            # print new line every row
            board_string += '\n'
        
        # prepend side to move
        if self.player_1 == 'x':
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
        
        elif self.player_1 == 'o':
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
                        
        # return board string
        return board_string

# main driver
if __name__ == '__main__':
    # create board instance
    board = Board()
    
    # start game loop
    board.game_loop()