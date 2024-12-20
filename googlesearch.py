

import requests

class GoogleSearch:
    def __init__(self, api_key, engine_id):
        """
        inicializa una nueva instancia de google
        esta clase permite realizar peticiones automatizadas
        ala API de google
        
        Args:
            api_key (str): clave api de google
            engine_id (str): identificador del motor
            de busqueda perzonalizado de google        
        
        """

        self.api_key = api_key
        self.engine_id = engine_id
    
    
    def search(self, query, start_page=1, pages=1, lang="lang_es"):
    
        final_results = []
        results_per_page = 10
        for page in range(pages):
            
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={start_index}&lr={lang}"
            response = requests.get(url)
            
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("items")
                cresults = self.custom_results(results)
                final_results.extend(cresults)
            else:
                print(f"Error obtenido al consultar la pagina: {page}: HTTP {response.status_code}")
                break
        return final_results

                
    def custom_results(self, results):
        """Filtra los resultados de la consulta."""
        
        custom_results = []
        for r in results:
            cresult = {}
            cresult["title"] = r.get("title")
            cresult["description"] = r.get("snippet")
            cresult["link"] = r.get("link")
            custom_results.append(cresult) 
            
        return custom_results       