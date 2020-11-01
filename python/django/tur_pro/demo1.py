#!/usr/bin/env python
# coding=utf-8
# Author: 
# Mail: 
# Created Time: 2019年08月10日 星期六 17时15分06秒

from turtle import *
from random import random,randint


screen = Screen()

width,height = 800,600

screen.setup(width,height)

screen.title('3d星空')

screen.bgcolor('black')

screen.mode('logo')
screen.delay(0)


t = Turtle(visible=False,shape='circle')

t.pencolor('white')
t.fillcolor('white')
t.penup()
t.setheading(-90)
t.goto(width/2,randint(-height/2,height/2))
stars = []

for i in range(200):
    star = t.clone()
    s = random()/3
    star.shapesize(s,s)
    star.speed(int(s*10))
    star.setx(width/2+randint(1,width))
    star.sety(randint(-height/2,height/2))
    star.showturtle()
    stars.append(star)

while True:
    for star in stars:
        star.setx(star.xcor()-3*star.speed())
        if star.xcor() < -width/2:
            star.hideturtle()
            star.setx(width/2+randint(1,width))
            star.sety(randint(-height/2,height/2))
            star.showturtle()
