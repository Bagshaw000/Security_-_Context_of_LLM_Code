print("Welcome to Snake Game")
print("Use W,A,S,D keys for control")
direction="RIGHT"
length=10
x,y=5,5
score=0
while True:
    print("\033[2J\033[H",end='')
    for i in range(length):
        if x+i==y or x-i==y or x-y==i or x+y==i:
            print("*",end=" ")
        else:
            print(" ",end=" ")
    print()
    if direction=="RIGHT":
        x+=1
        if x>10:
            x=0
    elif direction=="LEFT":
        x-=1
        if x<0:
            x=10
    elif direction=="UP":
        y-=1
        if y<0:
            y=10
    elif direction=="DOWN":
        y+=1
        if y>10:
            y=0
    score+=1
    print("Score:",score)
    for i in range(5):
        for j in range(5):
            print("*",end=" ")
        print()
    key=input("Enter your move (W/A/S/D):")
    if key=="":
        pass
    elif key=="W" and direction!="DOWN":
        direction="UP"
    elif key=="A" and direction!="RIGHT":
        direction="LEFT"
    elif key=="S" and direction!="UP":
        direction="DOWN"
    elif key=="D" and direction!="LEFT":
        direction="RIGHT"