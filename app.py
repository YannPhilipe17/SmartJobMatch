from flask import Flask, render_template, request
from core.parser import contenu_pdf
from core.jobs_api import chercher_jobs_google 
from core.matcher import analyse_compatibilite
from collections import Counter
import re
app = Flask(__name__)
app.config.from_object('config.Config') 


def deviner_mots_cles(texte):
    """Devine le métier principal en trouvant le mot le plus fréquent du CV."""
    if not texte: return "Emploi"
    
    # 1. On met tout en minuscule et on découpe les mots
    mots = re.findall(r'\w+', texte.lower())
    
    # 2. Liste  des mots inutiles
    mots_inutiles = {
        'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'est', 
        'pour', 'par', 'sur', 'dans', 'avec', 'mon', 'mes', 'cv', 'email', 
        'tel', 'com', 'fr', 'www', 'date', 'nom', 'prenom', 'page', 'skills', 
        'competences', 'education', 'experience', 'langues', 'profil'
    }
    
    # 3. On garde que les mots intéressants (> 3 lettres et pas dans la liste noire)
    mots_pertinents = [m for m in mots if len(m) > 3 and m not in mots_inutiles]
    
    # 4. On prend les 2 mots les plus fréquents
    compteur = Counter(mots_pertinents)
    top_mots = compteur.most_common(2) 
    
    if top_mots:

        return f"{top_mots[0][0]} {top_mots[1][0] if len(top_mots)>1 else ''}"
    return "Offres emploi"

# --- ROUTE PRINCIPALE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    jobs_tries = None
    erreur = None
    info_auto = None 

    if request.method == 'POST':
        fichier = request.files.get('cv_upload')
        search_query = request.form.get('job_search')
        city_query = request.form.get('city_search')

        if fichier and fichier.filename != '':
            texte_cv = contenu_pdf(fichier)
            
            if texte_cv:
                location = city_query if city_query else "France"

                if not search_query:
                    search_query = deviner_mots_cles(texte_cv)
                    info_auto = f"🔎 Recherche automatique détectée : '{search_query}'"
                
                print(f"🚀 Recherche : {search_query} à {location}")
                
                tous_les_jobs = chercher_jobs_google(requete=search_query, ville=location)
                jobs_tries = analyse_compatibilite(texte_cv, tous_les_jobs)
            else:
                erreur = "Impossible de lire le fichier PDF."
        else:
            erreur = "Veuillez sélectionner un fichier PDF."

    return render_template('home.html', jobs=jobs_tries, error=erreur, info=info_auto)

if __name__ == '__main__':
    app.run(debug=True, port=5000)