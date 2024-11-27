from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .utils.pdf_processor import PDFProcessor
from .utils.summarizer import Summarizer
import traceback
import os

bp = Blueprint('main', __name__)
summarizer = Summarizer()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}

@bp.route('/')
def index():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Debug information
        print(f"Upload folder: {current_app.config['UPLOAD_FOLDER']}")
        print(f"Upload folder exists: {current_app.config['UPLOAD_FOLDER'].exists()}")
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Try to save the file
        try:
            file_id, file_path = PDFProcessor.save_uploaded_file(
                file, 
                current_app.config['UPLOAD_FOLDER']
            )
            print(f"File saved successfully: {file_path}")
            return jsonify({'file_id': file_id})
        except Exception as save_error:
            print(f"Error saving file: {str(save_error)}")
            return jsonify({'error': f'Error saving file: {str(save_error)}'}), 500
            
    except Exception as e:
        print(f"Upload error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@bp.route('/summary/<file_id>')
def get_summary(file_id):
    try:
        file_path = current_app.config['UPLOAD_FOLDER'] / f"{file_id}.pdf"
        print(f"Looking for file: {file_path}")
        
        if not file_path.exists():
            return render_template('error.html', message="File not found"), 404
        
        text = PDFProcessor.extract_text(file_path)
        summary = summarizer.summarize(text)
        PDFProcessor.cleanup_file(file_path)
        return render_template('summary.html', summary=summary)
    except Exception as e:
        print(f"Summary error: {str(e)}")
        print(traceback.format_exc())
        return render_template('error.html', message=str(e)), 500

@bp.route('/status/<file_id>')
def get_status(file_id):
    try:
        file_path = current_app.config['UPLOAD_FOLDER'] / f"{file_id}.pdf"
        return jsonify({'status': 'completed' if file_path.exists() else 'processing'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 