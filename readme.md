# Hindi Summarization Chatbot with DOCX Support

A Flask-based web application that accepts `.docx` files containing Hindi text, summarizes the content using a pretrained mT5 model, and produces a downloadable `.docx` summary file.

## 📁 Project Structure

```
├── README.md
├── requirements.txt
├── summarizer.py
├── app.py
└── templates/
    ├── index.html
    ├── 404.html
    └── 500.html
```

## 🚀 Features

* **Hindi text summarization** using a pretrained mT5 model (Jayveersinh-Raj/hindi-summarizer-small)
* **DOCX upload**: Read large corpora from Word documents
* **DOCX download**: Save the summary as a new Word document
* **Enhanced error handling**: Proper handling of edge cases and file errors
* **Flash messages**: User-friendly notifications
* **Responsive UI**: Mobile-friendly interface with improved styling
* **Support for GPU (CUDA) acceleration**

## 🛠️ Setup

### Prerequisites

* Python 3.8+
* pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HJXCODE-810/hindi-summarizer-chatbot.git
   cd hindi-summarizer-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application

### Development Server

```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # For development mode with debug
flask run --host=0.0.0.0 --port=5000
```

Alternatively, you can run:

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser to use the application.

### Production Deployment

For production deployment, it's recommended to use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Testing the Application

1. Prepare a `.docx` file with Hindi text content.
2. Upload the file through the web interface.
3. Wait for the summarization process to complete.
4. Download the generated summary file.

## 🔧 Troubleshooting

### Common Issues

* **Model Loading Errors**: Check the `summarizer.log` file for details
* **File Upload Issues**: Ensure the file is a valid `.docx` format
* **Memory Errors**: For large documents, ensure your server has adequate RAM

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

* [HuggingFace Transformers](https://github.com/huggingface/transformers) for the pretrained models
* [Jayveersinh-Raj](https://huggingface.co/Jayveersinh-Raj) for the Hindi summarizer model
* [Flask](https://flask.palletsprojects.com/) for the web framework
* [python-docx](https://python-docx.readthedocs.io/) for DOCX handling
