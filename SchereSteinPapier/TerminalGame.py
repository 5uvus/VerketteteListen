import random


def cmdGame():
    playing = True
    while playing:
        corr_input = True
        moves = ['rock', 'paper', 'scissors', 'spock', 'lizard']
        getResult = {'rock': {"rock": "Draw", "paper": "Lose", "scissors": "Win", "spock": 'Lose', "lizard": "Win"},
                     'paper': {"paper": "Draw", "scissors": "Lose", "rock": "Win", "spock": "Win", "lizard": "Lose"},
                     'scissors': {"scissors": "Draw", "rock": "Lose", "paper": "Win", "spock": "Lose", "lizard": "Win"},
                     'spock': {"scissors": "Win", "rock": "Win", "paper": "Lose", "spock": "Draw", "lizard": "Lose"},
                     'lizard': {"scissors": "Lose", "rock": "Lose", "paper": "Win", "spock": "Win", "lizard": "Draw"}}
        enemy = random.choice(moves)

        if corr_input:
            print("-------------Rock Paper Scissors Spock Lizard-------------")
            player = input("Please enter your symbol: ")
            if player in moves:
                print("You chose: " + player)
                print("Enemy chose: " + enemy)
                print(getResult[player][enemy])

                again = input("Wanna play again? y/n")
                if again == "n":
                    print("Bye!")
                    playing = False
                else:
                    playing = True
            else:
                print("Wrong input! ")
                corr_input = False

if __name__ == '__main__':
    cmdGame()
