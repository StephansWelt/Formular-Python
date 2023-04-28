import pymongo
import time
import os
import random
import string
from simple_colors import *

#definiere verbindung zum Server | Abfrage für Anmelden oder registrieren
def verbinde_server():
    print(red("Verbinde zum Server..."))
    client = pymongo.MongoClient("mongodb+srv://<username>:<password>@blitzbot.k3jmp5m.mongodb.net/test?retryWrites=true&w=majority")
    db = client["meine_db"]
    benutzer_collection = db["benutzer"]
    time.sleep(1)
    auswahl = input(blue("Willst du dich anmelden oder registrieren? (a/r) ","bold"))
    if auswahl.lower() == "a":
        anmelden(benutzer_collection)
    elif auswahl.lower() == "r":
        registrieren(benutzer_collection)
    else:
        print(red("Ungültige Eingabe."))
    client.close()

#Definiere anmelde Formular
def anmelden(benutzer_collection):
    benutzername = input(green("Gib deinen Benutzernamen ein: "))
    benutzer = benutzer_collection.find_one({"benutzername": benutzername})
    if not benutzer:
        print(red("Benutzername nicht gefunden."))
        return

    if benutzer.get("locked"):
        print(red("Konto gesperrt. Bitte kontaktiere den Adminstrator."))
        return
    if benutzername == "EinfxchPingu":
        benutzername = f"Admin | {benutzername}"

    while True:
        passwort = input(green("Gib dein Passwort ein: "))
        if passwort != benutzer.get("passwort"):
            print(red("Falsches Passwort."))
            benutzer["login_attempts"] = benutzer.get("login_attempts", 0) + 1
            if benutzer["login_attempts"] >= 3:
                benutzer["locked"] = True
                print(red("Du hast zu offt das Falsche Password eingetragen und dein Account wurde gesperrt. Bitte wende dich an den support!"))
            benutzer_collection.update_one({"benutzername": benutzername}, {"$set": benutzer})
            if benutzer.get("locked"):
                return
        else:
            print(blue(f"Herzlich Willkommen zurück {benutzername}"))
            Hauptmenü(benutzername, benutzer_collection)
            break


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
    time.sleep(1)
    Hauptmenü(benutzername, benutzer_collection)
    if benutzername == "EinfxchPingu":
        benutzername = f"Admin | {benutzername}"

# Funktion zur Generierung eines zufälligen Codes
def generiere_code():
    code_laenge = 12
    zeichen = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(zeichen) for i in range(code_laenge))

# Funktion zum Entsperren eines Benutzers
# Funktion zum Entsperren eines Benutzers
# Funktion zum Entsperren eines Benutzers
def entsperren(benutzername, benutzer_collection):
    if benutzername == "EinfxchPingu":
        if input(blue("Möchtest du einen Benutzer entsperren? (j/n) ")) == "j":
            benutzername = input(green("Gib den Benutzernamen des zu entsperrenden Benutzers ein: "))
            benutzer = benutzer_collection.find_one({"benutzername": benutzername})
            if not benutzer:
                print(red("Benutzername nicht gefunden."))
                return
                if not benutzer.get("locked"):
                    print(blue("Dieser Benutzer ist nicht gesperrt."))
                    return
                    benutzer["locked"] = False
                    benutzer["login_attempts"] = 0
                    benutzer_collection.update_one({"benutzername": benutzername}, {"$set": benutzer})
                    print(blue(f"Der Benutzer {benutzername} wurde erfolgreich entsperrt."))
    else:
        print(red("Dazu hast du keine Rechte!"))

def Hauptmenü(benutzername, benutzer_collection):
    print()
    print(blue("HAUPTMENÜ"))
    print(black("------------"))
    print(green("1) Einstellungen"))
    print(green("2) KOMMT BALD"))
    print(green("3) KOMMT BALD"))
    Eingabe = input()
    if Eingabe == "1":
        print()
        print(blue("EINSTELLUNGEN"))
        print(black("------------"))
        print(green("1) Bentutzernamen ändern"))
        print(green("2) Benutzer entsperren"))
        print(green("3) Konto löschen"))
        Eingabe2 = input()
        if Eingabe2 == "1":
            print("Bald verfügbar")
        if Eingabe2 == "2":
            entsperren(benutzername, benutzer_collection)
        if Eingabe2 == "3":
            sicher = input(red("Sicher? J/N: "))
            if sicher == "J":
                myquery = { "benutzername": benutzername }
                benutzer_collection.delete_one(myquery)
                print(blue(f"{benutzername} wurde gelöscht."))
            if sicher == "N":
                print(red("Gute Entscheidung!"))
                print()
                Hauptmenü(benutzername, benutzer_collection)

verbinde_server()
