import PyPDF2
import re
import os

def extrair_dados_fairfax(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as arquivo:
            pdf = PyPDF2.PdfReader(arquivo)
            texto_completo = "".join([pagina.extract_text() or "" for pagina in pdf.pages])
            
            dados = {
                'Nome do Segurado': None,
                'CNPJ do Segurado': None,
                'Prêmio Total': None
            }

            # Padrões para Fairfax
            match_cnpj_segurado = re.search(
                r"Nome do Segurado\s+CNPJ\s*\n?(.+?)\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})",
                texto_completo,
                re.IGNORECASE
            )
            
            if match_cnpj_segurado:
                dados['Nome do Segurado'] = match_cnpj_segurado.group(1).strip()
                dados['CNPJ do Segurado'] = match_cnpj_segurado.group(2)

            # Captura a linha que contém todos os valores
            match_linha_valores = re.search(
                r"Importância Segurada.*?\nR\$.*", 
                texto_completo
            )

            if match_linha_valores:
                linha_valores = match_linha_valores.group(0)
                valores = re.findall(r"R\$[\s]*([\d.]+,\d{2})", linha_valores)
                if valores:
                    dados['Prêmio Total'] = f"R$ {valores[-1]}"

            return dados

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

# Processamento dos arquivos na pasta Fairfax
diretorio = "Fairfax"
for arquivo in os.listdir(diretorio):
    if arquivo.lower().endswith('.pdf'):
        caminho_completo = os.path.join(diretorio, arquivo)
        print(f"\nProcessando: {arquivo}")
        
        dados = extrair_dados_fairfax(caminho_completo)
        if dados:
            for chave, valor in dados.items():
                print(f"{chave}: {valor or 'Não encontrado'}")
