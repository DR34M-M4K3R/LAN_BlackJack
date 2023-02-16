#!/bin/python3
# encoding: utf-8


# Problème: https://stackoverflow.com/a/66075333

#________________________________________________________________________________________________
# Note: fonctionne correctement sur python 3. A executer de preference via une ligne de commande.
#________________________________________________________________________________________________


import socket
import random
import time

# Quitter l'application
from sys import exit





def server():

    t = time
    r = random


    # définition des variables
    d1=0
    d2=0
    score=0
    mise=0
    miseAdv=0
    nombreDe=0
    scoreAdv=0

    # Si 'win'==0, le joueur a perdu; si 'win'==1, le joueur a gagne; et si'win'==2, le joueur arrete la partie
    win=3

    end=False

    # petite manip pour obtenir l'addresse locale d'un pc sous Unix et Windows --> https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    print("\n\nVotre addresse à transmettre à votre adversaire: ",local_ip,"\n\n (Entrez \"127.0.1.1\" pour jouer sur un même ordinateur avec deux lignes de commandes.)")

    host = socket.gethostname()
    port = 2345
    server_socket = socket.socket()
    server_socket.bind(('', port))

    print("en attente d'un joueur...")


    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if(not data):
            break
        if(str(data)=="Test"):
            print("Connexion réussie.")
            break


    print(""""\n\n\n
                          ___________
                          |BlackJack|
    _______________________________________________________
    |                     Règles du jeu                   |
    |      - Par tour, vous lancez soit 1, soit 2 dés.    |
    |      - Si vous dépassez 21, vous avez perdu.        |
    |      - Si l'adversaire dépasse 21, vous avez gagné. |
    |      - Si vous arrêtez la partie, le joueur le +    |
    |                proche de 21 a gagné                 |
    |                                                     |
    |      - Si vous perdez, l'argent en jeu sera         |
    |               empoché par l'adversaire              |
    |                                                     |
    |                     Bonne chance                    |
    ______________________________________________________""")

    # Définition de la mise de départ par l'utilisateur
    while(mise==0):
        try:
            mise=int(input("\nEntrez le montant de votre mise de départ (€). >"))

        except ValueError:
            print("\n[!] Entrez un nombre!")

    # On envoie la valeur de la mise
    message = str(mise)
    conn.send(str(message).encode())

    # On obtient la valeur de la mise de l'adversaire
    while True:
        data = conn.recv(1024).decode()
        if(not data):
            break
        miseAdv=int(data)
        break




    scoreAdv=0
    d1=0
    d2=0
    score=0
    win=3


    # Boucle de partie
    while(win==3):
        reponse=99
        d1, d2,=0, 0
        # Affichage de l'interface
        print("""\n\n[!] A votre tour.\n

              _________________________
             |Argent en jeu: """,mise,"""+""",miseAdv,"""€ |
        ________________________________________
        |           Votre score: """,score,"""           |
        | [1] - lancer 1 dé | [2] Lancer 2 dés  |
        |        [0] - Arreter la partie        |
        _________________________________________""")




        # Boucle de gestion des exceptions
        while(reponse==99):
            try:
                reponse=int(input(">"))
                if(reponse!=0 and reponse!=1 and reponse!=2):
                    reponse=99
                    print("\n[!] Entrez \"0\" ,\"1\" ou \"2\".")

            # Si l'utilisateur entre une lettre
            except ValueError:
                print("\n[!] Entrez un nombre! 0, 1 ou 2.")


        # On lance 1 de
        if(reponse==1):
            nombreDe=1
            print("\n[-] Lancement du dé...")
            t.sleep(r.randint(10,15)/10)

            d1=r.randint(1,6)
            score=score+d1
            if(score>21):
                win=0
                break
            else:
                print("\n[-] Vous avez fait ",d1," points. Votre score est maintenant ", score)
                t.sleep(0.5)






        # On lance 2 des
        elif(reponse==2):
            print("\n[-] Lancement des dés...")
            nombreDe=2
            t.sleep(r.randint(10,15)/10)
            d1=r.randint(1,6)
            d2=r.randint(1,6)
            score=score+d1+d2
            if(score>21):
                # Le serveur perd, le client gagne.
                win=0

            else:
                print("\n[-] Vous avez fait ",d1,"+",d2," points. Votre score est maintenant ", score)
                t.sleep(0.5)


        elif(reponse==0):
            win=2
            message = "win2"
            conn.send(str(message).encode())
            break



        # On envoie le score actuel au client
        message = str(score)+";"+str(nombreDe)
        conn.send(str(message).encode())


        # Au tour de l'adversaire
        print("\n\n[-] L'adversaire joue...\n\n")
        while True:
            data = conn.recv(1024).decode()
            if(not data):
                break
            # Si le client informe que la partie se termine
            if(str(data)=="win2"):
                win=2
                break
            # On met à jour son score.

            #print(str(data)[:data.find(";")])

            scoreAdv=int(str(data)[:data.find(";")])
            break



        if(score>21):
            # Le serveur perd, le client gagne.
            win=0

        elif(scoreAdv>21):
            # Le serveur gagne, le client perd.
            win=1





    if(win==0):
        print("\n[!] Vous avez perdu. L'adversaire empoche ",mise+miseAdv,"€")
    elif(win==1):
        print("\n[$$$] Vous avez gagné! L'adversaire a dépassé 21 avec un score de ",scoreAdv)
        t.sleep(1)
    elif(win==2):
        print("\n[!] Comparaison des scores...")
        t.sleep(1)
        if(21-score>21-scoreAdv):
            print("\n[!] Vous avez perdu ",score," à ",scoreAdv,", L'adversaire empoche ",mise+miseAdv,"€")
        elif(21-score<21-scoreAdv):
            print("\n[$$$] Vous avez gagné! ",score," à ",scoreAdv,", vous remportez ",mise+miseAdv," euros!!!!!!")
            t.sleep(1)
    exit()



