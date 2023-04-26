import pymongo
import time
import os
from simple_colors import *

#definiere verbindung zum Server | Abfrage für Anmelden oder registrieren
def verbinde_server():
    print(red("Verbinde zum Server..."))
    client = pymongo.MongoClient("mongodb+srv://PythonAF:PythonAF@<Atlas Clusters>.k3jmp5m.mongodb.net/test?retryWrites=true&w=majority")
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
    benutzername = input(green("Gib deinen Benutzernamen ein: "))
    passwort = input(green("Gib dein Passwort ein: "))
    benutzer = benutzer_collection.find_one({"benutzername": benutzername, "passwort": passwort})
    if benutzer:
        print(blue(f"Herzlich Willkommen zurück {benutzername}"))
        Hauptmenü(benutzername, benutzer_collection)
    else:
        print(red("Die Email oder das Password ist Falsch."))
        print(blue("Bitte widerhole die Anmeldung","bold"))
        print(blue("--------------------------"))
        anmelden(benutzer_collection)

#Definiere registrierungs Formular
def registrieren(benutzer_collection):
    benutzername = input(green("Gib einen Benutzernamen ein: "))
    while True:
        passwort = input(green("Gib ein Passwort ein (mindestens 5 Zeichen): "))
        if len(passwort) < 5:
            print(red("Das Passwort muss mindestens 5 Zeichen lang sein."))
        else:
            break
    benutzer = {"benutzername": benutzername, "passwort": passwort}
    benutzer_collection.insert_one(benutzer)
    print(blue(f"Herzlich Willkommen {benutzername}!"))
    Hauptmenü(benutzername, benutzer_collection)

def Hauptmenü(benutzername, benutzer_collection):
    print()
    print(blue("HAUPTMENÜ"))
    print(black("------------"))
    print(green("1) Konto löschen"))
    Eingabe12 = input()
    if Eingabe12 == "1":
        myquery = { "benutzername": benutzername }
        benutzer_collection.delete_one(myquery)
        print(blue(f"{benutzername} wurde gelöscht."))
        verbinde_server()

verbinde_server()

