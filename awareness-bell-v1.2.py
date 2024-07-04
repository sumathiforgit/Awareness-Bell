"""
Awareness Bell Feature of Awareness Buddy App:

This app aids a person's awareness practice by playing a meditation bell sound at every quarter hour.
This bell can serve as a reminder to come to the present moment by observing either the breath or the body sensations.
Additionally, at the start of every hour this app reads aloud a Vipassana quote after the meditation bell sound.

Features:
1. Plays the sound of a meditation bell every 15 minutes.
2. At the start of each hour, reads aloud a Vipassana quote after playing the bell sound.
3. Displays the same quote at the command prompt window.
4. Has a start and a stop button to turn the app on and off.

Dependencies:
- pygame: Used for playing sound files.
- pyttsx3: Used for text-to-speech to read aloud quotes.
- random: Used for selecting a random quote from the file.
- time: Used for sleep function to create intervals.
- tkinter: Used for creating the graphical user interface.
- os: Used for operating system related tasks.
- docx: Used for reading quotes from a Word document.

Make sure the sound file and the quotes file paths are correctly specified.
"""

import os
import time
import random
import pygame
import pyttsx3
import threading
import tkinter as tk
from tkinter import messagebox
from docx import Document

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Path to the sound and quotes files:
bell_sound_path = r"D:\Awareness-Buddy\Awareness-Bell\Bell-Sounds\simple-bell.mp3"
quotes_file_path = r"D:\Awareness-Buddy\Awareness-Bell\vipassana-quotes.docx"

# Global variable to control the running state of the app
running = False

# Function to play the meditation bell sound
def play_bell_sound():
    """
    Initialize the pygame mixer and play the bell sound.
    This function will wait until the sound finishes playing.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(bell_sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Wait until the sound finishes playing

# Function to read and return a random Vipassana quote
def get_random_quote():
    """
    Read quotes from the quotes file and return a random quote.
    """
    doc = Document(quotes_file_path)
    quotes = [para.text for para in doc.paragraphs if para.text.strip() != ""]
    return random.choice(quotes).strip()  # Return a random quote without leading/trailing whitespace

# Function to read aloud a quote
def read_aloud(quote):
    """
    Use the pyttsx3 text-to-speech engine to read aloud the provided quote.
    """
    engine.say(quote)
    engine.runAndWait()

# Function to display a quote
def display_quote(quote):
    """
    Display the provided quote in a message box.
    """
    messagebox.showinfo("Vipassana Quote", quote)

# Main function to control the awareness bell
def awareness_bell():
    """
    Main loop to control the awareness bell. Plays the bell sound every 15 minutes
    and reads aloud and displays a random quote every hour.
    """
    global running
    last_hour = -1  # Variable to track the last hour when a quote was read
    while running:
        current_time = time.localtime()  # Get the current local time

        # Print time only when specific conditions are met for debugging
        if current_time.tm_min % 15 == 0 and current_time.tm_sec == 0:
            print(f"Current Time: {current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}")

            play_bell_sound()  # Play the bell sound

            # Check if it's the top of the hour and if it hasn't been handled already
            if current_time.tm_min == 0 and current_time.tm_hour != last_hour:
                last_hour = current_time.tm_hour  # Update last_hour to the current hour
                quote = get_random_quote()  # Get a random quote
                read_aloud(quote)  # Read the quote aloud
                print(f"Quote at {current_time.tm_hour}:00 - {quote}")  # Debugging statement
                display_quote(quote)  # Display the quote in a message box

            time.sleep(60)  # Wait for 60 seconds to avoid multiple triggers within the same minute
        time.sleep(1)  # Check the time every second

# Function to start the awareness bell
def start_awareness_bell():
    """
    Start the awareness bell by running the main loop in a separate thread.
    """
    global running
    if not running:
        running = True
        messagebox.showinfo("Awareness Bell", "Awareness Bell started.")
        awareness_thread = threading.Thread(target=awareness_bell)
        awareness_thread.start()

# Function to stop the awareness bell
def stop_awareness_bell():
    """
    Stop the awareness bell by setting the running flag to False.
    """
    global running
    if running:
        running = False
        messagebox.showinfo("Awareness Bell", "Awareness Bell stopped.")

# Set up the GUI
root = tk.Tk()
root.title("Awareness Bell")

# Start button
start_button = tk.Button(root, text="Start", command=start_awareness_bell)
start_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_awareness_bell)
stop_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
