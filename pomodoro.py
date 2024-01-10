import time
import sys
import os
import threading
from pyfiglet import Figlet
from pynput.keyboard import Key, Listener, Controller


running = False


def on_press(key):
    global running
    user_input = str(key).replace("'", "").lower()
    clear_screen()
    if user_input == "s":
        running = True
    else:
        print("Exiting...")
        running = False
        return False


def exit():
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    input()
    clear_screen()
    sys.exit()


def print_start_message():
    clear_screen()
    print_ascii("Pomodoro Timer\n")
    print("Press S to start the timer, or any other key to exit.")
    print(">>>")


def print_ascii(text):
    f = Figlet(font="slant")
    print(f.renderText(text))


def print_countdown(time_left):
    minutes = int(time_left / 60)
    seconds = int(time_left % 60)

    print_ascii("Time Left")
    print(f"{minutes:02d}:{seconds:02d}", end="\r")


def print_time_left(end_time):
    current_time = time.time()
    time_left = end_time - current_time
    print_countdown(time_left)


def start_keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")  # Clear terminal window


def main():
    print_start_message()
    listener_thread = threading.Thread(target=start_keyboard_listener)
    listener_thread.start()

    # Wait for user to start timer or exit
    while True and not running:
        pass

    try:
        end_time = time.time() + 25 * 60
        while running:
            print_time_left(end_time)
            time.sleep(1)
            clear_screen()
        exit()
    except KeyboardInterrupt:
        print("\nProgram exited.")
        sys.exit()


if __name__ == "__main__":
    main()
