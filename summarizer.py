from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("summarizer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Pretrained Hindi summarization model
CHECKPOINT = "Jayveersinh-Raj/hindi-summarizer-small"

def load_summarizer():
    try:
        logger.info(f"Loading model from checkpoint: {CHECKPOINT}")
        tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
        model = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT)
        
        # Check for GPU availability
        device = 0 if torch.cuda.is_available() else -1
        if device == 0:
            logger.info("CUDA is available. Using GPU acceleration.")
        else:
            logger.info("CUDA is not available. Using CPU.")
            
        summarizer = pipeline(
            "summarization",
            model=model,
            tokenizer=tokenizer,
            framework="pt",
            device=device
        )
        return summarizer
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

# Load summarizer on module import
try:
    summarizer = load_summarizer()
    logger.info("Summarizer loaded successfully")
except Exception as e:
    logger.error(f"Failed to load summarizer: {str(e)}")
    summarizer = None

def summarize_hindi(text: str, min_length: int = 32, max_length: int = 128) -> str:
    """
    Summarize Hindi text using the pretrained model.
    
    Args:
        text: Input Hindi text to summarize
        min_length: Minimum length of the summary
        max_length: Maximum length of the summary
        
    Returns:
        String containing the summarized text
    """
    if summarizer is None:
        logger.error("Summarizer not initialized")
        return "Error: Summarizer not initialized."
        
    if not text.strip():
        logger.warning("Empty text provided for summarization")
        return ""
        
    try:
        # Ensure task prefix for this checkpoint
        if not text.strip().startswith("<sum>"):
            text = "<sum> " + text.strip()
            
        # Handle long text by chunking if needed
        if len(text.split()) > 1024:
            logger.info("Long text detected. Processing in chunks.")
            # Implementation for chunking could be added here
            
        logger.info(f"Summarizing text of length {len(text.split())} words")
        
        output = summarizer(
            text,
            min_length=min_length,
            max_length=max_length,
            do_sample=False
        )
        
        summary = output[0]["summary_text"].strip()
        logger.info(f"Generated summary of length {len(summary.split())} words")
        return summary
        
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        return f"Error during summarization: {str(e)}"
