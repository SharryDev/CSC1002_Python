import turtle
from random import randrange
turtle.tracer(0)  # disable the animation

# set up the screen and the initial status bar
g_screen = turtle.Screen()
g_screen.setup(560, 620)
g_screen.title('Snake')

# set up the status area
g_status = turtle.Turtle()
g_status.hideturtle()
g_status.penup()
g_status.goto(0, 240)

'''the position of the snake and monster will be stored in list [x, y],
from [0, 0] at the left bottom to [24, 24] at the right top, later used in turtle display.'''

# set up the snake head and initial position
snake_head = turtle.Turtle("square")
snake_head.color('red')
snake_head.left(90)
snake_head.penup()
head_current_location = [12, 12]
head_target_location = []

# set up the snake tail and initial position
snake_tail = turtle.Turtle("square")
snake_tail.color('black')
snake_tail.hideturtle()
snake_tail.penup()
snake_tail.pencolor('blue')
snake_tail_length = 0
snake_tail_expand_num = 5  # initial tail length is 5
snake_tail_position = []

# set up the monster and random initial position
monsters = []
monster_target_locations = []

for _ in range(4):
    monster = turtle.Turtle('square')
    monster.color('purple')
    monster.penup()
    monsters.append(monster)
    target_location = [randrange(0, 24, 1), randrange(0, 24, 1)]
    while 7 <= target_location[0] <= 17 or 7 <= target_location[1] <= 17:
        target_location = [randrange(0, 24, 1), randrange(0, 24, 1)]
    monster_target_locations.append(target_location)

monster_1 = monsters[0]
monster_2 = monsters[1]
monster_3 = monsters[2]
monster_4 = monsters[3]

monster_current_location_1 = monster_target_location_1 = monster_target_locations[0]
monster_current_location_2 = monster_target_location_2 = monster_target_locations[1]
monster_current_location_3 = monster_target_location_3 = monster_target_locations[2]
monster_current_location_4 = monster_target_location_4 = monster_target_locations[3]

# set up some gaming initial parameters
g_time = 0  # gaming time
g_contact = 0  # snake tail and monster contact time
snake_motion = 'Paused'  # initial snake motion status
former_snake_motion = 'Paused'
snake_speed = 200  # initial snake speed
monster_speed = 900  # initial monster speed
is_start_time = True  # True if the game starts
is_end_time = False  # True if the game ends
valid_food_list = [1, 2, 3, 4, 5]  # food left for eating


# refresh the data and display the status bar
def refresh_status_bar():
    g_status.clear()
    g_status.write('Contact: ' + str(g_contact) + '          Time: ' + str(g_time)
                   + '          Motion: ' + snake_motion, align="center", font=('Arial', 16, 'bold'))


# refresh the game time every second after start
def refresh_time():
    global g_time
    global is_start_time
    global is_end_time

    if is_start_time:
        is_start_time = False
        g_screen.ontimer(refresh_time, 1000)
    else:
        if not is_end_time:
            g_time += 1
            refresh_status_bar()
            g_screen.ontimer(refresh_time, 1000)
        else:
            return


# display the frame of the game board
def draw_rectangle(turtle_obj, width, height, x, y):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.pendown()
    for _ in range(2):
        turtle_obj.forward(width)
        turtle_obj.left(90)
        turtle_obj.forward(height)
        turtle_obj.left(90)
    turtle_obj.penup()


def display_frame():
    global g_intro
    # Set up the screen frame
    screen_frame = turtle.Turtle()
    screen_frame.hideturtle()
    screen_frame.pensize(2)

    draw_rectangle(screen_frame, 500, 500, -250, -280)
    draw_rectangle(screen_frame, 500, 60, -250, 220)

    # Display the introduction
    g_intro = turtle.Turtle()
    g_intro.hideturtle()
    g_intro.penup()
    g_intro.goto(0, 145)
    g_intro.write("Click anywhere to start, have fun!!!", align="center", font=('Arial', 16, 'normal'))

    refresh_status_bar()
    g_screen.update()


# refresh and display the snake
def display_snake():
    # display the snake head
    snake_head.goto(-240 + head_current_location[0] * 20, -270 + head_current_location[1] * 20)
    # display the snake tail
    for each_block_location in snake_tail_position:
        snake_tail.goto(-240 + each_block_location[0] * 20, -270 + each_block_location[1] * 20)
        snake_tail.stamp()
    g_screen.update()


