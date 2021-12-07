import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

#import database
db = SQL("sqlite:///blackjack_table.db")

# routing the buttons to different webpages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/das_incl_intro")
def das_incl_intro():
    return render_template("das_incl_intro.html")

@app.route("/das_excl_intro")
def das_excl_intro():
    return render_template("das_excl_intro.html")

@app.route("/das_incl_main_text")
def das_incl_main_text():
    return render_template("das_incl_main_text.html")

@app.route("/das_excl_main")
def das_excl_main():
    return render_template("das_excl_main.html")

# Michelle @ Paul: I don't know where DAS vs NON-DAS fits into this part

# execute database search for DAS included
@app.route("/das_incl_submit", methods=["GET", "POST"])
def das_incl_submit():
    #save card inputs in variables
    dealer = request.form.get("card_input_dealer")
    card1 = request.form.get("card_input1")
    card2 = request.form.get("card_input2")
    total = card1 + card2

    # if two cards are the both As
    if card1 == 'A' and card2 == 'A':
        # result = stand
        return render_template("/das_incl_main_text.html", result='stand')

    # if one card is an A
        #execute search in soft table
    # else
    else:
        # execute search in hard table

        # execute search for what the user should do
        result = db.execute("SELECT ? FROM hard WHERE symbol = ?", dealer, total)
        # if result is hit
        # redirect to another site with extra input box
        # if result is stand 
        if result=='S':
            #show result page with stand
            return render_template("/das_incl_main_text.html", result='stand')
        # if result is double/stand
            # 
        # if result is double/hit
            #

