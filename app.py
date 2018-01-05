import queue as Queue
import threading
import time
from myDeezerApp import *


def add_input(input_queue):
    while True:
        user_input = sys.stdin.readline()
        input_queue.put(user_input)


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
    app.set_content(sys.argv[1])

    return 0


if __name__ == "__main__":
    main()
