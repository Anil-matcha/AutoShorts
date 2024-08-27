from gtts import gTTS
from pydub import AudioSegment
import random
import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ImageClip

def create_image_with_text(image_path):
    width, height = 720, 1280
    image = Image.new('RGB', (width, height), 'white')

    draw = ImageDraw.Draw(image)
    text = "Sample Text Overlay"
    font_size = 50

    try:
        # Load a font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Use a default font
        font = ImageFont.load_default()

    # Calculate text size
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

    # Calculate position
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw text on the image
    draw.text((text_x, text_y), text, font=font, fill='black')
    image.save(image_path)

def create_video_from_image_and_audio(image_path, audio_path, output_path):
    # Load the generated image
    image = ImageClip(image_path)

    # Load the audio file
    try:
        audio = AudioFileClip(audio_path)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    # Check if the audio file has duration
    if audio.duration <= 0:
        print("Audio file has no duration.")
        return

    # Set the duration of the image to match the audio duration
    image = image.set_duration(audio.duration)

    # Set the image as the video clip
    video = image.set_audio(audio)

    # Output the final video
    try:
        video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        print(f"Video saved as {output_path}")
    except Exception as e:
        print(f"Error creating video: {e}")

# Sample conversation with filler words and intentional silences
conversation = [
    "So, I was thinking we could go to the park later.",
    "But, umm, I’m not really sure if the weather will be good.",
    "You know, I’ve been, uh, really busy with work lately.",
    "Like, maybe we should plan for the weekend instead.",
    "Hmm, but I don't know if I have time, like, to go out.",
    "Anyway, let’s just see how things go."
]

# Create a list to hold audio segments
audio_segments = []

# Generate audio for each sentence and optionally add silence
for sentence in conversation:
    # Save the sentence as audio using gTTS
    tts = gTTS(text=sentence, lang='en')
    tts.save("sentence.mp3")
    
    # Load the sentence audio
    sentence_audio = AudioSegment.from_file('sentence.mp3')
    audio_segments.append(sentence_audio)
    
    # Randomly add silence
    if random.choice([True, False]):
        silence_duration = random.randint(1500, 4500)  # 1.5 to 4.5 seconds of silence
        silence = AudioSegment.silent(duration=silence_duration)
        audio_segments.append(silence)

# Combine all audio segments into one
final_audio = sum(audio_segments)

# Save the final audio
audio_file_path = "sample_conversation_with_fillers_and_silence.mp3"
final_audio.export(audio_file_path, format="mp3")

# Clean up temporary file
os.remove("sentence.mp3")

print(f"Audio file saved as {audio_file_path}")

# Create the image and video
image_path = "generated_image.jpg"
create_image_with_text(image_path)

output_path = "input_video.mp4"
create_video_from_image_and_audio(image_path, audio_file_path, output_path)
