from io import BytesIO

import librosa
import noisereduce as nr
from pydub import AudioSegment
import soundfile as sf


def convert_audio(audio_bytestream: BytesIO, input_format: str) -> BytesIO:
    """Функция принимает байтстрим аудиофайла и его исходный формат,
    конвертируя его в WAV, меняя частоту дескритизации на 16 кГц,
    переключает в моноканальный режим.

    Args:
        audio_bytes (BytesIO):  Байтстрим аудиофайла.
        input_format (str): Исходный формат файла.

    Returns:
        BytesIO: Байтстрим конвертированного файла.
    """
    audio = AudioSegment.from_file(audio_bytestream, format=input_format)
    audio = audio.set_frame_rate(16000).set_channels(1)

    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer


def denoise_audio(audio_bytestream: BytesIO) -> BytesIO:
    """Функция принимает байтстрим аудиофайла и старается убрать
    лишние шумы из аудио для улучшения качества звучания речи.
    """
    y, sr = librosa.load(audio_bytestream, sr=16000, mono=True)

    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    buffer = BytesIO()
    sf.write(buffer, reduced_noise, sr, format="WAV", subtype="PCM_16")
    buffer.seek(0)
    return buffer
