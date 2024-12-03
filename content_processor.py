# content_processor.py

import os
import re
import logging
import hashlib
from datetime import datetime
import warnings

import PyPDF2
import pytesseract
from PIL import Image
from docx import Document
from pdf2image import convert_from_path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ContentProcessor:
    def __init__(self, base_dir="crawler_output"):
        self.base_dir = base_dir
        self.create_directories()

    def create_directories(self):
        """Crée la structure de dossiers nécessaire."""
        directories = ['content', 'logs']
        for dir_name in directories:
            path = os.path.join(self.base_dir, dir_name)
            try:
                os.makedirs(path, exist_ok=True)
                logging.debug(f"Répertoire créé ou déjà existant : {path}")
            except OSError as e:
                logging.error(f"Impossible de créer le répertoire {path}: {e}")
                raise

    def sanitize_filename(self, file_path, page_number=None):
        """Crée un nom de fichier sécurisé."""
        url_hash = hashlib.md5(file_path.encode('utf-8')).hexdigest()[:8]
        filename = os.path.basename(file_path)
        if not filename:
            filename = 'index'
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        name, _ = os.path.splitext(filename)
        if page_number is not None:
            sanitized = f"{name}_page_{page_number:03d}_{url_hash}.txt"
        else:
            sanitized = f"{name}_{url_hash}.txt"
        logging.debug(f"Nom de fichier sanitizé: {sanitized}")
        return sanitized

    def extract_text_from_pdf(self, file_path):
        """Extrait le contenu de chaque page d'un PDF."""
        pages_content = []
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                logging.info(f"Nombre de pages dans {file_path}: {num_pages}")
                for page_number in range(num_pages):
                    page = reader.pages[page_number]
                    text = page.extract_text() or ""
                    
                    # Si le texte est vide, essayer l'OCR
                    if not text.strip():
                        logging.debug(f"Texte vide sur la page {page_number + 1}, tentative d'OCR.")
                        text = self.extract_text_with_ocr(file_path, page_number + 1)
                    
                    if text.strip():
                        pages_content.append({
                            'page': page_number + 1,
                            'text': text.strip()
                        })
        except PyPDF2.errors.PdfReadError as e:
            logging.error(f"Erreur de lecture du PDF {file_path}: {e}")
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction du PDF {file_path}: {e}")
        return pages_content

    def extract_text_with_ocr(self, file_path, page_number):
        """Extrait le texte via OCR avec une attention particulière aux tableaux."""
        try:
            images = convert_from_path(file_path, first_page=page_number, last_page=page_number)
            if images:
                custom_config = r'--oem 3 --psm 6'
                text = pytesseract.image_to_string(images[0], lang='fra', config=custom_config)
                logging.debug(f"OCR réussi pour la page {page_number} de {file_path}")
                return text
            logging.warning(f"Aucune image extraite pour la page {page_number} de {file_path}")
            return ""
        except Exception as e:
            logging.warning(f"OCR a échoué pour la page {page_number} de {file_path}: {e}")
            return ""

    def extract_text_from_docx(self, file_path):
        """Extrait le texte des fichiers DOCX."""
        pages_content = []
        try:
            doc = Document(file_path)
            current_text = []
            page_number = 1  # DOCX n'a pas de pages strictes
            for paragraph in doc.paragraphs:
                current_text.append(paragraph.text.strip())
            pages_content.append({
                'page': page_number,
                'text': "\n".join(current_text)
            })
            logging.debug(f"Extraction DOCX réussie pour {file_path}")
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction du DOCX {file_path}: {e}")
        return pages_content

    def process_files_in_directory(self, directory):
        """Traite tous les fichiers PDF et DOCX dans un répertoire donné."""
        logging.info(f"Processing files in directory: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in ['.pdf', '.doc', '.docx']:
                    file_path = os.path.join(root, file)
                    logging.info(f"Processing file: {file_path}")
                    try:
                        if file_ext == '.pdf':
                            pages_content = self.extract_text_from_pdf(file_path)
                        elif file_ext in ['.doc', '.docx']:
                            pages_content = self.extract_text_from_docx(file_path)
                        else:
                            logging.warning(f"Unsupported file type: {file_ext} for file {file_path}")
                            continue

                        if not pages_content:
                            logging.warning(f"No content extracted from {file_path}")
                            continue

                        for page_data in pages_content:
                            if not page_data.get('text'):
                                continue

                            # Générer le nom de fichier brut
                            filename = self.sanitize_filename(file_path, page_number=page_data['page'])
                            save_path = os.path.join(self.base_dir, 'content', filename)

                            # Sauvegarder le contenu brut en .txt
                            try:
                                with open(save_path, 'w', encoding='utf-8') as f:
                                    f.write(page_data['text'])
                                logging.info(f"Contenu brut sauvegardé dans : {save_path}")
                            except IOError as e:
                                logging.error(f"Erreur de sauvegarde pour {file_path} page {page_data['page']}: {e}")

                    except Exception as e:
                        logging.error(f"Erreur lors du traitement de {file_path}: {e}", exc_info=True)

    def run_pipeline(self, pdf_directory, doc_directory):
        """Exécute le pipeline de traitement sur les répertoires PDF et Doc."""
        logging.info("Starting ContentProcessor pipeline")
        self.process_files_in_directory(pdf_directory)
        self.process_files_in_directory(doc_directory)
        logging.info("ContentProcessor pipeline completed")
