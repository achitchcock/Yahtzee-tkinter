from tkinter import *
import random
import os
from functools import partial

ONES = 'Ones'
TWOS = 'Twos'
THREES = 'Threes'
FOURS =  'Fours'
FIVES = 'Fives'
SIXES = 'Sixes'
THREE_OF_A_KIND = 'Three Of A Kind'
FOUR_OF_A_KIND = 'Four Of A Kind'
FULL_HOUSE = 'Full House'
SMALL_STRAIGHT = 'Small Straight'
LARGE_STRAIGHT = 'Large Straight'
YAHTZEE = 'Yahtzee'
CHANCE = 'Chance'

ANIM_CAP = 15

class App(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.animCount = 15
        self.buttonCount = 13
        self.dieImages = []
        self.dieRolls = []
        for i in range(1, 7):
            file_path = os.path.join(os.path.curdir, 'dice', '{}.gif'.format(i))
            self.dieImages.append(PhotoImage(file=file_path))

        self.canvas = Canvas(width=420, height=500, bg='green')
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(row=1, column=1, sticky='news')

        self.rollButton = Button(self.buttonFrame, text="Roll Dice", font=('Impact', 30),
                                 command=partial(self.rollDice, 50))
        self.rollButton.grid(row=0, column=0, rowspan=6, sticky='news')

        self.categories = [ONES, TWOS, THREES, FOURS, FIVES, SIXES, THREE_OF_A_KIND, FOUR_OF_A_KIND, FULL_HOUSE,
                           SMALL_STRAIGHT, LARGE_STRAIGHT, YAHTZEE,CHANCE]

        self.scores = {i: 0 for i in self.categories}

        self.gameButtons = {}
        mcol = 1
        mrow = 0
        for t in self.categories:
            self.gameButtons[t] = Button(self.buttonFrame, text=t, command=partial(self.button_click, t))
            self.gameButtons[t].grid(row=mrow, column=mcol, sticky='news')
            mcol += 1
            if mcol == 3:
                mcol = 1
                mrow += 1

        self.displaysFrame = Frame(self.master)
        self.displaysFrame.grid(row=0, column=2, rowspan=3)
        self.displays = {}

        r = 0
        for i in self.categories:
            t = Label(self.displaysFrame, text=i, font=('Impact', 20))
            c = Canvas(self.displaysFrame, height=60, width=320, bg='green')
            s = Label(self.displaysFrame, text='', font=('Impact', 20))
            t.grid(row=r, column=0, sticky='news')
            c.grid(row=r, column=1, sticky='news')
            s.grid(row=r, column=2, sticky='news')
            r += 1
            self.displays[i] = [t, c, s]

    def button_click(self, text):
        if not self.dieRolls:
            return
        self.buttonCount -= 1
        self.gameButtons[text].config(state=DISABLED)
        self.scores[text] = self.dieRolls
        self.dieRolls.sort()
        self.displayDice(self.displays[text][1], self.dieRolls, 30)
        self.dieRolls = []
        if self.buttonCount == 0:
            self.score_game()
            return
            # score game here
        else:
            self.canvas.delete("all")
            self.rollButton.config(state=NORMAL)

    def displayDice(self, canvas, dice, start):
        if len(dice) == 0:
            return
        x = 30
        for i in range(5):
            canvas.create_image((x, start), image=self.dieImages[dice[i] - 1])
            x += 53

    def displayDiceRoll(self, canvas, dice, start):
        if len(dice) == 0:
            return
        x = 30
        for i in range(5):
            canvas.create_image((x, start + random.randint(-10,10)), image=self.dieImages[dice[i] - 1])
            x += 50 + (ANIM_CAP - self.animCount) * 2

    def rollDice(self, start):
        if self.animCount == ANIM_CAP:
            self.rollButton.config(state=DISABLED)
        self.dieRolls = [random.randint(1, 6) for x in range(5)]
        if self.animCount == 0:

            self.canvas.delete("all")
            self.displayDiceRoll(self.canvas, self.dieRolls, start)
            self.animCount = ANIM_CAP
            return
        else:
            self.canvas.delete("all")
            self.displayDiceRoll(self.canvas, self.dieRolls, start)
            self.animCount -= 1
            self.master.after(60, self.rollDice, start + random.randint(10, 30))

    def score_game(self):
        total = 0
        # Single number scores
        total += self.scores[ONES].count(1)
        total += self.scores[TWOS].count(2) * 2
        total += self.scores[THREES].count(3) * 3
        total += self.scores[FOURS].count(4) * 4
        total += self.scores[FIVES].count(5) * 5
        total += self.scores[SIXES].count(6) * 6
        # Three of a kind
        for i in set(self.scores[THREE_OF_A_KIND]):
            if self.scores[THREE_OF_A_KIND].count(i) == 3:
                total += sum(self.scores[THREE_OF_A_KIND])
        # Four of a kind
        for i in set(self.scores[FOUR_OF_A_KIND]):
            if self.scores[FOUR_OF_A_KIND].count(i) == 4:
                total += sum(self.scores[FOUR_OF_A_KIND])
        # Full House
        two = False
        three = False
        for i in self.scores[FULL_HOUSE]:
            if self.scores[FULL_HOUSE].count(i) == 3:
                three = True
            if self.scores[FULL_HOUSE].count(i) == 2:
                two = True
        if two and three:
            total += 25
        # Small straight
        st = set(self.scores[SMALL_STRAIGHT])
        if set('1234').issubset(st) or set('2345').issubset(st) or set('3456').issubset(st):
            total += 30
        # Large Straight
        st = set(self.scores[LARGE_STRAIGHT])
        if set('12345').issubset(st) or set('23456').issubset(st):
            total += 40
        # Yahtzee
        if len(set(self.scores[YAHTZEE])) == 1:
            total += 50
        # Chance
        total += sum(self.scores[CHANCE])

        self.canvas.create_text(200, 50, text="Score: {}".format(total), font=('Impact', 50))


root = Tk()
myapp = App(root)
myapp.mainloop()
