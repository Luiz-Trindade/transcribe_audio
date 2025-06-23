import os
import subprocess
from concurrent.futures import ProcessPoolExecutor as Process

from vosk import Model, KaldiRecognizer
import wave
import pytranscript as pt

# configuração geral
default_workers = os.cpu_count() or 4
INPUT_DIR       = "./files"
OUTPUT_DIR      = "transcricoes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# extensões suportadas
audio_video_exts = (
    ".mp3", ".wav", ".mkv", ".mp4", ".flac",
    ".avi", ".webm", ".m4a", ".mts"
)

# caminho para o seu modelo Vosk (substitua pelo local correto)
VOSK_MODEL_PATH = "./vosk-model-small-pt-0.3"


def ensure_mp3(file_path: str) -> str:
    """Converte .mts → .mp3 (se necessário) e remove o .mts original."""
    base, ext = os.path.splitext(file_path)
    if ext.lower() == ".mts":
        mp3_path = f"{base}.mp3"
        if not os.path.exists(mp3_path):
            cmd = ["ffmpeg", "-y", "-i", file_path, "-q:a", "4", "-vn", mp3_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Convertido para MP3: {file_path} → {mp3_path}")
        os.remove(file_path)
        return mp3_path
    return file_path


def to_wav(input_audio: str) -> str:
    """Gera um WAV válido para Vosk, removendo pré-existentes."""
    base, _ = os.path.splitext(input_audio)
    wav_path = f"{base}.wav"
    # remove se já existir
    if os.path.exists(wav_path):
        os.remove(wav_path)
    pt.to_valid_wav(input_audio, wav_path, start=0, end=None)
    print(f"🔄 WAV gerado: {wav_path}")
    return wav_path


def transcribe(file_name: str):
    """Função que cada worker irá executar."""
    try:
        # 1) converte MTS → MP3 e remove original
        in_path = os.path.join(INPUT_DIR, file_name)
        mp3_path = ensure_mp3(in_path)

        # 2) gera WAV válido
        wav_path = to_wav(mp3_path)

        # 3) abre WAV para obter sample rate
        wf = wave.open(wav_path, "rb")
        sr = wf.getframerate()

        # 4) carrega modelo e cria recognizer
        model = Model(VOSK_MODEL_PATH)
        rec = KaldiRecognizer(model, sr)

        # 5) processamento em streaming
        transcript_chunks = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                transcript_chunks.append(result)
        # resultado final
        transcript_chunks.append(rec.FinalResult())
        wf.close()

        # 6) coleta apenas o texto
        text = []
        for chunk in transcript_chunks:
            # cada chunk é JSON string com campo "text"
            try:
                import json
                obj = json.loads(chunk)
                text.append(obj.get("text", ""))
            except:
                continue

        # 7) gravação
        out_fname = os.path.splitext(os.path.basename(wav_path))[0] + "_transcript.txt"
        out_path  = os.path.join(OUTPUT_DIR, out_fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(" ".join(text))
        print(f"✅ Transcrição salva: {out_path}")

    except Exception as e:
        print(f"❌ Erro em '{file_name}': {e}")


if __name__ == "__main__":
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(audio_video_exts)]
    if not files:
        print("❌ Nenhum arquivo de áudio/vídeo encontrado no diretório.")
    else:
        workers = min(default_workers, len(files))
        print(f"🚀 Iniciando transcrição com {workers} workers...")
        with Process(max_workers=workers) as executor:
            executor.map(transcribe, files)
