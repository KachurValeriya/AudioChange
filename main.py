import sys
import librosa
import soundfile as sf
import noisereduce as nr
from PyQt6.QtWidgets import *

app = QApplication(sys.argv)
win = QMainWindow()
win.setWindowTitle("обработчик аудио")
win.setMinimumSize(400, 200)
central = QWidget()
win.setCentralWidget(central)
layout = QVBoxLayout(central)
load = QPushButton("загрузить")
label = QLabel("файл не выбран")
denoise = QPushButton("удалить шум")
denoise.setEnabled(False)
pitch = QPushButton("изменить тембр")
pitch.setEnabled(False)
save = QPushButton("сохранить")
save.setEnabled(False)
layout.addWidget(load)
layout.addWidget(label)
layout.addWidget(denoise)
layout.addWidget(pitch)
layout.addWidget(save)

audio = sr = result = None

def load_func():
    global audio, sr
    path = QFileDialog.getOpenFileName(win, "выберите аудио", "", "*.wav *.mp3")[0]
    if path:
        audio, sr = librosa.load(path)
        label.setText(path)
        for btn in (denoise, pitch, save):
            btn.setEnabled(True)

def denoise_func():
    global audio, result, sr
    if len(audio) > 0:
        result = nr.reduce_noise(y=audio, sr=sr)
        QMessageBox.information(win, "готово", "шум удалён!")

def pitch_func():
    global audio, result, sr
    if len(audio) > 0:
        user_input = QInputDialog.getInt(win, "тембр", "от -5 до 5:", 0, -5, 5)
        steps = user_input[0] 
        ok = user_input[1]    
        if ok:
            result = librosa.effects.pitch_shift(audio, sr=sr, n_steps=steps)
            QMessageBox.information(win, "готово", "тембр изменён")

def save_func():
    if sr:
        path = QFileDialog.getSaveFileName(win, "сохранить", "", "*.wav")[0]
        if path:
            if len(result) > 0:
                sf.write(path, result, sr)
            else:
                sf.write(path, audio, sr)
            QMessageBox.information(win, "готово", "сохранено!")

load.clicked.connect(load_func)
denoise.clicked.connect(denoise_func)
pitch.clicked.connect(pitch_func)
save.clicked.connect(save_func)

win.show()
sys.exit(app.exec())