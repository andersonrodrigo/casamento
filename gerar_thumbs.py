#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps
import time

ORIGINAIS = Path("/Volumes/CASAMENTO/fotos")
THUMBS = Path("/Volumes/CASAMENTO/fotos_thumbs")
MAX_LADO = 800
QUALIDADE = 75
EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}

def gerar_thumb(origem, destino):
    imagem = Image.open(origem)
    imagem = ImageOps.exif_transpose(imagem)
    if imagem.mode != "RGB":
        imagem = imagem.convert("RGB")
    imagem.thumbnail((MAX_LADO, MAX_LADO), Image.Resampling.LANCZOS)
    destino.parent.mkdir(parents=True, exist_ok=True)
    imagem.save(destino, "JPEG", quality=QUALIDADE, optimize=True)

def main():
    if not ORIGINAIS.exists():
        print(f"ERRO: pasta não encontrada: {ORIGINAIS}")
        return
    THUMBS.mkdir(parents=True, exist_ok=True)
    arquivos = [p for p in ORIGINAIS.iterdir()
                if p.is_file() and p.suffix.lower() in EXTENSOES]
    print("=" * 60)
    print("GERADOR DE THUMBNAILS")
    print("=" * 60)
    print(f"Originais : {ORIGINAIS}")
    print(f"Thumbnails: {THUMBS}")
    print(f"Fotos     : {len(arquivos)}")
    inicio = time.time()
    criadas = ignoradas = erros = 0
    for i, origem in enumerate(arquivos, 1):
        destino = THUMBS / f"{origem.stem}.jpg"
        if destino.exists():
            ignoradas += 1
            continue
        try:
            gerar_thumb(origem, destino)
            criadas += 1
            print(f"[{i}/{len(arquivos)}] OK   {origem.name}")
        except Exception as e:
            erros += 1
            print(f"[{i}/{len(arquivos)}] ERRO {origem.name}: {e}")
    print()
    print("=" * 60)
    print("FINALIZADO")
    print("=" * 60)
    print(f"Criadas  : {criadas}")
    print(f"Ignoradas: {ignoradas}")
    print(f"Erros    : {erros}")
    print(f"Tempo    : {time.time() - inicio:.1f}s")
    print(f"Destino  : {THUMBS}")

if __name__ == "__main__":
    main()
