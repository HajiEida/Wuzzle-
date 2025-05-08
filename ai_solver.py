from collections import defaultdict

class AISolver:
    def __init__(self, word_list):
        self.all_words = word_list
        self.reset()
    
    def reset(self):
        self.possible_words = self.all_words.copy()
        self.guess_history = []
    
    def solve(self, secret_word):
        self.reset()
        solution = []
        
        for attempt in range(6):
            guess, explanation = self._select_guess_with_explanation()
            feedback = self._get_feedback(guess, secret_word)
            
            solution.append({
                'guess': guess,
                'remaining': len(self.possible_words),
                'feedback': feedback,
                'explanation': explanation  # Added this line
            })
            
            if guess == secret_word:
                break
                
            self._apply_constraints(guess, feedback)
        
        return solution
    
    def _select_guess_with_explanation(self):
        if not self.guess_history:
            return "CRANE", "First guess: Using optimal starting word 'CRANE'"
        
        explanation = (f"Choosing from {len(self.possible_words)} possible words\n"
                    "Selected first valid word matching all constraints")
        
        return self.possible_words[0], explanation
    
    def _get_feedback(self, guess, secret):
        feedback = []
        secret_letters = list(secret)
        
        # First check correct positions
        for i in range(5):
            if guess[i] == secret_letters[i]:
                feedback.append('correct')
                secret_letters[i] = None
            else:
                feedback.append(None)
        
        # Then check present letters
        for i in range(5):
            if feedback[i] is None:
                if guess[i] in secret_letters:
                    feedback[i] = 'present'
                    secret_letters[secret_letters.index(guess[i])] = None
                else:
                    feedback[i] = 'absent'
        
        return feedback
    
    def _apply_constraints(self, guess, feedback):
        new_possible = []
        
        for word in self.possible_words:
            keep_word = True
            temp_word = list(word)
            
            # Apply correct position constraints
            for i in range(5):
                if feedback[i] == 'correct':
                    if word[i] != guess[i]:
                        keep_word = False
                        break
                    temp_word[i] = None
            
            if not keep_word:
                continue
                
            # Apply present/absent constraints
            for i in range(5):
                if feedback[i] == 'present':
                    if guess[i] not in temp_word:
                        keep_word = False
                        break
                    temp_word[temp_word.index(guess[i])] = None
                elif feedback[i] == 'absent':
                    if guess[i] in temp_word:
                        keep_word = False
                        break
            
            if keep_word:
                new_possible.append(word)
        
        self.possible_words = new_possible
        self.guess_history.append(guess)