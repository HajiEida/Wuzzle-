class Wuzzle:
    # for now 
    max_word_length = 5
    max_attempts = 6

    def __init__(self, secret: str):
        self.secret: str = secret
        self.attempts = []

    def is_solved(self):
        if len(self.attempts) > 0 and self.attempts[-1] == self.secret:
            return True
        else:
            return False

    def attempt(self, word: str):
        self.attempts.append(word)

    def remaining_attempts(self) -> int:
        return self.max_attempts - len(self.attempts)

    def can_attempt(self):
        if self.remaining_attempts() > 0 and not self.is_solved():
            return True
        else:
            return False