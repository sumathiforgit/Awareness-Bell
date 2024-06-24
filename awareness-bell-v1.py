"""
Awareness Buddy App - Awareness Bell Feature

This application is designed to aid awareness practice by playing a meditation bell sound 
as a reminder to come to the present moment or breathing at every quarter hour. 
At the start of every hour, the app reads aloud a random Vipassana quote
along with the meditation bell sound. 

Features:
1. Plays the meditation bell sound of Tibetan singing bowl every 15 minutes. 
2. At the start of each hour, reads aloud a random Vipassana quote after playing the sound.
3. Uses 'pygame' library for sound playback.
4. Uses 'pyttsx3' library for text-to-speech functionality.

Dependencies:
- pygame: Used for playing sound files.
- pyttsx3: Used for text-to-speech to read aloud quotes.
- random: Used for selecting a random quote from the file.
- datetime: Used for checking the current time.
- time: Used for sleep function to create intervals.

Make sure the sound file and the quotes file paths are correctly specified.
"""

import time
import os
from datetime import datetime
import random
import pyttsx3
import pygame
import docx

# Initialize Pygame
pygame.mixer.init()

# Path to the sound and quotes
sound_file = r"D:\Awareness Buddy\Awareness Bell\Bell Sounds\tibetan-singing-bowl.mp3"
quotes_file = r"D:\Awareness Buddy\Awareness Bell\Vipassana Quotes\vipassana-quotes.docx"

# Initialize text-to-speech engine
engine = pyttsx3.init()

def play_sound():
    """
    Play the Tibetan singing bowl sound.
    """
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def read_quote():
    """
    Read aloud a random Vipassana quote using text-to-speech.
    """
    with open(quotes_file, 'r', encoding='utf-8') as file:
        quotes = file.readlines()
    quote = random.choice(quotes).strip()
    engine.say(quote)
    engine.runAndWait()

def main():
    """
    Main function to control the timing of the awareness bell and quotes.
    Plays the meditation bell sound every 15 minutes.
    Reads a random quote at the start of each hour after playing the sound.
    """
    while True:
        current_time = datetime.now()
        if current_time.minute % 15 == 0:  # Check if the current time is at a 15-minute interval
            play_sound()
            if current_time.minute == 0:  # Check if it is the start of the hour
                read_quote()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
