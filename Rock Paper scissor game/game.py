import random

def get_user_choice():
    while True:
        user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ['rock', 'paper', 'scissors']:
            return user_choice
        else:
            print("Invalid choice. Please enter rock, paper, or scissors.")

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    outcomes = {'rock': {'rock': 0, 'paper': -1, 'scissors': 1},
                'paper': {'rock': 1, 'paper': 0, 'scissors': -1},
                'scissors': {'rock': -1, 'paper': 1, 'scissors': 0}}
    result = outcomes[user_choice][computer_choice]
    if result == 0:
        return "It's a tie!", 0
    elif result == 1:
        return "You win!", 1
    else:
        return "Computer wins!", -1

def print_results(user_choice, computer_choice, result):
    print(f"\nYou chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")
    print(result)

def main():
    print("Welcome to Rock, Paper, Scissors!")
    rounds = int(input("Enter the number of rounds you want to play: "))
    user_score = computer_score = ties = 0
    
    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}:")
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        
        result, score = determine_winner(user_choice, computer_choice)
        user_score += score if score == 1 else 0
        computer_score += score if score == -1 else 0
        ties += score if score == 0 else 0
        
        print_results(user_choice, computer_choice, result)
        print(f"\nCurrent Score - You: {user_score}, Computer: {computer_score}, Ties: {ties}")
    
    print("\nGame Over!")
    print(f"Final Score - You: {user_score}, Computer: {computer_score}, Ties: {ties}")

if __name__ == "__main__":
    main()
