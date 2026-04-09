import turtle
import time
import random


game_speed = 0.1
current_score = 0
highest_score = 0


window = turtle.Screen()
window.title("Classic 1997 Nokia Snake")
window.bgcolor("darkseagreen") 
window.setup(width=600, height=600)
window.tracer(0) 


head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup() 
head.goto(0, 0)
head.direction = "stop"


food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("black")
food.penup()
food.goto(0, 100)


tail_segments = []


pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 20, "bold"))


def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")


while True:
    window.update()

    
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1) 
        head.goto(0, 0)
        head.direction = "stop"

        
        for segment in tail_segments:
            segment.goto(1000, 1000)
        tail_segments.clear()

        
        current_score = 0
        game_speed = 0.1
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(current_score, highest_score), align="center", font=("Courier", 20, "bold"))

    
    if head.distance(food) < 20:
        
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)

        
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("black")
        new_segment.penup()
        tail_segments.append(new_segment)

        
        game_speed -= 0.001
        current_score += 10

        if current_score > highest_score:
            highest_score = current_score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(current_score, highest_score), align="center", font=("Courier", 20, "bold"))

    
    for index in range(len(tail_segments) - 1, 0, -1):
        x = tail_segments[index-1].xcor()
        y = tail_segments[index-1].ycor()
        tail_segments[index].goto(x, y)

    
    if len(tail_segments) > 0:
        x = head.xcor()
        y = head.ycor()
        tail_segments[0].goto(x, y)

    move()

    
    for segment in tail_segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            
            for segment in tail_segments:
                segment.goto(1000, 1000)
            tail_segments.clear()
            
            current_score = 0
            game_speed = 0.1
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(current_score, highest_score), align="center", font=("Courier", 20, "bold"))

    time.sleep(game_speed)

window.mainloop()