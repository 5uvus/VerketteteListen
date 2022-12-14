import random
import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from matplotlib import pyplot as plt
import requests
import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *



con = sqlite3.connect(
    "C:/Users/Hp/OneDrive - HTL Anichstrasse (1)/HTL Anichstraße/SWP_RUB/SchereSteinPapier/rockpaperscissorsspocklizard.sqlite3")

moves = ['rock', 'paper', 'scissors', 'spock', 'lizard']
getResult = {'rock': {"rock": "Draw", "paper": "Lose", "scissors": "Win", "spock": 'Lose', "lizard": "Win"},
                     'paper': {"paper": "Draw", "scissors": "Lose", "rock": "Win", "spock": "Win", "lizard": "Lose"},
                     'scissors': {"scissors": "Draw", "rock": "Lose", "paper": "Win", "spock": "Lose", "lizard": "Win"},
                     'spock': {"scissors": "Win", "rock": "Win", "paper": "Lose", "spock": "Draw", "lizard": "Lose"},
                     'lizard': {"scissors": "Lose", "rock": "Lose", "paper": "Win", "spock": "Win", "lizard": "Draw"}}
        
def saveToDB(name, player, enemy, result):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS spiele(name, player_chose, enemy_chose, result)")

    cur.execute("INSERT INTO spiele VALUES (?,?,?,?)", (name, player, enemy, result))
    con.commit()


def hardMode(name, player):
     print("hello")
     comp_choice = ""
     cur = con.cursor()
     
     stats = getStatistics(name, False, "player")
     
     v = list(stats.values())
     k = list(stats.keys())
     highest =  k[v.index(max(v))]
     
     winning_symboles = []
     for m in moves:
         if getResult[player][m] == "Lose":
             winning_symboles.append(m)
     
     comp_choice = random.choice(winning_symboles)
     return comp_choice
     
     
def uploadStatistics(name):
    cur = con.cursor()
    cur.execute('SELECT * FROM spiele')
    host = 'http://localhost:5000/upload'
    
    stats = getStatistics(name, False, "player")
    for key in stats:
        symboleCnt = stats[key]
        response = requests.put('%s/%s/%s' % (host, name, key), data={'name' : name, 'symbole' : key , 'cnt' : symboleCnt})
        print(response)
    
def getStatistics(name, printit, whichone):
    cur = con.cursor()
    player_win = 0
    comp_win = 0
    draw = 0
    query = """SELECT result FROM spiele where name = ?"""
    cur.execute(query, (name,))
    for row in cur.fetchall():
        if row[0] == 'Win':
            player_win += 1
        elif row[0] == 'Lose':
            comp_win += 1
        else:
            draw += 1

    player_stats = {"rock": 0, "paper": 0, "scissors": 0, "spock": 0, "lizard": 0}
    computer_stats = {"rock": 0, "paper": 0, "scissors": 0, "spock": 0, "lizard": 0}
    
    query = """SELECT player_chose, enemy_chose FROM spiele where name = ? """

    cur.execute(query, (name,))
    for row in cur.fetchall():
        if row[0] == "rock":
            player_stats["rock"] += 1
        if row[0] == "paper":
            player_stats["paper"] += 1
        if row[0] == "scissors":
            player_stats["scissors"] += 1
        if row[0] == "spock":
            player_stats["spock"] += 1
        if row[0] == "lizard":
            player_stats["lizard"] += 1
        if row[1] == "rock":
            computer_stats["rock"] += 1
        if row[1] == "paper":
            computer_stats["paper"] += 1
        if row[1] == "scissors":
            computer_stats["scissors"] += 1
        if row[1] == "spock":
            computer_stats["spock"] += 1
        if row[1] == "lizard":
            computer_stats["lizard"] += 1

    if(printit):
        print("\nPlayer has won " + str(player_win) + " times")
        print("Computer has won " + str(comp_win) + " times")
        print("There have been " + str(draw) + " draws")

        print("\nPlayer statistics: ")
        print(player_stats)

        print("\nComputer statistics: ")
        print(computer_stats)
    
    if whichone == "player":
        return player_stats
    else:
        return computer_stats

def leaderboard():
    cur = con.cursor()
    
    query = "select count(*), name from spiele where result = 'Win' group by name"
    
    players = []
    cur.execute(query)
    for row in cur.fetchall():
        players.append(row)

    players.sort(reverse = True)
    query = "select name from spiele group by name"
    cur.execute(query)
    
    
   # hinzufügen der Spieler die nie gewonnen haben
    
    players_str = ""
    for p in players:
        players_str = players_str + p[1] 
    
    for row in cur.fetchall():
        if row[0] not in players_str:
            players.append((0, row[0]))
    
   
    print(players)
    return players
    
