import curses
import random
from curses import textpad

def create_food(snake, box):
    food = None

    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food

def print_score(window, score):
    sh, sw = window.getmaxyx()
    score_text = f"Score: {score}"
    window.addstr(1, sw//2 - len(score_text)//2, score_text)
    window.refresh()

def main(window):
    curses.curs_set(0)
    window.nodelay(1)
    window.timeout(100)

    sh, sw = window.getmaxyx()
    padding = 3
    box = [[padding,padding],[sh-padding, sw-padding]]
    textpad.rectangle(window, box[0][0],box[0][1],box[1][0],box[1][1])

    snake = [[sh//2, sw//2+1],[sh//2, sw//2],[sh//2,sw//2-1]]
    snakechar = '█'
    direction = curses.KEY_RIGHT

    for y,x in snake:
        window.addstr(y, x, snakechar)

    food = create_food(snake,box)
    foodchar = '✹'
    window.addstr(food[0], food[1], foodchar)

    score = 0
    print_score(window, score)


    while True:
        key = window.getch()
        
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if key == curses.KEY_UP and direction != curses.KEY_DOWN and key != direction:
                direction = key
            elif key == curses.KEY_DOWN and direction != curses.KEY_UP and key != direction:
                direction = key
            elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT and key != direction:
                direction = key
            elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT and key != direction:
                direction = key

        head = snake[0]

        if direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]

        snake.insert(0, new_head)
        window.addstr(new_head[0], new_head[1], snakechar)

        if head == food:
            score+= 1
            food = create_food(snake,box)
            window.addstr(food[0], food[1], foodchar)
            print_score(window, score)
        else:
            window.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:]):
            msg = '    Game Over!    '
            window.addstr(sh//2, sw//2 - len(msg)//2, msg)
            window.nodelay(0)
            break

        window.refresh()

curses.wrapper(main)
