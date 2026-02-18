import requests
from bs4 import BeautifulSoup
import json

def extrair():
    url = "https://app.beneficiofacil.com.br/apbprodutos.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        # --- SOLUÇÃO ATÓMICA PARA ACENTOS ---
        # Forçamos o conteúdo para latin-1 e depois corrigimos para utf-8
        # Se o Maceió vira MaceiÃ³, é porque ele foi lido como UTF-8 quando era Latin-1
        try:
            texto_corrigido = response.content.decode('utf-8')
        except:
            texto_corrigido = response.content.decode('iso-8859-1')
            
        # Reforço extra: se o erro MaceiÃ³ aparecer, nós "desfazemos" ele
        if "Ã³" in texto_corrigido or "Ã£" in texto_corrigido:
            texto_corrigido = texto_corrigido.encode('cp1252').decode('utf-8')
        # -------------------------------------

        soup = BeautifulSoup(texto_corrigido, 'html.parser')
        tabelas = soup.find_all('table')
        
        lista_tarifas = []
        for tab in tabelas:
            linhas = tab.find_all('tr')
            if len(linhas) > 5:
                for linha in linhas:
                    cols = linha.find_all('td')
                    if len(cols) >= 4 and cols[0].text.strip().isdigit():
                        
                        def limpar(texto):
                            return " ".join(texto.strip().split())

                        valor_texto = cols[3].text.strip().replace('.', '').replace(',', '.')
                        try:
                            valor_num = float(valor_texto)
                        except:
                            valor_num = 0.0

                        lista_tarifas.append({
                            "codigo": limpar(cols[0].text),
                            "nome": limpar(cols[1].text),
                            "fornecedor": limpar(cols[2].text),
                            "valor": valor_num,
                            "uf": limpar(cols[7].text) if len(cols) > 7 else "",
                            "cidade": limpar(cols[8].text) if len(cols) > 8 else ""
                        })
        
        # Salvamos com indentação 4 para garantir que o Git veja como algo novo de novo
        with open('dados_tarifas.json', 'w', encoding='utf-8') as f:
            json.dump(lista_tarifas, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso: {len(lista_tarifas)} itens processados.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    extrair()
