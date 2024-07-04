"""
Awareness Bell Feature of Awareness Buddy App:

This application aids a person's awareness practice by playing a meditation bell sound at every quarter hour.
This bell serves as a reminder to come to the present moment or to breathing.
At the start of every hour, the app reads aloud a random Vipassana quote
along with the meditation bell sound. 

Features:
1. Plays the sound of Tibetan singing bowl every 15 minutes. 
2. At the start of each hour, reads aloud a random Vipassana quote after playing the sound.
3. Displays the same quote at the command prompt window. 

Dependencies:
- pygame: Used for playing sound files.
- pyttsx3: Used for text-to-speech to read aloud quotes.
- random: Used for selecting a random quote from the file.
- datetime: Used for checking the current time.
- time: Used for sleep function to create intervals.
- docx: Used for reading quotes from a Word document.
- tkinter: Used for creating the graphical user interface.

Make sure the sound file and the quotes file paths are correctly specified.
"""

import time
from datetime import datetime
import random
import pyttsx3
import pygame
import docx
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

# Initialize Pygame
pygame.mixer.init()

# Path to the sound and quotes
sound_file = r"D:\Awareness-Buddy\Awareness-Bell\Bell-Sounds\tibetan-singing-bowl.mp3"
quotes_file = r"D:\Awareness-Buddy\Awareness-Bell\vipassana-quotes.docx"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set speech rate (adjusted if needed)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)

# Flag to control the awareness bell loop
running = False

def play_sound():
    """
    Play the Tibetan singing bowl sound.
    """
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

def read_quote():
    """
    Read aloud a random Vipassana quote using text-to-speech.
    """
    try:
        doc = docx.Document(quotes_file)
        quotes = [para.text for para in doc.paragraphs if para.text.strip()]
        if quotes:
            # Select and read a random quote
            quote = random.choice(quotes).strip()
            print(f"Selected Quote: {quote}")  # Print the selected quote
            tts_thread = threading.Thread(target=speak_quote, args=(quote,))
            tts_thread.start()
        else:
            print("No quotes found in the file.")
    except Exception as e:
        print(f"Error reading quotes file: {e}")

def speak_quote(quote):
    """
    Speak the quote using text-to-speech in a separate thread.
    """
    try:
        print(f"Speaking Quote: {quote}")
        engine.say(quote)
        engine.runAndWait()
        print("Finished Speaking Quote")
    except Exception as e:
        print(f"Error with text-to-speech: {e}")

def awareness_bell():
    """
    Main function to control the timing of the awareness bell and quotes.
    Plays the meditation bell sound every 15 minutes.
    Reads a random quote at the start of each hour after playing the sound.
    """
    global running
    while running:
        current_time = datetime.now()
        print(f"Current Time: {current_time}")  # Debugging statement
        if current_time.minute % 15 == 0:  # Check if the current time is at a 15-minute interval
            play_sound()
            if current_time.minute == 0:  # Check if it is the start of the hour
                read_quote()
        time.sleep(60)  # Check every minute

def start_awareness_bell():
    """
    Start the awareness bell loop.
    """
    global running
    if not running:
        running = True
        threading.Thread(target=awareness_bell).start()
        print("Awareness Bell started")  # Debugging statement
    else:
        messagebox.showinfo("Info", "Awareness Bell is already running.")

def stop_awareness_bell():
    """
    Stop the awareness bell loop.
    """
    global running
    if running:
        running = False
        print("Awareness Bell stopped")  # Debugging statement
        messagebox.showinfo("Info", "Awareness Bell has been stopped.")
    else:
        messagebox.showinfo("Info", "Awareness Bell is not running.")

# Create a Tkinter window
root = tk.Tk()
root.title("Awareness Buddy")

# Apply styles using ttk
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.map('TButton', foreground=[('!disabled', 'blue')],
          background=[('!disabled', 'white')],
          relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

# Create Start and Stop buttons using ttk for better appearance
start_button = ttk.Button(root, text="Start", command=start_awareness_bell)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_awareness_bell)
stop_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
