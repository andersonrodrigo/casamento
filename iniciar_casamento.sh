#!/bin/bash

echo "========================================="
echo "   CASAMENTO IZABELLA & ANDERSON"
echo "========================================="
echo

cd "$(dirname "$0")"

echo "[1/3] Ativando ambiente Python..."
source venv/Scripts/activate

echo
echo "[2/3] Instalando/verificando dependencias..."
python -m pip install --upgrade pip
pip install flask pillow pillow-heif

echo
echo "[3/3] Iniciando servidor..."
echo
echo "========================================="
echo "   SERVIDOR DO CASAMENTO INICIADO"
echo "   http://localhost:8080"
echo "========================================="
echo

python app.py

echo
echo "========================================="
echo "   SERVIDOR ENCERRADO"
echo "========================================="
read -p "Pressione ENTER para fechar..."