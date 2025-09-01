import subprocess
import sounddevice as sd
import numpy as np

RTSP_URL = "rtsp://localhost:8554/audio"

def play_rtsp_audio():
    # Comando ffmpeg para capturar e converter o áudio em PCM cru
    cmd = [
        "ffmpeg",
        "-i", RTSP_URL,           # entrada RTSP
        "-vn",                    # ignora vídeo
        "-f", "s16le",            # saída: PCM 16-bit little endian
        "-acodec", "pcm_s16le",   # codec
        "-ac", "2",               # 2 canais (estéreo)
        "-ar", "44100",           # taxa de amostragem
        "pipe:1"                  # saída para stdout
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    sample_rate = 44100
    channels = 2
    blocksize = 1024

    # Cria stream de saída
    with sd.OutputStream(samplerate=sample_rate, channels=channels, dtype='int16') as stream:
        try:
            while True:
                # lê blocos de áudio cru
                raw_audio = process.stdout.read(blocksize * channels * 2)  # 2 bytes por amostra
                if not raw_audio:
                    break

                # converte para numpy
                audio_array = np.frombuffer(raw_audio, dtype=np.int16)

                # garante formato correto (N, canais)
                if len(audio_array) == 0:
                    continue
                audio_array = audio_array.reshape(-1, channels)

                # escreve no stream
                stream.write(audio_array)
        except KeyboardInterrupt:
            print("Interrompido pelo usuário")
        finally:
            process.kill()

if __name__ == "__main__":
    play_rtsp_audio()
