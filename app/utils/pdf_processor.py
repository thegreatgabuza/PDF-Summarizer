import PyPDF2
from pathlib import Path
import uuid
import os

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def save_uploaded_file(file, upload_folder: Path) -> tuple[str, Path]:
        """Save an uploaded file and return its ID and path."""
        try:
            # Ensure upload folder exists
            if not upload_folder.exists():
                upload_folder.mkdir(parents=True, exist_ok=True)
            
            file_id = str(uuid.uuid4())
            filename = f"{file_id}.pdf"
            file_path = upload_folder / filename
            
            # Save the file
            file.save(str(file_path))
            
            # Verify file was saved
            if not file_path.exists():
                raise Exception("File was not saved successfully")
                
            return file_id, file_path
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")

    @staticmethod
    def cleanup_file(file_path: Path):
        """Remove a processed file."""
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            if file_path.exists():
                os.remove(str(file_path))
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {str(e)}") 