# refresh and display the food
def display_food():
    global food_1
    global food_2
    global food_3
    global food_4
    global food_5

    foods = []

    for _ in range(5):
        food = turtle.Turtle()
        food.penup()
        food.hideturtle()
        foods.append(food)

    food_1 = foods[0]
    food_2 = foods[1]
    food_3 = foods[2]
    food_4 = foods[3]
    food_5 = foods[4]

    food_1.goto(-240 + food_location_1[0] * 20, -278 + food_location_1[1] * 20)
    food_1.write('1', align="center", font=('Arial', 16, 'normal'))

    food_2.goto(-240 + food_location_2[0] * 20, -278 + food_location_2[1] * 20)
    food_2.write('2', align="center", font=('Arial', 16, 'normal'))

    food_3.goto(-240 + food_location_3[0] * 20, -278 + food_location_3[1] * 20)
    food_3.write('3', align="center", font=('Arial', 16, 'normal'))

    food_4.goto(-240 + food_location_4[0] * 20, -278 + food_location_4[1] * 20)
    food_4.write('4', align="center", font=('Arial', 16, 'normal'))

    food_5.goto(-240 + food_location_5[0] * 20, -278 + food_location_5[1] * 20)
    food_5.write('5', align="center", font=('Arial', 16, 'normal'))


# refresh and display the monster
def display_monster():
    monster_1.goto(-240 + monster_target_location_1[0] * 20, -270 + monster_target_location_1[1] * 20)
    monster_2.goto(-240 + monster_target_location_2[0] * 20, -270 + monster_target_location_2[1] * 20)
    monster_3.goto(-240 + monster_target_location_3[0] * 20, -270 + monster_target_location_3[1] * 20)
    monster_4.goto(-240 + monster_target_location_4[0] * 20, -270 + monster_target_location_4[1] * 20)

    g_screen.update()


# display that game is over on the top of monster
def display_game_over():
    game_over_reminder = turtle.Turtle()
    game_over_reminder.penup()
    game_over_reminder.hideturtle()
    game_over_reminder.pencolor('purple')
    game_over_reminder.goto(0, 190)
    game_over_reminder.write('Game Over!',  align="center", font=('Arial', 20, 'bold'))


# display that user wins the game on the top of snake
def display_game_win():
    game_win_reminder = turtle.Turtle()
    game_win_reminder.penup()
    game_win_reminder.hideturtle()
    game_win_reminder.pencolor('red')
    game_win_reminder.goto(0, 190)
    game_win_reminder.write('Winner!', align="center", font=('Arial', 20, 'bold'))


# detect if food's positions contain overlapping
def is_food_valid(loc_1, loc_2, loc_3, loc_4, loc_5):
    loc_list = []
    for loc in [loc_1, loc_2, loc_3, loc_4, loc_5]:
        if loc not in loc_list:
            loc_list.append(loc)
    if len(loc_list) == 5 and [12, 12] not in loc_list:
        return True
    else:
        # if position overlaps, return False
        return False


# set the random position of food
def set_food():
    global food_location_1
    global food_location_2
    global food_location_3
    global food_location_4
    global food_location_5
    global original_food_pos_1
    global original_food_pos_2
    global original_food_pos_3
    global original_food_pos_4
    global original_food_pos_5

    food_locations = []
    original_food_positions = []

    for _ in range(5):
        location = [randrange(0, 25, 1), randrange(0, 25, 1)]
        food_locations.append(location)
        original_food_positions.append(location.copy())

    food_location_1 = food_locations[0]
    food_location_2 = food_locations[1]
    food_location_3 = food_locations[2]
    food_location_4 = food_locations[3]
    food_location_5 = food_locations[4]

    original_food_pos_1 = original_food_positions[0]
    original_food_pos_2 = original_food_positions[1]
    original_food_pos_3 = original_food_positions[2]
    original_food_pos_4 = original_food_positions[3]
    original_food_pos_5 = original_food_positions[4]

    # set up the food position again if containing overlapping
    if not is_food_valid(food_location_1, food_location_2,
                         food_location_3, food_location_4, food_location_5):
        set_food()


# set the snake to go up
def set_snake_direction_up():
    global snake_motion
    snake_motion = 'Up'


# set the snake to go down
def set_snake_direction_down():
    global snake_motion
    snake_motion = 'Down'


