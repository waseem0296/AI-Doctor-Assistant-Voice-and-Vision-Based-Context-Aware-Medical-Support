# import gradio as gr
# from ai_brain import image_encoder, analyze_image
# from voice_of_patient import transcription_from_voice_text
# from voice_of_doctor import text_to_speech_with_gtts

# # === Global states ===
# conversation_history = []
# stored_image_base64 = None
# image_uploaded = False

# # === System Prompt ===
# system_prompt = """You have to act as professiona doctor, i know you are not but this is for learning purpose.
# what's in this image?. Do you find anything wrong with it medically?
# If you make differential, suggest some remies for them. Don't add any number or special characters in your response. Your responce should be in one long paragraph.Also always answer as if you are answering to a real person.
# Don't say 'In the image I see' but say 'With what I see, I think you have....'
# Don't responce as an AI in the markdown, Your answer should mimic that of an actual doctor not an AI bot,
# Keep your answer concise (max 2 sentences). No preamble, start your answer right away please
# """

# # === Processing Function ===
# def process_input(audio_filepath, image_filepath):
#     global stored_image_base64, image_uploaded, conversation_history

#     # Transcribe audio
#     user_text = transcription_from_voice_text(audio_filepath)

#     # If image is uploaded for the first time
#     if image_filepath and not image_uploaded:
#         stored_image_base64 = image_encoder(image_filepath)
#         image_uploaded = True

#     # Check if image is present
#     if not stored_image_base64:
#         return user_text, "Please provide an image first.", "doctor_response.mp3", conversation_history

#     # Build full prompt using system_prompt + previous questions
#     conversation_text = " ".join([f"User: {u}\nDoctor: {r}" for u, r in conversation_history])
#     full_prompt = system_prompt + conversation_text + "\nUser: " + user_text

#     # Get AI doctor response
#     doctor_text = analyze_image(user_input=full_prompt, base64_image=stored_image_base64)

#     # Generate audio
#     audio_path = "doctor_response.mp3"
#     text_to_speech_with_gtts(doctor_text, output_file=audio_path)

#     # Save to history
#     conversation_history.append((user_text, doctor_text))

#     return user_text, doctor_text, audio_path, conversation_history

# # === Reset Function ===
# def reset_session():
#     global conversation_history, stored_image_base64, image_uploaded
#     conversation_history = []
#     stored_image_base64 = None
#     image_uploaded = False
#     return "", "", None, []

# # === UI with Blocks ===
# with gr.Blocks(title="AI Doctor Assistant") as demo:
#     gr.Markdown("## AI Doctor with Vision and Voice\nUpload an image **once**, then ask multiple voice questions.")

#     with gr.Row():
#         audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Ask a question by voice")
#         image_input = gr.Image(type="filepath", label="Upload Image (only once)")

#     with gr.Row():
#         user_textbox = gr.Textbox(label="Transcribed Question")
#         doctor_textbox = gr.Textbox(label="Doctor's Response")
#         doctor_audio = gr.Audio(label="Doctor's Voice Response")

#     chatbot = gr.Chatbot(label="Conversation History (Q&A)")

#     with gr.Row():
#         submit_btn = gr.Button("Ask Doctor")
#         reset_btn = gr.Button("Reset Consultation")

#     submit_btn.click(
#         fn=process_input,
#         inputs=[audio_input, image_input],
#         outputs=[user_textbox, doctor_textbox, doctor_audio, chatbot]
#     )

#     reset_btn.click(
#         fn=reset_session,
#         outputs=[user_textbox, doctor_textbox, doctor_audio, chatbot]
#     )

# demo.launch(debug=True)


import gradio as gr
from ai_brain import image_encoder, analyze_image
from voice_of_patient import transcription_from_voice_text
from voice_of_doctor import text_to_speech_with_gtts

# === Global State ===
conversation_history = []
stored_image_base64 = None
image_uploaded = False
first_question = True  # Flag for system prompt

