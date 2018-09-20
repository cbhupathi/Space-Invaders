#Caroline Bhupathi
#cbhupathi@wesleyan.edu
#COMP 112 (lab section 7)
#Final Project (Space Invaders)
#December 17th, 2016

import turtle
import math
import time
import os
import random

turtle.setup(width = 700, height = 700)
turtle.title("Space Invaders")
turtle.bgcolor("black")
turtle.bgpic("finalproject_bg.gif")

#position of player
userx_position = 0
USERY_POSITION = 250

#list of enemies, where each enemy has x, y position and current direction
enemies_position = [[-100, 150, "left"], [100, 150, "left"], [0, 50, "right"], [-250, 0, "left"], [250, 0, "left"], [-230, -50, "right"], [230, -50, "right"], [-200, -100, "left"], [200, -100, "left"], [-160, -150, "right"], [160, -150, "right"], [-110, -200, "left"], [110, -200, "left"], [-50, -250, "right"], [50, -250, "right"]]

#position of bullets currently in flight
bullets_position = []

#if we should stop the game
gameover = False

frame_counter = 0
speed_counter = 11
score_counter = 0
high_scores = []
scores_and_names = 200

def main():
    turtle.tracer(0,0)
    turtle.hideturtle()
    turtle.onkey(key_left, "Left")
    turtle.onkey(key_right, "Right")
    turtle.onkey(key_space, "space")
    turtle.listen()
    reset()
    while not gameover:
        turtle.clear()
        physics()
        ai()
        if gameover == True:
            endofgame()
        else:
            frame()
            turtle.update()
            time.sleep(0.02)
            global frame_counter
            frame_counter += 1
    
def reset(): #set up the initial position of the enemies and player
    global userx_position
    global USERY_POSITION
    userx_position = 0
    USERY_POSITION = 250
    global enemies_position
    enemies_position = [[-100, 150, "left"], [100, 150, "left"], [0, 50, "right"], [-250, 0, "left"], [250, 0, "left"], [-230, -50, "right"], [230, -50, "right"], [-200, -100, "left"], [200, -100, "left"], [-160, -150, "right"], [160, -150, "right"], [-110, -200, "left"], [110, -200, "left"], [-50, -250, "right"], [50, -250, "right"]]
    global bullets_position
    bullets_position = []
    global gameover
    gameover = False
    global frame_counter
    frame_counter = 0
    global speed_counter
    speed_counter = 11
    global score_counter
    score_counter = 0
    global scores_and_names
    scores_and_names = 200

def key_left(): #move the player’s ship left
    global userx_position
    if (userx_position + 7.5) - 17.5 >= -300:
        userx_position -= 10

def key_right(): #move the player’s ship right
    global userx_position
    if (userx_position + 7.5) + 17.5 <= 300:
        userx_position += 10

def key_space(): #add a new bullet to the game world
    global userx_position
    global USERY_POSITION
    global bullets_position
    user_position = [(userx_position + 7.5), (USERY_POSITION - 12.99)]
    if len(bullets_position) < 10:
        bullets_position.append(user_position)

def physics(): #update the position of any bullet currently in flight
    global bullets_position
    global enemies_position
    global score_counter
    for bullets in bullets_position.copy():
        if bullets[1] <= -290:
            bullets_position.remove(bullets)
        elif not enemies_position == []:
            for enemy in enemies_position.copy():
                distance_bullet = math.sqrt(math.pow(bullets[0] - enemy[0], 2) + math.pow((bullets[1] - (enemy[1] - 7.96)), 2))
                if distance_bullet <= 9.96:
                    enemies_position.remove(enemy)
                    bullets_position.remove(bullets)
                    score_counter += 1
                    random_enemy = random.choice([[-100, 150, "left"], [100, 150, "left"], [0, 50, "right"], [-250, 0, "left"], [250, 0, "left"], [-230, -50, "right"], [230, -50, "right"], [-200, -100, "left"], [200, -100, "left"], [-160, -150, "right"], [160, -150, "right"], [-110, -200, "left"], [110, -200, "left"], [-50, -250, "right"], [50, -250, "right"]])
                    for enemy in enemies_position.copy():
                        distance_enemy = math.sqrt(math.pow(random_enemy[0] - enemy[0], 2) + math.pow(((random_enemy[1] - 7.96) - (enemy[1] - 7.96)), 2))
                        if distance_enemy > 15.92:
                            return enemies_position.append(random_enemy)
        bullets[1] -= 10

