import os
import json
import sys
import random
import time

test_path = input("Enter the test folder >>>")
test_dict = {}

points = 0

with open(test_path + "/test.json", "r") as f:
    test_dict = json.load(f)

print(test_dict)


for question in test_dict:
    print("\n" + question["question"])
    
    answers = list(question["answers"].keys())
    random.shuffle(answers)
    for idx, answer in enumerate(answers, 1):
        print(f"{idx}. {answer}")
    
    while True:
        try:
            user_input = input("Enter the number of your answer: ")
            selected_idx = int(user_input) - 1 
            
            if 0 <= selected_idx < len(answers):
                selected_answer = answers[selected_idx]
                if question["answers"][selected_answer] == 1:
                    print("Good Job!")
                    points += 1
                else:
                    print("Wrong answer!")
                break
            else:
                print("Please enter a valid number from the list!")
        except ValueError:
            print("Please enter a valid number!")

print("\nYour final score is:", points)





