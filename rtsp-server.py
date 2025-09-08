import subprocess

def stream_audio(file_path, rtsp_url="rtsp://localhost:8554/audio"):
    cmd = [
        "ffmpeg",
        "-re",                # envia no tempo real (não mais rápido que o normal)
        "-i", file_path,      # arquivo de entrada (ex: musica.mp3)
        "-acodec", "aac",     # codec de áudio
        "-ar", "44100",       # taxa de amostragem
        "-ac", "2",           # número de canais
        "-f", "rtsp",         # formato de saída
        "-rtsp_transport", "tcp",  # transporte via TCP
        rtsp_url
    ]

    subprocess.call(cmd)

if __name__ == "__main__":
    # exemplo de uso
    stream_audio("assets/samba.wav", "rtsp://localhost:8554/audio")
