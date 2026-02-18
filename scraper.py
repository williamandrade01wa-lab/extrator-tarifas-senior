import requests
from bs4 import BeautifulSoup
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'iso-8859-1'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tenta encontrar a tabela pelo seletor mais comum em sites ASP
        tabela = soup.find('table')
        
        lista_tarifas = []
        if tabela:
            linhas = tabela.find_all('tr')
            print(f"Encontradas {len(linhas)} linhas na tabela.")
            
            for linha in linhas:
                cols = linha.find_all('td')
                # Verificamos se a linha tem pelo menos 4 colunas e se a primeira não é o cabeçalho
                if len(cols) >= 4 and cols[0].text.strip().isdigit():
                    lista_tarifas.append({
                        "codigo": cols[0].text.strip(),
                        "nome": cols[1].text.strip(),
                        "fornecedor": cols[2].text.strip(),
                        "valor": cols[3].text.strip(),
                        "uf": cols[7].text.strip() if len(cols) > 7 else "",
                        "cidade": cols[8].text.strip() if len(cols) > 8 else ""
                    })
        
        # Se a lista ainda estiver vazia, vamos imprimir o HTML para debug (ver no log do Actions)
        if not lista_tarifas:
            print("AVISO: Nenhuma tarifa processada. Verifique se o site mudou a estrutura.")
            # Opcional: print(soup.prettify()[:500]) # Imprime só o começo para não lotar o log
            
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Erro fatal: {e}")

if __name__ == "__main__":
    extrair()
