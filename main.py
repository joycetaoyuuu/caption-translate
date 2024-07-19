
# reference: https://python.plainenglish.io/polyglot-captions-transforming-multilingual-content-with-python-powered-caption-generation-7036da70d834

# packages
import ffmpeg
import os
import time
from googletrans import Translator
from faster_whisper import WhisperModel

class AudioGenerator:
    """
    Get audio from video.
    """

    def __init__(self):
        pass

    def get_audio(self,video):
        """
        Extracts audio from video and save the audio in the mp3 format.
        Parameters:
            video (str): The name of the video file.
        Returns:
            str: The name of the audio file.
        """
        self.video = video
        audio = f"{os.path.splitext(self.video)[0]}_audio.mp3"
        
        # use ffmpeg to extract audio from the input video
        ffmpeg.input(self.video).output(audio).run(overwrite_output=True)

        return audio

        
class AudioToCaptions:
    """
    Get captions from audio.
    """

    def __init__(self):
        pass

    def transcribe(self,audio):
        """
        Transcribes captions from audio using speech recognition model Whisper.
        Parameters:
            audio (str): The name of audio file.
        Returns:
            list: List of segments of captions.
        """
        self.audio = audio
        model = WhisperModel("small") # load the whisper model
        segments, info = model.transcribe(audio) # audio to text
        language = info[0]
        segments = list(segments)
        return segments
    


class CaptionTranslator:
    """
    Translate captions to another language.
    """

    def __init__(self,caption_segments):
        """
        Parameters:
            segments (list): List of segments of the captions.
        """
        self.segments = caption_segments

    def translate(self,language):
        """
        Translates the captions to another language using googletrans.
        Parameters:
            language (str): the destination language
        Returns:
            str: the name of the translated caption file.
        """

        translator = Translator() # load the translator

        subtitle_file = f'subtitle.{language}.srt' # define the return file
        text = ""
        # go through each segment
        for index, segment in enumerate(self.segments):
            segment_start = time.strftime('%H:%M:%S,000',time.gmtime(segment.start)) # reformat the timestamp
            segment_end = time.strftime('%H:%M:%S,000',time.gmtime(segment.end)) # reformat the timestamp
            text += f"{str(index + 1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            translated_text = translator.translate(segment.text,dest=language) # translate the text
            text += f"{translated_text.text} \n" # add to text
            text += "\n"
        
        with open(subtitle_file, "w", encoding="utf-8") as f: # save to the file
            f.write(text)

        return subtitle_file



class AddSubtitle:
    """
    Add the subtitle to the video.
    """

    def __init__(self,video):
        self.video = video

    def add_sub(self,subtitle):
        """
        Add the given subtitle to the video.
        Parameters:
            subtitle (str): The name of the subtitle.
        Returns:
            str: The name of the video with new subtitle.
        """
        self.subtitle = subtitle

        output_file = f"{self.video.replace('.mp4','')}_with_captions.mp4"

        video_stream = ffmpeg.input(self.video)

        # add subtitle and audio to the video
        style = "Fontsize=23,BackColour=&H80000000,BorderStyle=3"
        ffmpeg.concat(video_stream.filter("subtitles",self.subtitle,force_style = style),video_stream.audio,v=1,a = 1).output(output_file).run(overwrite_output=True)

        return output_file


# run the script

if __name__ == '__main__':
    audio = AudioGenerator().get_audio("sample.mp4")
    captions = AudioToCaptions().transcribe(audio)
    translated_captions = CaptionTranslator(captions).translate('en')
    AddSubtitle("sample.mp4").add_sub(translated_captions)



