from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TOPIC1 = "French"
TOPIC2 = "English"
TOPIC_FILE = "data/french_words.csv"
to_learn = {}
current_card = {}

# Checks if words_to_learn.csv exists
try:
    data = pandas.read_csv("data/words_to_learn.csv")
# If not, the original data list is used
except FileNotFoundError:
    original_data = pandas.read_csv(TOPIC_FILE)
    to_learn = original_data.to_dict(orient="records")
# If words_to_learn.csv exists, it'll use that as the word bank
else:
    to_learn = data.to_dict(orient="records")


# ------------------------------ NEW WORD ---------------------------------------------------------------
def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    topic1_word = current_card[TOPIC1]
    canvas.itemconfig(card_title, text=TOPIC1, fill="black")
    canvas.itemconfig(card_word, text=topic1_word, fill="black")
    canvas.itemconfig(game_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


# ------------------------------ Flip Card ---------------------------------------------------------
def flip_card():
    canvas.itemconfig(card_title, text=TOPIC2, fill="white")
    topic2_word = current_card[TOPIC2]
    canvas.itemconfig(card_word, text=topic2_word, fill="white")
    canvas.itemconfig(game_image, image=card_back)


# ------------------------------ Flip Card ---------------------------------------------------------
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_word()


# ------------------------------ USER INTERFACE ---------------------------------------------------------
window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Create background flashcard
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
game_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Wrong button with art
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)

# Right button with art
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

new_word()

window.mainloop()
