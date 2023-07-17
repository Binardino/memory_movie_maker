import os
import random
from moviepy.editor import ImageSequenceClip, VideoFileClip, concatenate_videoclips
from moviepy.audio.io import AudioFileClip

def create_wrapup_video(videos_path, photos_path, output_path, music_path=None):
    # Get a list of videos and sort them by date
    videos = sorted([f for f in os.listdir(videos_path) if f.endswith(('.mp4', '.avi', '.mov'))],
                    key=lambda x: os.path.getctime(os.path.join(videos_path, x)))

    # Get a list of photos and sort them by date
    photos = sorted([f for f in os.listdir(photos_path) if f.endswith(('.jpg', '.jpeg', '.png'))],
                    key=lambda x: os.path.getctime(os.path.join(photos_path, x)))

    clips = []
    sequence = []

    # Add videos to the clips list and sequence
    for video in videos:
        video_clip = VideoFileClip(os.path.join(videos_path, video))
        clips.append(video_clip)
        sequence.append(video)

        # Add a random delay between videos
        delay = random.uniform(0.5, 1.5)
        clips.append(video_clip.fx(VideoFileClip.set_duration, video_clip.duration + delay))
        sequence.append(None)

    # Add photos to the clips list and sequence
    num_photos = len(photos)
    for i in range(0, num_photos, 15):
        photo_group = photos[i:i+15]
        for photo in photo_group:
            photo_clip = ImageSequenceClip([os.path.join(photos_path, photo)], durations=[0.5])
            clips.append(photo_clip)
            sequence.append(photo)

    final_clip = concatenate_videoclips(clips)
    final_clip.set_fps(24)  # Set the FPS value

    if music_path:
        # Add the soundtrack to the final clip
        music = AudioFileClip(music_path)
        final_clip = final_clip.set_audio(music)

    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    return sequence

# Example usage
videos_folder = r'C:\Users\LangloisR\Pictures\Screenshots'
photos_folder = r'C:\Users\LangloisR\Pictures\Screenshots'
output_file = r'C:\Users\LangloisR\Pictures\Screenshotsvideo.mp4'
#music_file = r'C:\Users\LangloisR\Pictures\Screenshots/music.mp3'  # Optional

sequence = create_wrapup_video(videos_folder, photos_folder, output_file) #, music_file)

# To regenerate the video with a custom order
# Modify the 'sequence' list as desired, then call the function again
# new_output_file = '/path/to/new_output/video.mp4'
# create
