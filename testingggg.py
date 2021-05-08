import sys
import random
import pandas as pd
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Widget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button = QtWidgets.QPushButton("Spectrogram")
        button.clicked.connect(self.plot)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.canvas)
        lay.addWidget(button)
        self.plot()

    def plot(self):
        samplingFrequency, signalData = wavfile.read('voice.wav')
        fig = plt.figure()
        plt.subplot(111)
        plt.specgram(signalData, Fs=samplingFrequency)
        plt.xlabel('Time(sec)')
        plt.ylabel('Frequency(Hz)')
        #plt.show()
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())