import moondream as md
from PIL import Image
import os
import logging
from pathlib import Path
import tarfile
import shutil
import gzip

logger = logging.getLogger(__name__)

class MoondreamModel:
    def __init__(self):
        self.model = None
        self.encoded_image = None
        self.model_path = "moondream-latest-mtb.tar"
        self.initialize_model()
        
    def initialize_model(self):
        """Initialize the Moondream model"""
        try:
            if not os.path.exists(self.model_path):
                # Check for both possible source files
                gz_path = "moondream-latest-int8.bin.gz"
                bin_path = "moondream-latest-int8.bin"
                
                if os.path.exists(gz_path):
                    logger.info("Found .gz model file, extracting...")
                    # Extract .gz to .bin first
                    with gzip.open(gz_path, 'rb') as f_in:
                        with open(bin_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    logger.info("Extracted .gz file successfully")
                
                if os.path.exists(bin_path):
                    logger.info("Creating tar archive from .bin file...")
                    os.makedirs("temp_model", exist_ok=True)
                    
                    # Extract contents from .bin file
                    with tarfile.open(bin_path, "r:*") as bin_tar:
                        bin_tar.extractall("temp_model")
                    
                    # Create new tar archive with extracted files
                    with tarfile.open(self.model_path, "w") as tar:
                        for root, _, files in os.walk("temp_model"):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, "temp_model")
                                tar.add(file_path, arcname=arcname)
                    
                    # Cleanup
                    shutil.rmtree("temp_model")
                    logger.info("Created tar archive successfully")
                else:
                    raise FileNotFoundError(
                        "\nModel file not found. Please download it using either:\n"
                        "1. Gzipped version:\n"
                        "wget https://huggingface.co/vikhyatk/moondream2/resolve/client/moondream-latest-int8.bin.gz\n"
                        "\n2. Or the extracted version:\n"
                        "wget https://huggingface.co/vikhyatk/moondream2/resolve/client/moondream-latest-int8.bin"
                    )
            
            logger.info(f"Loading model from {self.model_path}...")
            self.model = md.VL(self.model_path)
            logger.info("Moondream model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Moondream model: {str(e)}")
            raise

    def process_image(self, image_path):
        """Process an image and return its initial caption"""
        try:
            image = Image.open(image_path)
            self.encoded_image = self.model.encode_image(image)
            
            # Generate initial caption
            result = self.model.caption(self.encoded_image)
            return result["caption"]
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise

    def ask_question(self, question, stream=False):
        """Ask a question about the processed image"""
        try:
            if self.encoded_image is None:
                raise ValueError("No image has been processed yet")
                
            if stream:
                return self.model.query(self.encoded_image, question, stream=True)["answer"]
            return self.model.query(self.encoded_image, question)["answer"]
        except Exception as e:
            logger.error(f"Error asking question: {str(e)}")
            raise

    def get_caption(self, stream=False):
        """Get caption for the processed image"""
        try:
            if self.encoded_image is None:
                raise ValueError("No image has been processed yet")
            
            if stream:
                return self.model.caption(self.encoded_image, stream=True)["caption"]
            return self.model.caption(self.encoded_image)["caption"]
        except Exception as e:
            logger.error(f"Error getting caption: {str(e)}")
            raise