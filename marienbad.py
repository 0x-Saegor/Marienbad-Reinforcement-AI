# Auteur : Arthur Le Gall
# Date : 09-01-2025
# Version : 1.0
# Python version : 3.10.11
# Description : Jeu de Marienbad avec un algorithme de renforcement pour l'IA

from os import system
import matplotlib.pyplot as plt
import random

# Create a global variable to count the number of games played
cpt = 0


def main():
    """
    Main function
    """
    clearScreen()

    print("------ Bienvenue dans le jeu de Marienbad ------")

    # Game mode selection
    while True:
        print("""1 pour JvsO
2 pour JvsJ
3 pour Demo""")
        game_mode_selection = int(input("Choisissez le mode de jeu -> "))
        while game_mode_selection not in [1, 2, 3]:
            game_mode_selection = int(input("Choisissez le mode de jeu -> "))
        break

    # Game mode selection
    if game_mode_selection == 1:
        JvO()
    elif game_mode_selection == 2:
        JvJ()
    elif game_mode_selection == 3:
        RunGameDemo()


### Functions to play in JvO mode ###


def JvO():
    """
    JvO mode
    """
    clearScreen()
    print("------ Mode de jeu : Joueur contre Ordinateur ------")

    # Player names
    joueur1 = str(input("Entrez le nom du joueur: "))
    joueur2 = "Ordinateur"
    joueurs = [joueur2, joueur1]

    # Number of lines
    while True:
        nombreLignes = int(input(
            "Combien de lignes d'allumettes souhaitez vous ? -> "))
        if nombreLignes >= 2:
            break

    print()

    # Creation of the matches table and memorisation generation
    allumettes = createMatchesArray(nombreLignes)
    memorisation = generate_memorisation(nombreLignes)
    game_state_history = []

    # Start the game
    startNewGame_JvO(memorisation, game_state_history, allumettes, joueurs)


def startNewGame_JvO(memorisation: dict, game_state_history: list, allumettes: list, joueurs: list):
    """
    Start a new game in JvO mode
    """

    # Creating the game variables
    win = False
    tour = 0
    allumettes_base = allumettes.copy()

    # Main loop, exit when a player wins
    while not win:
        joueur = joueurs[tour % 2]

        # If the state is not in the memorisation, we generate all possible plays for this state
        if joueur == "Ordinateur":
            if str(allumettes) not in memorisation:
                coups_generes = generate_all_plays_for_state(allumettes)
                memorisation[str(allumettes)] = {str(
                    coups_generes[j]): 50 for j in range(len(coups_generes))}

        # Player/Computer plays
        playJvO(joueur, allumettes, memorisation, game_state_history)

        # Check if a player has won
        if checkForWinner(allumettes):
            win = True

            if joueur == "Ordinateur":
                print("L'ordinateur a gagné")

                # If the computer wins, we add 10 to the memorisation for each state played
                for etat_coup in game_state_history:
                    memorisation[str(etat_coup[0])][str(
                        etat_coup[1])] += 10
            else:
                print(f"{joueur} a gagné")

                # If the computer loses, we remove 5 from the memorisation for each state played
                for etat_coup in game_state_history:
                    if memorisation[str(etat_coup[0])][str(etat_coup[1])] > 5:
                        memorisation[str(etat_coup[0])
                                     ][str(etat_coup[1])] -= 5

            # Ask the user if he wants to restart the game
            restart = str(input(
                "Voulez-vous relancer une partie ? Il est conseillé de jouer plusieurs fois car l'IA doit s'entraîner (O/N/M for menu) : "))
            while restart not in ["O", "o", "N", "n", "M", "m"]:
                restart = str(input(
                    "Voulez-vous relancer une partie ? Il est conseillé de jouer plusieurs fois car l'IA doit s'entraîner (O/N/M for menu) : "))
            if restart == "O" or restart == "o":
                clearScreen()
                game_state_history = []
                startNewGame_JvO(memorisation, [], allumettes_base, joueurs)
            elif restart == "M" or restart == "m":
                main()

        tour += 1


def playJvO(joueur, allumettes: list, memorisation: dict, game_state_history: list):
    """
    Play in JvO mode
    """
    # Display the matches
    display_board(allumettes)
    print(joueur + " est en train de jouer.")

    # AI plays
    if (joueur == "Ordinateur"):
        # Reinforcement based selection
        selectedLine, matchesToRemove = select_move_based_on_memory(
            allumettes, memorisation)

        # Add the state and the move to the history
        game_state_history.append(
            (allumettes.copy(), (selectedLine, matchesToRemove)))

    else:

        # Player plays
        while True:
            selectedLine = int(input("Quelle ligne souhaitez vous jouer ? "))
            if isLineValid(selectedLine, allumettes):
                break

        while True:
            matchesToRemove = int(input(
                "Combien d'allumettes souhaitez vous retirer ? "))
            if isMatchCountValid(selectedLine, matchesToRemove, allumettes):
                break

    print(
        f"{joueur} a joué ligne {selectedLine} et a retiré {matchesToRemove} allumettes")
    print("")
    allumettes[selectedLine - 1] -= matchesToRemove


