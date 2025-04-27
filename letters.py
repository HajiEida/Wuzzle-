class Letter_state:
    def __init__(self, character: str):
        self.character: str = character
        self.in_word: bool = False
        self.in_position: bool = False


    def __repr__(self):
        status = f"{self.character} is in word:{self.in_word}   is in position:{self.in_position}"
        return status