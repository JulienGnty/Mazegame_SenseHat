#!/usr/bin/env python3

import paho.mqtt.client as ClientMqtt
import mazegame as mzg
import time
import json


# variables à modifier
AdresseCourtier         = "courtier"
Port                    = 1883
Utilisateur             = ""
MotDePasse              = ""
SujetsPourPublication   = ["/maze/data"]
SujetsPourSouscription  = ["/maze/players/signin"]
tempo_publish           = 0.25

EstConnecte = False
nbJoueurs = 0

maze_dict = {}
data_sent = {}
client = ClientMqtt.Client()                                # création d'une nouvelle instance    

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au courtier MQTT")
        global EstConnecte                                  # utilisation de la variable *globale*
        EstConnecte = True                                 # indication de la connexion
    else:
        print("Échec de la connexion")

def on_message(client, userdata, message):
    sujet  = message.topic
    valeur = json.loads(str(message.payload,"utf-8"))

    global maze_dict

    if "message" in valeur and "name" in valeur:
        if valeur["message"] == "signin":
            if len(maze_dict["players"]) < 6:
                if valeur["name"] not in maze_dict["players"]:
                    print("j'ajoute",valeur["name"])
                    maze_dict = mzg.add_player(maze_dict, valeur["name"], visible=False)
                    add_sub("/maze/players/"+str(valeur["name"]))
            else:
                remove_sub("/maze/players/signin")
        if valeur["name"] in maze_dict["players"]:
            if valeur["message"] == "up":
                maze_dict = mzg.move_player_up(maze_dict,valeur["name"])
            elif valeur["message"] == "down":
                maze_dict = mzg.move_player_down(maze_dict,valeur["name"])
            elif valeur["message"] == "left":
                maze_dict = mzg.move_player_left(maze_dict,valeur["name"])
            elif valeur["message"] == "right":
                maze_dict = mzg.move_player_right(maze_dict,valeur["name"])
            else:
                pass
                #print("Couldn't understand message", valeur["message"],"on", sujet)
            maze_dict = mzg.update_player_view(maze_dict,valeur["name"])
            maze_dict = mzg.check_players_status(maze_dict)
    else:
        pass
        #print("Couldn't understand ", valeur,"on",sujet)
    


def add_sub(name):
    global SujetsPourSouscription, client
    SujetsPourSouscription.append(name)
    client.subscribe(name)

def remove_sub(name):
    global SujetsPourSouscription, client
    SujetsPourSouscription.remove(name)
    client.unsubscribe(name)

def init_mqtt():
    # client.username_pw_set(Utilisateur, password=MotDePasse)  # définition utilisateur+motdepasse
    # (non utilisé ici)
    global client
    client.on_connect = on_connect                               # assignation de la fonction de 'callback'
    client.on_message = on_message                               # assignation de la fonction de 'callback'

    client.connect(AdresseCourtier, port=Port)                  # connexion au courtier
    client.loop_start()                                         # début de la boucle
    while EstConnecte != True:                                  # attente de la connexion
        time.sleep(0.1)

    for Sujet in SujetsPourSouscription:                        # abonnement aux sujets souhaités
        client.subscribe(Sujet)
        print("souscription au sujet :", Sujet)


def main():
    global maze_dict, client, AdresseCourtier
    try:
        broker = ""
        width = 0
        height = 0
        while not(broker):
            broker = input("Broker IP address: ")
        AdresseCourtier = broker
        while not(8 <= width <= 40):
            width = int(input("Width of maze (between 8 and 40 inclusive): "))
        while not(8 <= height <= 40):
            height = int(input("Height of maze (between 8 and 40 inclusive): "))
        maze_dict = mzg.init_maze(width,height)
        mzg.mazegen.print_maze(maze_dict["maze"])
        init_mqtt()
        while True:
            data_out = {}
            for p in maze_dict["players"]:
                data_out[p] = {
                    "pos": maze_dict["players"][p]["pos"],
                    "status": maze_dict["players"][p]["status"],
                    "rank": maze_dict["players"][p]["rank"],
                    "color": maze_dict["players"][p]["color"],
                    "grid": mzg.set_maze_display(maze_dict,p,display_w=8, display_h=8)
                }
            data_out = json.dumps(data_out)
            for Sujet in SujetsPourPublication:                 # publication sur les sujets souhaités
                client.publish(Sujet, data_out)
            time.sleep(tempo_publish)

    except KeyboardInterrupt:
        print(" arrêt par l'utilisateur !")
        client.disconnect()
        client.loop_stop()
    except:
        print("Unknown Error")
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    main()
