import requests
from bs4 import BeautifulSoup
import os

def raspar_lei_goias(url, nome_arquivo):
    print(f"--- Iniciando extração de: {url} ---")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 1. O robô "visita" o site
        resposta = requests.get(url, headers=headers, timeout=15)
        resposta.encoding = 'utf-8' # Garante que os acentos fiquem certos
        
        if resposta.status_code == 200:
            # 2. O robô "lê" o HTML do site
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # 3. Limpeza: Pegamos apenas o texto (removemos menus e anúncios)
            # Dica: Em sites do governo, o texto costuma estar em 'body' ou 'article'
            texto_limpo = soup.get_text(separator='\n', strip=True)
            
            # 4. Caminho para salvar na pasta de leis
            caminho_salvar = os.path.join('leis_goias', nome_arquivo)
            
            # 5. Criamos o arquivo .txt com o conteúdo
            with open(caminho_salvar, 'w', encoding='utf-8') as f:
                f.write(texto_limpo)
            
            print(f"✅ Sucesso! Lei salva em: {caminho_salvar}")
        else:
            print(f"❌ Erro ao acessar o site: Status {resposta.status_code}")

    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

# --- TESTE DO ROBÔ ---
# Exemplo: Link de uma lei tributária de Goiás (você pode trocar pelo link que quiser)
link_exemplo = "https://legisla.queiroz.go.gov.br/pesquisa_legislacao/ver_legislacao.php?id=12345" 
raspar_lei_goias(link_exemplo, "lei_atualizada.txt")
