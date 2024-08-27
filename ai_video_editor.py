import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips

def transcribe_video(video_path):
    """
    Transcribes the video and returns the result with word-level timestamps.
    
    Args:
        video_path (str): Path to the video file to be transcribed.
    
    Returns:
        dict: Transcription result containing word-level timestamps.
    """
    # Load the Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the video
    result = model.transcribe(video_path, prompt="Umm,let me think like,hmm... Okay,here's what I'm,like,thinking.", word_timestamps=True)
    
    return result

def identify_silence_periods(transcription, video_duration, threshold=1.0, buffer=0.1):
    """
    Identifies silence periods in the transcription based on the threshold.
    
    Args:
        transcription (dict): The transcription result with word-level timestamps.
        threshold (float): The minimum duration of silence to be considered.
    
    Returns:
        list: A list of tuples where each tuple contains the start and end time of a silence period.
    """
    silence_periods = []
    words = transcription['segments']
    previous_end = 0

    for word in words:
        start_time = word['start']
        if start_time - previous_end > threshold:
            silence_periods.append((previous_end+buffer, start_time-buffer))
        previous_end = word['end']

    if video_duration - previous_end > threshold:
        silence_periods.append((previous_end+buffer, video_duration-buffer))

    return silence_periods

def cut_silences(input_video, output_video, silence_periods):
    """
    Removes the silence periods from the video and saves the result.
    
    Args:
        input_video (str): Path to the input video file.
        output_video (str): Path to save the output video file.
        silence_periods (list): A list of tuples indicating silence periods (start, end).
    """
    # Load the video
    video = VideoFileClip(input_video)

    # Create a list of clips without the silence periods
    clips = []
    last_end = 0

    for (start, end) in silence_periods:
        if last_end < start:
            clips.append(video.subclip(last_end, start))
        last_end = end

    # Add the final clip if there's any remaining video after the last silence
    if last_end < video.duration:
        clips.append(video.subclip(last_end, video.duration))

    # Concatenate the remaining clips
    if clips:
        final_clip = concatenate_videoclips(clips)
        # Write the result to a file
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")
    else:
        # If no clips are left after cutting silences, save the original video
        video.write_videofile(output_video, codec="libx264", audio_codec="aac")

# Example usage:
if __name__ == "__main__":
    video_path = "input_video.mp4"       # Path to your video file
    output_path = "output_video.mp4"    # Path to save the edited video

    video = VideoFileClip(video_path)
    video_duration = video.duration

    # Step 1: Transcribe the video
    transcription_result = transcribe_video(video_path)
    print("Transcript", transcription_result)

    # Step 2: Identify silence periods
    silence_periods = identify_silence_periods(transcription_result, video_duration, threshold=0.5)

    # Step 3: Cut silences from the video
    cut_silences(video_path, output_path, silence_periods)
