from turtle import *
from random import randint
import pygame
import time

pygame.init()
sfx_paddle = pygame.mixer.Sound("audio/paddle.mp3")
sfx_block = pygame.mixer.Sound("audio/block.mp3")
sfx_win = pygame.mixer.Sound("audio/win.mp3")
sfx_win_life = pygame.mixer.Sound("audio/win_life.mp3")
sfx_lose = pygame.mixer.Sound("audio/lose.mp3")
sfx_lose_life = pygame.mixer.Sound("audio/lose_life.mp3")
sfx_bg = pygame.mixer.Sound("audio/bg.mp3")
sfx_bg.set_volume(0.35)


class Breakout:
    def __init__(self):
        sfx_bg.play()
        self.score = 0
        self.remain_lives = 3
        self.direction_x = 0.5
        self.direction_y = 0.5
        self.image = "img/heart.gif"

        self.paddle = Turtle("square")
        self.paddle.color("white")
        self.paddle.penup()
        self.paddle.teleport(x=0, y=-200)
        self.paddle.shapesize(1, 6)

        self.ball = Turtle("circle")
        self.ball.color("#f5fcff")
        self.ball.teleport(x=0, y=-160)
        self.ball.penup()
        self.block_list = []

        self.screen = Screen()
        self.screen.title("Breakout")
        self.screen.setup(width=800, height=600)
        self.screen.bgcolor("#0c161c")
        self.screen.tracer(0)

        self.screen.onkeypress(lambda: self.move_paddle("left"), "Left")
        self.screen.onkeypress(lambda: self.move_paddle("right"), "Right")
        self.screen.listen()

        self.scoreboard = Turtle()
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(-380, 250)
        self.scoreboard.color("white")
        self.scoreboard.write(f"Score: {self.score}", font=("Arial", 28, "normal"))

        self.lives = Turtle()
        self.lives.penup()
        self.lives.hideturtle()
        self.lives.goto(250, 250)
        self.lives.color("white")
        self.lives.write(f"Lives: {self.remain_lives}", font=("Arial", 28, "normal"))

    def move_paddle(self, side: str):
        if self.paddle.pos()[0] > -340 and side == "left":
            self.paddle.bk(20)
        if self.paddle.pos()[0] < 340 and side == "right":
            self.paddle.fd(20)

    def move_ball(self):
        new_x = self.ball.xcor() + self.direction_x
        new_y = self.ball.ycor() + self.direction_y
        self.ball.goto(new_x, new_y)

    def create_blocks(self):
        colormode(255)
        y = 0
        for list_blocks in range(4):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            rgb = r, g, b
            x = 320
            indeed_list = []
            for block in range(6):
                block = Turtle("square")
                block.color(rgb)
                block.penup()
                block.teleport(x=x, y=-y)
                block.shapesize(1.5, 5)
                x -= 130
                indeed_list.append(block)
            self.block_list.append(indeed_list)
            y -= 65

    def collision_blocks(self):
        for line in self.block_list:
            for block in line:
                if self.ball.distance(block) < 65:
                    if -30 <= self.ball.ycor() <= -10 or 30 <= self.ball.ycor() <= 50 or 90 <= self.ball.ycor() <= 110 or 170 <= self.ball.ycor() <= 190:
                        block_color = block.color()
                        self.ball.color((int(block_color[0][0]), int(block_color[0][1]), int(block_color[0][2])),
                                        (int(block_color[1][0]), int(block_color[1][1]), int(block_color[1][2])))
                        block.hideturtle()
                        line.remove(block)
                        self.score += 10
                        self.scoreboard.clear()
                        self.scoreboard.write(f"Score: {self.score}", font=("Arial", 28, "normal"))
                        if self.score == 200:
                            self.remain_lives += 1
                            self.lives.clear()
                            self.lives.write(f"Lives: {self.remain_lives}", font=("Arial", 28, "normal"))
                            sfx_win_life.play()

                        if len(line) == 0:
                            self.block_list.remove(line)

                        sfx_block.play()
                        return True

    def default(self):
        self.paddle.goto(0, -200)
        self.ball.goto(0, -180)
        self.direction_x *= -1
        self.direction_y *= -1

    def reset_game(self):
        self.lives.clear()
        self.lives.write(f"Lives: {self.remain_lives}", font=("Arial", 28, "normal"))
        self.default()

    def game_over(self):
        for line in self.block_list:
            for block in line:
                block.hideturtle()
        you_lose = Turtle()
        you_lose.penup()
        you_lose.hideturtle()
        you_lose.goto(-175, 0)
        you_lose.color("white")
        you_lose.write(f"Game Over", font=("Arial", 48, "normal"))
        sfx_lose.play()

    def win(self):
        you_win = Turtle()
        you_win.penup()
        you_win.hideturtle()
        you_win.goto(-135, 0)
        you_win.color("white")
        you_win.write(f"You Win", font=("Arial", 48, "normal"))
        sfx_win.play()

    def run(self):
        game_over = False
        self.create_blocks()

        while not game_over:
            if self.collision_blocks():
                self.direction_y *= -1
            if self.ball.xcor() == -385 or self.ball.xcor() == 385:
                self.direction_x *= -1
            if self.ball.ycor() == -180 and self.ball.distance(self.paddle) < 70:
                self.direction_y *= -1
                left_side_paddle = self.paddle.xcor() - 60

                if self.paddle.xcor() > self.ball.xcor() >= left_side_paddle:
                    self.direction_x = abs(self.direction_x) * -1
                else:
                    self.direction_x = abs(self.direction_x)

                ball_color = self.ball.color()
                self.paddle.color((int(ball_color[0][0]), int(ball_color[0][1]), int(ball_color[0][2])),
                                  (int(ball_color[1][0]), int(ball_color[1][1]), int(ball_color[1][2])))

                sfx_paddle.play()

            if self.ball.ycor() == 290:
                self.direction_y *= -1

            if self.ball.ycor() == -290:
                self.remain_lives -= 1
                if self.remain_lives > 0:
                    self.reset_game()
                else:
                    self.reset_game()
                    self.game_over()
                    game_over = True
                sfx_lose_life.play()

            if len(self.block_list) == 0:
                self.win()
                game_over = True
            self.move_ball()
            self.screen.update()

        self.screen.exitonclick()


game = Breakout()
game.run()
