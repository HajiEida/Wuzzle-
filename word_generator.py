import random
from collections import Counter
import nltk
from nltk.corpus import words as nltk_words


nltk.download('words') 
class WordGenerator:
    def __init__(self):
        self.valid_words = []

        for word in nltk_words.words():
            if len(word) == 5 and word.isalpha():
                self.valid_words.append(word.upper())
        
        self.position_probs = self._train_probability_model()

    def _train_probability_model(self):
        position_probs = []

        for i in range(5):
            position_probs.append({}) 

        for pos in range(5):  
            counter = Counter()

            for word in self.valid_words:
                letter = word[pos]  
                counter[letter] += 1  
            total_letters = sum(counter.values())
            
            position_prob_dict = {}

            for char, count in counter.items():
                probability = count / total_letters
                position_prob_dict[char] = probability
                position_probs[pos] = position_prob_dict
        return position_probs

    def generate_word(self):

        while True:
            letters = []
            for pos in range(5):  
                possible_letters = list(self.position_probs[pos].keys())
                letter_weights = list(self.position_probs[pos].values())
                
                chosen_letter = random.choices(possible_letters, weights=letter_weights)[0]
                letters.append(chosen_letter)
            
            candidate = ''.join(letters)
            
            if candidate in self.valid_words:
                return candidate
            