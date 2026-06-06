import librosa as lr
from pydub import AudioSegment
from librosa.effects import time_stretch
import soundfile as sf
from datetime import datetime

time = datetime.now()
y, sr = lr.load("ruka.mp3", sr= None)
speedup = time_stretch(y=y, rate=1.5)

sf.write("speedup.wav", speedup, sr)

print(f"work time:{datetime.now()-time}")