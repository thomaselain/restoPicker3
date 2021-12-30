import tkinter as tk
import json
import pprint
import requests
import sys
import random


WIN_H = 600
WIN_W = 900

def printResults():
    if curlResults is not None:
        pprint.pprint(curlResults.text)

############# curl Queries #############
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

        print("------ "+ingredient+"-------")

        curlResults = requests.get(
        'https://www.themealdb.com/api/json/v1/1/filter.php?i='
        + ingredient)

        if curlResults is not None:
            return curlResults.json()
        else:
            bestIngredients.pop(ingredient)

    return None
########################################




def updateLikes(a, b):
    data['Likes'][a] = b

#############################################
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(str(WIN_W) + 'x' + str(WIN_H))
        self.likes = dict()
        self.creer_widgets()
        self.rowconfigure(1, {'minsize': 30, 'bg': '#000'})


    def creer_widgets(self):
        self.minScore = tk.Scale(self, label='Minimum score', fg='#00f', activebackground='#aaa', from_=0, to=10, orient='horizontal')
        self.minScore.grid(row=0, column=0, columnspan=3, sticky='e')

        self.close = tk.Button(self, text="Close", command=self.quit)
        self.close.grid(row=0, column=5)
        self.search = tk.Button(self, text="Search", command=getRandomMealFromIngredient(self.minScore.get()))
        self.search.grid(row=0, column=6)
        
        likesRow = 2
        likesCol = 0
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
            print(self.likes[i].winfo_rooty())
            if likesRow > 6:
                likesCol = likesCol + 1
                likesRow = 2
            else:
                likesRow = likesRow + 1
#############################################



def main():
    global data

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
