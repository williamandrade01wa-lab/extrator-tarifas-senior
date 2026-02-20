import requests
from bs4 import BeautifulSoup
import csv
import sys

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    print(f"📡 Acessando: {url}")
    
    try:
        # 1. Baixa o HTML
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 2. Analisa o HTML
        soup = BeautifulSoup(response.text, 'lxml')
        tabela = soup.find('table') # Ajuste o seletor se necessário
        
        if not tabela:
            print("❌ Erro: Tabela não encontrada no HTML.")
            return

        linhas = tabela.find_all('tr')
        print(f"📊 Analisando {len(linhas)} linhas...")

        # 3. Salva o CSV
        with open('tarifas_senior.csv', 'w', newline='', encoding='iso-8859-1') as f:
            escritor = csv.writer(f, delimiter=';')
            
            contagem = 0
            for linha in linhas:
                colunas = [col.text.strip() for col in linha.find_all(['td', 'th'])]
                if colunas:
                    escritor.writerow(colunas)
                    contagem += 1
            
            print(f"✅ Sucesso! {contagem} linhas gravadas em 'tarifas_senior.csv'.")

    except Exception as e:
        print(f"❌ Erro na extração: {e}")

if __name__ == "__main__":
    extrair()