# === System Prompt for First-Time Only ===
system_prompt = """You have to act as professiona doctor, i know you are not but this is for learning purpose.
what's in this image?. Do you find anything wrong with it medically?
If you make differential, suggest some remies for them. Don't add any number or special characters in your response. Your responce should be in one long paragraph.Also always answer as if you are answering to a real person.
Don't say 'In the image I see' but say 'With what I see, I think you have....'
Don't responce as an AI in the markdown, Your answer should mimic that of an actual doctor not an AI bot,
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please
"""

# === Main Processing ===
def process_input(audio_filepath, image_filepath,typed_input):
    global stored_image_base64, image_uploaded, conversation_history, first_question

    # Convert voice to text
    if typed_input:
        user_text=typed_input.strip()
    elif audio_filepath:
        user_text= transcription_from_voice_text(audio_filepath)
    else:
        user_text="Analyze the uploaded image."

    # Handle image if first time
    if image_filepath and not image_uploaded:
        stored_image_base64 = image_encoder(image_filepath)
        image_uploaded = True

    if not stored_image_base64:
        return user_text, "Please provide an image first.", "doctor_response.mp3", conversation_history, "", None


    # Build the conversation context
    conversation_text = " ".join([f"User: {u}\nDoctor: {r}" for u, r in conversation_history])

    # Add system prompt only for first question
    if first_question:
        full_prompt = system_prompt + "\nUser: " + user_text
        first_question = False
    else:
        full_prompt = conversation_text + "\nUser: " + user_text

    # AI Doctor reply
    doctor_text = analyze_image(user_input=full_prompt, base64_image=stored_image_base64)
    
    # Generate speech
    audio_path = "doctor_response.mp3"
    text_to_speech_with_gtts(doctor_text, output_file=audio_path)

    # Update conversation history
    conversation_history.append((user_text, doctor_text))

    return user_text, doctor_text, audio_path, conversation_history, "",None  # Reset audio input

# === Reset Session ===
def reset_session():
    global conversation_history, stored_image_base64, image_uploaded, first_question
    conversation_history = []
    stored_image_base64 = None
    image_uploaded = False
    first_question = True
    return "", "", None, [], "", None

# === Gradio UI ===
with gr.Blocks(title="AI Doctor Assistant") as demo:
    gr.HTML("""
    <style>
    #submit-btn:hover {
        background-color: #2ecc71 !important;
        color: white;
        transition: 0.3s;
        font-weight: bold;
    }
    #reset-btn:hover {
        background-color: #e74c3c !important;
        color: white;
        transition: 0.3s;
        font-weight: bold;
    }
    </style>
    """)
    gr.Markdown("## AI Doctor with Vision and Voice\n.")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Ask a Question")
            typed_input=gr.Textbox(label="You can type your question if you not speak",placeholder="E.g What medicine should I take?")
            image_input = gr.Image(type="filepath", label="Upload Medical Image")

        with gr.Column():
            user_textbox = gr.Textbox(label="Transcribed Question")
            doctor_textbox = gr.Textbox(label="Doctor's Response")
           
            doctor_audio = gr.Audio(label="Doctor's Voice Response")

    chatbot = gr.Chatbot(label="Chat History")

    with gr.Row():
        # submit_btn = gr.Button("Ask Doctor")
        # reset_btn = gr.Button("Reset Consultation")
        submit_btn = gr.Button("Ask Doctor", elem_id="submit-btn")
        reset_btn = gr.Button("Reset Consultation", elem_id="reset-btn")

    submit_btn.click(
        fn=process_input,
        inputs=[audio_input, image_input, typed_input],
        outputs=[user_textbox, doctor_textbox, doctor_audio, chatbot, typed_input, audio_input]
    )

    reset_btn.click(
        fn=reset_session,
        outputs=[user_textbox, doctor_textbox, doctor_audio, chatbot, typed_input, audio_input]
    )

demo.launch(debug=True)