### Functions to play in demo mode ###


def RunGameDemo():
    """
    Run the game in demo mode
    """
    clearScreen()
    print("------ Mode de jeu : DEMO ------")

    # Player names
    joueurs = ["Ordinateur", "Algorithme"]

    # Number of lines for the demo
    nombreLignes = input(
        "Entrez le nombre de lignes pour la démo : ")

    # Verifying the integrity of the input
    while True:
        if nombreLignes.isdigit():
            if int(nombreLignes) >= 2:
                break
            else:
                print("Veuillez entrer un nombre supérieur ou égal à 2")
                nombreLignes = input(
                    "Entrez le nombre de lignes pour la démo : ")
        else:
            print("Veuillez entrer un nombre supérieur ou égal à 2")
            nombreLignes = input(
                "Entrez le nombre de lignes pour la démo : ")

    nombreLignes = int(nombreLignes)

    # Number of occurrences for the demo
    nb_occurences = input(
        "Entrez le nombre d'occurences pour la démo (10 000 conseillé, si vide 10 000 par défaut) : ")

    # Verifying the integrity of the input
    while True:
        if nb_occurences.isdigit() or nb_occurences == "":
            if nb_occurences == "":
                break
            elif int(nb_occurences) >= 1:
                break
        else:
            print("Veuillez entrer un nombre supérieur ou égal à 1")
            nb_occurences = input(
                "Entrez le nombre d'occurences pour la démo (10 000 conseillé, si vide 10 000 par défaut) : ")

    nb_occurences = int(nb_occurences) if nb_occurences != "" else 10000

    # Creation of the matches table
    allumettes = createMatchesArray(nombreLignes)

    # Memorisation generation
    memorisation = generate_memorisation(nombreLignes)
    liste_etat_coups_joues = []

    # Start the game simulations
    execute_game_simulations(memorisation, liste_etat_coups_joues,
                             allumettes, joueurs, nb_occurences)


def execute_game_simulations(memorisation: dict, liste_etat_coups_joues: list, allumettes: list, joueurs: list, nb_occurences: int = 10000):
    """
    Run game simulations for the demo mode
    """

    # Retrieve the global variable to count the number of games played
    global cpt

    # Create the variables for the game
    win = False
    tab_victoires = []
    allumettes_base = allumettes.copy()
    
    cumulative_victories = []
    cumulative_losses = []

    while cpt < nb_occurences:  # Number of games to simulate
        tour = 0  # Reset the turn counter which is used to determine which player is playing
        while not win:  # Exit the loop when a player wins
            joueur = joueurs[tour % 2]

            # If the state is not in the memorisation, we generate all possible plays for this state
            if joueur == "Ordinateur":
                if str(allumettes) not in memorisation:
                    coups_generes = generate_all_plays_for_state(allumettes)
                    memorisation[str(allumettes)] = {str(
                        coups_generes[j]): 50 for j in range(len(coups_generes))}

            # Algorithm/Computer plays
            playDemo(joueur, allumettes, memorisation,
                     liste_etat_coups_joues)

            # Check if a player has won
            if checkForWinner(allumettes):
                win = True

                if joueur == "Ordinateur":
                    # If the computer wins, we add 1 to the list of victories
                    tab_victoires.append(1)

                    # We add 10 to the memorisation for each state played, it encourages the computer to play the same moves
                    for etat_coup in liste_etat_coups_joues:
                        memorisation[str(etat_coup[0])][str(
                            etat_coup[1])] += 10
                else:
                    # If the computer loses, we add 0 to the list of victories
                    tab_victoires.append(0)

                    # We remove 5 from the memorisation for each state played, it encourages the computer to play different moves
                    for etat_coup in liste_etat_coups_joues:
                        if memorisation[str(etat_coup[0])][str(etat_coup[1])] > 5:
                            memorisation[str(etat_coup[0])
                                         ][str(etat_coup[1])] -= 5
                            
                # We add the number of victories and losses to the cumulative lists to display the evolution of the victories over time
                cumulative_victories.append(tab_victoires.count(1))
                cumulative_losses.append(tab_victoires.count(0))

            tour += 1  # Increment the turn counter to change the player

        cpt += 1  # Increment the number of games played
        win = False  # Reset the win variable to False
        # Reset the allumettes list to its initial state
        allumettes = allumettes_base.copy()
        liste_etat_coups_joues = []  # Reset the list of played states and moves

    print()

    print(
        f"Il y a {tab_victoires.count(1)} victoires pour l'ordinateur et {tab_victoires.count(0)} défaites, l'ordinateur a joué {cpt} parties contre un algorithme {'aléatoire' if len(allumettes) >=4 else 'utilisant la stratégie gagnante'}")
    print(
        f"Pourcentage de victoires : {round(tab_victoires.count(1)/len(tab_victoires)*100, 2)}%, si cela est inférieur à 90%, il est conseillé de relancer le programme avec plus d'occurences")

    print("")
    print("Les statistiques ont plus de sens pour un nombre de ligne de 2 ou 3 car l'IA joue contre l'algorithme gagnant")
    stats_wanted = str(input(
        "Voulez-vous afficher les statistiques de victoires et défaites ? (O/N) : "))
    while stats_wanted not in ["O", "o", "N", "n"]:
        stats_wanted = str(input(
            "Voulez-vous afficher les statistiques de victoires et défaites ? : "))
        
    if stats_wanted == "O" or stats_wanted == "o":        
        plt.figure(figsize=(10, 6))
        plt.plot(cumulative_victories, label="Victoires cumulées de l'ordinateur", color='b')
        plt.plot(cumulative_losses, label="Défaites cumulées de l'ordinateur", color='r')
        plt.xlabel('Nombre de parties simulées')
        plt.ylabel('Nombre cumulatif')
        plt.title('Évolution des victoires et défaites de l\'ordinateur au fil du temps')
        plt.grid(True)
        plt.legend()
        plt.show()


    # We ask the user if he wants to restart the program
    restart = str(input("Voulez-vous recommencer ? (O/N/M menu) : "))
    if restart == "O" or restart == "o":
        cpt = 0
        clearScreen()
        RunGameDemo()
    elif restart == "M" or restart == "m":
        cpt = 0
        main()


