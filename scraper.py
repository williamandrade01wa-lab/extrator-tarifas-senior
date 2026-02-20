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

        with open('tarifas_senior.csv', 'w', newline='', encoding='iso-8859-1') as f:
            escritor = csv.writer(f, delimiter=';')
            
            for i, linha in enumerate(linhas):
                # Pega todas as colunas que existirem na linha
                colunas = [col.text.strip() for col in linha.find_all(['td', 'th'])]
                
                # Só processa se a linha tiver dados (evita linhas vazias)
                if len(colunas) > 3:
                    
                    # 1. REMOVE A COLUNA TIPO (Índice 2)
                    # Usamos o pop para tirar o 'Fornecedor/Tipo' e manter o resto intacto
                    colunas.pop(2) 
                    
                    # 2. AJUSTA O VALOR UNITÁRIO (Agora no novo Índice 2 após o pop)
                    if i > 0: # Pula o cabeçalho na hora de formatar número
                        valor_raw = colunas[2]
                        # Limpa R$, pontos de milhar e espaços
                        v_limpo = valor_raw.replace('R$', '').replace('.', '').replace(' ', '').replace(',', '.').strip()
                        try:
                            # Força 2 casas decimais e volta para vírgula
                            colunas[2] = "{:.2f}".format(float(v_limpo)).replace('.', ',')
                        except:
                            pass # Se falhar, mantém como está

                    escritor.writerow(colunas)
            
            print(f"✅ Sucesso! Coluna Tipo removida e Valor formatado com 2 casas.")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    extrair()
