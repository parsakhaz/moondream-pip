import os
import requests
from tqdm import tqdm
import gzip
import shutil
import argparse

def download_model(model_url=None, output_path=None):
    """Download and extract the Moondream model."""
    
    if model_url is None:
        model_url = "https://huggingface.co/vikhyatk/moondream2/resolve/client/moondream-latest-int8.bin.gz?download=true"
    
    if output_path is None:
        output_path = "moondream-latest-int8.bin"
        
    gz_path = f"{output_path}.gz"
    
    # Check if the extracted model already exists
    if os.path.exists(output_path):
        print(f"Model already exists at {output_path}")
        return True
        
    try:
        # Download the model if the .gz file doesn't exist
        if not os.path.exists(gz_path):
            print(f"Downloading model from {model_url}")
            response = requests.get(model_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(gz_path, 'wb') as f:
                with tqdm(total=total_size, unit='iB', unit_scale=True, desc="Downloading") as pbar:
                    for data in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                        size = f.write(data)
                        pbar.update(size)
        
        # Extract the model
        print(f"Extracting model to {output_path}")
        with gzip.open(gz_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                with tqdm(desc="Extracting", unit='iB', unit_scale=True) as pbar:
                    shutil.copyfileobj(f_in, f_out)
                    
        # Clean up the .gz file
        os.remove(gz_path)
        print("Model download and extraction complete!")
        return True
        
    except Exception as e:
        print(f"Error downloading/extracting model: {str(e)}")
        # Clean up partial files
        if os.path.exists(gz_path):
            os.remove(gz_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and extract the Moondream model")
    parser.add_argument("--url", help="Alternative model URL", default=None)
    parser.add_argument("--output", help="Output path for the model", default=None)
    
    args = parser.parse_args()
    
    success = download_model(args.url, args.output)
    if not success:
        exit(1) 