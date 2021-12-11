import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import decision

# Configure application
app = Flask(__name__)

# Paul 1208 - Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Paul 1208 - Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# import database
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

    # Paul 1208 - POST
    if request.method == "POST":

        #save card inputs in variables
        dealer = request.form.get("card_input_dealer")
        card1 = request.form.get("card_input1")
        card2 = request.form.get("card_input2")

        # if two cards are the same
        if card1 == card2:

            # execute search in split table
            result = db.execute("SELECT * FROM split_das WHERE LeftCard = ? AND DealerCard = ?", card1, dealer)
            if result[0]["Decision"] == 'Y':
                return decision("split")
            elif result[0]["Decision"] == 'N':
                # the decision will be not split, but need to further check what to do next
                # set two texts become integers first and add sum up them
                total = int(card1) + int(card2)
                # turn the result back to text format in order to search it from SQL
                total_text = str(total)
                # if the total is larger than 17, which I forgot to put these scenarios in SQL
                if total > 17:
                    # show result page with do not split, but stand
                    return decision("do not split, but stand")
                else:
                    # execute search for what the user should do
                    result = db.execute("SELECT * FROM hard WHERE Symbol = ? AND DealerCard = ?", total_text, dealer)
                    # if result is hit
                    if result[0]["Decision"] == 'H':
                        # show result page with do not split, but hit
                        return decision("do not split, but hit")
                    # if result is stand
                    elif result[0]["Decision"] == 'S':
                        # # show result page with do not split, but stand
                        return decision("do not split, but stand")
                    # if result is double/hit
                    elif result[0]["Decision"] == 'D':
                        # show result page with do not split, but double
                        return decision("do not split, but double")
                    # if others
                    else:
                        # show result page with cannot defined
                        return decision("cannot defined (hard)")
            else:
                return decision("cannot defined (split)")

        # if one card is an A
        elif card1 == 'A' or card2 == 'A':
            #execute search in soft table
            result = db.execute("SELECT * FROM soft WHERE LeftCard = ? AND RightCard = ? AND DealerCard = ?", card1, card2, dealer)

            if result[0]["Decision"] == 'S':
                return decision("stand")
            elif result[0]["Decision"] == 'Ds':
                return decision("double if allowed, otherwise stand")
            elif result[0]["Decision"] == 'H':
                return decision("hit")
            elif result[0]["Decision"] == 'D':
                return decision("double if allowed, otherwise hit")
            else:
                return decision("cannot defined (soft)")

        # else
        else:
            # set two texts become integers first and add sum up them
            total = int(card1) + int(card2)
            # turn the result back to text format in order to search it from SQL
            total_text = str(total)
            # if the total is larger than 17, which I forgot to put these scenarios in SQL
            if total > 17:
                # show result page with stand
                return decision("stand")
            else:
                # execute search for what the user should do
                result = db.execute("SELECT * FROM hard WHERE Symbol = ? AND DealerCard = ?", total_text, dealer)
                # if result is hit
                if result[0]["Decision"] == 'H':
                    return decision("hit")
                # if result is stand
                elif result[0]["Decision"] == 'S':
                    # show result page with stand
                    return decision("stand")
                # if result is double/hit
                elif result[0]["Decision"] == 'D':
                    # show result page with double
                    return decision("double")
                # if others
                else:
                    # show result page with cannot defined
                    return decision("cannot defined (hard)")