import numpy as np
import matplotlib.pyplot as plt

fig,axs=plt.subplots(2,3)


t=np.arange(0,1,1e-3)

y=np.zeros_like(t)

for f in [10,30,50,70,90]:
    y+=np.sin(2*np.pi*f*t)
axs[0,0].plot(t,y)



w=np.hanning(t.shape[0])




y_windowed=y*w
axs[0,1].plot(t,y_windowed)


y_windowed_fft=np.fft.fft(y_windowed)

axs[0,2].plot(y_windowed_fft.real)
axs[0,2].plot(y_windowed_fft.imag)

y_windowed_fft_ifft=np.fft.ifft(y_windowed_fft)
axs[1,0].plot(np.abs(y_windowed_fft))
axs[1,1].plot(y_windowed_fft_ifft)
axs[1,2].plot(y_windowed_fft_ifft/w)

plt.show()