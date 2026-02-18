import requests
from bs4 import BeautifulSoup
import json

def extrair():
    # URL que você me passou
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    
    print(f"Acessando {url}...")
    try:
        # Simulando um navegador para evitar bloqueios simples
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'iso-8859-1' 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table')
        
        lista_tarifas = []
        if tabela:
            # Pega todas as linhas da tabela
            linhas = tabela.find_all('tr')
            for linha in linhas[1:]: # Pula o cabeçalho
                cols = linha.find_all('td')
                if len(cols) >= 4:
                    lista_tarifas.append({
                        "codigo": cols[0].text.strip(),
                        "nome": cols[1].text.strip(),
                        "fornecedor": cols[2].text.strip(),
                        "valor": cols[3].text.strip(),
                        "prazo_recarga": cols[4].text.strip() if len(cols) > 4 else "",
                        "uf": cols[7].text.strip() if len(cols) > 7 else "",
                        "cidade": cols[8].text.strip() if len(cols) > 8 else ""
                    })
            
            # Salva o resultado em JSON
            with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
                json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
            print(f"Sucesso! {len(lista_tarifas)} itens extraídos.")
        else:
            print("Tabela não encontrada na página.")
            
    except Exception as e:
        print(f"Erro na extração: {e}")

if __name__ == "__main__":
    extrair()
