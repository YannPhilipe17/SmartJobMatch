import pdfplumber

def contenu_pdf(fichier_source):
    """Extraction brute du texte depuis le fichier uploadé."""
    texte_brut = ""
    try:
        with pdfplumber.open(fichier_source) as pdf:
            for page in pdf.pages:
                fragment = page.extract_text()
                if fragment:
                    texte_brut += fragment + "\n"
        return texte_brut
    except Exception as e:
        print(f"Erreur parsing : {e}")
        return None