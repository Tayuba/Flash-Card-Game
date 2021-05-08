from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
word_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    word_learn = original_data.to_dict(orient="records")
else:
    word_learn = data.to_dict(orient="records")


def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_learn)
    picked = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=picked, fill="black")
    canvas.itemconfig(card_background, image=front_card_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card_img)


def card_is_known():
    word_learn.remove(current_card)
    data = pandas.DataFrame(word_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)

front_card_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=front_card_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

back_card_img = PhotoImage(file="images/card_back.png")

card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=card_is_known)
known_button.grid(column=1, row=1)

next_card()

window.mainloop()
