import requests
import os
import time

def baixar_lei(nome, url):
    print(f"📥 Tentando baixar {nome}...")
    
    # Cabeçalhos para fingir ser um navegador real (evita bloqueios)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Aumentamos o timeout para 60 segundos (mais paciência)
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status() # Verifica se a página carregou certo
        
        # Cria o caminho da pasta biblioteca_juridica (um nível acima da pasta app)
        pasta_destino = os.path.join("..", "biblioteca_juridica")
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            
        caminho_arquivo = os.path.join(pasta_destino, f"{nome}.txt")
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"✅ {nome} salvo com sucesso!")
        
        # Pequena pausa para não sobrecarregar o servidor do governo
        time.sleep(2) 
        
    except Exception as e:
        print(f"❌ Erro ao baixar {nome}: {e}")

# Lista de links (Priorizando os que você pediu)
leis_para_baixar = {
    "Constituicao_Federal": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm",
    "Codigo_Civil": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",
    "CPC": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm",
    "CLT": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm",
    "CTN": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm",
    "CTE_Goias": "https://appasp.economia.go.gov.br/legislacao/arquivos/CTE/CTE.htm"
}

if __name__ == "__main__":
    print("🚀 INICIANDO SUPER RASPADOR JURÍDICO...")
    for nome, url in leis_para_baixar.items():
        baixar_lei(nome, url)
    print("\n🏁 Processo finalizado!")