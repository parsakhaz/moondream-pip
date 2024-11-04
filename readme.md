# Moondream Streamlit Interface

A web interface for the Moondream vision language model, built with Streamlit. Upload images, get descriptions, and chat about the images using natural language.

## Features

- 🖼️ Image upload and analysis
- 💬 Interactive chat about images
- 🚀 Local processing for privacy
- 🎯 CUDA support for faster processing
- 📥 Automatic model weight downloading with progress tracking

## Prerequisites

- Python 3.8+
- NVIDIA GPU with CUDA support (recommended)
- Microsoft Visual C++ Redistributable 2019 ([Download here](https://aka.ms/vs/16/release/vc_redist.x64.exe))
- ~2GB disk space for model weights

## Installation

1. **Clone the Repository**

~~~bash
git clone https://github.com/yourusername/moondream-streamlit.git
cd moondream-streamlit
~~~

2. **Create and Activate Virtual Environment**

~~~bash
# Remove existing venv if present
deactivate  # If in a virtual environment
rmdir /s /q venv  # On Windows
rm -rf venv      # On Linux/Mac

# Create new environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
~~~

3. **Install PyTorch with CUDA Support**

~~~bash
pip3 install torch==2.5.1+cu121 torchvision==0.20.1+cu121 --index-url https://download.pytorch.org/whl/cu121
~~~

4. **Install Other Dependencies**

~~~bash
pip install -r requirements.txt
~~~

5. **Download Model Weights**

~~~bash
# Download gzipped weights
wget https://huggingface.co/vikhyatk/moondream2/resolve/client/moondream-latest-int8.bin.gz
~~~

## Important Note About Model Format

The Moondream library expects the model in a specific TAR archive format. The application handles format conversion automatically:

When starting up, it checks for and processes the model files in this order:

1. First looks for the gzipped file (moondream-latest-int8.bin.gz)
   - If found, extracts it to a .bin file
2. Then looks for the extracted .bin file (moondream-latest-int8.bin)
   - If found, processes it by:
     a. Extracting contents to a temporary directory
     b. Creating a proper TAR archive with the required structure
     c. Cleaning up temporary files

The final TAR archive will contain:

- vision_encoder.onnx
- vision_projection.onnx
- text_encoder.onnx
- text_decoder files
- tokenizer.json
- initial_kv_caches.npy
- config.json

The resulting file will be named `moondream-latest-mtb.tar`.

## Running the Application

Start the Streamlit server:

~~~bash
streamlit run app/main.py
~~~

The application will be available at [http://localhost:8501](http://localhost:8501)

On first run, if you haven't already downloaded the model weights, the application will automatically download them (~2GB) with a progress bar. This may take a few minutes depending on your internet connection.

## Project Structure

~~~visualization
moondream-streamlit/
├── app/
│   ├── components/
│   │   ├── chat_interface.py    # Chat UI component
│   │   └── image_uploader.py    # Image upload component
│   ├── utils/
│   │   ├── logger.py           # Logging configuration
│   │   └── moondream_integration.py  # Moondream model wrapper
│   └── main.py                 # Main Streamlit application
├── logs/                       # Application logs
├── moondream-latest-int8.bin   # Model weights (downloaded on first run, after extraction)
├── moondream-latest-mtb.tar    # Converted model archive (created automatically)
├── requirements.txt            # Project dependencies
└── README.md                   # This file
~~~

Usage

1. Launch the application using the steps above
2. Upload an image using the file uploader
3. Wait for the image description to generate
4. Ask questions about the image using the chat interface
5. View the chat history below the input field

Troubleshooting
CUDA Issues

- Ensure you have the correct NVIDIA drivers installed
- Verify CUDA installation with torch.cuda.is_available()
- Check GPU compatibility with CUDA 12.1

ONNX DLL Error

- Install Microsoft Visual C++ Redistributable 2019
- Restart your computer after installation
- Check Windows Event Viewer for detailed error messages

Logging
The application logs are stored in the logs/ directory with timestamps. Each session creates a new log file with the format: app_YYYYMMDD_HHMMSS.log

Contributing
Feel free to open issues or submit pull requests with improvements.

License
MIT License - feel free to use and modify as needed.
