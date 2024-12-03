# master_pipeline.py

import os
import logging
from datetime import datetime

from crawler import WebCrawler  # Assurez-vous que crawler.py est dans le même répertoire ou ajustez le chemin
from content_processor import ContentProcessor  # Assurez-vous que content_processor.py est dans le même répertoire ou ajustez le chemin

def main():
    """Fonction principale pour exécuter le WebCrawler puis le ContentProcessor."""
    # Configuration initiale
    start_url = "https://www.ouellet.com/fr-ca/"  # Remplacez par l'URL de départ souhaitée
    max_depth = 3  # Ajustez la profondeur selon vos besoins

    # Initialiser et exécuter le WebCrawler
    try:
        crawler = WebCrawler(start_url, max_depth)
        crawler.crawl()
    except Exception as e:
        logging.critical(f"Erreur critique lors du crawling : {str(e)}")
        return

    # Récupérer le répertoire de sortie du crawler
    crawler_output_dir = crawler.base_dir

    # Définir les répertoires PDF et Doc
    pdf_directory = os.path.join(crawler_output_dir, 'PDF')
    doc_directory = os.path.join(crawler_output_dir, 'Doc')

    # Initialiser et exécuter le ContentProcessor
    try:
        processor = ContentProcessor(base_dir=crawler_output_dir)
        processor.run_pipeline(pdf_directory, doc_directory)
    except Exception as e:
        logging.critical(f"Erreur critique lors du traitement du contenu : {str(e)}")
        return

    logging.info("Pipeline complet terminé avec succès.")

if __name__ == "__main__":
    main()
