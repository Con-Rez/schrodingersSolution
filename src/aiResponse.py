import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from model.aiModel import get_response
from linked_list import LinkedListHelp
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
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

# Initialize the linked list to store responses
response_list = LinkedListHelp()

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Function to handle the submission
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


# Function to handle the upload file
def on_file_upload():
    upload_window = tk.Toplevel(root)
    upload_window.title("Submit Expectations")

    upload_text_box = tk.Text(upload_window, height=10, width=50)
    upload_text_box.pack(pady=10)
    
    def submit_upload():
        expectations_content = upload_text_box.get("1.0", tk.END).strip()
        if expectations_content.strip():
            # Close the upload window
            upload_window.destroy()
            on_load_file(expectations_content)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    submit_button = tk.Button(upload_window, text="Submit", command=submit_upload)
    submit_button.pack(pady=10)

# Function to handle the upload folder
def on_folder_upload():
    upload_window = tk.Toplevel(root)
    upload_window.title("Submit Expectations")

    upload_text_box = tk.Text(upload_window, height=10, width=50)
    upload_text_box.pack(pady=10)
    
    def submit_upload():
        expectations_content = upload_text_box.get("1.0", tk.END).strip()
        if expectations_content.strip():
            # Close the upload window
            upload_window.destroy()
            on_load_folder(expectations_content)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    submit_button = tk.Button(upload_window, text="Submit", command=submit_upload)
    submit_button.pack(pady=10)

# Function to update the progress bar and get Response from AI
def update_progress_bar(expectations_content, num_files, file_paths):
    progress_bar["maximum"] = num_files
    for cur_progress, file_path in enumerate(file_paths):
        file_content = read_file(file_path)
        response_content = get_response(expectations_content, file_content)
        response_list.prepend(response_content)  # Store response in linked list
        progress_bar["value"] = cur_progress + 1
        root.update_idletasks()  # Update the progress bar
    response_label = tk.Label(root, text="Files stored!", font=("Helvetica", 12))
    response_label.pack(pady=10)

    # Call to output response to screen
    on_ai_response()

# Function to handle the AI response and text box
def on_ai_response():
    # Process the uploaded content
    response_window = tk.Toplevel(root)
    response_window.title("AI Response")
    
    # Create a text box to display the response
    response_text = tk.Text(response_window, wrap=tk.WORD)
    response_text.pack(expand=True, fill=tk.BOTH)
    
    # Insert the response into the text box
    while True:
        response_content = response_list.dequeue()
        if response_content is None:
            break
        response_text.insert(tk.END, response_content)
    
    # Add a scrollbar to the text box
    scrollbar = tk.Scrollbar(response_window, command=response_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    response_text.config(yscrollcommand=scrollbar.set)

# Function to handle the load button, read content from a file(s), and track number of files
def on_load_file(expectations_content):
    file_paths = filedialog.askopenfilenames(title="Select a file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_paths:
        num_files = len(file_paths)
        update_progress_bar(expectations_content, num_files, file_paths)

# Function to handle the load folder button, read content from all files in the folder, and track number of files
def on_load_folder(expectations_content):
    folder_path = filedialog.askdirectory(title="Select a folder")
    if folder_path:
        file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        num_files = len(file_paths)
        update_progress_bar(expectations_content, num_files, file_paths)
   
# Create a button to submit the input
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=20)

# Create a button to load content from a file
load_button = tk.Button(root, text="Load from File", command=on_file_upload)
load_button.pack(pady=10)

# Create a button to load content from a folder
load_folder_button = tk.Button(root, text="Load from Folder", command=on_folder_upload)
load_folder_button.pack(pady=10)

# Run the application
root.mainloop()