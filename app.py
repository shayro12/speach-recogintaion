from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

def transcript_extract(video_name):
    import speech_recognition as sr
    from pydub import AudioSegment
    import os

    # Load the video file
    v_format= video_name.split(".")[-1]
    video = AudioSegment.from_file(video_name, format=v_format)
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export("audio.wav", format="wav")

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Open the audio file
    with sr.AudioFile("audio.wav") as source:
        audio_text = r.record(source)
    # Recognize the speech in the audio
    text = r.recognize_google(audio_text, language='en-US')
    return text




app = Flask(__name__)

@app.route("/", methods=['GET'])
def default():
    return 'hello world',200


@app.route('/upload')
def upload_file_land():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      output=transcript_extract(f.filename)
      return f'transcript is:\t{output}'
		
if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True , port=5000)
