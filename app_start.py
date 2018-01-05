#!/usr/bin/env python
# coding: utf8

import Queue
import threading
import time
from myDeezerApp import *


# Funktion zum einlesen der Benutzereingaben. Diese werden dann der input_queue hinzugefügt
def add_input(input_queue):
    while True:
        user_input = sys.stdin.readline()
        input_queue.put(user_input)


def process_input(app):
    input_queue = Queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    # Auf Benutzereingaben warten, solange die App aktiv ist...
    while app.connection.active or app.player.active:

        # Kleiner Delay...
        time.sleep(0.1)

        # Wenn es in der input_queue neue Benutzereingaben gibt...
        if not input_queue.empty():

            # Nehme Befehle aus der Liste
            command = input_queue.get()

            # Wenn es genau einen Befehl gibt und  der Befehl aus der Liste erlaubter Eingaben stammt, rufe "process_command" des app-Objekts auf
            if len(command) != 2 or command[0] not in "SP+-R?MVvQ":
                print ("INVALID COMMAND")
                log_command_info()
            else:
                app.process_command(command)


def argv_error():
    print ("Please give the content as argument like:")
    print ("""\t"dzmedia:///track/10287076"        (Single track example)""")
    print ("""\t"dzmedia:///album/607845"          (Album example)""")
    print ("""\t"dzmedia:///playlist/1363560485"   (Playlist example)""")
    print ("""\t"dzradio:///radio-220"             (Radio example)""")  # TODO: check for radio
    print ("""\t"dzradio:///user-743548285"        (User Mix example)""")  # TODO: check for user


def log_connect_info(app):
    if app.debug_mode:
        print ("---- Deezer NativeSDK version: {}".format(Connection.get_build_id()))
        print ("---- Application ID: {}".format(app.your_application_id))
        print ("---- Product ID: {}".format(app.your_application_name))


def log_command_info():
    print ("######### MENU #########")
    print ("- Please enter keys for command -")
    print ("\tS : START/STOP")
    print ("\tP : PLAY/PAUSE")
    print ("\t+ : NEXT")
    print ("\t- : PREVIOUS")
    print ("\tR : NEXT REPEAT MODE")
    print ("\t? : TOGGLE SHUFFLE MODE")
    print ("\tM : TOGGLE MUTE")
    print ("\tV : VOLUME UP")
    print ("\tv : VOLUME DOWN")
    print ("\tQ : QUIT")
    print ("########################")


def main():

    # Fehler und Exit, wenn URL-Parameter fehlt.
    if len(sys.argv) != 2:
        argv_error()
        return 1
    
    # MyDeezerApp-Klasse ergibt sich aus myDeezerApp.py. Diese enthält sämtliche Methoden zur Interaktion mit der Deezer API
    app = MyDeezerApp(True)

    # Logging v. allgemeinen Infos zum app-Objekt
    log_connect_info(app)
 
    # Übergabe der URL, die abgespielt werden soll.
    app.set_content(sys.argv[1])

    # Zeige bei Start der Anwendung eine Liste aller möglichen Befehle an
    log_command_info()

    # Rufe Funktion auf, die auf Benutzereingaben wartet und diese an das app-Objekt weitergibt
    process_input(app)

    return 0


if __name__ == "__main__":
    main()
