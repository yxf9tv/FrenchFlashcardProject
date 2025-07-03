from tkinter import *
import pandas as pd
import random
import os

#-----------------Constants------------------#
BACKGROUND_COLOR = "#B1DDC6"
#-----------------Word Selection-------------#
data = pd.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient='records')
current_card = {}
#-----------------Score Tracking-------------#
known = 0
unknown = 0
total = 0
#----------Functions----------#
def update_score():
    canvas.itemconfig(score_text, text=f"Total: {total} | ✅ {known} | ❌ {unknown}")


def next_card():
    global current_card, known, unknown, total, flip
    total += 1
    current_card = random.choice(to_learn)

    canvas.itemconfig(canvas_bg, image=card_front)
    canvas.itemconfig(title, text="French", font=('italic', 20),fill='black')
    canvas.itemconfig(front_word, text=current_card["French"], font=('Arial',50), fill='black')

    update_score()
    flip = window.after(3000, flip_card)


def flip_card():

    canvas.itemconfig(canvas_bg, image=card_back)
    canvas.itemconfig(title, text="English", font=('italic',20), fill='white')
    canvas.itemconfig(front_word, text=current_card["English"], font=("Arial",50), fill='white')

def known_words():
    global known
    known += 1
    with open("study_results.txt", 'a') as results:
        results.write(f"Known: {current_card["French"]} = {current_card["English"]}\n")
    next_card()

def unknown_words():
    global unknown
    unknown += 1
    with open("study_results.txt", 'a') as results:
        results.write(f"Unknown: {current_card["French"]} = {current_card["English"]}\n")
    next_card()

#------------------UI--------------------#
window = Tk()
window.title("Language Flashcards")
window.config(bg="#B1DDC6", padx=50, pady=50)

canvas = Canvas(height=650,width=900, bg="#B1DDC6",borderwidth=0,highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_bg = canvas.create_image(450,300,image=card_front)
title = canvas.create_text(450, 150, text="",font=("Arial", 20, "italic"))

front_word = canvas.create_text(450, 275, text="", font=("Arial", 50, "bold"))
back_word = canvas.create_text(450, 275, text="", font=("Arial", 50, "bold"))

score_text = canvas.create_text(725, 75, text=f"Total: {total} | {known} | {unknown}", font=("Arial", 15))

canvas.grid(row=0,column=0,columnspan=2)

# create card_back after flip over function
correct = PhotoImage(file="images/right.png")
right_button = Button(image=correct, bg="#B1DDC6", highlightthickness=0, borderwidth=0, activebackground="#B1DDC6", command=known_words) #command=right_button)
right_button.grid(row=1, column=0)

incorrect = PhotoImage(file="images/wrong.png")
left_button = Button(image=incorrect, bg="#B1DDC6", highlightthickness=0, borderwidth=0, activebackground="#B1DDC6", command=unknown_words)
left_button.grid(row=1,column=1)

# Results tracking



session_number = 1

if os.path.exists("study_results.txt"):
    with open("study_results.txt", "r") as file:
        lines = file.readlines()
        session_number = sum(1 for line in lines if line.strip().startswith("Session")) + 1

with open("study_results.txt", 'w') as results:
   results.write(f"Session Number: {session_number}\n")


# Start session
next_card()
window.mainloop()