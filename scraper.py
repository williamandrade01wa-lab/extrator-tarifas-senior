import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    # URL inicial para pegar os cookies de sessão
    url_base = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    # URL da busca que deveria retornar tudo
    url_busca = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://app.beneficiofacil.com.br/apbprodutos.asp',
        'Connection': 'keep-alive'
    }
    
    try:
        # Criamos uma sessão para carregar os cookies do site
        session = requests.Session()
        
        # 1. Visita a home para "ganhar" os cookies do servidor ASP
        session.get(url_base, headers=headers, timeout=30)
        
        # 2. Agora sim, faz a busca com a sessão ativa
        response = session.get(url_busca, headers=headers, timeout=30)
        
        # (O restante da lógica de tratamento de texto continua igual...)
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
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    valor_original = limpar(cols[3].text).replace('.', '').replace(',', '.')
                    try:
                        valor_num = valor_original.replace('.', ',') 
                    except:
                        valor_num = "0,00"

                    lista_tarifas.append([
                        codigo_txt, limpar(cols[1].text), limpar(cols[2].text),
                        valor_num, limpar(cols[4].text), limpar(cols[5].text),
                        limpar(cols[6].text), limpar(cols[7].text), 
                        limpar(cols[8].text), limpar(cols[9].text)
                    ])

        with open('tarifas_senior.csv', 'w', encoding='iso-8859-1', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 'Prazo cartão novo', 'Tipo', 'UF', 'Cidade', 'Data Tarifa'])
            writer.writerows(lista_tarifas)
        
        print(f"Sucesso: {len(lista_tarifas)} itens processados.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
