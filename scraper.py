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
        print("Iniciando conexao...")
        
        response = session.get(url, headers=headers, timeout=180, stream=True)
        response.raise_for_status() 
        
        # Lendo o conteúdo bruto
        conteudo = response.content
        
        # Tenta decodificar o que vem do site (geralmente latin-1 ou utf-8)
        try:
            texto_html = conteudo.decode('utf-8')
        except:
            texto_html = conteudo.decode('iso-8859-1')

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
                    # Formatacao do valor (12,50)
                    v_raw = limpar(cols[3].text).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        valor_num = "{:.2f}".format(float(v_raw)).replace('.', ',')
                    except:
                        valor_num = "0,00"

                    lista_tarifas.append([
                        codigo_txt, 
                        limpar(cols[1].text), 
                        limpar(cols[2].text), 
                        valor_num, 
                        limpar(cols[4].text), 
                        limpar(cols[5].text), 
                        limpar(cols[7].text), 
                        limpar(cols[8].text), 
                        limpar(cols[9].text)
                    ])

        # GRAVACAO EM TXT COM ENCODING ANSI (Windows-1252)
        # Removi o emoji do print para evitar erros no console do Linux
        with open('tarifas_senior.txt', 'w', encoding='cp1252', newline='', errors='replace') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 'Prazo cartão novo', 'UF', 'Cidade', 'Data Tarifa'])
            writer.writerows(lista_tarifas)
        
        print("Arquivo TXT gerado com sucesso em ANSI.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
