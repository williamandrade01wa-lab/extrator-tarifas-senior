import requests
from bs4 import BeautifulSoup
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        # FORÇAR A CODIFICAÇÃO CORRETA AQUI
        response.encoding = 'iso-8859-1' 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tabelas = soup.find_all('table')
        
        lista_tarifas = []
        for tab in tabelas:
            linhas = tab.find_all('tr')
            if len(linhas) > 5:
                for linha in linhas:
                    cols = linha.find_all('td')
                    if len(cols) >= 4 and cols[0].text.strip().isdigit():
                        
                        # LIMPEZA DOS TEXTOS (Acentos e Espaços)
                        nome_limpo = cols[1].text.strip()
                        fornecedor_limpo = cols[2].text.strip()
                        cidade_limpo = cols[8].text.strip() if len(cols) > 8 else ""
                        
                        # FORMATAÇÃO DO VALOR (Transforma "6,90" em 6.90)
                        valor_texto = cols[3].text.strip().replace('.', '').replace(',', '.')
                        try:
                            valor_num = float(valor_texto)
                        except:
                            valor_num = valor_texto

                        lista_tarifas.append({
                            "codigo": cols[0].text.strip(),
                            "nome": nome_limpo,
                            "fornecedor": fornecedor_limpo,
                            "valor": valor_num,
                            "uf": cols[7].text.strip() if len(cols) > 7 else "",
                            "cidade": cidade_limpo
                        })
        
        # SALVAR GARANTINDO UTF-8
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
        
        print(f"Finalizado com sucesso: {len(lista_tarifas)} itens.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
