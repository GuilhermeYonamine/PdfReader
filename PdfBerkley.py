import PyPDF2 as py
import re

with open("Berkley/Fatura.pdf", "rb") as arquivo:
    pdf = py.PdfReader(arquivo)
    num_paginas = len(pdf.pages)
    print(f"Número de páginas: {num_paginas}")

    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text()

    # Extração do nome da empresa
    nome_empresa = re.search(r"Nome:\s*(.*?)\s*CNPJ:", texto_completo)
    if nome_empresa:
        nome = nome_empresa.group(1).strip()
        print(f"Nome do Segurado: {nome}")
    else:
        print("Nome da empresa não encontrado")
# Extração do CNPJ
    cnpj = re.search(r"CNPJ:\s*([0-9./-]+)", texto_completo)
    if cnpj:
        print(f"CNPJ do Segurado: {cnpj.group(1)}")
    else:
        print("CNPJ não encontrado")
    
    # Extração do prêmio total
    premio = re.search(r"Prêmio Total:\s*\(R\$\)\s*([0-9,.]+)", texto_completo)
    if premio:
        print(f"Prêmio Total: R$ {premio.group(1)}")
    else:
        print("Prêmio não encontrado")

    
    # Extração das datas de vigência
    datas = re.findall(r'(?:Vigência|Período de Vigência|Vigencia|VIGÊNCIA)[\s:à\-]*(\d{2}/\d{2}/\d{4})', 
                      texto_completo, re.IGNORECASE)

    if len(datas) >= 2:
        print(f"Data de vigência: {datas[1]}")
    else:
        # Padrão alternativo para datas no formato "dd/mm/aaaa à dd/mm/aaaa"
        datas_alternativas = re.findall(r'(\d{2}/\d{2}/\d{4})\s*à\s*(\d{2}/\d{2}/\d{4})', texto_completo)
        if datas_alternativas:
            print(f"Segunda data de vigência: {datas_alternativas[0][1]}")
        else:
            print("Não foi possível identificar a segunda data de vigência.")