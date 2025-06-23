# 📝 Transcrição de Áudio/Vídeo com Vosk + Python

Este projeto realiza a transcrição automática de arquivos de áudio e vídeo usando o modelo offline [Vosk](https://alphacephei.com/vosk/). Ele processa vários arquivos em paralelo, realiza conversões automáticas e gera arquivos `.txt` com as transcrições.

## 📂 Estrutura
.
├── files/                    # Diretório de entrada com arquivos de áudio/vídeo
├── transcricoes/            # Saída com transcrições .txt
├── vosk-model-small-pt-0.3/ # Modelo Vosk em português
├── transcribe\_vosk.py       # Script principal
└── README.md

## ✅ Funcionalidades

- Suporte a vários formatos: `.mp3`, `.wav`, `.mp4`, `.mkv`, `.avi`, `.mts`, `.flac`, etc.
- Conversão automática de `.mts` para `.mp3` e depois para `.wav`
- Transcrição usando modelo Vosk offline
- Processamento paralelo com múltiplos núcleos
- Geração de arquivos `.txt` no diretório de saída
- 100% offline, sem dependência de nuvem

## ⚙️ Requisitos

- Python 3.7 ou superior
- FFmpeg instalado e disponível no PATH

### Instalação de dependências

```bash
pip install vosk pytranscript
```

## 📥 Baixar modelo Vosk

Baixe o modelo desejado (exemplo em português):

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip
```

## 🚀 Como usar

1. Coloque os arquivos de mídia em `./files`
2. Execute o script:

```bash
python transcribe_vosk.py
```

3. As transcrições aparecerão no diretório `./transcricoes`

## 🔄 Conversões automáticas

* `.mts` → `.mp3`
* qualquer formato de áudio → `.wav` válido para Vosk

Arquivos `.mts` são excluídos após conversão. Arquivos `.wav` antigos são sobrescritos automaticamente.

## 🧠 Créditos

* [Vosk](https://github.com/alphacep/vosk-api)
* [pytranscript](https://pypi.org/project/pytranscript/)

## 📄 Licença

Distribuído sob a licença MIT.
