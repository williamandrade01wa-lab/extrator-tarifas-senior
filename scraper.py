import requests
from bs4 import BeautifulSoup
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        # Se o site usa ISO-8859-1, convertemos explicitamente aqui
        # Isso corrige MaceiÃ³ -> Maceió
        texto_corrigido = response.content.decode('iso-8859-1')
        
        soup = BeautifulSoup(texto_corrigido, 'html.parser')
        tabelas = soup.find_all('table')
        
        lista_tarifas = []
        for tab in tabelas:
            linhas = tab.find_all('tr')
            if len(linhas) > 5:
                for linha in linhas:
                    cols = linha.find_all('td')
                    if len(cols) >= 4 and cols[0].text.strip().isdigit():
                        
                        valor_texto = cols[3].text.strip().replace('.', '').replace(',', '.')
                        try:
                            valor_num = float(valor_texto)
                        except:
                            valor_num = 0.0

                        lista_tarifas.append({
                            "codigo": cols[0].text.strip(),
                            "nome": cols[1].text.strip(),
                            "fornecedor": cols[2].text.strip(),
                            "valor": valor_num,
                            "uf": cols[7].text.strip() if len(cols) > 7 else "",
                            "cidade": cols[8].text.strip() if len(cols) > 8 else ""
                        })
        
        # Salvamos com UTF-8 explícito
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso: {len(lista_tarifas)} itens.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
