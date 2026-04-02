import requests
from bs4 import BeautifulSoup
import os

def capturar_lei(url, nome_arquivo):
    print(f"--- Iniciando captura de: {url} ---")
    
    # Headers para o site não achar que somos um ataque hacker
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 1. Faz o pedido ao site
        r = requests.get(url, headers=headers, timeout=30)
        r.encoding = 'utf-8' # Garante que os acentos de Goiás fiquem corretos
        
        if r.status_code == 200:
            # 2. Limpa o HTML e extrai o texto
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Remove scripts e estilos CSS para o texto ficar limpo
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            # Pega o texto principal
            texto = soup.get_text(separator='\n', strip=True)
            
            # 3. Garante que a pasta de destino existe
            os.makedirs('leis_goias', exist_ok=True)
            
            # 4. Salva o arquivo .txt
            caminho = os.path.join('leis_goias', nome_arquivo)
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            
            print(f"✅ Sucesso: {nome_arquivo} salvo com {len(texto)} caracteres.")
        else:
            print(f"❌ Erro HTTP {r.status_code} ao acessar {url}")

    except Exception as e:
        print(f"❌ Falha crítica ao processar {nome_arquivo}: {e}")

# --- LISTA DE TAREFAS DO SEU ROBÔ (SITES ESTÁVEIS) ---
fontes_de_verdade = {
    "CTE_Goias.txt": "https://appasp.economia.go.gov.br/legislacao/arquivos/CTE/CTE.htm",
    "RCTE_Goias.txt": "http://appasp.economia.go.gov.br/legislacao/arquivos/Rcte/RCTE.htm",
    "Constituicao_Federal.txt": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm",
    "CTN_Nacional.txt": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm"
}

# Execução em lote
if __name__ == "__main__":
    for nome_txt, link_url in fontes_de_verdade.items():
        capturar_lei(link_url, nome_txt)
