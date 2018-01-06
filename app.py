import queue as Queue
import threading
import time
from myDeezerApp import *


app = None
current_url = None
last_url = None

def get_RFID_content():
    return "dzmedia:///track/10287076"

def add_input(input_queue):
    while True:
        """
        MUSIC CONTROL OVER RFID-CHIP
        """

        RFID = get_RFID_content()

        if RFID is not None:
            # An RFID-Card is inserted

            if RFID != current_url:
                # A RFID-Chip was inserted; set as new URL to play!
                current_url = RFID

                # Check if it is a new one (then set new content) or if chip was reinserted (then: continue play)
                if RFID == last_url:
                    # Continue playing
                    print("Continue Song")
                    input_queue.put("P")
                else:
                    # Entirely new Chip; Start new Song
                    print("Start New Song")
                    app.set_content(RFID)

        else:
            # No RFID-Card is inserted; Check the last Status of current_url

            if current_url is not None:
                # Issue Command to Pause music and set current_url to None
                print("Pause Playing")
                input_queue.put("P")
                last_url = current_url
                current_url = None

        #user_input = sys.stdin.readline()

        """
        OTHER BUTTON CONTROL
        """


def main():

    # Init app Object
    app = MyDeezerApp(True)
    print("---- Deezer NativeSDK version: {}".format(Connection.get_build_id()))
    print("---- Application ID: {}".format(app.your_application_id))
    print("---- Product ID: {}".format(app.your_application_name))

    # Init Command Queue
    input_queue = Queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    # Wait for User Input
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
            else:
                app.process_command(command)

    # Übergabe der URL, die abgespielt werden soll.
    #app.set_content(sys.argv[1])

    return 0


if __name__ == "__main__":
    main()
