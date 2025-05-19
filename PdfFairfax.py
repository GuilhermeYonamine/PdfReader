import PyPDF2
import re

with open("Fatura2.pdf", "rb") as arquivo:
    pdf = PyPDF2.PdfReader(arquivo)
    num_paginas = len(pdf.pages)
    print(f"Número de páginas: {num_paginas}")

    texto_completo = ""
    for pagina in pdf.pages:
        texto_completo += pagina.extract_text()

    # Padrão para encontrar o Prêmio Líquido
    padrao_premio_liquido = r"Prêmio\s*Líquido.*?R\$\s*([\d.,]+)"
    match_premio_liquido = re.search(padrao_premio_liquido, texto_completo, re.IGNORECASE | re.DOTALL)
    
    if match_premio_liquido:
        premio_liquido = match_premio_liquido.group(1)
        print(f"Prêmio Líquido: R$ {premio_liquido}")
    else:
        print("Prêmio Líquido não encontrado.")

    # Extrair outros campos (opcional)
    cnpj = re.search(r"CNPJ[:\s]*([\d./-]+)", texto_completo, re.IGNORECASE)
    if cnpj:
        print(f"CNPJ: {cnpj.group(1)}")

    vencimento = re.search(r"Vencimento[:\s]*([\d/]+)", texto_completo, re.IGNORECASE)
    if vencimento:
        print(f"Vencimento: {vencimento.group(1)}")

    # Verificar o texto completo (para depuração)
    # print("\nTexto completo extraído do PDF:")
    # print(texto_completo)