# set the snake to go left
def set_snake_direction_left():
    global snake_motion
    snake_motion = 'Left'


# set the snake to go right
def set_snake_direction_right():
    global snake_motion
    snake_motion = 'Right'


# set the snake to pause and continue
def set_snake_paused():
    global snake_motion
    global former_snake_motion

    if snake_motion != 'Paused':
        former_snake_motion = snake_motion
        snake_motion = 'Paused'  # snake pauses
    else:
        snake_motion = former_snake_motion


# check if the next step of snake is movable, return False if not
def is_snake_movable(target_loc):
    if 0 <= target_loc[0] <= 24 and 0 <= target_loc[1] <= 24:
        return True
    else:
        return False


# let snake move at a certain time interval
def snake_move():
    global snake_motion
    global snake_speed
    global head_target_location
    global head_current_location
    global snake_tail_length
    global snake_tail_position
    tail_to_expand_position = [12, 12]

    if is_game_over():
        return  # stop moving if game over
    else:
        # when snake doesn't pause
        if snake_motion != 'Paused':
            # find the position snake head goes
            if snake_motion == 'Up':
                refresh_status_bar()
                head_target_location = [head_current_location[0], head_current_location[1] + 1]
            elif snake_motion == 'Down':
                refresh_status_bar()
                head_target_location = [head_current_location[0], head_current_location[1] - 1]
            elif snake_motion == 'Left':
                refresh_status_bar()
                head_target_location = [head_current_location[0] - 1, head_current_location[1]]
            elif snake_motion == 'Right':
                refresh_status_bar()
                head_target_location = [head_current_location[0] + 1, head_current_location[1]]

            # when snake can move to next position
            if is_snake_movable(head_target_location):
                # update the position of every block of snake tail
                if snake_tail_length > 0:
                    tail_to_expand_position = snake_tail_position[snake_tail_length - 1]
                    for verse_order in range(snake_tail_length):
                        if verse_order <= snake_tail_length - 1:
                            snake_tail_position[snake_tail_length - verse_order - 1] \
                                = snake_tail_position[snake_tail_length - verse_order - 2]
                    snake_tail_position[0] = head_current_location
                # update the current snake head position
                head_current_location = head_target_location

                # expand the snake tail if needed
                if snake_tail_expand_num != 0:
                    snake_expand(tail_to_expand_position)
                else:
                    snake_speed = 200

                # display the moved snake based on the position
                snake_tail.clearstamps()
                display_snake()
                eat_food()
                # move the snake again after a certain time interval
                g_screen.ontimer(snake_move, snake_speed)
            # when snake can't move to next position (blocked by frame/tail)
            else:
                g_screen.ontimer(snake_move, snake_speed)

        # when snake pauses
        else:
            refresh_status_bar()
            g_screen.ontimer(snake_move, snake_speed)


# expand the snake tail
def snake_expand(to_expand_pos):
    global snake_tail_length
    global snake_tail_expand_num
    global snake_tail_position
    global snake_speed

    snake_speed = 400  # snake slows down when expanding the tail
    snake_tail_position.append(to_expand_pos)
    snake_tail_length += 1
    snake_tail_expand_num -= 1


# check if the next step of monster is movable, return False if not
def is_monster_movable(target_loc):
    # check if board frame blocks the movement of monster
    if 0 <= target_loc[0] <= 23 and 0 <= target_loc[1] <= 23:
        return True
    else:
        return False


# let snake move at a certain time interval
def move_monster(monster_num, current_location, target_location, check_contact_func):
    global monster_speed

    if is_game_over():
        return  # monster stops when game over

    delta_x = head_current_location[0] - current_location[0]
    delta_y = head_current_location[1] - current_location[1]

    # set monster's next step by chasing snake head
    if delta_y >= delta_x and delta_y >= -delta_x and delta_y >= 0:
        target_location[0], target_location[1] = current_location[0], current_location[1] + 1
    elif delta_y <= delta_x and delta_y <= -delta_x and delta_y <= 0:
        target_location[0], target_location[1] = current_location[0], current_location[1] - 1
    elif -delta_x <= delta_y <= delta_x and delta_x >= 0:
        target_location[0], target_location[1] = current_location[0] + 1, current_location[1]
    elif delta_x <= delta_y <= -delta_x and delta_x <= 0:
        target_location[0], target_location[1] = current_location[0] - 1, current_location[1]

    random_speed = randrange(-200, 200, 1)

    # check if next step is movable and move the monster
    if is_monster_movable(target_location):
        current_location[:] = target_location
        check_contact_func()
        display_monster()
        # move the monster again after a certain time interval
        g_screen.ontimer(lambda: move_monster(monster_num, current_location, target_location, check_contact_func),
                         monster_speed + random_speed)
    else:
        target_location[:] = current_location
        check_contact_func()
        g_screen.ontimer(lambda: move_monster(monster_num, current_location, target_location, check_contact_func),
                         monster_speed + random_speed)


