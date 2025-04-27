from logic import Wuzzle

def main():
    wuzzle = Wuzzle("rayan")

    while wuzzle.can_attempt():
        x = input("GUESS: ")

        if len(x) != wuzzle.max_word_length:
            print(f"Word must be of {wuzzle.max_word_length} LETTERS")
            continue
        
        wuzzle.attempt(x)
        result = wuzzle.guess(x)
        print(*result, sep="\n")
    if wuzzle.is_solved():
        print("correct")
    else:
        print("incorrect")

    if not wuzzle.is_solved():
        print(f"Game Over! The word was {wuzzle.secret}")

main()