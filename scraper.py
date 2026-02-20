import requests
from bs4 import BeautifulSoup
import csv

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    print(f"📡 Acessando: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        tabela = soup.find('table')
        
        if not tabela:
            print("❌ Erro: Tabela não encontrada.")
            return

        linhas = tabela.find_all('tr')
        print(f"📊 Processando {len(linhas)} linhas para Importador Senior...")

        with open('tarifas_senior.csv', 'w', newline='', encoding='iso-8859-1') as f:
            # O importador do Senior costuma preferir ponto e vírgula
            escritor = csv.writer(f, delimiter=';')
            
            # Começamos de 1 para pular o cabeçalho do HTML, 
            # já que o Importador Automático geralmente lê dados puros.
            for linha in linhas[1:]:
                colunas = [col.text.strip() for col in linha.find_all('td')]
                
                if len(colunas) >= 4:
                    cod = colunas[0]
                    desc = colunas[1]
                    # colunas[2] é o TIPO -> REMOVIDO
                    valor_raw = colunas[3]

                    # --- TRATAMENTO DO VALOR UNITÁRIO ---
                    # Remove R$, espaços e pontos de milhar. 
                    # Mantém a vírgula para o campo "Número" do Senior entender as decimais.
                    valor_limpo = valor_raw.replace('R$', '').replace('.', '').replace(' ', '').strip()
                    
                    # Grava no CSV: COD;DESCRICAO;VALOR
                    escritor.writerow([cod, desc, valor_limpo])
            
            print(f"✅ CSV pronto para o Processo Automático Senior!")

    except Exception as e:
        print(f"❌ Erro na extração: {e}")

if __name__ == "__main__":
    extrair()
