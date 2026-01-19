from serpapi import GoogleSearch
from config import Config

def chercher_jobs_google(requete="Data Scientist CIFRE", ville="Paris"):
    """
    Interroge Google Jobs via SerpApi pour récupérer de vraies offres.
    """
    print(f"🌍 Recherche Google Jobs pour : {requete} à {ville}...")

    params = {
        "engine": "google_jobs",     
        "q": f"{requete} {ville}",  
        "hl": "fr",                  
        "gl": "fr",                  
        "api_key": Config.SERPAPI_KEY 
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        

        jobs_list = results.get("jobs_results", [])
        
        offres_propres = []
        
        for job in jobs_list:

            offre = {
                "id": job.get("job_id"),
                "poste": job.get("title"),
                "entreprise": job.get("company_name"),
                "ville": job.get("location", "France"),

                "type": job.get("detected_extensions", {}).get("schedule_type", "Non précisé"),
                "description": job.get("description", "Pas de description disponible."),

                "competences": ", ".join(job.get("extensions", [])), 

                "url": job.get("apply_options", [{}])[0].get("link", "#") 
            }
            offres_propres.append(offre)
            
        print(f"✅ {len(offres_propres)} offres trouvées via API.")
        return offres_propres

    except Exception as e:
        print(f"❌ Erreur API : {e}")
        # En cas de panne ou quota dépassé, on renvoie une liste vide pour ne pas faire planter 
        return []