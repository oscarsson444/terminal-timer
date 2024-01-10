import time
import sys
import os
import threading
from playsound import playsound
from pyfiglet import Figlet
from pynput.keyboard import Key, Listener, Controller


running = False
done = False
MINUTES = 25


def on_press(key):
    global running
    user_input = str(key).replace("'", "").lower()
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
    print_in_star_square("Press S to start the timer, or any other key to exit.")


def print_ascii(text):
    f = Figlet(font="slant")
    print(f.renderText(text))


def print_terminal(end_time):
    global done
    current_time = time.time()
    time_left = end_time - current_time
    if time_left <= 0 and not done:
        playsound("done-sound.mp3", False)
        done = True

    if not done:
        minutes = int(time_left / 60)
        seconds = int(time_left % 60)
        print_in_star_square(f"{minutes:02d}:{seconds:02d}")
    else:
        print_in_star_square("Times Up! Press Enter to exit.")


def print_in_star_square(text):
    # Define the width of the square based on the length of the text
    width = 100  # Add 4 to leave some space around the text
    # Define the height of the square
    height = 5  # Adjust this value to change the height of the square

    # Calculate padding for the text
    padding = width - 2 - len(text)
    left_padding = padding // 2
    right_padding = padding - left_padding
    clear_screen()
    print_ascii("Pomodoro Timer")

    # Print top border
    print("*" * width)
    # Print padding lines
    for _ in range((height - 3) // 2):
        print("*" + " " * (width - 2) + "*")
    # Print text line
    print("*" + " " * left_padding + text + " " * right_padding + "*")
    # Print padding lines
    for _ in range((height - 3) // 2):
        print("*" + " " * (width - 2) + "*")
    # Print bottom border
    print("*" * width)


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
        end_time = time.time() + MINUTES * 60
        while running:
            print_terminal(end_time)
            time.sleep(1)

        exit()
    except KeyboardInterrupt:
        print("\nProgram exited.")
        sys.exit()


if __name__ == "__main__":
    main()
