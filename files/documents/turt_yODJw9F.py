import turtle
tur = turtle.Turtle()
wn = turtle.Screen()
tur.speed(15)

for i in range(12):
    for color in ('red','magenta','blue','cyan','green','yellow'):
        tur.color(color)
        tur.circle(100)
        tur.left(20)
wn.exitonclick()
