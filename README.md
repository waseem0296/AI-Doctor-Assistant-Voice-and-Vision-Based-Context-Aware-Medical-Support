# AI Doctor Assistant – Voice and Vision Based Context-Aware Medical Support

---

##  Project Overview

AI Doctor Assistant is an intelligent healthcare assistant that interacts with users through **voice or text** queries and analyzes **medical images** for diagnostic suggestions. Built using **Gradio**, **Groq LLMs**, **Whisper for speech recognition**, and **gTTS for voice replies**, this tool mimics real doctor-like conversations while maintaining context across interactions.

This is for **learning and demonstration purposes only**, not a replacement for licensed medical professionals.

---

##  Features

- **Voice Input**: Ask questions through your microphone.
- **Text Input**: Type medical questions manually.
- **Image Upload**: Upload a medical image (e.g., X-ray, skin lesion).
- **Context-Aware Dialogue**: Maintains history for natural conversations.
- **Multimodal Diagnosis**: Combines image + text understanding using Groq's LLaMA model.
- **Text-to-Speech Output**: Doctor’s response is spoken back using gTTS.
- **Live Chat Interface**: Displays the Q&A history for reference.

---

## Technologies Used

| Component             | Tool/Library                | Description                                               |
|----------------------|-----------------------------|-----------------------------------------------------------|
| UI Framework         | Gradio                      | For building the front-end interface                      |
| LLM API              | Groq                        | Uses LLaMA-4-Scout for image + text-based inference       |
| Speech Recognition   | Whisper (via Groq)          | Converts audio to text                                    |
| Text-to-Speech       | gTTS                        | Converts doctor replies into natural audio                |
| Audio Processing     | PyDub + ffmpeg              | Used for audio formatting and playback                    |
| Environment Handling | python-dotenv               | Secure key management                                     |

---

## Project Structure

ai-doctor-assistant/
│
├── app.py # Gradio interface and app logic
├── ai_brain.py # Image processing and Groq API logic
├── voice_of_patient.py # Handles voice-to-text conversion
├── voice_of_doctor.py # Converts doctor reply to speech
├── requirements.txt # Dependencies list
├── .env # Contains GROQ_API_KEY
├── README.md # Project documentation


---

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-doctor-assistant.git
cd ai-doctor-assistant
## Install requirements
pip install -r requirements.txt

## Add Your .env File
### Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here

## Ensure FFmpeg is Installed
Windows: Download FFmpeg
## Run app
python app.py


##  How to Use

1. Launch the app – it will automatically open in your browser.
2. Upload a **medical image** (required once per session).
3. Ask your medical question via **voice input** or **text input**.
4. Click on **“Ask Doctor”**.
5. Get a **textual diagnosis** and an accompanying **voice reply**.
6. View the complete **conversation history** in the chat panel.
7. Click **“Reset Consultation”** to start a new session.



## Sample Use Cases

- What is this patch on the skin?
- Is this X-ray showing a fracture?
- What medicine should I take for this condition?
- Is this scan showing anything abnormal?

## Requirements.txt
gradio
gtts
python-dotenv
pydub
speechrecognition
groq





