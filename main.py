import sys
import os
import datetime
import pyaudio
import wave
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget, QHBoxLayout

class VoiceRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording = False

    def initUI(self):
        self.setWindowTitle("Voice Recorder")
        self.setGeometry(100, 100, 400, 400)

        self.record_btn = QPushButton("Record")
        self.stop_btn = QPushButton("Stop")
        self.save_btn = QPushButton("Save")
        self.record_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.save_btn.clicked.connect(self.save_recording)
        self.record_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(False)

        self.recordings_list = QListWidget()
        self.recordings_list.itemClicked.connect(self.load_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.record_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.recordings_list)
        self.setLayout(layout)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.record_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.save_btn.setEnabled(False)
            self.recorded_frames = []
            self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            self.recordings_list.clear()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.record_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.save_btn.setEnabled(True)
            self.stream.stop_stream()
            self.stream.close()

            # Add the recorded audio to the list
            self.recordings_list.addItem("Recording {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def save_recording(self):
        if not self.recorded_frames:
            return
        output_filename = datetime.datetime.now().strftime("recording_%Y%m%d%H%M%S.wav")
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.recorded_frames))
        self.recordings_list.currentItem().setData(1, output_filename)

    def load_recording(self):
        item = self.recordings_list.currentItem()
        if item:
            recording_filename = item.data(1)
            if recording_filename:
                os.system(f"start {recording_filename}")  # On Windows, open the default media player to play the recording

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceRecorderApp()
    ex.show()
    sys.exit(app.exec_())