def client():

    host = str(input("Entrez l'addresse de l'hote >"))
    port = 2345

    t = time
    r = random

    # définition des variables
    d1=0
    d2=0
    score=0
    mise=0
    argentGagne=0
    scoreAdv=0

    # Si 'win'==0, le joueur a perdu; si 'win'==1, le joueur a gagne; et si'win'==2, le joueur arrete la partie
    win=3

    end=False


    # Connexion à lhôte
    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = "Test"
    client_socket.send(message.encode())



    print("""\n\n\n
                          ___________
                          |BlackJack|
    _______________________________________________________
    |                     Règles du jeu                   |
    |      - Par tour, vous lancez soit 1, soit 2 dés.    |
    |      - Si vous dépassez 21, vous avez perdu.        |
    |      - Si l'adversaire dépasse 21, vous avez gagné. |
    |      - Si vous arrêtez la partie, le joueur le +    |
    |                proche de 21 a gagné                 |
    |                                                     |
    |      - Si vous perdez, l'argent en jeu sera         |
    |               empoché par l'adversaire              |
    |                                                     |
    |                     Bonne chance                    |
    ______________________________________________________""")




    # Définition de la mise de départ par l'utilisateur
    while(mise==0):
        try:
            mise=int(input("\nEntrez le montant de votre mise de départ (€). >"))

        except ValueError:
            print("\n[!] Entrez un nombre!")


    # On envoie la valeur de la mise
    message = str(mise)
    client_socket.send(str(message).encode())


    # On obtient la valeur de la mise de l'adversaire
    while True:
        data = client_socket.recv(1024).decode()
        if(not data):
            break
        miseAdv=int(data)
        break


    scoreAdv=0
    d1=0
    d2=0
    score=0
    win=3
    nombreDe=0

    # Premier tour, le serveur à la main.
    print("\n\n[-] L'adversaire joue...\n\n")
    while True:
        data = client_socket.recv(1024).decode()
        if(not data):
            break
        print("aaa")
        print("l'adversaire à lancé", str(data)[data.find(";")+1:],"dés.")
        scoreAdv=int(str(data)[:data.find(";")])
        break



    # Boucle de partie
    while(win==3):
        reponse=99
        d1, d2,=0, 0


        # Affichage de l'interface
        print("""\n\n[!] A votre tour.\n

              _________________________
             |Argent en jeu: """,mise,"""+""",miseAdv,"""€ |
        ________________________________________
        |           Votre score: """,score,"""           |
        | [1] - lancer 1 dé | [2] Lancer 2 dés  |
        |        [0] - Arreter la partie        |
        _________________________________________""")



        # Boucle de gestion des exceptions
        while(reponse==99):
            try:
                reponse=int(input(">"))
                if(reponse!=0 and reponse!=1 and reponse!=2):
                    reponse=99
                    print("\n[!] Entrez \"0\" ,\"1\" ou \"2\".")

            # Si l'utilisateur entre une lettre
            except ValueError:
                print("\n[!] Entrez un nombre! 0, 1 ou 2.")


        # On lance 1 de
        if(reponse==1):
            print("\n[-] Lancement du dé...")
            nombreDe=1
            t.sleep(r.randint(10,15)/10)

            d1=r.randint(1,6)
            score=score+d1
            if(score>21):
                win=1
                break
            else:
                print("\n[-] Vous avez fait ",d1," points. Votre score est maintenant ", score)
                t.sleep(0.5)



        # On lance 2 des
        elif(reponse==2):
            print("\n[-] Lancement des dés...")
            nombreDe=2
            t.sleep(r.randint(10,15)/10)
            d1=r.randint(1,6)
            d2=r.randint(1,6)
            score=score+d1+d2
            if(score>21):
                win=1
                break
            else:
                print("\n[-] Vous avez fait ",d1,"+",d2," points. Votre score est maintenant ", score)
                t.sleep(0.5)



        elif(reponse==0):
            win=2
            message = "win2"
            client_socket.send(str(message).encode())
            break



        # On envoie le score actuel au client
        message = str(score)+";"+str(nombreDe)
        client_socket.send(str(message).encode())


        # Au tour de l'adversaire
        print("\n\n[-] L'adversaire joue...\n\n")
        while True:
            data = client_socket.recv(1024).decode()
            if(not data):
                break
            # Si le serveur informe que la partie se termine
            if(str(data)=="win2"):
                win=2
                break
            print("l'adversaire à lancé", str(data)[data.find(";")+1:],"dés.")
            scoreAdv=int(str(data)[:data.find(";")])
            break

        if(score>21):
            # Le serveur gagne, le client perd.
            win=1

        elif(scoreAdv>21):
            # Le serveur perd, le client gagne.
            win=0



    if(win==0):
        print("\n[$$$] Vous avez gagné, l'adversaire à dépassé 21 avec un score de ", scoreAdv," Vous empochez ",mise+miseAdv,"€")
    elif(win==1):
        print("\n[!] Vous avez perdu. L'adversaire empoche ",mise+miseAdv,"€")
        t.sleep(1)
    elif(win==2):
        print("\n[!] Comparaison des scores...")
        t.sleep(1)
        if(21-score>21-scoreAdv):
            print("\n[!] Vous avez perdu ",score," à ",scoreAdv,", L'adversaire empoche ",mise+miseAdv,"€")
        elif(21-score<21-scoreAdv):
            print("\n[$$$] Vous avez gagné! ",score," à ",scoreAdv,", vous remportez ",mise+miseAdv," euros!!!!!!")
            t.sleep(1)
    exit()


a=0
while(a==0):
    a=str(input("Voulez vous:  [1] - Héberger une partie | [2] - Rejoindre une partie"))
    if(a=="1"):
        server()
    elif(a=="2"):
        client()
    else:
        print("Entrez \"1\" ou \"2\"")
        a=0
