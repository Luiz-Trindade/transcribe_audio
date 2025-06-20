import os
import subprocess
import whisper
from concurrent.futures import ProcessPoolExecutor as Process

default_workers = os.cpu_count() or 4
whisper_model   = "tiny"
INPUT_DIR       = "./files"  
OUTPUT_DIR      = "transcricoes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Extensões suportadas para transcrição
audio_video_exts = (".mp3", ".wav", ".mkv", ".mp4", ".flac", ".avi", ".webm", ".m4a", ".mts")

# Função que converte MTS para MP3 e remove o original
def ensure_mp3(file_path: str) -> str:
    base, ext = os.path.splitext(file_path)
    if ext.lower() == ".mts":
        mp3_path = f"{base}.mp3"
        # se já existe mp3, usa direto
        if not os.path.exists(mp3_path):
            cmd = ["ffmpeg", "-i", file_path, "-q:a", "4", "-vn", mp3_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Convertido para MP3: {file_path} -> {mp3_path}")
        # remove o arquivo original
        os.remove(file_path)
        return mp3_path
    return file_path

# Função para transcrever um arquivo de áudio
def transcribe(file_name: str):
    try:
        model = whisper.load_model(whisper_model)
        
        file_path = os.path.join(INPUT_DIR, file_name)
        # converte se necessário
        work_path = ensure_mp3(file_path)

        print(f"🎙️ Iniciando transcrição: {os.path.basename(work_path)}")
        res = model.transcribe(work_path, fp16=False)

        out_txt = os.path.splitext(os.path.basename(work_path))[0] + "_transcript.txt"
        out_path = os.path.join(OUTPUT_DIR, out_txt)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res["text"])
        print(f"✅ Transcrição salva: {out_path}")

    except Exception as e:
        print(f"❌ Erro em '{file_name}': {e}")

# Lê todos os arquivos suportados e executa em paralelo
if __name__ == "__main__":
    # lista inicial
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(audio_video_exts)]
    if not files:
        print("Nenhum arquivo de áudio/vídeo encontrado no diretório.")
    else:
        with Process(max_workers=min(default_workers, len(files))) as executor:
            executor.map(transcribe, files)
