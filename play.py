from logic import Wuzzle

def main():
    wuzzle = Wuzzle("rayan")

    while wuzzle.can_attempt():
        x = input("GUESS: ")
        wuzzle.attempt(x)

    if wuzzle.is_solved():
        print("correct")
    else:
        print("incorrect")

    if not wuzzle.is_solved():
        print(f"Game Over! The word was {wuzzle.secret}")

main()