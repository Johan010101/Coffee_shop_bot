import pyttsx3
import random
import time

def speak(text, rate=140, use_random_effects=True, volume=1.0):
    """Speaks the given text with enhanced random effects."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    if use_random_effects:
        apply_random_effects(engine, text)
    else:
        engine.say(text)

    engine.runAndWait()
    engine.stop()

def apply_random_effects(engine, text):
    """Applies a wider range of random speech effects to the text."""
    words = text.split()
    new_words = []
    for i, word in enumerate(words):
        new_words.append(word)

        # Pause after punctuation
        if word.endswith(('.', ',', '!', '?')) and random.random() < 0.5:
          time.sleep(random.uniform(0.3, 0.6))

        # Random interjection
        if random.random() < 0.1:  # 10% chance
            interjection = random.choice(["uh", "um", "err", "like", "you know", "well"])
            new_words