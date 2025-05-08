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
        
        for _ in range(6):  # Max 6 attempts
            guess, explanation = self._make_guess_with_explanation()
            feedback = self._calculate_feedback(guess, secret_word)
            
            solution.append({
                'guess': guess,
                'remaining': len(self.possible_words),
                'explanation': explanation
            })
            
            if guess == secret_word:
                break
                
            self._update_possibilities(guess, feedback)
        
        return solution
    
    def _make_guess_with_explanation(self):
        """Returns guess with percentage-based reasoning"""
        if not self.guess_history:
            return "CRANE", self._get_first_guess_explanation()
        
        if len(self.possible_words) > 1 and self.guess_history[-1] in self.possible_words:
            self.possible_words.remove(self.guess_history[-1])
            explanation = f"🔄 Forced new guess (previous didn't reduce possibilities)\n"

        # Calculate letter frequencies and percentages
        position_stats = self._calculate_position_stats()
        
        # Score words based on letter frequencies
        scored_words = self._score_words(position_stats)
        top_word = scored_words[0][0]

        if len(scored_words) == 1:
            return top_word, f"🎯 Only possible word remaining: {top_word}"

        explanation = self._build_explanation(position_stats, scored_words)
        return top_word, explanation

    def _get_first_guess_explanation(self):
        """Detailed explanation for optimal first guess"""
        return """🎯 First Guess Strategy:
        
CRANE is statistically optimal because:
- Tests 5 distinct letters covering 73% of common letters
- Letter frequencies in position:
  C(4.3%) R(6.8%) A(8.2%) N(5.0%) E(11.2%)
- Maximizes information gain potential"""

    def _calculate_position_stats(self):
        """Calculate letter frequencies and percentages for each position"""
        position_freq = [defaultdict(int) for _ in range(5)]
        total_words = len(self.possible_words)
        
        for word in self.possible_words:
            for i, letter in enumerate(word):
                position_freq[i][letter] += 1
        
        # Convert counts to percentages
        position_stats = []
        for i in range(5):
            stats = {}
            for letter, count in position_freq[i].items():
                stats[letter] = (count, (count/total_words)*100)
            position_stats.append(stats)
        
        return position_stats

    def _score_words(self, position_stats):
        """Score words based on letter position frequencies"""
        scored_words = []
        for word in self.possible_words:
            score = sum(position_stats[i].get(c, (0, 0))[0] for i, c in enumerate(word))
            scored_words.append((word, score))
        
        return sorted(scored_words, key=lambda x: -x[1])

    def _build_explanation(self, position_stats, scored_words):
        """Build detailed percentage-based explanation"""
        total_words = len(self.possible_words)
        explanation = f"🔍 Analyzing {total_words} possible words:\n\n"
        
        # Add position-wise letter percentages
        explanation += "📊 Letter Frequency by Position (%):\n"
        for i in range(5):
            letters = sorted(position_stats[i].items(), 
                           key=lambda x: -x[1][1])[:3]  # Top 3 letters per position
            explanation += f"  Position {i+1}: "
            explanation += ", ".join(f"{ltr}({pct:.1f}%)" for ltr, (cnt, pct) in letters)
            explanation += "\n"
        
        # Add top candidate analysis
        explanation += "\n🏆 Top Candidate Words:\n"
        for rank, (word, score) in enumerate(scored_words[:3], 1):
            letter_info = []
            for i, c in enumerate(word):
                cnt, pct = position_stats[i].get(c, (0, 0))
                letter_info.append(f"{c}({pct:.1f}%)")
            
            explanation += (
                f"{rank}. {word} (Score: {score})\n"
                f"   Letters: {' + '.join(letter_info)}\n"
            )
        
        explanation += f"\n✅ Selected '{scored_words[0][0]}' (highest combined percentage score)"
        return explanation
    
    def _calculate_feedback(self, guess, secret):
        """Precise feedback calculation handling duplicates"""
        feedback = []
        secret = list(secret)
        
        # First pass: Correct positions
        for i in range(5):
            if guess[i] == secret[i]:
                feedback.append('correct')
                secret[i] = None  # Mark as used
            else:
                feedback.append(None)
        
        # Second pass: Present letters
        for i in range(5):
            if feedback[i] is None and guess[i] in secret:
                feedback[i] = 'present'
                secret[secret.index(guess[i])] = None
            elif feedback[i] is None:
                feedback[i] = 'absent'
        
        return feedback
    
    def _update_possibilities(self, guess, feedback):
        """Strict elimination of impossible words"""
        new_possible = []
        for word in self.possible_words:
            valid = True
            temp_word = list(word)
            
            # Check correct positions
            for i in range(5):
                if feedback[i] == 'correct' and word[i] != guess[i]:
                    valid = False
                    break
                elif feedback[i] == 'correct':
                    temp_word[i] = None
            
            # Check present/absent letters
            if valid:
                for i in range(5):
                    if feedback[i] == 'present':
                        if guess[i] not in temp_word:
                            valid = False
                            break
                        temp_word[temp_word.index(guess[i])] = None
                    elif feedback[i] == 'absent' and guess[i] in temp_word:
                        valid = False
                        break
            
            if valid:
                new_possible.append(word)
        
        self.possible_words = new_possible
        self.guess_history.append(guess)