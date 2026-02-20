import requests
from bs4 import BeautifulSoup
import csv
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        session = requests.Session()
        print("Iniciando conexao...")
        response = session.get(url, headers=headers, timeout=180, stream=True)
        response.raise_for_status() 
        
        try:
            texto_html = response.content.decode('utf-8')
        except:
            texto_html = response.content.decode('iso-8859-1')

        soup = BeautifulSoup(texto_html, 'html.parser')
        todas_as_linhas = soup.find_all('tr')
        
        lista_tarifas = []
        lista_para_json = [] # Lista separada para o JSON (com dicionarios)
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    
                    # --- FILTRO TIPO P ---
                    tipo_produto = limpar(cols[6].text).upper()
                    if tipo_produto == "P":
                        continue 
                    
                    # --- TRATAMENTO VALOR ---
                    v_raw = limpar(cols[3].text).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        valor_num = "{:.2f}".format(float(v_raw)).replace('.', ',')
                    except:
                        valor_num = "0,00"

                    # 1. Dados para o TXT (Lista de listas)
                    dados_linha = [
                        codigo_txt, limpar(cols[1].text), limpar(cols[2].text), 
                        valor_num, limpar(cols[4].text), limpar(cols[5].text), 
                        limpar(cols[7].text), limpar(cols[8].text), limpar(cols[9].text)
                    ]
                    lista_tarifas.append(dados_linha)

                    # 2. Dados para o JSON (Dicionário estruturado)
                    lista_para_json.append({
                        "codigo": codigo_txt,
                        "nome": limpar(cols[1].text),
                        "fornecedor": limpar(cols[2].text),
                        "valor": valor_num,
                        "uf": limpar(cols[7].text),
                        "cidade": limpar(cols[8].text)
                    })

        # --- SALVANDO TXT (Para o Senior - ANSI) ---
        with open('tarifas_senior.txt', 'w', encoding='cp1252', newline='', errors='replace') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 'Prazo cartão novo', 'UF', 'Cidade', 'Data Tarifa'])
            writer.writerows(lista_tarifas)

        # --- SALVANDO JSON (Para uso geral - UTF-8) ---
        with open('tarifas_senior.json', 'w', encoding='utf-8') as f:
            json.dump(lista_para_json, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso! TXT e JSON gerados. Itens processados: {len(lista_tarifas)}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