def playDemo(joueur, allumettes: list, memorisation: dict, game_state_history: list):
    """
    Play in demo mode
    """

    # AI plays
    if (joueur == "Ordinateur"):
        res = []
        # Reinforcement learning
        res = select_move_based_on_memory(allumettes, memorisation)
        selectedLine = res[0]
        matchesToRemove = res[1]
        game_state_history.append(
            (allumettes.copy(), (selectedLine, matchesToRemove)))

    # Algorithm plays
    else:
        # If the number of matches is less than 4, the algorithm can force a win
        if (len(allumettes) < 4):
            nimsum = 0
            if (len(allumettes) > 0):
                nimsum = allumettes[0]
                for i in range(1, len(allumettes)):
                    nimsum = nimsum ^ allumettes[i]

            if (nimsum != 0):
                # Find the line and the number of matches to play using the nimsum
                for i in range(len(allumettes)):
                    ligne = allumettes[i]
                    # Number of matches after the move
                    targetLigne = ligne ^ nimsum

                    if (targetLigne < ligne):
                        # Stock the line and the number of matches to play (index + 1 because the index starts at 0)
                        selectedLine = i + 1
                        # Number of matches to play
                        matchesToRemove = ligne - targetLigne
            else:
                selectedLine, matchesToRemove = pick_random_matches(allumettes)

        # If the number of matches is greater than 3, the algorithm will always win and we do not want that to reinforce the AI
        else:
            selectedLine, matchesToRemove = pick_random_matches(allumettes)

    # Remove the matches from the line
    allumettes[selectedLine - 1] -= matchesToRemove


### Functions to play in JvJ mode ###


