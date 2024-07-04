import time
from datetime import datetime
import random
import pyttsx3
import pygame
import docx

# Initialize Pygame
pygame.mixer.init()

# Path to the sound and quotes
sound_file = r"D:\Awareness-Buddy\Awareness-Bell\Bell-Sounds\tibetan-singing-bowl.mp3"
quotes_file = r"D:\Awareness-Buddy\Awareness-Bell\vipassana-quotes.docx"

# Initialize text-to-speech engine
engine = pyttsx3.init()

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
            print(f"Selected Quote: {quote}")  # Minimal debugging
            engine.say(quote)
            engine.runAndWait()
        else:
            print("No quotes found in the file.")
    except Exception as e:
        print(f"Error reading quotes file: {e}")

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
