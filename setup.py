"""Installation script for required packages with Conda environment setup."""
import subprocess
import sys
import os

CONDA_ENV_NAME = "support-ai"
PYTHON_VERSION = "3.10"  

def create_conda_env():
    """Create and activate a Conda environment."""
    print(f"Creating Conda environment '{CONDA_ENV_NAME}' with Python {PYTHON_VERSION}...")
    
    # Create Conda environment
    subprocess.run([
        "conda", "create", "-y", "-n", CONDA_ENV_NAME, f"python={PYTHON_VERSION}"
    ], check=True)

    print(f"Conda environment '{CONDA_ENV_NAME}' created successfully!")

def install_requirements():
    """Install all required packages inside the Conda environment."""
    print(f"Installing required packages in Conda environment '{CONDA_ENV_NAME}'...")
    
    # Core packages
    packages = [
        "pip",
        "langchain-community",
        "langchain-core",
        "langgraph",
        "langchain-openai",
        "pillow",
        "transformers",
        "torchvision"
    ]
    
    # OpenVINO packages
    openvino_packages = [
        "--pre",
        "-U",
        "--extra-index-url",
        "https://storage.openvinotoolkit.org/simple/wheels/pre-release",
        "openvino_tokenizers",
        "openvino"
    ]
    
    # Install core packages inside Conda environment
    subprocess.run([
        "conda", "run", "-n", CONDA_ENV_NAME, "pip", "install"
    ] + packages, check=True)

    # Install OpenVINO packages
    subprocess.run([
        "conda", "run", "-n", CONDA_ENV_NAME, "pip", "install"
    ] + openvino_packages, check=True)

    # Install optimum-intel from GitHub
    subprocess.run([
        "conda", "run", "-n", CONDA_ENV_NAME, "pip", "install",
        "git+https://github.com/huggingface/optimum-intel.git"
    ], check=True)

    print("All packages installed successfully!")

def set_environment_variables():
    """Set required environment variables."""
    print("Setting environment variables...")
    
    api_key = input("Enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = api_key

    # Save to .env file for persistence
    try:
        with open(".env", "w") as env_file:
            env_file.write(f"OPENAI_API_KEY={api_key}\n")
        print("API key saved to .env file")
    except Exception as e:
        print(f"Could not save to .env file: {e}")
        print("Please set the API key manually in future sessions.")

def display_activation_instructions():
    """Display instructions for activating the Conda environment."""
    print("\nSetup complete!")
    print(f"To activate the Conda environment, run:")
    print(f"  conda activate {CONDA_ENV_NAME}")
    print("Then, you can start the support agent with:")
    print("  python main.py")

if __name__ == "__main__":
    create_conda_env()
    install_requirements()
    set_environment_variables()
    display_activation_instructions()
