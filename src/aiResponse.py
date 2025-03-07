import tkinter as tk
from tkinter import messagebox
from model.aiModel import get_response

# Create the main window
root = tk.Tk()
root.title("Schrodinger's Solution")

# Create a text box for user input on the left half of the window. Title it "Expectations"
frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)

label = tk.Label(frame, text="Expectations", font=("Helvetica", 14))
label.pack()

text_box_expectations = tk.Text(frame, height=10, width=50)
text_box_expectations.pack(pady=10)

# Create a text box for user input on the right half of the window next to the previous text box. Title it "Code"
frame_code = tk.Frame(root)
frame_code.pack(side=tk.RIGHT, padx=20, pady=20)

label_code = tk.Label(frame_code, text="Code", font=("Helvetica", 14))
label_code.pack()

text_box_code = tk.Text(frame_code, height=10, width=50)
text_box_code.pack(pady=10)

# Function to handle the submit button, add response at bottom of the window
def on_submit():
    # Get the content from the text box
    expectations_content = text_box_expectations.get("1.0", tk.END).strip()
    code_content = text_box_code.get("1.0", tk.END).strip()

    if code_content.strip():
        # Get the response from the aiModel.py
        response_content = get_response(expectations_content,code_content)
        response_window = tk.Toplevel(root)
        response_window.title("AI Response")
        
        # Create a text box to display the response
        response_text = tk.Text(response_window, wrap=tk.WORD)
        response_text.pack(expand=True, fill=tk.BOTH)
        
        # Insert the response into the text box
        response_text.insert(tk.END, response_content)
        
        # Add a scrollbar to the text box
        scrollbar = tk.Scrollbar(response_window, command=response_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        response_text.config(yscrollcommand=scrollbar.set)
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
   
# Create a button to submit the input
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=20)

# Run the application
root.mainloop()