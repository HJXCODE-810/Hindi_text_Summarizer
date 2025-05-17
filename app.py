import os
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from summarizer import summarize_hindi
from docx import Document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SUMMARY_FOLDER'] = 'summaries'
app.secret_key = 'hindi_summarizer_secret_key'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SUMMARY_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if file part exists in the request
        if 'doc_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['doc_file']
        
        # Check if user submitted an empty form
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and file.filename.endswith('.docx'):
            try:
                # Save uploaded file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                # Read DOCX content
                doc = Document(filepath)
                full_text = '\n'.join([para.text for para in doc.paragraphs if para.text])

                if not full_text.strip():
                    flash('The uploaded document appears to be empty')
                    return redirect(request.url)

                # Summarize
                summary_text = summarize_hindi(full_text)

                # Write summary to new DOCX
                summary_doc = Document()
                # Add Unicode-aware heading for Hindi
                heading = summary_doc.add_heading('', level=1)
                heading_run = heading.add_run('सारांश')
                heading_run.font.name = 'Nirmala UI'
                
                # Add paragraphs with proper Unicode font
                for line in summary_text.split('\n'):
                    if line.strip():
                        para = summary_doc.add_paragraph('')
                        run = para.add_run(line)
                        run.font.name = 'Nirmala UI'  # Set Unicode-compatible font
                
                summary_filename = f"summary_{file.filename}"
                summary_path = os.path.join(app.config['SUMMARY_FOLDER'], summary_filename)
                summary_doc.save(summary_path)

                return redirect(url_for('download_summary', filename=summary_filename))
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Please upload a valid .docx file')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_summary(filename):
    path = os.path.join(app.config['SUMMARY_FOLDER'], filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        flash('Summary file not found')
        return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)