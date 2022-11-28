import curses
from curses import wrapper
from random import randint

stdscr = curses.initscr()   #initialise screen
curses.noecho() #turn off automatic echoing of keys
curses.curs_set(False)  #set cursor to False
#create a new window in the screen
win = curses.newwin(40,80, 0, 0)
win.keypad(True)
win.border(0) #draw a border at the edges
win.nodelay(True)

#snake stuff
class Snake:
    def __init__(self, body_ch):
        self.pos = [(20,3), (21,3), (22,3)]
        self.body = body_ch

    def new_pos(self, key):
        y = self.pos[0][0]
        x = self.pos[0][1]
        if key == ord('l'):
            x+=1
        if key == ord('h'):
            x-=1
        if key == ord('k'):
            y-=1
        if key == ord('j'):
            y+=1
        return (y,x)

    def move(self, key):
        (y,x) = self.new_pos(key)
        self.pos.insert(0, (y,x)) #calculate the new position and insert
        tail = self.pos.pop() #pop the tail
        win.addch(tail[0], tail[1], ' ') #add a space where tail used to be

    def eat(self, key):
        (y,x) = self.new_pos(key)
        self.pos.insert(0, (y,x))

        
#Food stuff
class Food():
    def __init__(self, food_ch):
        self.ch = food_ch
        self.pos = (randint(1,38), randint(1,78))

    def realloc(self):
        self.pos = (randint(1,38), randint(1,78))
        win.addch(self.pos[0], self.pos[1], self.ch)

def main(stdscr):
    snake = Snake("o")
    food = Food("a")
    key = 107
    score = 0
    win.addstr(0,17, "SNAKES WITH VIM CONTROLS")
    win.addch(food.pos[0], food.pos[1], food.ch) #add initial food

    while True: #game loop
        win.addstr(0,2, "score: "+ str(score))
        win.timeout(200 - (len(snake.pos)*4)) #wait time for key input reduces with snake length (looking for a better formula since this will stop break at len = 50)

        #dynamics
        usr_key = win.getch() #get user input
        old_key = key
        
        key = usr_key if usr_key != -1 else old_key

        if key not in [ord('h'), ord('j'), ord('k'), ord('l')]: #exclude wrong inputs
            key = old_key

        if snake.pos[0] == food.pos:
            score += 1
            snake.eat(key)
            food.realloc()

        else:
            snake.move(key)
        
        #break loop
        if snake.pos[0][0] == 0:
            break
        if snake.pos[0][0] == 39:
            break
        if snake.pos[0][1] == 0:
            break
        if snake.pos[0][1] == 79:
            break
        if snake.pos[0] in snake.pos[1:]:
            break

        #add snake to window
        win.addch(snake.pos[0][0], snake.pos[0][1], snake.body)

    return score

#Ending the application
curses.endwin()

score= wrapper(main)
print(f"You Died. Your score is: {score}")
