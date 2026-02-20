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
        print(f"📊 Processando colunas: Cod, Nome, Valor Unit, Prazo recarga, Prazo cartão novo, UF, Cidade, Data Tarifa")

        with open('tarifas_senior.csv', 'w', newline='', encoding='iso-8859-1') as f:
            escritor = csv.writer(f, delimiter=';')
            
            for i, linha in enumerate(linhas):
                colunas = [col.text.strip() for col in linha.find_all(['td', 'th'])]
                
                if len(colunas) >= 9:
                    # Mapeamento baseado no que você passou:
                    # 0:Cod | 1:Nome | 2:Fornecedor (Ignorar) | 3:Valor Unit | 4:Prazo recarga 
                    # 5:Prazo cartão novo | 6:UF | 7:Cidade | 8:Data Tarifa
                    
                    if i == 0:
                        # Cabeçalho: Mantém todas exceto a coluna [2]
                        cabecalho = [colunas[0], colunas[1], colunas[3], colunas[4], colunas[5], colunas[6], colunas[7], colunas[8]]
                        escritor.writerow(cabecalho)
                    else:
                        # Dados:
                        cod = colunas[0]
                        nome = colunas[1]
                        valor_raw = colunas[3]
                        prazo_rec = colunas[4]
                        prazo_cart = colunas[5]
                        uf = colunas[6]
                        cidade = colunas[7]
                        data_tar = colunas[8]

                        # --- AJUSTE VALOR UNITARIO (2 CASAS) ---
                        v_limpo = valor_raw.replace('R$', '').replace('.', '').replace(' ', '').replace(',', '.').strip()
                        try:
                            valor_final = "{:.2f}".format(float(v_limpo)).replace('.', ',')
                        except:
                            valor_final = "0,00"

                        # Grava a linha com as 8 colunas finais
                        escritor.writerow([cod, nome, valor_final, prazo_rec, prazo_cart, uf, cidade, data_tar])
            
            print(f"✅ CSV gerado com 8 colunas (Tipo/Fornecedor removido) e Valor formatado.")

    except Exception as e:
        print(f"❌ Erro na extração: {e}")

if __name__ == "__main__":
    extrair()
