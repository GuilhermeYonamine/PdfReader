import PyPDF2
import re

# Abre e lê o PDF
with open("Fairfax/Fatura2.pdf", "rb") as arquivo:
    pdf = PyPDF2.PdfReader(arquivo)
    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text() or ""

    # Captura o nome do segurado e seu CNPJ
    match_cnpj_segurado = re.search(
        r"Nome do Segurado\s+CNPJ\s*\n?(.+?)\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})",
        texto_completo,
        re.IGNORECASE
    )
    if match_cnpj_segurado:
        nome_segurado = match_cnpj_segurado.group(1).strip()
        cnpj_segurado = match_cnpj_segurado.group(2)
        print(f"Nome do Segurado: {nome_segurado}")
        print(f"CNPJ do Segurado: {cnpj_segurado}")
    else:
        print("CNPJ do segurado não encontrado.")

    # Captura a linha que contém todos os valores
    match_linha_valores = re.search(
        r"Importância Segurada.*?\nR\$.*", 
        texto_completo
    )

    if match_linha_valores:
        linha_valores = match_linha_valores.group(0)
        # Extrai todos os valores monetários da linha
        valores = re.findall(r"R\$[\s]*([\d.]+,\d{2})", linha_valores)
        if valores:
            premio_total = valores[-1]  # Último valor é o Prêmio Total
            print(f"Prêmio Total: R$ {premio_total}")
        else:
            print("Nenhum valor monetário encontrado na linha de valores.")
    else:
        print("Linha de valores não encontrada.")
