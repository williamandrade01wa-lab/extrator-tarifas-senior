import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://app.beneficiofacil.com.br/apbprodutos.asp'
    }
    
    try:
        session = requests.Session()
        print("Iniciando conexão com stream... Aguardando resposta do servidor.")
        
        response = session.get(url, headers=headers, timeout=180, stream=True)
        response.raise_for_status() 
        conteudo_bruto = response.content
        
        print(f"Download concluído. Tamanho do arquivo: {len(conteudo_bruto) / 1024:.2f} KB")

        try:
            texto_html = conteudo_bruto.decode('utf-8')
        except:
            texto_html = conteudo_bruto.decode('iso-8859-1')
            
        if "Ã³" in texto_html or "Ã£" in texto_html:
            texto_html = texto_html.encode('cp1252').decode('utf-8')

        soup = BeautifulSoup(texto_html, 'html.parser')
        
        lista_tarifas = []
        todas_as_linhas = soup.find_all('tr')
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        print(f"Analisando {len(todas_as_linhas)} linhas de HTML...")

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    
                    # --- AJUSTE VALOR UNITÁRIO (Garante padrão 0,00) ---
                    # Limpa R$, pontos de milhar e converte para float usando ponto
                    v_raw = limpar(cols[3].text).replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        # Força 2 casas decimais (ex: 12.00) e depois troca para vírgula (12,00)
                        valor_num = "{:.2f}".format(float(v_raw)).replace('.', ',')
                    except:
                        valor_num = "0,00"

                    # Mantendo todas as colunas conforme o seu código original
                    lista_tarifas.append([
                        codigo_txt,                 # Cod.
                        limpar(cols[1].text),       # Nome
                        limpar(cols[2].text),       # Fornecedor (MANTIDO)
                        valor_num,                  # Valor Unit. (FORMATADO 2 CASAS)
                        limpar(cols[4].text),       # Prazo recarga
                        limpar(cols[5].text),       # Prazo cartão novo
                        limpar(cols[7].text),       # UF
                        limpar(cols[8].text),       # Cidade
                        limpar(cols[9].text)        # Data Tarifa
                    ])

        # Gravação do CSV Final
        with open('tarifas_senior.csv', 'w', encoding='iso-8859-1', newline='', errors='replace') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([
                'Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 
                'Prazo cartão novo', 'UF', 'Cidade', 'Data Tarifa'
            ])
            writer.writerows(lista_tarifas)
        
        print(f"Sucesso Total: {len(lista_tarifas)} itens processados.")

    except Exception as e:
        print(f"Erro crítico durante o scraping: {e}")

if __name__ == "__main__":
    extrair()