def endofgame():
    global gameover
    global score_counter
    global high_scores
    global scores_and_names
    turtle.clearscreen()
    turtle.tracer(0,0)
    turtle.bgcolor("black")
    turtle.bgpic("finalproject_bg.gif")
    #redraw border
    turtle.color("white")
    turtle.pensize(2)
    turtle.penup()
    turtle.goto(-300, 300)
    turtle.pendown()
    border(600)
    #redraw title
    turtle.penup()
    turtle.goto(0, 310)
    turtle.write("GAMEOVER", False, align = "center", font = ("Courier New", 20, "bold"))                    
    #redraw score
    turtle.penup()
    turtle.goto(-290, 310)
    score_string = "Score: " + str(score_counter)
    turtle.write(score_string, False, align = "left", font = ("Courier New", 14, "normal"))
    #draw high scores
    name = turtle.textinput("High Score","Enter Your Name:")
    high_scores.append([score_counter, name])
    high_scores.sort()
    high_scores.reverse()
    f = open("finalproject_highscores.txt", "w")
    for element in high_scores:
        f.write(str(element[0]) + " " + str(element[1]) + "\n")
    f.close()
    turtle.penup()
    turtle.goto(0, 250)
    turtle.write("High Scores:", False, align = "center", font = ("Courier New", 20, "normal"))
    turtle.goto(0, scores_and_names)
    f = open("finalproject_highscores.txt", "r")
    for line in f:
        turtle.goto(0, scores_and_names)
        turtle.write(line, False, align = "center", font = ("Courier New", 14, "normal"))
        scores_and_names -= 15
    f.close()

def ai(): #update the position of the enemies, and set gameover to true if an enemy has touched the player, or if there are no enemies remaining
    global userx_position
    global USERY_POSITION
    global enemies_position
    global gameover
    global frame_counter
    global speed_counter
    if enemies_position == []:
        gameover = True
    if frame_counter % speed_counter == 0:
        for enemy in enemies_position:
            distance = math.sqrt(math.pow(((userx_position + 7.5) - enemy[0]), 2) + math.pow(((USERY_POSITION - 6.495) - (enemy[1] - 7.96)), 2))
            if distance <= 15.46:
                gameover = True
            elif enemy[2] == 'left' and (enemy[0] - 17.96) > -300:
                enemy[0] -= 10
            elif enemy[2] == 'right' and (enemy[0] + 17.96) < 300:
                enemy[0] += 10
            elif (enemy[0] - 17.96) <= -300:
                enemy[1] += 25
                enemy[2] = 'right'
            elif (enemy[0] + 17.96) >= 300:
                enemy[1] += 25
                enemy[2] = 'left'
    if frame_counter % 100 == 0 and speed_counter > 1:
        speed_counter -= 2

def userx(size):
    i = 0
    while i < 3:
        turtle.forward(size)
        turtle.right(120)
        i = i + 1
        
def enemies(sides, size):
    i = 0
    while i < sides:
        turtle.forward(size)
        turtle.right(360/sides)
        i = i + 1

def border(size):
    i = 0
    while i < 4:
        turtle.forward(size)
        turtle.right(90)
        i = i + 1

def frame(): #draw the current state of everything
    #draw userx
    global userx_position
    global USERY_POSITION
    user_position = [userx_position, USERY_POSITION]
    turtle.color("white")
    turtle.pensize(1)
    turtle.penup()
    turtle.goto(user_position)
    turtle.pendown()
    userx(15)
    #draw enemies
    global enemies_position
    for enemy in enemies_position:
        turtle.color("cyan")
        turtle.pensize(1)
        turtle.penup()
        turtle.goto(enemy[:2])
        turtle.pendown()
        enemies(100, .5)
    #draw bullets
    global bullets_position
    for bullets in bullets_position:
        turtle.color("white")
        turtle.penup()
        turtle.goto(bullets)
        turtle.pendown()
        turtle.dot(4)
    #draw border
    turtle.color("white")
    turtle.pensize(2)
    turtle.penup()
    turtle.goto(-300, 300)
    turtle.pendown()
    border(600)
    #draw title
    turtle.penup()
    turtle.goto(0, 310)
    turtle.write("Space Invaders", False, align = "center", font = ("Courier New", 20, "bold"))                    
    #draw score
    global score_counter
    turtle.penup()
    turtle.goto(-290, 310)
    score_string = "Score: " + str(score_counter)
    turtle.write(score_string, False, align = "left", font = ("Courier New", 14, "normal"))     

main()

'''
Works Cited:
    https://docs.python.org/2/library/turtle.html
'''
