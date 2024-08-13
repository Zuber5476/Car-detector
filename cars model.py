import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the model (example - replace with your actual model loading code)
model = load_model("cars model.h5")

# Initializing the GUI
top = tk.Tk()
top.geometry("800x600")
top.title("Traffic Signal Analyzer")
top.configure(background="#CDCDCD")

# Initializing the labels
label1 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
label3 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
sign_image = Label(top)

# Defining detect function to analyze traffic signal image using model
def Detect(file_path):
    try:
        global label1, label2, label3
        image = Image.open(file_path)
        image = image.resize((128, 128))  # Resize image to fit model input size (example)
        image = np.array(image)  # Convert PIL image to numpy array
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image / 255.0  # Normalize image

        # Perform prediction using your model
        pred = model.predict(image)

        # Example predictions - modify as per your model's output structure
        car_color = "Red" if pred[0][0] > 0.5 else "Blue"  # Example binary prediction
        car_count = int(np.round(pred[1][0]))  # Example numerical prediction
        gender_male_count = int(np.round(pred[2][0]))  # Example count of males
        gender_female_count = int(np.round(pred[2][1]))  # Example count of females
        other_vehicles_count = int(np.round(pred[3][0]))  # Example count of other vehicles

        # Update labels with predictions
        label1.config(foreground="#011638", text=f"Predicted Car Color: {car_color}")
        label2.config(foreground="#011638", text=f"Predicted Car Count: {car_count}")
        label3.config(foreground="#011638", text=f"Predicted Gender - Male: {gender_male_count}, Female: {gender_female_count}, Other Vehicles: {other_vehicles_count}")

    except Exception as e:
        print("Error:", e)

# Defining show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Analyze Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining upload image function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.config(text=" ")
        label2.config(text=" ")
        label3.config(text=" ")
        show_Detect_button(file_path)

    except Exception as e:
        print("Error:", e)

# Button to upload an image
upload = Button(top, text="Upload Traffic Signal Image", command=upload_image, padx=10, pady=5)
upload.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
upload.pack(side="bottom", pady=50)

# Packing labels and image display
sign_image.pack(side="bottom", expand=True)
label1.pack()
label2.pack()
label3.pack()

# Label for heading
heading = Label(top, text="Traffic Signal Analyzer", pady=20, font=("arial", 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Start GUI main loop
top.mainloop()