# check if snake eats food, and remove the eaten ones
def eat_food():
    global snake_tail_expand_num

    if food_location_1 == head_current_location:
        food_1.clear()
        food_location_1[0] = -1  # move the eaten food out of the game board
        food_location_1[1] = -1
        valid_food_list.remove(1)
        snake_tail_expand_num += 1
    if food_location_2 == head_current_location:
        food_2.clear()
        food_location_2[0] = -2
        food_location_2[1] = -2
        valid_food_list.remove(2)
        snake_tail_expand_num += 2
    if food_location_3 == head_current_location:
        food_3.clear()
        food_location_3[0] = -3
        food_location_3[1] = -3
        valid_food_list.remove(3)
        snake_tail_expand_num += 3
    if food_location_4 == head_current_location:
        food_4.clear()
        food_location_4[0] = -4
        food_location_4[1] = -4
        valid_food_list.remove(4)
        snake_tail_expand_num += 4
    if food_location_5 == head_current_location:
        food_5.clear()
        food_location_5[0] = -5
        food_location_5[1] = -5
        valid_food_list.remove(5)
        snake_tail_expand_num += 5


def move_food():
    global valid_food_list
    global is_end_time

    def is_food_movable(target_food_loc):
        if 0 <= target_food_loc[0] <= 24 and 0 <= target_food_loc[1] <= 24:
            return True
        else:
            return False

    def move_food_1():
        global food_location_1
        random_offset_x = randrange(-2, 2, 1)
        random_offset_y = randrange(-2, 2, 1)
        food_target_location = [food_location_1[0] + random_offset_x, food_location_1[1] + random_offset_y]
        if is_food_movable(food_location_1):
            if is_food_movable(food_target_location) and is_food_valid(food_target_location, food_location_2,
                                                                       food_location_3, food_location_4, food_location_5):
                food_location_1 = food_target_location
                food_1.clear()
                food_1.goto(-240 + food_location_1[0] * 20, -278 + food_location_1[1] * 20)
                food_1.write('1', align="center", font=('Arial', 16, 'normal'))
            else:
                move_food_1()

        else:
            pass

    def move_food_2():
        global food_location_2
        random_offset_x = randrange(-2, 2, 1)
        random_offset_y = randrange(-2, 2, 1)
        food_target_location = [food_location_2[0] + random_offset_x, food_location_2[1] + random_offset_y]
        if is_food_movable(food_location_2):
            if is_food_movable(food_target_location) and is_food_valid(food_location_1, food_target_location,
                                                                       food_location_3, food_location_4, food_location_5):
                food_location_2 = food_target_location
                food_2.clear()
                food_2.goto(-240 + food_location_2[0] * 20, -278 + food_location_2[1] * 20)
                food_2.write('2', align="center", font=('Arial', 16, 'normal'))
            else:
                move_food_2()

        else:
            pass


    def move_food_3():
        global food_location_3
        random_offset_x = randrange(-2, 2, 1)
        random_offset_y = randrange(-2, 2, 1)
        food_target_location = [food_location_3[0] + random_offset_x, food_location_3[1] + random_offset_y]
        if is_food_movable(food_location_3):
            if is_food_movable(food_target_location) and is_food_valid(food_location_1, food_location_2,
                                                                       food_target_location, food_location_4, food_location_5):
                food_location_3 = food_target_location
                food_3.clear()
                food_3.goto(-240 + food_location_3[0] * 20, -278 + food_location_3[1] * 20)
                food_3.write('3', align="center", font=('Arial', 16, 'normal'))
            else:
                move_food_3()

        else:
            pass

    def move_food_4():
        global food_location_4
        random_offset_x = randrange(-2, 2, 1)
        random_offset_y = randrange(-2, 2, 1)
        food_target_location = [food_location_4[0] + random_offset_x, food_location_4[1] + random_offset_y]
        if is_food_movable(food_location_4):
            if is_food_movable(food_target_location) and is_food_valid(food_location_1, food_location_2,
                                                                       food_location_3, food_target_location, food_location_5):
                food_location_4 = food_target_location
                food_4.clear()
                food_4.goto(-240 + food_location_4[0] * 20, -278 + food_location_4[1] * 20)
                food_4.write('4', align="center", font=('Arial', 16, 'normal'))
            else:
                move_food_4()

        else:
            pass


    def move_food_5():
        global food_location_5
        random_offset_x = randrange(-2, 2, 1)
        random_offset_y = randrange(-2, 2, 1)
        food_target_location = [food_location_5[0] + random_offset_x, food_location_5[1] + random_offset_y]
        if is_food_movable(food_location_5):
            if is_food_movable(food_target_location) and is_food_valid(food_location_1, food_location_2,
                                                         food_location_3, food_location_4, food_target_location):
                food_location_5 = food_target_location
                food_5.clear()
                food_5.goto(-240 + food_location_5[0] * 20, -278 + food_location_5[1] * 20)
                food_5.write('5', align="center", font=('Arial', 16, 'normal'))
            else:
                move_food_5()

        else:
            pass

    if not is_end_time:

        move_food_1()
        move_food_2()
        move_food_3()
        move_food_4()
        move_food_5()

        # every 5 seconds
        g_screen.ontimer(move_food, 3000)


