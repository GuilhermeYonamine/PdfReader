import PyPDF2
import re
import os

def extrair_dados_seguro(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as arquivo:
            pdf = PyPDF2.PdfReader(arquivo)
            texto_completo = "".join([pagina.extract_text() or "" for pagina in pdf.pages])
            
            dados = {
                'Nome do Segurado': None,
                'Coligada': None,
                'Ramo': None,
                'Endosso': None,
                'Prêmio Líquido': None
            }

            # Padrões ajustados
            padroes = {
                'Nome do Segurado': r"Nome:\s*(.*?)\s*CNPJ:",
                'Coligada': r"Código Corretor.*?Nome Social:\s*([^\n-]+?)\s*(?:\d|-)",
                'Ramo': r"Ramo\s*.*?-\s*(.*?)\s",
                'Endosso': r"Endosso\s*Data de emissão\n.*?(\d{6,})\s+\d{2}/\d{2}/\d{4}",
                'Prêmio Líquido': r"Prêmio Líquido:\s*\(R\$\)\s*([\d.,]+)"
            }

            for campo, padrao in padroes.items():
                try:
                    match = re.search(padrao, texto_completo, re.DOTALL)
                    if match:
                        valor = match.group(1).strip()
                        # Tratamentos específicos
                        if campo == 'Coligada':
                            valor = re.sub(r'Nome Social:\s*', '', valor)
                            valor = re.sub(r'\s+', ' ', valor).strip()
                        dados[campo] = valor
                except Exception as e:
                    print(f"Erro no campo {campo}: {str(e)}")

            return dados

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

# Processamento dos arquivos
diretorio = "Berkley"
for arquivo in os.listdir(diretorio):
    if arquivo.lower().endswith('.pdf'):
        caminho_completo = os.path.join(diretorio, arquivo)
        print(f"\nProcessando: {arquivo}")
        
        dados = extrair_dados_seguro(caminho_completo)
        if dados:
            for chave, valor in dados.items():
                print(f"{chave}: {valor or 'Não encontrado'}")
