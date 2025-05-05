from letters import Letter_state

class Wuzzle:
    max_word_length = 5
    max_attempts = 6

    def __init__(self, secret: str):
        self.secret: str = secret.upper()
        self.attempts = []

    def is_solved(self):
        return bool(self.attempts) and self.attempts[-1] == self.secret

    def attempt(self, word: str):
        self.attempts.append(word.upper())

    def guess(self, word: str):
        word = word.upper()
        result = []

        for i in range(self.max_word_length):
            char = word[i]
            letter = Letter_state(char)
            if char in self.secret:
                letter.in_word = True
            if char == self.secret[i]:
                letter.in_position = True
            result.append(letter)
        return result

    def remaining_attempts(self):
        return self.max_attempts - len(self.attempts)

    def can_attempt(self):
        return self.remaining_attempts() > 0 and not self.is_solved()
