import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    # URL de busca completa
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp?acao=pesquisar&nome=&fornecedor=0&tipo=0&uf="
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://app.beneficiofacil.com.br/apbprodutos.asp'
    }
    
    try:
        session = requests.Session()
        print("Iniciando conexão com stream... Aguardando resposta do servidor.")
        
        # stream=True mantém a porta aberta para o servidor "cuspir" as 80k linhas sem pressa
        # Aumentamos o timeout para 180 segundos caso o servidor seja lento
        response = session.get(url, headers=headers, timeout=180, stream=True)
        
        # Forçamos o download completo do conteúdo antes de fechar a conexão
        response.raise_for_status() 
        conteudo_bruto = response.content
        
        print(f"Download concluído. Tamanho do arquivo: {len(conteudo_bruto) / 1024:.2f} KB")

        # Tratamento de encoding (ISO-8859-1 é comum em sites ASP)
        try:
            texto_html = conteudo_bruto.decode('utf-8')
        except:
            texto_html = conteudo_bruto.decode('iso-8859-1')
            
        if "Ã³" in texto_html or "Ã£" in texto_html:
            texto_html = texto_html.encode('cp1252').decode('utf-8')

        # Usamos o parser 'lxml' se estiver disponível, por ser muito mais rápido para HTMLs gigantes
        # Se não, o soup usará o 'html.parser' padrão.
        soup = BeautifulSoup(texto_html, 'html.parser')
        
        lista_tarifas = []
        # Encontramos todas as linhas (tr) da página
        todas_as_linhas = soup.find_all('tr')
        
        def limpar(texto):
            return " ".join(texto.strip().split())

        print(f"Analisando {len(todas_as_linhas)} linhas de HTML...")

        for linha in todas_as_linhas:
            cols = linha.find_all('td')
            
            # Verificamos se a linha tem o mínimo de colunas e se a primeira é código numérico
            if len(cols) >= 10:
                codigo_txt = limpar(cols[0].text)
                if codigo_txt.isdigit():
                    
                    # Tratamento do valor (Substituindo ponto por nada e vírgula por ponto para o float, 
                    # depois voltando para vírgula para o padrão Senior)
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

        # Gravação do CSV Final
        with open('tarifas_senior.csv', 'w', encoding='iso-8859-1', newline='', errors='replace') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([
                'Cod.', 'Nome', 'Fornecedor', 'Valor Unit.', 'Prazo recarga', 
                'Prazo cartão novo', 'Tipo', 'UF', 'Cidade', 'Data Tarifa'
            ])
            writer.writerows(lista_tarifas)
        
        print(f"Sucesso Total: {len(lista_tarifas)} itens processados.")

    except Exception as e:
        print(f"Erro crítico durante o scraping: {e}")

if __name__ == "__main__":
    extrair()


import ftplib

def subir_ftp(arquivo_local):
    # Substitua pelos seus dados
    ftp_host = "seu_ftp_ou_ip"
    ftp_user = "seu_usuario"
    ftp_pass = "sua_senha"
    
    try:
        print(f"Conectando ao FTP {ftp_host}...")
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login(user=ftp_user, passwd=ftp_pass)
            with open(arquivo_local, 'rb') as f:
                # O comando STOR grava o arquivo no servidor
                ftp.storbinary(f'STOR {arquivo_local}', f)
        print("Arquivo enviado ao FTP com sucesso!")
    except Exception as e:
        print(f"Erro no FTP: {e}")

# Chame a função no final do seu script principal
# subir_ftp('tarifas_senior.csv')