def JvJ():
    """
    JvJ mode
    """
    clearScreen()
    print("------ Mode de jeu : Joueur contre Joueur ------")

    # Player names
    joueur1 = str(input("Entrez le nom du joueur 1 : "))
    joueur2 = str(input("Entrez le nom du joueur2 : "))
    joueurs = ["", ""]

    # First player selection
    while True:
        firstPlayerSelection = int(input(
            f"Premier joueur : 1 pour {joueur1} ou 2 pour {joueur2} : "))
        if firstPlayerSelection == 1 or firstPlayerSelection == 2:
            break

    if (firstPlayerSelection == 1):
        joueurs[0] = joueur1
        joueurs[1] = joueur2
    else:
        joueurs[0] = joueur2
        joueurs[1] = joueur1

    win = False
    tour = 0
    while True:
        nombreLignes = int(input(
            "Combien de lignes d'allumettes souhaitez vous ? -> "))
        if nombreLignes >= 2:
            break

    # Creation of the matches table
    allumettes = createMatchesArray(nombreLignes)

    # Main loop
    while win != True:
        joueur = joueurs[tour % 2]

        # Player plays
        playJVJ(joueur, allumettes)

        # Check if a player has won
        if (checkForWinner(allumettes)):
            win = True
            print(joueur + " a gagné")

            # Ask the user if he wants to restart the game
            restart = str(input(
                "Voulez-vous relancer une partie ? (O/N/M pour menu) : "))
            while restart not in ["O", "o", "N", "n", "M", "m"]:
                restart = str(input(
                    "Voulez-vous relancer une partie ? (O/N/M pour menu) : "))
            if restart == "O" or restart == "o":
                clearScreen()
                JvJ()
            elif restart == "M" or restart == "m":
                main()

        tour += 1


def playJVJ(joueur, allumettes):
    """
    Play in JvJ mode
    """

    # Display the matches
    clearScreen()
    display_board(allumettes)
    print(joueur + " est en train de jouer.")

    # Player plays
    while True:
        selectedLine = int(input("Quelle ligne souhaitez vous jouer ? "))
        if isLineValid(selectedLine, allumettes):
            break

    while True:
        matchesToRemove = int(
            input("Combien d'allumettes souhaitez vous retirer ? "))
        if isMatchCountValid(selectedLine, matchesToRemove, allumettes):
            break

    # Remove the matches from the line
    allumettes[selectedLine - 1] -= matchesToRemove


### Functions to play with matches ###


def createMatchesArray(numberOfRows):
    """
    Create the matches array
    """

    matches_per_row = [0 for i in range(numberOfRows)]
    matchesToRemove = 1
    for i in range(numberOfRows):
        matches_per_row[i] = matchesToRemove
        matchesToRemove += 2
    return matches_per_row


def pick_random_matches(allumettes: list):
    """
    Pick random matches
    """
    selectedLine = 0
    matchesToRemove = 0

    # Pick a random line and verify that it is not empty
    while True:
        selectedLine = random.randint(1, len(allumettes))
        if isLineValid(selectedLine, allumettes):
            break
    while True:
        matchesToRemove = random.randint(1, allumettes[selectedLine - 1])
        if isMatchCountValid(selectedLine, matchesToRemove, allumettes):
            break

    return selectedLine, matchesToRemove


### Generation of the memorisation ###


def generate_base_state(n: int):
    """
    Generate all possible states for the game of Marienbad with n lines
    """

    return [2*x+1 for x in range(n)]


def generate_all_plays_for_state(state: list):
    """
    Generate all possible plays for a given state
    """

    plays = []

    for i in range(len(state)):
        for j in range(state[i], 0, -1):
            plays.append((i+1, j))

    return plays


def generate_memorisation(n: int):
    """
    Generate memorisation for the game of Marienbad with n lines
    """

    base_state = generate_base_state(n)
    all_plays = generate_all_plays_for_state(base_state)
    memorisation = {}

    memorisation[str(base_state)] = {str(
        all_plays[j]): 50 for j in range(len(all_plays))}

    return memorisation


def select_move_based_on_memory(tab: list, memorisation: dict):
    """
    Select a move based on the memorisation and the weights of the moves
    """

    # Get the weights of the moves
    poids_liste = [x for x in memorisation[str(tab)].values()]

    # Select a move based on the weights, the probability of selecting a move is proportional to its weight
    choix = random.choices(
        list(memorisation[str(tab)].keys()), weights=poids_liste)

    # Convert the move to a list
    choix = eval(choix[0])
    return choix


### Functions to display the game ###


def clearScreen():
    """
    Simple function to clear the console screen
    """
    system("cls")


def display_board(tab):
    """
    Display the matches
    """

    for i in range(len(tab)):
        print(f"{i + 1} : ", end="")
        for j in range(tab[i]):
            print("|", end=" ")
        print("")


### Functions to verify the integrity of the game ###


def isLineValid(ligne, tab: list):
    """
    Check if the line is valid
    """
    return (ligne > 0 and ligne <= len(tab) and tab[ligne - 1] > 0)


def isMatchCountValid(ligne, matchesToRemove, tab: list):
    """
    Check if the number of matches is valid
    """
    return (tab[ligne - 1] >= matchesToRemove and matchesToRemove >= 1)


def checkForWinner(allumettes: list):
    """
    Check if a player has won (no matches left)
    """

    win = True
    for i in range(len(allumettes)):
        if (allumettes[i] != 0):
            win = False

    return win


main()
