import requests
from bs4 import BeautifulSoup
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    
    # Cabeçalhos que imitam exatamente um navegador Chrome no Windows
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,.*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://app.beneficiofacil.com.br/',
        'Connection': 'keep-alive'
    }
    
    try:
        # Usamos uma sessão para manter cookies (importante para sites ASP)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        response.encoding = 'iso-8859-1'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estratégia: Procurar por todas as tabelas e pegar a que tiver mais linhas
        tabelas = soup.find_all('table')
        print(f"Total de tabelas encontradas na página: {len(tabelas)}")
        
        lista_tarifas = []
        
        for i, tab in enumerate(tabelas):
            linhas = tab.find_all('tr')
            if len(linhas) > 5: # Provavelmente é a nossa tabela de produtos
                print(f"Analisando Tabela #{i} com {len(linhas)} linhas...")
                for linha in linhas:
                    cols = linha.find_all('td')
                    # Tentamos identificar a linha de dados (ajustado para a ordem que você passou)
                    if len(cols) >= 4:
                        texto_cod = cols[0].text.strip()
                        # Se o primeiro campo for número, é um produto
                        if texto_cod.isdigit():
                            lista_tarifas.append({
                                "codigo": texto_cod,
                                "nome": cols[1].text.strip(),
                                "fornecedor": cols[2].text.strip(),
                                "valor": cols[3].text.strip(),
                                "uf": cols[7].text.strip() if len(cols) > 7 else "",
                                "cidade": cols[8].text.strip() if len(cols) > 8 else ""
                            })
        
        if not lista_tarifas:
            print("LOG DEBUG: O HTML recebido tem o seguinte começo:")
            print(response.text[:500]) # Isso vai nos dizer se caímos numa tela de erro/bloqueio
            
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
        
        print(f"Finalizado: {len(lista_tarifas)} itens salvos.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
