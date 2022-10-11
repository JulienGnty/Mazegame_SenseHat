#!/usr/bin/env python3

import paho.mqtt.client as ClientMqtt
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED, DIRECTION_DOWN, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_RIGHT
import json
import digit_grid as dg

# variables à modifier
AdresseCourtier         = "192.168.1.20"
Port                    = 1883
Utilisateur             = ""
MotDePasse              = ""
SujetsPourPublication   = ["/maze/players/signin"]
SujetsPourSouscription  = ["/maze/data"]
tempo_publish           = 1

EstConnecte = False
Ingame = False
Finished = False
Name = "julien"
S = SenseHat()
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

    global Ingame, SujetsPourPublication, S, Finished, tempo_publish

    if Ingame:
        S.set_pixels(valeur[Name]["grid"])
        if valeur[Name]["status"] == "end":
            Finished = True
            S.set_pixels(dg.set_digit_grid(valeur[Name]["rank"],valeur[Name]["color"]))
            if "/maze/data" in SujetsPourSouscription:
                remove_sub("/maze/data")
                SujetsPourPublication.remove("/maze/players/"+Name)
            tempo_publish = 10
    else:
        if Name in valeur:
            SujetsPourPublication.remove("/maze/players/signin")
            Ingame = True
            tempo_publish = 0.25
        else:
            print("Waiting for signing in")
    # pour convertir un message reçu en UTF8, il faut penser à : message.payload.decode("utf-8")
    
    # à écrire ici :
    # le code des actions associées aux messages reçus (SUBSCRIBE)  !
    #print("Message reçu sur le sujet", sujet, ":", valeur)


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

    return client

def publish(client, data_out):
    for Sujet in SujetsPourPublication:                 # publication sur les sujets souhaités
        client.publish(Sujet, data_out)


def main():
    global S, SujetsPourPublication, Name, AdresseCourtier
    try:
        name = ""
        broker = ""
        while not(broker):
            broker = input("Broker IP address: ")
        AdresseCourtier = broker
        while not(name):
            name = input("Enter your name: ")
        Name = name.replace("/","").lower()
        SujetsPourPublication.append("/maze/players/"+Name)
        print(SujetsPourPublication[-1])
        client = init_mqtt()
        while True:
            data_out = {}
            direction = ""
            if Ingame and not(Finished):
                already_treated = False
                for event in S.stick.get_events():
                    if event.action in (ACTION_PRESSED, ACTION_HELD) and not already_treated:
                        if event.direction == DIRECTION_DOWN:
                            direction = "down"
                            already_treated = True
                        if event.direction == DIRECTION_UP:
                            direction = "up"
                            already_treated = True
                        if event.direction == DIRECTION_RIGHT:
                            direction = "right"
                            already_treated = True
                        if event.direction == DIRECTION_LEFT:
                            direction = "left"
                            already_treated = True
                data_out = json.dumps({"message":direction,"name":Name})
                publish(client, data_out)
            elif not(Ingame) and not(Finished):
                data_out = json.dumps({"message":"signin","name":Name})
                publish(client, data_out)
            
            
            time.sleep(tempo_publish)

    except KeyboardInterrupt:
        print(" arrêt par l'utilisateur !")
        S.clear()
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    main()
