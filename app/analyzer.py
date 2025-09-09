import re

def analisar_linha(linha: str) -> dict:
    """Simples analisador de logs - pode ser expandido"""
    resultado = {
        "linha": linha.strip(),
        "nivel": None,
        "detalhes": None
    }

    if "error" in linha.lower():
        resultado["nivel"] = "ALERTA"
        resultado["detalhes"] = "Erro detectado"
    elif "fail" in linha.lower():
        resultado["nivel"] = "ALERTA"
        resultado["detalhes"] = "Falha detectada"
    elif "warning" in linha.lower():
        resultado["nivel"] = "AVISO"
        resultado["detalhes"] = "Possível problema"
    else:
        resultado["nivel"] = "INFO"
        resultado["detalhes"] = "Sem problemas"

    return resultado
