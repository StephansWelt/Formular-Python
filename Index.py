import pymongo
import time
import os
import string
import random
from simple_colors import *

#definiere verbindung zum Server | Abfrage für Anmelden oder registrieren
def verbinde_server():
    print(red("Verbinde zum Server..."))
    try:
        client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<closter>.k3jmp5m.mongodb.net/test?retryWrites=true&w=majority")
        db = client["mein_db"]
    except pymongo.errors.ConnectionFailure as e:
        print("Verbindung zur MongoDB-Datenbank konnte nicht hergestellt werden:", e)
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
    if benutzername != "EinfxchPingu":
        if benutzer.get("locked"):
            print(red("Konto gesperrt. Bitte kontaktiere den Support."))
            return

    while True:
        passwort = input(green("Gib dein Passwort ein: "))
        if passwort != benutzer.get("passwort"):
            print(red("Falsches Passwort."))
            benutzer["login_attempts"] = benutzer.get("login_attempts", 0) + 1
            if benutzername != "EinfxchPingu":
                if benutzer["login_attempts"] >= 3:
                    benutzer["locked"] = True
                    print(red("Zu viele falsche Anmeldeversuche. Konto gesperrt."))
                benutzer_collection.update_one({"benutzername": benutzername}, {"$set": benutzer})
                if benutzer.get("locked"):
                    return
        else:
            print(blue(f"Herzlich Willkommen zurück {benutzername}"))
            Hauptmenü(benutzername, benutzer_collection)
            break


#Definiere registrierungs Formular
def registrieren(benutzer_collection):
    while True:
        benutzername = input(green("Gib einen Benutzernamen ein: "))
        benutzer = benutzer_collection.find_one({"benutzername": benutzername})
        if benutzer:
            print(red("Dieser Benutzername ist bereits registriert. Bitte versuche es erneut."))
        else:
            break
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
def entsperren(benutzername, benutzer_collection):
    if benutzername == "EinfxchPingu":
        print(green("Willkommen, Admin!"))
        if input(blue("Möchtest du einen Benutzer entsperren? (j/n) ")) == "j":
            benutzername = input(green("Gib den Benutzernamen des zu entsperrenden Benutzers ein: "))
            benutzer = benutzer_collection.find_one({"benutzername": benutzername})
            if not benutzer:
                print(red("Benutzername nicht gefunden."))
                return
            if not benutzer.get("locked"):
                print(red("Dieser Benutzer ist nicht gesperrt."))
                return
            benutzer["locked"] = False
            benutzer["login_attempts"] = 0
            benutzer_collection.update_one({"benutzername": benutzername}, {"$set": benutzer})
            print(blue(f"Der Benutzer {benutzername} wurde erfolgreich entsperrt."))
    else:
        print(red("Dazu hast du keine Rechte!"))
        Hauptmenü(benutzername, benutzer_collection)
        
        
        
def alle_accounts_loeschen(benutzer_collection, benutzername):
    if benutzername == "EinfxchPingu":
        if input(red("Möchtest du wirklich alle Benutzerkonten löschen? (j/n) ")) == "j":
            benutzer_collection.delete_many({})
            print(green("Alle Benutzerkonten wurden gelöscht! Einen Schönen Tag noch EinfxchPingu"))
        else:
            print(blue("Das Löschen aller Benutzerkonten wurde abgebrochen."))
    else:
        print(red("Dazu hast du keine Rechte!"))
        Hauptmenü(benutzername, benutzer_collection)



def alle_benutzer_anzeigen(benutzer_collection, benutzername):
    if benutzername == "EinfxchPingu":
        benutzer = benutzer_collection.find({})
        for b in benutzer:
            print(b)
    else:
        print(red("Dazu hast du keine Rechte!"))
        Hauptmenü(benutzername, benutzer_collection)



def Hauptmenü(benutzername, benutzer_collection):
    print()
    print(blue("HAUPTMENÜ"))
    print(black("------------"))
    print(red("1) Admin"))
    print(green("2) KOMMT BALD"))
    print(green("3) KOMMT BALD"))
    Eingabe = input()
    if Eingabe == "1":
        print()
        print(red("ADMIN - EINSTELLUNGEN", "bold"))
        print(black("------------"))
        print(green("1) Liste aller Benutzer"))
        print(green("2) Benutzer entsperren"))
        print(red("3) Konto löschen"))
        print(red("4) Alle Konten löschen"))
        
        Eingabe2 = input()
        if Eingabe2 == "1":
            alle_benutzer_anzeigen(benutzer_collection, benutzername)
        if Eingabe2 == "2":
            entsperren(benutzername, benutzer_collection)
        if Eingabe2 == "4":
            alle_accounts_loeschen(benutzer_collection, benutzername)
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
