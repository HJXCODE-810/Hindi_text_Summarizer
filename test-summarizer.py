import unittest
import os
import shutil
from app import app
from summarizer import summarize_hindi

class TestSummarizer(unittest.TestCase):
    
    def setUp(self):
        # Create test directories if they don't exist
        app.config['UPLOAD_FOLDER'] = 'test_uploads'
        app.config['SUMMARY_FOLDER'] = 'test_summaries'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['SUMMARY_FOLDER'], exist_ok=True)
        
        # Configure the test client
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
    def tearDown(self):
        # Clean up test directories
        if os.path.exists('test_uploads'):
            shutil.rmtree('test_uploads')
        if os.path.exists('test_summaries'):
            shutil.rmtree('test_summaries')
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DOCTYPE html', response.data)
        self.assertIn(b'DOCX', response.data)
    
    def test_summarize_hindi_function(self):
        # Test with a simple Hindi text
        hindi_text = "<sum> यह एक परीक्षण वाक्य है। हम यह जांच रहे हैं कि क्या सारांशकर्ता सही ढंग से काम कर रहा है।"
        summary = summarize_hindi(hindi_text, min_length=5, max_length=20)
        
        # Check that we got a non-empty summary
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)
    
    def test_404_page(self):
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

if __name__ == '__main__':
    unittest.main()
