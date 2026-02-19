import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    # URL parametrizada para retornar todos os registros
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://app.beneficiofacil.com.br/apbprodutos.asp'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        
        try:
            texto_corrigido = response.content.decode('utf-8')
        except:
            texto_corrigido = response.content.decode('iso-8859-1')
            
        if "Ã³" in texto_corrigido or "Ã£" in texto_corrigido:
            texto_corrigido = texto_corrigido.encode('cp1252').decode('utf-8')

        soup = BeautifulSoup(texto_corrigido, 'html.parser')
        lista_tarifas = []
        todas_as_linhas = soup.find_all('tr')
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            
            # Verificamos se tem colunas suficientes e se a primeira é o código (número)
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    
                    # Tratamento do valor para o padrão Senior (vírgula decimal)
                    valor_original = limpar(cols[3].text).replace('.', '').replace(',', '.')
                    try:
                        valor_num = valor_original.replace('.', ',') 
                    except:
                        valor_num = "0,00"

                    lista_tarifas.append([
                        codigo_txt,                 # Cod.
                        limpar(cols[1].text),       # Nome
                        limpar(cols[2].text),       # Fornecedor
                        valor_num,                  # Valor Unit.
                        limpar(cols[4].text),       # Prazo recarga
                        limpar(cols[5].text),       # Prazo cartão novo
                        limpar(cols[6].text),       # Tipo
                        limpar(cols[7].text),       # UF
                        limpar(cols[8].text),       # Cidade
                        limpar(cols[9].text)        # Data Tarifa
                    ])

        # Gravação do CSV
        with open('tarifas_senior.csv', 'w', encoding='iso-8859-1', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([
                'Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 
                'Prazo cartão novo', 'Tipo', 'UF', 'Cidade', 'Data Tarifa'
            ])
            writer.writerows(lista_tarifas)
        
        print(f"Sucesso: {len(lista_tarifas)} itens processados.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
