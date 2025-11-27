import random
import time
import os

def save_score(game, score):
    file = open("brain_scores.txt", "a")
    file.write(f"{game},{score},{time.strftime('%Y-%m-%d')}\n")
    file.close()

def show_history():
    if not os.path.exists("brain_scores.txt"):
        print("No history yet!")
        return
    
    print("\n--- Your Progress ---")
    file = open("brain_scores.txt", "r")
    data = file.readlines()
    file.close()
    
    count = 0
    for line in data:
        if count >= len(data) - 10:
            info = line.strip().split(",")
            print(f"{info[0]}: {info[1]} points on {info[2]}")
        count = count + 1
    input("\nPress Enter to continue...")

def memory_game():
    print("\n=== MEMORY TEST ===")
    print("Remember the numbers that appear!")
    time.sleep(2)
    
    difficulty = 3
    points = 0
    
    round_num = 0
    while round_num < 5:
        nums = []
        i = 0
        while i < difficulty:
            nums.append(random.randint(0, 9))
            i = i + 1
        
        print("\nRemember these:")
        num_str = ""
        for n in nums:
            num_str = num_str + str(n) + " "
        print(num_str)
        time.sleep(2 + difficulty * 0.5)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\nWhat were the numbers? (space separated)")
        user_input = input("Your answer: ")
        
        user_nums = user_input.split()
        is_correct = True
        
        if len(user_nums) != len(nums):
            is_correct = False
        else:
            i = 0
            while i < len(nums):
                if int(user_nums[i]) != nums[i]:
                    is_correct = False
                    break
                i = i + 1
        
        if is_correct == True:
            print("Correct! +10 points")
            points = points + 10
            difficulty = difficulty + 1
        else:
            correct_ans = ""
            for n in nums:
                correct_ans = correct_ans + str(n) + " "
            print(f"Wrong! It was: {correct_ans}")
            break
        
        round_num = round_num + 1
    
    print(f"\nFinal Score: {points}")
    save_score("Memory", points)
    input("Press Enter to continue...")

def reaction_game():
    print("\n=== REACTION SPEED TEST ===")
    print("Press Enter as FAST as you can when you see GO!")
    time.sleep(2)
    
    total = 0
    
    i = 0
    while i < 5:
        print("\nGet ready...")
        wait_time = random.uniform(1, 4)
        time.sleep(wait_time)
        
        print("GO!")
        start_time = time.time()
        input()
        end_time = time.time()
        
        react_time = end_time - start_time
        total = total + react_time
        print(f"Your time: {react_time:.3f} seconds")
        time.sleep(1)
        i = i + 1
    
    average = total / 5
    points = int(max(0, 100 - (average * 50)))
    
    print(f"\nAverage reaction time: {average:.3f} seconds")
    print(f"Score: {points}")
    save_score("Reaction", points)
    input("Press Enter to continue...")

def pattern_game():
    print("\n=== PATTERN RECOGNITION ===")
    print("Find the next number in the sequence!")
    time.sleep(2)
    
    points = 0
    
    all_patterns = [
        ([2, 4, 6, 8], 10),
        ([5, 10, 15, 20], 25),
        ([1, 2, 4, 8], 16),
        ([3, 6, 9, 12], 15),
        ([10, 20, 30, 40], 50)
    ]
    
    random.shuffle(all_patterns)
    
    round_count = 0
    while round_count < 3:
        sequence = all_patterns[round_count][0]
        correct_answer = all_patterns[round_count][1]
        
        print(f"\nRound {round_count + 1}")
        seq_str = ""
        for num in sequence:
            seq_str = seq_str + str(num) + ", "
        seq_str = seq_str[:-2]
        print(f"Sequence: {seq_str}")
        
        user_guess = int(input("What's the next number? "))
        
        if user_guess == correct_answer:
            print("Correct! +15 points")
            points = points + 15
        else:
            print(f"Wrong! Answer was {correct_answer}")
        
        round_count = round_count + 1
    
    print(f"\nFinal Score: {points}")
    save_score("Pattern", points)
    input("Press Enter to continue...")

def typing_game():
    print("\n=== HACKER TYPING CHALLENGE ===")
    print("Type the strings EXACTLY as shown, as fast as you can!")
    time.sleep(2)
    
    points = 0
    total_seconds = 0
    
    round_no = 0
    while round_no < 5:
        str_length = random.randint(6, 12)
        random_string = ""
        
        letters = "abcdefghijklmnopqrstuvwxyz"
        j = 0
        while j < str_length:
            random_string = random_string + random.choice(letters)
            j = j + 1
        
        print(f"\n--- Round {round_no + 1} ---")
        print(f"Type this: {random_string}")
        
        start = time.time()
        user_typed = input(">>> ")
        end = time.time()
        
        time_elapsed = end - start
        total_seconds = total_seconds + time_elapsed
        
        if user_typed == random_string:
            bonus = max(0, 20 - int(time_elapsed * 2))
            round_points = 15 + bonus
            print(f"Perfect! +{round_points} points ({time_elapsed:.2f}s)")
            points = points + round_points
        else:
            print(f"Wrong! You typed: {user_typed}")
            print(f"Correct was: {random_string}")
        
        round_no = round_no + 1
    
    avg = total_seconds / 5
    print(f"\nAverage typing speed: {avg:.2f} seconds")
    print(f"Final Score: {points}")
    save_score("Typing", points)
    input("Press Enter to continue...")

def main():
    print("=" * 40)
    print("   ATTENTION SPAN TRAINER")
    print("   Brain Training Mini Games")
    print("=" * 40)
    
    running = True
    while running:
        print("\n--- MAIN MENU ---")
        print("1. Memory Test")
        print("2. Reaction Speed")
        print("3. Pattern Recognition")
        print("4. Hacker Typing Challenge")
        print("5. View Progress")
        print("6. Exit")
        
        user_choice = input("\nChoose a game (1-6): ")
        
        if user_choice == "1":
            memory_game()
        elif user_choice == "2":
            reaction_game()
        elif user_choice == "3":
            pattern_game()
        elif user_choice == "4":
            typing_game()
        elif user_choice == "5":
            show_history()
        elif user_choice == "6":
            print("\nThanks for training your brain!")
            running = False
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()