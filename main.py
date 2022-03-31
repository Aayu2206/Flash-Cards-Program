from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B6FFCE"

try:
    # Checks if the file of cards that are yet to learn exists,
    # Thus only showing those cards in the canvas.
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # Generating a dataframe from original data
    original_data = pandas.read_csv("data/french_words.csv")
    # Creating list of dictionaries from original data
    to_learn = original_data.to_dict(orient="records")
else:
    # Creating list of dictionaries from the words to learn file
    to_learn = data.to_dict(orient="records")

current_card = {}

def next_card():
    '''picks a random french word/translation and put the word into the flashcard.
    Everytime users presses (right/wrong) buttons.'''
    global current_card, flip_timer
    # Waits for the button to get pressed. does not starts the 3 sec timer in background
    window.after_cancel(flip_timer)
    # Picking random cards from list of dicts
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text = 'French',fill="black")
    canvas.itemconfig(card_word, text = current_card['French'],fill="black")
    canvas.itemconfig(card_background, image = card_front_img)

    flip_timer = window.after(3000,func= flip_card)

def flip_card():
    '''flips the card and shows the english translation'''
    canvas.itemconfig(card_title, text = 'English', fill= "white")
    canvas.itemconfig(card_word, text = current_card['English'], fill= "white")
    canvas.itemconfig(card_background, image = card_back_img)

def user_known():
    '''removes the cards that the user knows and creates a csv of cards that user does not know.'''
    to_learn.remove(current_card)
    # Creating new DataFrame for the words user does not know
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flash Cards")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
flip_timer = window.after(3000,func= flip_card)

canvas = Canvas(width=800,height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400,263, image = card_front_img)

card_title = canvas.create_text(400,150,text="Title", font=("Arial",40,"italic"))
card_word = canvas.create_text(400,263,text="word", font=("Arial",60,"bold"))

canvas.config(highlightthickness=0,bg=BACKGROUND_COLOR)
canvas.grid(column=0,row=0,columnspan=2)


# Cross Button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button1 = Button(image= cross_image,highlightthickness=0,bg=BACKGROUND_COLOR,command= next_card)
unknown_button1.grid(row=1,column=0)

# Check Button
tick_image = PhotoImage(file="images/right.png")
unknown_button2 = Button(image= tick_image,highlightthickness=0,bg=BACKGROUND_COLOR,command= user_known)
unknown_button2.grid(row=1,column=1)

# starts showing cards as the code starts running, not waiting for button press
next_card()

window.mainloop()