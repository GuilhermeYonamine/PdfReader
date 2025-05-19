import PyPDF2 as py
import re

with open("Fatura.pdf", "rb") as arquivo:
    pdf = py.PdfReader(arquivo)
    num_paginas = len(pdf.pages)
    print(f"Número de páginas (len): {num_paginas}")

    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text()

    premio = re.search(r"Prêmio Total:\s*\(R\$\)\s*([0-9,.]+)", texto_completo)
    print(f"Prêmio Total: R$ {premio.group(1)}")  # Correto: premio.group(1)

    cnpj = re.search(r"CNPJ:\s*([0-9./-]+)", texto_completo)
    print(f"CNPJ: {cnpj.group(1)}")    

    vencimento = re.search(r"Vigência:\s*([0-9/]+)", texto_completo)
    print(f"Vencimento: {vencimento.group(1)}")
        
    # print(texto_completo)

    for pagina in range(num_paginas): 
        conteudo = pdf.pages[pagina].extract_text()
        # print(f"\nConteúdo da página {pagina + 1}:")
        # print(conteudo)
        # print(type(conteudo))