# check if snake head crush monster, or snake eats all food, and end the game
def is_game_over():
    global is_end_time

    # Check if head and monster collide
    for monster_current_location in [monster_current_location_1, monster_current_location_2, monster_current_location_3, monster_current_location_4]:
        if  monster_current_location[0] - head_current_location[0] == 0 and monster_current_location[1] - head_current_location[1] == 0 :
            display_game_over()
            is_end_time = True
            return True

    # Check if snake eats all the food
    if snake_tail_length == 20:
        display_game_win()
        is_end_time = True
        return True

    return False


# detect if monster contacts snake
def check_contact_1():
    global g_contact
    for each_block in snake_tail_position:
        if -1 <= monster_current_location_1[0] - each_block[0] <= 0:
            if -1 <= monster_current_location_1[1] - each_block[1] <= 0:
                g_contact += 1
                refresh_status_bar()
                return


def check_contact_2():
    global g_contact
    for each_block in snake_tail_position:
        if -1 <= monster_current_location_2[0] - each_block[0] <= 0:
            if -1 <= monster_current_location_2[1] - each_block[1] <= 0:
                g_contact += 1
                refresh_status_bar()
                return


def check_contact_3():
    global g_contact
    for each_block in snake_tail_position:
        if -1 <= monster_current_location_3[0] - each_block[0] <= 0:
            if -1 <= monster_current_location_3[1] - each_block[1] <= 0:
                g_contact += 1
                refresh_status_bar()
                return


def check_contact_4():
    global g_contact
    for each_block in snake_tail_position:
        if -1 <= monster_current_location_4[0] - each_block[0] <= 0:
            if -1 <= monster_current_location_4[1] - each_block[1] <= 0:
                g_contact += 1
                refresh_status_bar()
                return


# start the game if click detected
def start_game(x, y):
    global g_intro
    global g_time
    g_intro.clear()
    g_screen.onclick(None)

    display_food()  # set up the food
    move_food()
    refresh_time()  # set up the timer
    snake_move()  # move the snake
    move_monster(1, monster_current_location_1, monster_target_location_1, check_contact_1)
    move_monster(2, monster_current_location_2, monster_target_location_2, check_contact_2)
    move_monster(3, monster_current_location_3, monster_target_location_3, check_contact_3)
    move_monster(4, monster_current_location_4, monster_target_location_4, check_contact_4)
    return x, y


# main execution function of the game
def main():
    display_frame()
    display_snake()
    display_monster()
    set_food()
    g_screen.onkey(set_snake_direction_up, 'Up')
    g_screen.onkey(set_snake_direction_down, 'Down')
    g_screen.onkey(set_snake_direction_left, 'Left')
    g_screen.onkey(set_snake_direction_right, 'Right')
    g_screen.onkey(set_snake_paused, 'space')
    g_screen.onclick(start_game)


if __name__ == '__main__':
    main()
    g_screen.listen()
    g_screen.mainloop()
