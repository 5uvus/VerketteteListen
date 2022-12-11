import random
import sqlite3

con = sqlite3.connect(
    "C:/Users/Hp/OneDrive - HTL Anichstrasse (1)/HTL Anichstraße/SWP_RUB/SchereSteinPapier/rockpaperscissorsspocklizard.sqlite3")


def saveToDB(player, enemy, result):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS spiele(player_chose, enemy_chose, result)")

    cur.execute("INSERT INTO spiele VALUES (?,?,?)", (player, enemy, result))
    con.commit()
    con.close()


def getStatistics():
    cur = con.cursor()
    player_win = 0
    comp_win = 0
    draw = 0
    cur.execute('SELECT result FROM spiele')
    for row in cur.fetchall():
        if row[0] == 'Win':
            player_win += 1
        elif row[0] == 'Lose':
            comp_win += 1
        else:
            draw += 1

    player_stats = {"rock": 0, "paper": 0, "scissors": 0, "spock": 0, "lizard": 0}
    computer_stats = {"rock": 0, "paper": 0, "scissors": 0, "spock": 0, "lizard": 0}
    cur.execute('SELECT player_chose, enemy_chose FROM spiele')
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

    print("Player has won " + str(player_win) + " times")
    print("Computer has won " + str(comp_win) + " times")
    print("There have been " + str(draw) + " draws")

    print("\nPlayer statistics: ")
    print(player_stats)

    print("\nComputer statistics: ")
    print(computer_stats)


# do_stuff_with_row
def cmdGame():
    playing = True
    while playing:
        moves = ['rock', 'paper', 'scissors', 'spock', 'lizard']
        getResult = {'rock': {"rock": "Draw", "paper": "Lose", "scissors": "Win", "spock": 'Lose', "lizard": "Win"},
                     'paper': {"paper": "Draw", "scissors": "Lose", "rock": "Win", "spock": "Win", "lizard": "Lose"},
                     'scissors': {"scissors": "Draw", "rock": "Lose", "paper": "Win", "spock": "Lose", "lizard": "Win"},
                     'spock': {"scissors": "Win", "rock": "Win", "paper": "Lose", "spock": "Draw", "lizard": "Lose"},
                     'lizard': {"scissors": "Lose", "rock": "Lose", "paper": "Win", "spock": "Win", "lizard": "Draw"}}
        enemy = random.choice(moves)

        print("-------------Rock Paper Scissors Spock Lizard-------------")
        chose = input("Wanna play or view the statistics? p/s?")
        if chose == "p":
            player = input("Please enter your symbol: ")
            if player in moves:
                print("You chose: " + player)
                print("Enemy chose: " + enemy)
                print(getResult[player][enemy])
                saveToDB(player, enemy, getResult[player][enemy])
                again = input("Wanna play again? y/n")
                if again == "n":
                    print("Bye!")
                    playing = False
                else:
                    playing = True
            else:
                print("Wrong input! ")
        else:
            getStatistics()


if __name__ == '__main__':
    cmdGame()
