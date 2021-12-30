import tkinter as tk
import json
import pprint
import requests
import sys
import random

# Global variables for GUI's dimentions
WIN_H = 600
WIN_W = 900

# print curl result in console
def printResults():
    if curlResults is not None:
        pprint.pprint(curlResults.text)

# Get a random meal from themealdb.com api
# the meal's main ingredient must have a better note than the argument in order to be picked
def getRandomMealFromIngredient(score):
    bestIngredients = dict();
    print('min score :')
    print(score)

    # select all the ingredients with a good enough score
    for i in data["Likes"]:
        if float(data["Likes"][i]) > score:
            bestIngredients[i] = data["Likes"][i]
    pprint.pprint(bestIngredients)

    # get a random meal with this ingredient
    while len(bestIngredients) > 0:
        ingredient = random.choice(list(bestIngredients))
        curlResults = requests.get(
        'https://www.themealdb.com/api/json/v1/1/filter.php?i='
        + ingredient)

        if curlResults is not None:
            return curlResults.json()
        else:
            bestIngredients.pop(ingredient)

# Needs to be moved in Application or (TODO)replaced by lambda function somehow
def updateLikes(a, b):
    data['Likes'][a] = b

# Only use the Application class for the GUI methods
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(str(WIN_W) + 'x' + str(WIN_H))
        self.likes = dict()
        self.create_widgets()
        self.rowconfigure(1, {'minsize': 30})


    def create_widgets(self):
        # Score slider
        # (used to choose how good the ingredients must be in order to be selected by getRandomMealFromIngredient)
        self.minScore = tk.Scale(self, label='Minimum score', fg='#00f', activebackground='#aaa', from_=0, to=10, orient='horizontal')
        self.minScore.grid(row=0, column=0, columnspan=3, sticky='e')

        # Close button
        self.close = tk.Button(self, text="Close", command=self.quit)
        self.close.grid(row=0, column=5)

        # Search button
        self.search = tk.Button(self, text="Search", command=getRandomMealFromIngredient(self.minScore.get()))
        self.search.grid(row=0, column=6)
        
        likesRow = 2
        likesCol = 0
        #retrieve data from user/preferences.json and store it in Application.Scale objects
        for i in data['Likes']:
            self.likes[i] = tk.Scale(
                self,
                label=i,
                command=lambda value, name=i: updateLikes(name, value),
                from_=0,
                to=10,
                resolution=0.1,
                orient='horizontal'
               )
            self.likes[i].set(data['Likes'][i])
            self.likes[i].grid(row=likesRow, column=likesCol)

            #Make a grid with all ingredients (could be better)
            if likesRow > 6:
                likesCol = likesCol + 1
                likesRow = 2
            else:
                likesRow = likesRow + 1
#############################################



def main():
    global data

    # TODO
    # Add a prompt to ask the user's name 
    # then use this name as
    # userData/name/likes.json
    # userData/name/preferences.json
    data_json = open('data.json')
    data = json.load(data_json)
    data_json.close()

    pprint.pprint(data)

    app = Application()
    app.title("RestoPicker 3.0")
    app.mainloop()

if __name__ == '__main__':
    main()
