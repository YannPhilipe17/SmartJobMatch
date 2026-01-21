from sentence_transformers import util

_modele_nlp = None

def get_model():

    global _modele_nlp
    if _modele_nlp is None:

        from sentence_transformers import SentenceTransformer
        _modele_nlp = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print(" Modèle NLP chargé en mémoire !")
    return _modele_nlp

def analyse_compatibilite(texte_candidat, liste_jobs):
    """
    Compare le candidat avec une liste d'offres et injecte un score.
    """
    if not texte_candidat or not liste_jobs:
        return []


    model = get_model()

    # 2. Vectorisation du CV
    vecteur_candidat = model.encode(texte_candidat, convert_to_tensor=True)

    resultats = []

    for job in liste_jobs:
        # Création du contexte
        contexte_job = f"{job.get('poste', '')} {job.get('description', '')} {job.get('competences', '')}"
        
        vecteur_job = model.encode(contexte_job, convert_to_tensor=True)

        # Calcul similarité cosinus
        sim = util.cos_sim(vecteur_candidat, vecteur_job)
        
        # On ajoute le score
        job['pourcentage'] = int(sim.item() * 100)
        resultats.append(job)

    # Tri par pertinence décroissante
    return sorted(resultats, key=lambda x: x['pourcentage'], reverse=True)
