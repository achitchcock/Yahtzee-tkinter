from tkinter import *
import random
import os
from functools import partial

class App(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.animCount = 15
        self.buttonCount = 13
        self.dieImages = []
        self.dieRolls = [0,0,0,0,0]
        for i in range(1,7):
            file_path = os.path.join(os.path.curdir, 'dice', '{}.gif'.format(i))
            self.dieImages.append(PhotoImage(file=file_path))

        self.canvas = Canvas(width=420,height=500,bg='green')
        self.canvas.grid(row=0,column=0,columnspan=2)

        self.buttonFrame = Frame(self.master,bg='red')
        self.buttonFrame.grid(row=1,column=1,sticky='news')

        self.rollButton = Button(self.buttonFrame,text="Roll Dice",font=('Impact',30),command=partial(self.rollDice,50))
        self.rollButton.grid(row=0, column=0,rowspan=5,sticky='news')

        self.categories = ['Ones','Twos','Threes','Fours','Fives','Sixes','Three Of A Kind','Four Of A Kind',
                           'Full House','Small Straight','Large Straight','Yahtzee','Chance']

        self.scores = {i:0 for i in self.categories}

        self.gameButtons = {}
        mcol = 1
        mrow = 0
        for t in self.categories:
            self.gameButtons[t] = Button(self.buttonFrame,text=t,command=partial(self.buttonClick, t))
            self.gameButtons[t].grid(row=mrow,column=mcol,sticky='news')
            mcol += 1
            if mcol==4:
                mcol=1
                mrow+=1


        self.displaysFrame = Frame(self.master)
        self.displaysFrame.grid(row=0,column=2,rowspan=3)
        self.displays = {}

        r = 0
        for i in self.categories:
            t = Label(self.displaysFrame,text=i,font=('Impact',20))
            c = Canvas(self.displaysFrame, height=60,width=320,bg='green')
            s = Label(self.displaysFrame,text='',font=('Impact',20))
            t.grid(row=r,column=0,sticky='news')
            c.grid(row=r,column=1,sticky='news')
            s.grid(row=r,column=2,sticky='news')
            r+=1
            self.displays[i] = [t,c,s]
                   
    def buttonClick(self, text):
        print(text)
        self.buttonCount -=1
        print(self.buttonCount)
        self.gameButtons[text].config(state=DISABLED)
        self.scores[text] = self.dieRolls
        self.dieRolls.sort()
        self.displayDice(self.displays[text][1],self.dieRolls,30)
        if self.buttonCount == 0:
            self.scoreGame()
            return
            #score game here
        else:
            self.rollButton.config(state=NORMAL)
            

    def displayDice(self, canvas, dice, start):
        if len(dice) == 0:
            return
        x = 30
        for i in range(5):
            canvas.create_image((x,start),image = self.dieImages[dice[i]-1])
            x += 50 + (15-self.animCount)*2
            


    def rollDice(self,start):
        if self.animCount == 15:
            self.rollButton.config(state=DISABLED)
        if self.animCount == 0:
            self.animCount = 15
            return
        self.dieRolls = [random.randint(1,6) for x in range(5)]
        #print(d)
        if self.animCount == 0:
            self.animCount = 15
            return
        else:
            self.canvas.delete("all")
            self.displayDice(self.canvas,self.dieRolls,start)
            self.animCount -= 1
            self.master.after(120,self.rollDice,start + random.randint(10,30))


    def scoreGame(self):
        total = 0
        # Single number scores
        total += self.scores['Ones'].count(1)
        total += self.scores['Twos'].count(2)*2
        total += self.scores['Threes'].count(3)*3
        total += self.scores['Fours'].count(4)*4
        total += self.scores['Fives'].count(5)*5
        total += self.scores['Sixes'].count(6)*6
        # Three of a kind
        for i in set(self.scores['Three of a kind']):
            if self.scores['Three of a kind'].count(i) == 3:
                total += sum(self.scores['Three of a kind'])
        # Four of a kind
        for i in set(self.scores['Four of a kind']):
            if self.scores['Four of a kind'].count(i) == 4:
                total += sum(self.scores['Four of a kind'])
        # Full House
        two = False
        three = False
        for i in self.scores['Full house']:
            if self.scores['Full house'].count(i) == 3:
                three = True
            if self.scores['Full house'].count(i) == 2:
                two = True
        if two and three:
            total += 25
        # Small straight
        st = set(self.scores['small straight'])
        if set('1234').issubset(st) or set('2345').issubset(st) or set('3456').issubset(st):
            total += 30
        # Large Straight
        st = set(self.scores['Large Straight'])
        if set('1234').issubset(st) or set('2345').issubset(st) or set('3456').issubset(st):
            total += 40
        # Yahtzee
        if len(set(self.scores['Yahtzee'])) == 1:
            total += 50
        # Chance
        total += sum(self.scores['Chance'])
        

        self.canvas.create_text(200,50,text="Score: {}".format(total),font=('Impact',50))
            


root = Tk()
myapp = App(root)
myapp.mainloop()