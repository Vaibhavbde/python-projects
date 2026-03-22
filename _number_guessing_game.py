# ============================================================
# Level 1 - Task 2: Number Guessing Game
# Codveda Python Development Internship
# ============================================================

import random

MAX_ATTEMPTS = 7

def get_guess(attempt, max_attempts):
    """Prompt the user for a valid integer guess between 1 and 100."""
    while True:
        try:
            guess = int(input(f"\nAttempt {attempt}/{max_attempts} - Enter your guess (1-100): "))
            if 1 <= guess <= 100:
                return guess
            print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def play_game():
    print("=" * 45)
    print("       Number Guessing Game")
    print("=" * 45)
    print(f"I'm thinking of a number between 1 and 100.")
    print(f"You have {MAX_ATTEMPTS} attempts. Good luck!\n")

    secret = random.randint(1, 100)
    attempts_used = 0

    for attempt in range(1, MAX_ATTEMPTS + 1):
        guess = get_guess(attempt, MAX_ATTEMPTS)
        attempts_used += 1

        if guess == secret:
            print(f"\n🎉 Correct! You guessed it in {attempts_used} attempt(s)!")
            return
        elif guess < secret:
            print("  ↑ Too low!")
        else:
            print("  ↓ Too high!")

        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"  {remaining} attempt(s) remaining.")

    print(f"\n😞 Out of attempts! The number was {secret}.")

def main():
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
