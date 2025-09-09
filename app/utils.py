import os
import json

def garantir_pasta(pasta: str):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def salvar_json(dados, caminho: str):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
