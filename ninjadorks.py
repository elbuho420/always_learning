
from dotenv import load_dotenv, set_key
from results_parser import ResultsParser
from file_downloader import FileDownloader
import os
from googlesearch import GoogleSearch
import argparse
import sys

def env_config():
    """Configurar el archivo .env con los valores proporcionados"""
    api_key = input("Introduce tu API_KEY de google: ")
    engine_id = input("Introduce el ID del buscador personalizado de google: ")
    set_key(".env", "API_KEY_GOOGLE", api_key)
    set_key(".env", "SEARCH_ENGINE_ID", engine_id)
    

def main(query, configure_env, start_page, pages, lang, output_json, output_html, download):
    
    #comprobamos si existe el fichero .env
    #cargamos las variables en el entorno
    
    env_exists = os.path.exists(".env")
    
    if not env_exists or configure_env:
        env_config()
        print("Archivo .env configurado satisfactoriamente.")
        sys.exit(1)
      
    #cargamos las variables de entorno  
    load_dotenv()
    

    #leemos la clave y el ID
    
    API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")


    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    
    if not query:
        print("Indica una consulta con el comando -q. utiliza el comando -h para mostrar la ayuda.")
        sys.exit(1)
        
        
    gseach = GoogleSearch(API_KEY_GOOGLE, SEARCH_ENGINE_ID)

    resultados = gseach.search(query,
                                start_page=start_page, 
                                pages=pages,
                                lang=lang)
    
    rparser = ResultsParser(resultados)
    
    
    # mostar los resultados en linea de consola de comandos
    rparser.mostrar_pantalla()
    
    if output_html:
        rparser.exportar_html(output_html)
    
    if output_json:
        rparser.exportar_json(output_json)
        
    if download:
        
        file_types = download.split(",")
        
        urls = [resultado['link'] for resultado in resultados]
        fdownloader = FileDownloader("Downloads")
        fdownloader.filtar_descargar_archivos(urls, file_types)
        
    
    
    
if __name__ == "__main__":
    #configuracion de los argumentos del programa
    
    parser = argparse.ArgumentParser(description="Esta herramienta realizar hacking con buscadores de manera automatica")    
    parser.add_argument("-q", "--query", type=str,
                    help="Especifica el dork que desea buscar.\nEjemplo: -q 'filetype:sql \"Mysql dump\" (pass|password|passwd|pwd '")
    parser.add_argument("-c", "--configure", action="store_true", 
                    help="Inicia el proceso de configuracion del archivo .env.\n Utiliza esta opcion sin otros argumentos para configurar las claves")
    parser.add_argument("--start-page", type=int, default=1,
                    help="Define la pagina de inicio del buscador para obtener resultados")
    parser.add_argument("--pages", type=int, default=1,
                    help="Numero de paginas de resultado de busqueda")
    parser.add_argument("--lang", type=str, default="lang_es",
                    help="Codigo de idioma para los resultados de busqueda. Por defecto es 'lang_es' (español)")
    parser.add_argument("--json", type=str,
                        help="Exporta los resultados en formato JSON en el fichero especificado.")
    parser.add_argument("--html", type=str,
                        help="Exporta los resultados a formato HTML en el fichero especificado.")
    parser.add_argument("--download", type=str, default="all",
                        help="Especifica las extensiones de los archivos que quieres descargar separadas entre coma. EJ: --download 'pdf,doc,sql'")
    
    
    
    
    args = parser.parse_args()
    
    main(query=args.query,
         configure_env=args.configure,
         pages=args.pages,
         start_page=args.start_page,
         lang=args.lang,
         output_html=args.html,
         output_json=args.json,
         download=args.download)
    
    
         
    
    
    


