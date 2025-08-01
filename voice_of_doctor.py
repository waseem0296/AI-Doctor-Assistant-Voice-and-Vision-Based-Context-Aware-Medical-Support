from gtts import gTTS
import os
import subprocess
import platform
def text_to_speech_with_gtts(input_text,output_file):
    language="en"
    audioobj=gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_file)
    os_name=platform.system()
    if os_name=="Windows":
        ffplay_path = r"D:\ffmpeg-7.1.1-essentials_build\bin\ffplay.exe"
        subprocess.run([
                ffplay_path,
                "-nodisp",        
                "-autoexit",       
                output_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        

# input_text="Hello, my name is doctor ali"
# text_to_speech_with_gtts(input_text=input_text,output_file="text_to_Speech_testing.mp3")
