import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=180, stream=True)
        response.raise_for_status() 
        
        # Tratamento de encoding para não quebrar acentos no TXT
        texto_html = response.content.decode('iso-8859-1')

        soup = BeautifulSoup(texto_html, 'html.parser')
        todas_as_linhas = soup.find_all('tr')
        
        lista_tarifas = []
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    # Formatação do valor (0,00)
                    v_raw = limpar(cols[3].text).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        valor_num = "{:.2f}".format(float(v_raw)).replace('.', ',')
                    except:
                        valor_num = "0,00"

                    lista_tarifas.append([
                        codigo_txt, limpar(cols[1].text), limpar(cols[2].text), 
                        valor_num, limpar(cols[4].text), limpar(cols[5].text), 
                        limpar(cols[7].text), limpar(cols[8].text), limpar(cols[9].text)
                    ])

        # GRAVAÇÃO EM TXT
        with open('tarifas_senior.txt', 'w', encoding='iso-8859-1', newline='') as f:
            # Mantemos o delimitador ; pois o importador da Senior aceita em TXT
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 'Prazo cartão novo', 'UF', 'Cidade', 'Data Tarifa'])
            writer.writerows(lista_tarifas)
        
        print(f"✅ TXT gerado com {len(lista_tarifas)} linhas!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