def displayStats(name, printit):
    cur = con.cursor()
    statsPlayer = getStatistics(name, False, "player")
    
    vP = list(statsPlayer.values())
    kP = list(statsPlayer.keys())
    
    symbolePropsPlayer = []
    sumUpPlayer = sum(vP)
    for val in vP:
        symbolePropsPlayer.append(val / sumUpPlayer)
    
    statsComputer = getStatistics(name, False, "computer")
    
    vC = list(statsComputer.values())
    kC = list(statsComputer.keys())
    
    symbolePropsComputer = []
    sumUpComputer = sum(vC)
    for val in vC:
        symbolePropsComputer.append(val / sumUpComputer)
        
    player_win = 0
    comp_win = 0
    draw = 0
    
    query = """SELECT result FROM spiele where name = ?"""
    cur.execute(query, (name,))
    for row in cur.fetchall():
        if row[0] == 'Win':
            player_win += 1
        elif row[0] == 'Lose':
            comp_win += 1
        else:
            draw += 1
    
    query = """SELECT COUNT(*) FROM spiele where name = ?"""
    cur.execute(query, (name,))
    rows = cur.fetchone()
    
    #print(rows)
    win_propability = player_win / rows[0]
    lose_propability = comp_win / rows[0]
    draw_propability = draw / rows[0]
    
    c = ['red', 'yellow', 'black', 'blue', 'orange']
    
    fig, axs = plt.subplots(2,2)
    fig.suptitle('Statistics Monitoring for Player: ' + name)
    axs[0,0].bar(kP,symbolePropsPlayer, align="center", color = random.shuffle(c))
    for i in range(len(kP)):
        axs[0,0].text(i,symbolePropsPlayer[i],round(symbolePropsPlayer[i],2))
    axs[0,0].set_title("Player probabilites:")
    axs[1,0].bar(kC,symbolePropsComputer, align="center", color = random.shuffle(c))
    for i in range(len(kC)):
        axs[1,0].text(i,symbolePropsComputer[i],round(symbolePropsComputer[i],2))
    axs[1,0].set_title("Computer probabilities:")
    
    allPlayersStats = leaderboard()
    player_names = []
    player_wins = []
    
    for p in allPlayersStats:
        player_names.append(p[1])
        player_wins.append(p[0])
    axs[1,1].bar(player_names, player_wins, align ="center",color = random.shuffle(c))
    axs[1,1].set_title("Leaderboard:")
    axs[1,1].set_xlabel("Player Names")
    axs[1,1].set_ylabel("Wins")
    for i in range(len(player_names)):
        axs[1,1].text(i,player_wins[i],round(player_wins[i],2))
    
    circle_values = np.array([win_propability, lose_propability, draw_propability])
    label = ["Win", "Lose", "Draw"]
    axs[0,1].pie(circle_values, labels = label, autopct='%1.2f%%')
    axs[0,1].legend( loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
    
    
    axs[0,1].set_title("Win/Lose Ratio:")
    plt.tight_layout()
    
    plt.show()


def start():
    print("hello")
    newWindow = Toplevel(master)

    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
    Label(newWindow,
          text ="This is a new window").pack()
def realGame():
    # root window
    root = tk.Tk()
    root.geometry('300x200')
    root.resizable(False, False)
    root.title('Button Demo')
    
    # exit button
    play_button = ttk.Button(
    root,
    text='Play the Game',
    command=start 
    )
    play_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
    )
    root.mainloop()

def cmdGame():
    leaderboard()
    playing = True
    while playing:
        enemy = ""
        print("-------------Rock Paper Scissors Spock Lizard-------------")
        name = input("Please enter your name: ")
        chose = input("Wanna play/view statistics/upload? p/s/u?")
        if chose == "p":
            basic_mode = input("Do you want to play by yourself or wanna let 2 bots play against each other? y/b")
            if basic_mode == "y":
                player = input("Please enter your symbol: ")
                mode = input("Normal mode or hard mode? n/h")
                
                if mode == "n":
                    enemy = random.choice(moves)
                elif mode =="h":
                    enemy = hardMode(name, player)
            
                if player in moves:
                    print("You chose: \t" + player)
                    print("Enemy chose: \t" + enemy)
                    print("Result: \t" + getResult[player][enemy])
                    saveToDB(name, player, enemy, getResult[player][enemy])
                
                    again = input("Wanna play again? y/n")
                    if again == "n": 
                        print("Bye!")
                        playing = False
                        con.close()
                    else:
                        playing = True
                else:
                    print("Wrong input! ")
            elif basic_mode == "b":
                bot1 = random.choice(moves)
                bot2 = random.choice(moves)
                print("Bot 1 chose: \t" + bot1)
                print("Bot 2 chose: \t" + bot2)
                if getResult[bot1][bot2] == "Win":
                    print("Bot 1 has won the game!")
                elif getResult[bot1][bot2] == "Lose":
                    print("Bot 2 has won the game!")
                elif getResult[bot1][bot2] == "Draw":
                    print("There has been a draw!")
        elif chose =="s":
            getPrint = input("Do you want to view the statistics as a Graphic? y/n")
            if getPrint == "n":
                getStatistics(name, True)
            elif getPrint =="y":
                displayStats(name, False)
        elif chose == "u":
             uploadStatistics(name)



if __name__ == '__main__':
    cmdGame()
