from sentence_transformers import SentenceTransformer, util


print("init: chargement modèle NLP...")
modele_nlp = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def analyse_compatibilite(texte_candidat, liste_jobs):
    """
    Compare le candidat avec une liste d'offres et injecte un score.
    """
    if not texte_candidat or not liste_jobs:
        return []

    # 1. Vectorisation du CV
    vecteur_candidat = modele_nlp.encode(texte_candidat, convert_to_tensor=True)

    resultats = []

    for job in liste_jobs:

        contexte_job = f"{job['poste']} {job['description']} {job['competences']}"
        
        vecteur_job = modele_nlp.encode(contexte_job, convert_to_tensor=True)

        # Calcul similarité cosinus
        sim = util.cos_sim(vecteur_candidat, vecteur_job)
        

        job['pourcentage'] = int(sim.item() * 100)
        resultats.append(job)

    # Tri par pertinence décroissante
    return sorted(resultats, key=lambda x: x['pourcentage'], reverse=True)