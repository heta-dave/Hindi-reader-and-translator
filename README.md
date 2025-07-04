# OCR + Hindi Translator GUI App

A desktop application built using Python that detects text (Hindi or English) from uploaded images, translates Hindi text into English, speaks it aloud, and displays estimated translation accuracy — all inside a clean, pastel-themed Tkinter interface.

---

## Features

- 📷 Upload images with Hindi or English text
- 🔍 Extract printed text using [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- 🌐 Translate Hindi to English using [Deep Translator](https://pypi.org/project/deep-translator/)
- 🎯 Display estimated **translation accuracy**
- 🗣 Speak extracted **Hindi text aloud** using `gTTS` (Google Text-to-Speech)
- 🌗 Light and Dark theme toggle
- 💫 Intuitive and aesthetic UI with pastel tones

---

## Demo

![App Screenshot]![App](https://github.com/user-attachments/assets/d07d02bf-24b5-4eea-b5bc-17926a8c7c5d)
<!-- Replace with actual screenshot path -->

---

## Tech Stack

- Python
- EasyOCR
- Deep Translator
- gTTS (Google Text-to-Speech)
- Pillow (image display)
- Tkinter (GUI)
- Playsound (audio playback)

---

## Getting Started

### 📦 Installation

1. **Clone this repository**
```bash
git clone https://github.com/your-username/ocr-hindi-translator.git
cd ocr-hindi-translator
