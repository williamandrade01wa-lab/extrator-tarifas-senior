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
        
        conteudo = response.content
        
        try:
            texto_html = conteudo.decode('utf-8')
        except:
            texto_html = conteudo.decode('iso-8859-1')

        soup = BeautifulSoup(texto_html, 'html.parser')
        todas_as_linhas = soup.find_all('tr')
        
        lista_tarifas = []
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        print(f"Analisando {len(todas_as_linhas)} linhas...")

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            
            # Verificamos se a linha tem as colunas necessárias
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                
                if codigo_txt.isdigit():
                    # --- NOVO FILTRO: TIPO "P" ---
                    # cols[6] costuma ser a coluna 'Tipo' no layout desse site
                    tipo_produto = limpar(cols[6].text).upper()
                    
                    if tipo_produto == "p":
                        continue # Pula esta linha e vai para a próxima
                    
                    # --- SE PASSOU PELO FILTRO, CONTINUA O PROCESSAMENTO ---
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
                        limpar(cols[7].text), # UF
                        limpar(cols[8].text), # Cidade
                        limpar(cols[9].text)  # Data Tarifa
                    ])

        # GRAVACAO EM TXT (ANSI/Windows-1252)
        with open('tarifas_senior.txt', 'w', encoding='cp1252', newline='', errors='replace') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 'Prazo cartão novo', 'UF', 'Cidade', 'Data Tarifa'])
            writer.writerows(lista_tarifas)
        
        print(f"Sucesso! {len(lista_tarifas)} itens gravados (Filtro Tipo P aplicado).")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
