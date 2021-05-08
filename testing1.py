import scipy.signal as signal
import matplotlib.pyplot as plt
def stft(x, **params):
    ''' 
    :param x: 
    :param params: 
    :return: 
    ''''''

    :param x: input signal
         :param params: {fs: sampling frequency;
                                         Window: window. The default is the Hamming window;
                                         Nperseg: the length of each segment, the default is 256,
                                         Noverlap: The number of points overlapped. The COLA constraint needs to be met when specifying a value. The default is half the length of the window.
                                         Nfft: fft length,
                                         Detrend: (str, function or False) specifies how to go to the trend, the default is Flase, not to trend.
                                         Return_onesided: The default is True, which returns a one-sided spectrum.
                                         Boundary: By default, 0 is added to both ends of the time series.
                                         Padded: whether to fill the time series with 0 (when the length is not enough),
                                         Axis: you don't have to care about this parameter}
         :return: f: sampling frequency array; t: segment time array; Zxx: STFT result
    '''
    f, t, zxx = signal.stft(x, **params)
    return f, t, zxx


 Def stft_specgram(x, picname=None, **params): #picname is the name given to the image, in order to save the image
    f, t, zxx = stft(x, **params)
    plt.pcolormesh(t, f, np.abs(zxx))
    plt.colorbar()
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.tight_layout()
    if picname is not None:
                 Plt.savefig('..\\picture\\' + str(picname) + '.jpg') #Save Image
         Plt.clf() #Clear the canvas
    return t, f, zxx
