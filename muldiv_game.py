import tkinter as tk
import random

# Initialize score tracking
correct_count = 0
total_count = 0
score_update = True
time_delay = 3000

# Function to generate a random math problem (multiplication or division)
def generate_problem():
    global number1, number2, correct_answer, operation
    number1 = random.randint(1, 10)
    
    # Decide whether it's multiplication or division
    if random.choice(["*", "/"]) == "*":
        operation = "*"
        number2 = random.randint(1, 10)
        correct_answer = number1 * number2
    else:
        operation = "/"
        number2 = random.randint(1, 10)
        correct_answer = number1
        number1 = number1 * number2  # Ensure no fractional results
    
    # Update the labels with the generated numbers
    problem_label.config(text=f"Problem: {number1} {operation} {number2}")
    hint_label.config(text="")  # Clear previous hint
    generate_choices()

# Function to generate multiple choice answers
def generate_choices():
    global correct_answer
    
    # Generate wrong answers
    wrong_answer1 = correct_answer + random.choice([-1, 1, -2, 2])
    wrong_answer2 = correct_answer + random.choice([-3, 3, -4, 4])

    # Ensure all answers are distinct and between 1 and 400
    wrong_answer1 = max(1, wrong_answer1)
    wrong_answer2 = max(1, wrong_answer2)

    # Adjust if wrong answers coincide with each other or the correct answer
    while wrong_answer1 == wrong_answer2 or wrong_answer1 == correct_answer:
        wrong_answer1 = random.randint(1, 400)
    while wrong_answer2 == correct_answer or wrong_answer2 == wrong_answer1:
        wrong_answer2 = random.randint(1, 400)
    
    choices = [correct_answer, wrong_answer1, wrong_answer2]
    random.shuffle(choices)
    
    # Assign the choices to buttons
    button1.config(text=f"{choices[0]}", command=lambda: check_answer(choices[0]))
    button2.config(text=f"{choices[1]}", command=lambda: check_answer(choices[1]))
    button3.config(text=f"{choices[2]}", command=lambda: check_answer(choices[2]))

# Function to check the user's answer and update score
def check_answer(user_input):
    global correct_count, total_count, score_update
    disable_buttons()
    if user_input == correct_answer:
        hint_label.config(text=f"Correct! The result is {correct_answer}.", fg="green")
        root.after(time_delay, generate_problem)  # Wait 3 seconds, then generate a new problem
        root.after(time_delay, lambda: hint_label.config(text=""))  # Clear hint after 3 seconds
        root.after(time_delay, lambda: enable_buttons())  # Re-enable buttons after 3 seconds
        
        # Remove the matrix if it exists
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        if score_update:
            total_count += 1
            correct_count += 1
            update_score()  # Update score and percentage display
        question_counter_label.config(text=f"Answered: {total_count}")
        score_update = True
    else:
        hint_label.config(text=f"Incorrect. Look at the table below to help you!", fg="red")
        # Create matrix with rainbow background
        create_matrix()
        enable_buttons()
        if score_update:
            total_count += 1
            update_score()  # Update score and percentage display
        score_update = False

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

        # Check for prize condition
        if (total_count == prize_threshold and percentage > 90) or (total_count == 2*prize_threshold and percentage > 70):
            show_prize_popup()

def show_prize_popup():
    prize_popup = tk.Toplevel(root)
    prize_popup.title("Well Done Madeleine!")
    prize_popup.geometry("800x100")
    prize_popup.config(bg="#F0F0F0")

    message_label = tk.Label(prize_popup, text="Congratulations for your hard work! You get a prize! ", font=("Helvetica", 12), bg="#F0F0F0")
    message_label.pack(pady=20, padx=20)

    # Disable main window interaction until popup is closed
    root.wait_window(prize_popup)

def enable_buttons():
    button1.config(state=tk.NORMAL)
    button2.config(state=tk.NORMAL)
    button3.config(state=tk.NORMAL)

def disable_buttons():
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.DISABLED)
    button3.config(state=tk.DISABLED)

def hex_to_rgb(hex_color):
    """ Convert hex color to RGB tuple. """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_text_color(bg_color):
    """ Determine the best text color (black or white) based on background color. """
    rgb = hex_to_rgb(bg_color)
    # Calculate luminance using the standard formula
    luminance = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
    # Return black if background is light, else return white
    return "black" if luminance > 0.5 else "white"

# Function to create the rainbow pattern and display matrix with headers
def create_matrix():
    rainbow_colors = [
        "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", 
        "#4B0082", "#9400D3", "#FF1493", "#1E90FF", "#32CD32"
    ]
    
    # Display header row (numbers 1 to 20)
    for i in range(1, 16):
        label = tk.Label(matrix_frame, text=str(i), font=("Helvetica", 12), width=3, height=2, bg="lightgray")
        label.grid(row=0, column=i)
    
    # Display header column (numbers 1 to 20)
    for i in range(1, 16):
        label = tk.Label(matrix_frame, text=str(i), font=("Helvetica", 12), width=3, height=2, bg="lightgray")
        label.grid(row=i, column=0)
    
    # Create the matrix and apply rainbow background
    for row in range(1, 16):
        for col in range(1, 16):
            # The color is determined by the maximum distance of the cell from the main diagonal (1,1) to (n,n)
            distance = max(row, col)
            color = rainbow_colors[(distance - 1) % len(rainbow_colors)]
            
            canvas = tk.Canvas(matrix_frame, width=50, height=50, bg=color, highlightthickness=0)
            canvas.grid(row=row, column=col)
            # Draw the larger oval with a white outline and the background matching the cell's color
            # Determine the text color based on the background color
            text_color = get_text_color(color)

            canvas.create_oval(1, 1, 48, 48, fill=color, outline=text_color, width=2)
            
            # Display the number in the center of the oval
            canvas.create_text(25, 25, text=f"{row * col}", font=("Helvetica", 9), fill=text_color)
            
            # Highlight the cells of the dividend
            if operation == '/':
                if row * col == number1:
                    canvas.create_oval(1, 1, 48, 48, fill="white", outline="black", width=4)  # Thicker white outline
                    canvas.create_text(25, 25, text=f"{row * col}", font=("Helvetica", 9), fill="black")

# Setup the main window
root = tk.Tk()
root.title("Multiplication/Division Game with Matrix")
root.geometry("1500x1600")
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

# Score label at the bottom
score_label = tk.Label(root, text="Score: 0%", font=("Helvetica", 14), bg="#F0F0F0")
score_label.pack(pady=10, padx=10, anchor="se")

# Create a label for the question counter
question_counter_label = tk.Label(root, text="Answered: 0", font=("Helvetica", 14), bg="#F0F0F0")
question_counter_label.pack(pady=10, padx=10, anchor="sw")

prize_threshold = random.randint(35, 75)

# Frame for the matrix
matrix_frame = tk.Frame(root, bg="#F0F0F0")
matrix_frame.pack(pady=20)

# Start the game with a random problem
generate_problem()

root.mainloop()
