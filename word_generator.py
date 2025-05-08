import random
from collections import Counter
import nltk
from nltk.corpus import words as nltk_words


<<<<<<< HEAD
nltk.download('words')
class WordGenerator:
    def __init__(self):
        self.valid_words = [w.upper() for w in nltk_words.words() if len(w) == 5 and w.isalpha()]
        
=======
nltk.download('words')  # Downloads the word list
class WordGenerator:
    def __init__(self):
        # Get all 5-letter English words
        self.valid_words = [w.upper() for w in nltk_words.words() if len(w) == 5 and w.isalpha()]
        
        # Train the probability model
>>>>>>> c597c766b55d878585fbcac52927805ffbd8d61d
        self.position_probs = self._train_probability_model()

    def _train_probability_model(self):
        """Calculate how often each letter appears in each position"""
<<<<<<< HEAD
        position_probs = [{} for _ in range(5)]

        for pos in range(5):
            counter = Counter(word[pos] for word in self.valid_words)
            total_letters = sum(counter.values())
            
=======
        position_probs = [{} for _ in range(5)]  # One dict per letter position

        for pos in range(5):  # For each letter position (1st-5th)
            # Count how often each letter appears in this position
            counter = Counter(word[pos] for word in self.valid_words)
            total_letters = sum(counter.values())
            
            # Calculate probability for each letter in this position
>>>>>>> c597c766b55d878585fbcac52927805ffbd8d61d
            position_probs[pos] = {char: count/total_letters 
                                    for char, count in counter.items()}
        return position_probs

    def generate_word(self):
        """Generate a word using letter probabilities"""
<<<<<<< HEAD
        for _ in range(100):
=======
        for _ in range(100):  # Try up to 100 times
            # Build a word letter by letter using probabilities
>>>>>>> c597c766b55d878585fbcac52927805ffbd8d61d
            letters = [
                random.choices(
                    list(self.position_probs[pos].keys()),
                    weights=list(self.position_probs[pos].values())
                )[0]
                for pos in range(5)
            ]
            candidate = ''.join(letters)
            
<<<<<<< HEAD
            if candidate in self.valid_words:
                return candidate
        
        return random.choice(self.valid_words)

=======
            # Only return if it's a real word
            if candidate in self.valid_words:
                return candidate
        
        # Fallback to random selection if no valid word generated
        return random.choice(self.valid_words)
>>>>>>> c597c766b55d878585fbcac52927805ffbd8d61d
