# -*- coding: utf-8 -*-
from fastapi import FastAPI, UploadFile, File
import os
import shutil
import glob
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

LOGS_DIR = "logs"
OUTPUT_DIR = "output"
UPLOAD_DIR = "uploaded_logs_temp"

# Garante que os diretórios necessários existem
def garantir_pasta(pasta: str):
    """Cria o diretório se ele não existir."""
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        logging.info(f"Diretório criado: {pasta}")

def salvar_json(dados: list, filepath: str):
    """Salva os dados de análise em um arquivo JSON."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        logging.info(f"Análise salva em: {filepath}")
    except IOError as e:
        logging.error(f"Erro ao salvar o arquivo JSON {filepath}: {e}")

def analisar_linha(linha: str):
    """
    Classifica eventos de log conforme risco, com justificativa e mitigação
    """
    linha_lower = linha.lower()

    if "failed password" in linha_lower or "authentication failure" in linha_lower:
        return {
            "evento": linha.strip(),
            "risco": "Alto",
            "justificativa": "Tentativa de acesso não autorizado detectada.",
            "acao_mitigadora": "Habilitar bloqueio após múltiplas tentativas e revisar acessos."
        }
    elif "connection refused" in linha_lower or "timeout" in linha_lower:
        return {
            "evento": linha.strip(),
            "risco": "Médio",
            "justificativa": "Falha de conexão pode indicar scanner de rede ou instabilidade.",
            "acao_mitigadora": "Verificar firewall, IDS/IPS e estabilidade do serviço."
        }
    elif "error" in linha_lower or "warn" in linha_lower:
        return {
            "evento": linha.strip(),
            "risco": "Baixo",
            "justificativa": "Erro genérico identificado no log.",
            "acao_mitigadora": "Revisar logs de aplicação e corrigir configuração."
        }
    else:
        return {
            "evento": linha.strip(),
            "risco": "Informativo",
            "justificativa": "Sem indícios de risco relevante.",
            "acao_mitigadora": "Nenhuma ação necessária."
        }

def processar_logs_do_diretorio():
    """Processa todos os arquivos de log nos diretórios 'logs' e 'uploaded_logs_temp'."""
    garantir_pasta(LOGS_DIR)
    garantir_pasta(OUTPUT_DIR)

    arquivos = glob.glob(os.path.join(LOGS_DIR, "*.log")) + \
               glob.glob(os.path.join(LOGS_DIR, "*.txt"))
    
    arquivos += glob.glob(os.path.join(UPLOAD_DIR, "*.log")) + \
               glob.glob(os.path.join(UPLOAD_DIR, "*.txt"))

    resultados_totais = {}
    if not arquivos:
        return {"processados": "Nenhum arquivo de log encontrado para processar."}

    for arquivo in arquivos:
        nome_arquivo = os.path.basename(arquivo)
        resultados = []
        try:
            with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                for linha in f:
                    if linha.strip():
                        resultados.append(analisar_linha(linha))
        except IOError as e:
            logging.error(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
            continue

        saida_json_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(nome_arquivo)[0]}.json")
        salvar_json(resultados, saida_json_path)
        resultados_totais[nome_arquivo] = saida_json_path
    
    for arquivo_temp in glob.glob(os.path.join(UPLOAD_DIR, "*")):
        shutil.move(arquivo_temp, os.path.join(LOGS_DIR, os.path.basename(arquivo_temp)))
        logging.info(f"Arquivo movido de '{UPLOAD_DIR}' para '{LOGS_DIR}': {os.path.basename(arquivo_temp)}")

    return {"processados": resultados_totais}


# Endpoint raiz
@app.get("/")
def root():
    """Mensagem de boas-vindas para o Mini-SIEM."""
    return {"message": "Mini-SIEM rodando 🚀"}

# Endpoint para processar logs em lote
@app.get("/analisar")
def analisar_logs():
    """
    Processa todos os arquivos .log e .txt presentes no diretório 'logs/'
    e gera um relatório JSON para cada um.
    """
    logging.info("Iniciando a análise de todos os logs existentes.")
    return processar_logs_do_diretorio()

@app.post("/upload_log")
async def upload_log(file: UploadFile = File(...)):
    """
    Recebe um arquivo de log via upload, o salva, analisa e retorna a análise.
    O arquivo de log original é salvo para processamento futuro.
    """
    garantir_pasta(UPLOAD_DIR)
    
    filepath_temp = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(filepath_temp, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.info(f"Arquivo temporariamente salvo: {filepath_temp}")
    except IOError as e:
        return {"erro": f"Erro ao salvar o arquivo: {e}"}

    resultados = processar_logs_do_diretorio()

    return {
        "arquivo_recebido": file.filename,
        "saida_analise": resultados.get("processados", {}).get(file.filename),
        "total_linhas": len(resultados.get("processados", {}).get(file.filename, []))
    }

if __name__ == "__main__":
    import uvicorn
    garantir_pasta(LOGS_DIR)
    garantir_pasta(OUTPUT_DIR)
    garantir_pasta(UPLOAD_DIR)
    logging.info("🔍 Iniciando o Mini-SIEM...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
