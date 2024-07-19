# extract the caption words from a short video
# https://python.plainenglish.io/polyglot-captions-transforming-multilingual-content-with-python-powered-caption-generation-7036da70d834


import ffmpeg
import os
import time
from googletrans import Translator
from faster_whisper import WhisperModel

class AudioGenerator:
    """
    Extract audio from video.
    """

    def __init__(self,video):
        self.video = video

    def get_audio(self):
        audio = f"{os.path.splitext(self.video)[0]}_audio.mp3"
        
        ffmpeg.input(self.video).output(audio).run(overwrite_output=True)
        return audio

        
class AudioToCaptions:
    """
    Transcribe captions from audio using speech recognition model Whisper.
    """

    def __init__(self,audio):
        self.audio = audio

    def transcribe(self):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio)
        language = info[0]
        segments = list(segments)
        return segments
    


# translate the caption words into english

class TranslateToEnglish:

    def __init__(self,caption_segments):
        self.segments = caption_segments

    def translate(self):

        translator = Translator()
        
        language = 'English'

        subtitle_file = f'subtitle.{language}.srt'
        text = ""
        for index, segment in enumerate(self.segments):
            segment_start = time.strftime('%H:%M:%S,000',time.gmtime(segment.start))
            segment_end = time.strftime('%H:%M:%S,000',time.gmtime(segment.end))
            text += f"{str(index + 1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            translated_text = translator.translate(segment.text,dest='en')
            text += f"{translated_text.text} \n"
            text += "\n"
        
        with open(subtitle_file, "w", encoding="utf-8") as f:
            f.write(text)

        return subtitle_file





# replace the caption in the video to the tanslated words


class AddSubtitle:

    def __init__(self,video,subtitle):
        self.video = video
        self.subtitle = subtitle

    def add_sub(self):
        output_file = f"{self.video.replace('.mp4','')}_with_captions.mp4"


        video_stream = ffmpeg.input(self.video)

        ffmpeg.concat(video_stream.filter("subtitles",self.subtitle),video_stream.audio,v=1,a = 1).output(output_file).run(overwrite_output=True)

        return output_file


# run

if __name__ == '__main__':
    audio = AudioGenerator("sample.mp4").get_audio()
    captions = AudioToCaptions(audio).transcribe()
    translated_captions = TranslateToEnglish(captions).translate()
    AddSubtitle("sample.mp4",translated_captions).add_sub()



