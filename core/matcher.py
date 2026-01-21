from sentence_transformers import util
import gc 



def analyse_compatibilite(texte_candidat, liste_jobs):
    if not texte_candidat or not liste_jobs:
        return []


    from sentence_transformers import SentenceTransformer
    

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


    try:
        vecteur_candidat = model.encode(texte_candidat, convert_to_tensor=True)
        resultats = []

        for job in liste_jobs:
            contexte_job = f"{job.get('poste', '')} {job.get('description', '')} {job.get('competences', '')}"
            vecteur_job = model.encode(contexte_job, convert_to_tensor=True)
            
            sim = util.cos_sim(vecteur_candidat, vecteur_job)
            job['pourcentage'] = int(sim.item() * 100)
            resultats.append(job)
            
    finally:

        print("🧹 Nettoyage de la mémoire RAM...")
        del model
        gc.collect() #

    return sorted(resultats, key=lambda x: x['pourcentage'], reverse=True)
