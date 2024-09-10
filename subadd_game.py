import tkinter as tk
import random

# Initialize score tracking
correct_count = 0
total_count = 0
score_update = True
time_delay = 3000

# Function to generate a random math problem (addition or subtraction)
def generate_problem():
    global number1, number2, correct_answer, operation
    number1 = random.randint(0, 20)
    
    # Decide whether it's addition or subtraction
    if random.choice(["+", "-"]) == "+":
        operation = "+"
        number2 = random.randint(0, 20 - number1)  # Ensure result is between 1 and 20
        correct_answer = number1 + number2
    else:
        operation = "-"
        number2 = random.randint(0, number1)  # Ensure no negative results
        correct_answer = number1 - number2
    
    # Update the labels with the generated numbers
    problem_label.config(text=f"Problem: {number1} {operation} {number2}")
    hint_label.config(text="")  # Clear previous hint
    canvas.delete("all")  # Clear previous number line
    generate_choices()

# Function to generate multiple choice answers
def generate_choices():
    global correct_answer
    
    # Generate wrong answers
    wrong_answer1 = correct_answer + random.choice([-1, 1, -2, 2])
    wrong_answer2 = correct_answer + random.choice([-3, 3, -4, 4])

    # Ensure all answers are distinct and between 1 and 20
    wrong_answer1 = max(0, wrong_answer1)
    wrong_answer2 = max(0, wrong_answer2)

    # Adjust if wrong answers coincide with each other or the correct answer
    while wrong_answer1 == wrong_answer2 or wrong_answer1 == correct_answer:
        wrong_answer1 = random.randint(0, 20)
    while wrong_answer2 == correct_answer or wrong_answer2 == wrong_answer1:
        wrong_answer2 = random.randint(0, 20)
    
    choices = [correct_answer, wrong_answer1, wrong_answer2]
    random.shuffle(choices)
    
    # Assign the choices to buttons
    button1.config(text=f"{choices[0]}", command=lambda: check_answer(choices[0]))
    button2.config(text=f"{choices[1]}", command=lambda: check_answer(choices[1]))
    button3.config(text=f"{choices[2]}", command=lambda: check_answer(choices[2]))

# Function to check the user's answer and update score
def check_answer(user_input):
    global correct_count, total_count, score_update
    if user_input == correct_answer:
        hint_label.config(text=f"Correct! The result is {correct_answer}.", fg="green")
        root.after(time_delay, lambda: hint_label.config(text=""))  # Clear hint after 5 seconds
        root.after(time_delay, generate_problem)  # Wait 5 seconds, then generate a new problem
        if score_update:
            total_count += 1
            correct_count += 1
            update_score()  # Update score and percentage display
        score_update = True
    else:
        hint_label.config(text=f"Incorrect. Look at the number line below to help you!", fg="red")
        draw_number_line()  # Show the number line
        if score_update:
            total_count += 1
            update_score()  # Update score and percentage display
        score_update = False

# Function to draw the number line based on the problem
def draw_number_line():
    canvas.delete("all")  # Clear the canvas
    
    # Draw the base number line from 1 to 20
    start = 0
    end = 20
    number_range = list(range(start, end + 1))  # List of numbers for the number line
    
    # Draw the line
    canvas.create_line(50, 50, 1050, 50, width=2)
    
    # Draw dots and numbers for 1 to 20
    for i, num in enumerate(number_range):
        x_pos = 50 + (i * 50)  # Spread dots evenly along the line
        canvas.create_oval(x_pos-5, 45, x_pos+5, 55, fill="black")  # Draw the dot
        canvas.create_text(x_pos, 70, text=f"{num}", font=("Helvetica", 10))  # Display the number
    
    # Draw the thick blue line for the first number
    blue_line_end = 50 + (number1) * 50
    canvas.create_line(50, 50, blue_line_end, 50, fill="blue", width=5)  # Blue line up to number1
    
    if operation == "+":
        # Draw the thick green line for addition
        green_line_end = blue_line_end + number2 * 50
        canvas.create_line(blue_line_end, 50, green_line_end, 50, fill="green", width=5)  # Green line for added amount
    elif operation == "-":
        # Draw the green dotted line for subtraction
        green_line_end = blue_line_end - number2 * 50
        for x in range(blue_line_end, green_line_end, -10):  # Draw dotted line
            canvas.create_line(x, 50, x - 5, 50, fill="green", width=5)

# Function to update and display the score percentage
def update_score():
    if total_count > 0:
        percentage = (correct_count / total_count) * 100
        score_text = f"Score: {percentage:.2f}%"
        
        if percentage < 50:
            score_label.config(fg="red")
        elif percentage < 90:
            score_label.config(fg="orange")
        elif percentage < 95:
            score_label.config(fg="lightgreen")
        else:
            score_label.config(fg="darkgreen")
        
        score_label.config(text=score_text)

# Setup the main window
root = tk.Tk()
root.title("Addition/Subtraction Game")
root.geometry("1200x600")
root.config(bg="#F0F0F0")

# Labels and widgets
problem_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#F0F0F0")
problem_label.pack(pady=10)

entry_label = tk.Label(root, text="Choose the correct result:", font=("Helvetica", 12), bg="#F0F0F0")
entry_label.pack(pady=10)

# Frame to hold the multiple-choice buttons
button_frame = tk.Frame(root, bg="#F0F0F0")
button_frame.pack(pady=10)

# Multiple-choice buttons placed in a horizontal layout
button1 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button1.grid(row=0, column=0, padx=10)

button2 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button2.grid(row=0, column=1, padx=10)

button3 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button3.grid(row=0, column=2, padx=10)

# Hint label to display feedback
hint_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#F0F0F0", fg="red")
hint_label.pack(pady=10)

# Canvas for the number line
canvas = tk.Canvas(root, width=1100, height=100, bg="#F0F0F0")
canvas.pack(pady=10)

# Score label at the bottom right
score_label = tk.Label(root, text="Score: 0%", font=("Helvetica", 12), bg="#F0F0F0", fg="black")
score_label.pack(pady=10, padx=10, anchor="se")

# Start the game by generating a random problem
generate_problem()

# Run the tkinter loop
root.mainloop()
