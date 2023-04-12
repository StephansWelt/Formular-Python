#Anmelde und Register Formular von EinfxchPingu
import pymongo
import time
import os
from simple_colors import *

#definiere verbindung zum Server | Abfrage für Anmelden oder registrieren
def verbinde_server():
    print(red("Verbinde zum Server..."))
    client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<Atlas Clusters>.k3jmp5m.mongodb.net/test?retryWrites=true&w=majority")
    db = client["meine_db"]
    benutzer_collection = db["benutzer"]
    time.sleep(3)
    auswahl = input(blue("Willst du dich anmelden oder registrieren? (a/r) ","bold"))
    if auswahl.lower() == "a":
        anmelden(benutzer_collection)
    elif auswahl.lower() == "r":
        registrieren(benutzer_collection)
    else:
        print(red("Ungültige Eingabe."))
    client.close()

#Definiere anmelde Forumlar
def anmelden(benutzer_collection):
    benutzername = input(blue("Gib deinen Benutzernamen ein: "))
    passwort = input(blue("Gib dein Passwort ein: "))
    benutzer = benutzer_collection.find_one({"benutzername": benutzername, "passwort": passwort})
    if benutzer:
        print(blue(f"Herzlich Willkommen zurück {benutzername}"))
    else:
        print(red("Die Email oder das Password ist Falsch."))

#Definiere registrierungs Formular
def registrieren(benutzer_collection):
    benutzername = input(blue("Gib einen Benutzernamen ein: "))
    passwort = input(blue("Gib ein Passwort ein: "))
    benutzer = {"benutzername": benutzername, "passwort": passwort}
    benutzer_collection.insert_one(benutzer)
    print(blue(f"Herzlich Willkommen {benutzername}!"))

verbinde_server()

#Ersetzte <username> , <password> und <Atlas Clusters> durch deine Daten von MongoDB.
