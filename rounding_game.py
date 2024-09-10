import tkinter as tk
import random
# import emoji

# Initialize score tracking
correct_count = 0
total_count = 0
score_update = True
time_delay = 3000

# Function to generate a random integer and a random rounding base
def generate_number_and_base():
    global number, rounding_base, correct_answer
    number = random.randint(1, 100000)
    rounding_base = random.choice([10, 100, 1000, 10000])  # Randomly select the rounding base
    correct_answer = logical_round(number, rounding_base)
    number_label.config(text=f"Number: {number:,}")  # Format number with commas
    base_label.config(text=f"Round to the nearest: {rounding_base:,}")
    hint_label.config(text="")  # Clear previous hint
    canvas.delete("all")  # Clear previous number line
    generate_choices()

# Function to logically round the number
def logical_round(num, base):
    return round(num / base) * base

# Function to generate multiple choice answers
def generate_choices():
    global correct_answer, rounding_base
    
    # Generate the correct answer
    correct_answer = logical_round(number, rounding_base)
    
    # Generate a wrong answer by rounding to a different base
    different_base = random.choice([b for b in [10, 100, 1000, 10000] if b != rounding_base])
    wrong_answer_different_base = logical_round(number, different_base)
    
    # Generate a wrong answer by rounding incorrectly to the same base (floor or ceiling)
    wrong_answer_incorrect_rounding = correct_answer + random.choice([-rounding_base, rounding_base])
    if wrong_answer_incorrect_rounding < 0:
        wrong_answer_incorrect_rounding = correct_answer + rounding_base
    
    # Ensure all answers are distinct
    choices = [correct_answer, wrong_answer_different_base, wrong_answer_incorrect_rounding]
    if len(set(choices)) < 3:  # Ensure uniqueness
        choices[2] = wrong_answer_different_base + 10  # Modify one of the incorrect answers if needed
    
    random.shuffle(choices)  # Shuffle the choices
    
    # Assign the choices to buttons
    button1.config(text=f"{choices[0]:,}", command=lambda: check_answer(choices[0]))
    button2.config(text=f"{choices[1]:,}", command=lambda: check_answer(choices[1]))
    button3.config(text=f"{choices[2]:,}", command=lambda: check_answer(choices[2]))


# Function to check the user's answer and update score
def check_answer(user_input):
    global correct_count, total_count, score_update
    if user_input == correct_answer:
        hint_label.config(text=f"Correct! The correct rounded value is {correct_answer:,}.", fg="green")
        root.after(time_delay, lambda: hint_label.config(text=""))  # Clear hint after 5 seconds
        root.after(time_delay, generate_number_and_base)  # Wait 5 seconds, then generate a new number and base for the next round
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

# Function to provide hints by drawing a pretty number line
def draw_number_line():
    canvas.delete("all")  # Clear the canvas
    start = correct_answer - 5 * rounding_base  # Start 5 increments before the original number
    end = correct_answer + 5 * rounding_base  # End 5 increments after the original number
    number_range = list(range(start, end + rounding_base, rounding_base))  # List of numbers for the number line
    
    # Draw the line
    canvas.create_line(50, 50, 1150, 50, width=2)
    
    # Draw dots and numbers
    for i, num in enumerate(number_range):
        x_pos = 50 + (i * 100)  # Spread dots evenly along the line
        canvas.create_oval(x_pos-5, 45, x_pos+5, 55, fill="blue")  # Draw the dot
        canvas.create_text(x_pos, 70, text=f"{num:,}", font=("Helvetica", 10))  # Display the number

    # Draw a red tick at the actual number
    if start <= number <= end:
        # Calculate position of actual number on the line
        num_position = (number - start) / (end - start) * 1100
        actual_x_pos = num_position
        canvas.create_line(actual_x_pos, 30, actual_x_pos, 70, fill="red", width=3)  # Mark the actual number

# Function to update and display the score percentage with emojis
def update_score():
    if total_count > 0:
        percentage = (correct_count / total_count) * 100
        score_text = f"Score: {percentage:.2f}% "
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
root.title("Rounding Game")
root.geometry("1500x600")
root.config(bg="#F0F0F0")

# Labels and widgets
number_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#F0F0F0")
number_label.pack(pady=10)

base_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#F0F0F0")
base_label.pack(pady=10)

entry_label = tk.Label(root, text="Choose the correct rounded value:", font=("Helvetica", 12), bg="#F0F0F0")
entry_label.pack(pady=10)

# Frame to hold the buttons side by side
button_frame = tk.Frame(root, bg="#F0F0F0")
button_frame.pack(pady=5)

# Multiple-choice buttons
button1 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button1.pack(side="left", padx=10)

button2 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button2.pack(side="left", padx=10)

button3 = tk.Button(button_frame, text="", font=("Helvetica", 12), bg="#0a95e6", fg="white")
button3.pack(side="left", padx=10)

# Hint label to display feedback
hint_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#F0F0F0", fg="red")
hint_label.pack(pady=10)

# Canvas for the number line
canvas = tk.Canvas(root, width=1200, height=100, bg="#F0F0F0")
canvas.pack(pady=10)

# Score label at the bottom right
score_label = tk.Label(root, text="Score: 0%", font=("Helvetica", 12), bg="#F0F0F0", fg="black")
score_label.pack(pady=10, padx=10, anchor="se")

# Start the game by generating a random number and rounding base
generate_number_and_base()

# Run the tkinter loop
root.mainloop()
