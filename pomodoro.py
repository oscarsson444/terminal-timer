import time
import sys
import os
from pyfiglet import Figlet
from pynput.keyboard import Key, Listener, Controller
from colorama import Fore, Style
import simpleaudio

running = None
done = True
MINUTES = 1
END_TIME = 0

wave_obj = simpleaudio.WaveObject.from_wave_file("done-sound.wav")


def on_press(key):
    global running
    global done
    global END_TIME
    user_input = str(key).replace("'", "").lower()
    if user_input == "s":
        print("Starting...")
        END_TIME = time.time() + 5
        running = True
        done = False
        return False


def exit():
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    input()
    clear_screen()
    sys.exit()


def print_start_message():
    print_in_star_square("Press S to start the timer and Ctrl+C to exit.")


def print_ascii(text):
    f = Figlet(font="slant", width=100)
    print(Fore.BLUE + f.renderText(text))
    Style.RESET_ALL


def print_terminal(end_time):
    global done
    current_time = time.time()
    time_left = end_time - current_time
    play_obj = None
    if time_left <= 0 and not done:
        play_obj = wave_obj.play()
        done = True

    if not done:
        minutes = int(time_left / 60)
        seconds = int(time_left % 60)
        print_in_star_square(f"{minutes:02d}:{seconds:02d}", time_left)
        time.sleep(1)
    else:
        print_in_star_square("Times Up! Press Ctrl+C to exit or S to restart.")
        start_keyboard_listener()
        if play_obj is not None:
            play_obj.stop()


def print_in_star_square(text, time_left=None):
    # Define the width of the square based on the length of the text
    width = 85  # Add 4 to leave some space around the text
    # Define the height of the square
    height = 5  # Adjust this value to change the height of the square

    # Calculate padding for the text
    padding = width - 2 - len(text)
    left_padding = padding // 2
    right_padding = padding - left_padding
    progress = 0
    if time_left is not None:
        progress = (MINUTES * 60 - time_left) / (MINUTES * 60)

    clear_screen()
    print_ascii("Pomodoro Timer")

    # Print top border
    print(Fore.GREEN + "*" * int(width * progress), end="")
    print(Style.RESET_ALL + "*" * int(width * (1 - progress)))
    # Print padding lines
    for _ in range((height - 3) // 2):
        print("*" + " " * (width - 2) + "*")
    # Print text line
    print("*" + " " * left_padding + text + " " * right_padding + "*")
    # Print padding lines
    for _ in range((height - 3) // 2):
        print("*" + " " * (width - 2) + "*")
    # Print bottom border
    print(Fore.GREEN + "*" * int(width * progress), end="")
    print(Style.RESET_ALL + "*" * int(width * (1 - progress)))


def start_keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")  # Clear terminal windows


def main():
    try:
        print_start_message()
        start_keyboard_listener()

        while running:
            print_terminal(END_TIME)

        exit()
    except KeyboardInterrupt:
        print("\nProgram exited.")
        exit()


if __name__ == "__main__":
    main()
