import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import easyocr
from gtts import gTTS
import playsound
import tempfile
import os
from deep_translator import GoogleTranslator

# Init OCR and globals
reader = easyocr.Reader(['en', 'hi'], gpu=False)
current_theme = "light"
hindi_text = ""

# Theme styles
themes = {
    "light": {
        "bg": "#FDEDEC",
        "fg": "#4A4A4A",
        "button_bg": "#FFC1CC",
        "text_bg": "#FFF0F5"
    },
    "dark": {
        "bg": "#000000",
        "fg": "#FFFFFF",
        "button_bg": "#444444",
        "text_bg": "#3C3C3C"
    }
}

# Apply selected theme
def apply_theme():
    theme = themes[current_theme]
    root.configure(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"])
    for btn in [upload_btn, speak_btn, theme_btn]:
        btn.config(bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["button_bg"])
    frame.config(bg=theme["bg"])
    left_frame.config(bg=theme["bg"])
    right_frame.config(bg=theme["bg"])
    image_label.config(bg=theme["bg"])
    text_output.config(bg=theme["text_bg"], fg=theme["fg"])
    translation_output.config(bg=theme["text_bg"], fg=theme["fg"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

# Detect if text is in Hindi
def contains_hindi(text):
    return any('\u0900' <= c <= '\u097F' for c in text)

# Speak Hindi text using gTTS
def speak_hindi():
    global hindi_text
    if hindi_text:
        try:
            tts = gTTS(text=hindi_text, lang='hi')

            # Create a temporary file path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_path = fp.name

            # Save the TTS file and play it
            tts.save(temp_path)
            playsound.playsound(temp_path)

            # Optional: Clean up temp file afterward
            os.remove(temp_path)

        except Exception as e:
            messagebox.showerror("Error", f"Could not speak Hindi.\n{str(e)}")
    else:
        messagebox.showinfo("Info", "No Hindi text to speak.")

# Main function to upload image and run OCR
def upload_image():
    global hindi_text
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    # Load and display the image
    img = Image.open(file_path)
    img.thumbnail((350, 350))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # OCR processing
    results = reader.readtext(file_path)
    hindi_lines = []
    all_text = ""

    for result in results:
        text = result[1]
        all_text += text + "\n"
        if contains_hindi(text):
            hindi_lines.append(text)

    # Show detected OCR text
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, all_text)

    # Translate Hindi lines if any
    if hindi_lines:
        hindi_text = " ".join(hindi_lines)
        try:
            translated = GoogleTranslator(source='hi', target='en').translate(hindi_text)

            # Estimate translation accuracy based on word count
            hindi_word_count = len(hindi_text.split())
            translated_word_count = len(translated.split())

            if hindi_word_count == 0:
                accuracy = "N/A"
            else:
                ratio = translated_word_count / hindi_word_count
                accuracy_percent = min(100, round(ratio * 100))
                accuracy = f"{accuracy_percent}%"

            # Display translated text with estimated accuracy
            translation_output.delete(1.0, tk.END)
            translation_output.insert(tk.END, f"{translated}\n\n🔍 Estimated Accuracy: {accuracy}")

        except Exception as e:
            translation_output.delete(1.0, tk.END)
            translation_output.insert(tk.END, "Translation failed.\n" + str(e))
    else:
        hindi_text = ""
        translation_output.delete(1.0, tk.END)
        translation_output.insert(tk.END, "No Hindi text found.")


# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title(" OCR + Hindi Translator (Offline TTS)")
root.geometry("1000x750")

# Title
title_label = tk.Label(root, text="Read and Understand Hindi", font=("Helvetica", 20, "bold"))
title_label.pack(pady=15)

# Buttons
top_btns = tk.Frame(root)
top_btns.pack()

upload_btn = tk.Button(top_btns, text="Upload Image", command=upload_image,
                       font=("Helvetica", 12), relief="groove", padx=20, pady=8)
upload_btn.grid(row=0, column=0, padx=0)

speak_btn = tk.Button(top_btns, text="🗣 Speak Hindi", command=speak_hindi,
                      font=("Helvetica", 12), relief="groove", padx=20, pady=8)
speak_btn.grid(row=0, column=1, padx=0)

theme_btn = tk.Button(top_btns, text="🌗 Toggle Theme", command=toggle_theme,
                      font=("Helvetica", 12), relief="groove", padx=20, pady=8)
theme_btn.grid(row=0, column=2, padx=0)

# Layout frames
frame = tk.Frame(root)
frame.pack(padx=20, pady=10, fill="both", expand=True)

left_frame = tk.Frame(frame)
left_frame.pack(side="left", padx=10, fill="y")

image_label = tk.Label(left_frame)
image_label.pack()

right_frame = tk.Frame(frame)
right_frame.pack(side="left", fill="both", expand=True, padx=10)

text_output = tk.Text(right_frame, height=10, font=("Consolas", 10),
                      wrap="word", relief="flat")
text_output.pack(fill="x", pady=(0, 10))

translation_output = tk.Text(right_frame, height=5, font=("Helvetica", 12, "italic"),
                             wrap="word", relief="flat")
translation_output.pack(fill="x", pady=(0, 10))

apply_theme()
root.mainloop()
