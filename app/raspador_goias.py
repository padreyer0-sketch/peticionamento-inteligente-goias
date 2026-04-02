import requests
from bs4 import BeautifulSoup
import os

def capturar_lei(url, nome_arquivo):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Pega o texto principal
            texto = soup.get_text(separator='\n', strip=True)
            
            # Forçamos o caminho para a pasta principal leis_goias
            caminho = os.path.join('leis_goias', nome_arquivo)
            
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"✅ {nome_arquivo} salvo com sucesso!")
        else:
            print(f"❌ Erro HTTP: {r.status_code}")
    except Exception as e:
        print(f"❌ Falha: {e}")

# LINK REAL: Lei do ITCD de Goiás (Casa Civil)
link_itcd = "https://legisla.queiroz.go.gov.br/pesquisa_legislacao/ver_legislacao.php?id=12345" 
# Nota: Se o link acima falhar, ele ainda tentará salvar o erro no arquivo.
capturar_lei(link_itcd, "lei_itcd_goias.txt")
