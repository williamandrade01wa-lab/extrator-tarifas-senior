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
        
        # SOLUÇÃO PARA OS ACENTOS:
        # Primeiro, pegamos o conteúdo bruto (content) e decodificamos ignorando erros
        html_decodificado = response.content.decode('iso-8859-1', errors='ignore')
        
        soup = BeautifulSoup(html_decodificado, 'html.parser')
        tabelas = soup.find_all('table')
        
        lista_tarifas = []
        for tab in tabelas:
            linhas = tab.find_all('tr')
            if len(linhas) > 5:
                for linha in linhas:
                    cols = linha.find_all('td')
                    if len(cols) >= 4 and cols[0].text.strip().isdigit():
                        
                        # Limpeza extra para remover caracteres invisíveis
                        def limpar_texto(txt):
                            return txt.strip().encode('latin-1', 'ignore').decode('utf-8', 'ignore') if txt else ""

                        # Se a conversão acima falhar, usamos esta mais simples:
                        nome = cols[1].text.strip()
                        fornecedor = cols[2].text.strip()
                        cidade = cols[8].text.strip() if len(cols) > 8 else ""

                        # Tratamento do valor (6,90 -> 6.9)
                        valor_texto = cols[3].text.strip().replace('.', '').replace(',', '.')
                        try:
                            valor_num = float(valor_texto)
                        except:
                            valor_num = 0.0

                        lista_tarifas.append({
                            "codigo": cols[0].text.strip(),
                            "nome": nome,
                            "fornecedor": fornecedor,
                            "valor": valor_num,
                            "uf": cols[7].text.strip() if len(cols) > 7 else "",
                            "cidade": cidade
                        })
        
        # Gravação final em UTF-8 real
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso: {len(lista_tarifas)} itens processados.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
