import librosa
import librosa.display
import IPython.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as ms
ms.use('seaborn-muted')


# Load the example track
y, sr = librosa.load('/usr/share/sounds/alsa/Front_Center.wav')
print ('a')
# Play it back!
IPython.display.Audio(data=y, rate=sr)

# How about separating harmonic and percussive components?
y_h, y_p = librosa.effects.hpss(y)
print ('b')
# Play the harmonic component
IPython.display.Audio(data=y_h, rate=sr)

# Play the percussive component
IPython.display.Audio(data=y_p, rate=sr)
print ('c')
# Pitch shifting?  Let's gear-shift by a major third (4 semitones)
y_shift = librosa.effects.pitch_shift(y, sr, 7)

IPython.display.Audio(data=y_shift, rate=sr)

# Or time-stretching?  Let's slow it down
y_slow = librosa.effects.time_stretch(y, 0.5)

IPython.display.Audio(data=y_slow, rate=sr)

# How about something more advanced?  Let's decompose a spectrogram with NMF, and then resynthesize an individual component
D = librosa.stft(y)

# Separate the magnitude and phase
S, phase = librosa.magphase(D)
print ('d')
# Decompose by nmf
print ('h')
components, activations = librosa.decompose.decompose(S, n_components=8, sort=True)
print ('g')
# Visualize the components and activations, just for fun

plt.figure(figsize=(12,4))
print ('e')
plt.subplot(1,2,1)
librosa.display.specshow(librosa.logamplitude(components**2.0, ref_power=np.max), y_axis='log')
plt.xlabel('Component')
plt.ylabel('Frequency')
plt.title('Components')

plt.subplot(1,2,2)
librosa.display.specshow(activations, x_axis='time')
plt.xlabel('Time')
plt.ylabel('Component')
plt.title('Activations')
print ('f')
plt.tight_layout()

print(components.shape, activations.shape)

# Play back the reconstruction
# Reconstruct a spectrogram by the outer product of component k and its activation
D_k = components.dot(activations)

# invert the stft after putting the phase back in
y_k = librosa.istft(D_k * phase)

# And playback
print('Full reconstruction')

IPython.display.Audio(data=y_k, rate=sr)

# Resynthesize.  How about we isolate just first (lowest) component?
k = 0

# Reconstruct a spectrogram by the outer product of component k and its activation
D_k = np.multiply.outer(components[:, k], activations[k])

# invert the stft after putting the phase back in
y_k = librosa.istft(D_k * phase)

# And playback
print('Component #{}'.format(k))

IPython.display.Audio(data=y_k, rate=sr)

# Resynthesize.  How about we isolate a middle-frequency component?
k = len(activations) / 2

# Reconstruct a spectrogram by the outer product of component k and its activation
D_k = np.multiply.outer(components[:, k], activations[k])

# invert the stft after putting the phase back in
y_k = librosa.istft(D_k * phase)

# And playback
print('Component #{}'.format(k))

IPython.display.Audio(data=y_k, rate=sr)

# Resynthesize.  How about we isolate just last (highest) component?
k = -1

# Reconstruct a spectrogram by the outer product of component k and its activation
D_k = np.multiply.outer(components[:, k], activations[k])

# invert the stft after putting the phase back in
y_k = librosa.istft(D_k * phase)

# And playback
print('Component #{}'.format(k))

IPython.display.Audio(data=y_k, rate=sr)
