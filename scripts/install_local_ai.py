#!/usr/bin/env python3
"""
Installation script for local AI and OCR dependencies
"""

import subprocess
import sys
import os
import requests
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_python_packages():
    """Install Python packages for local AI and OCR"""
    packages = [
        "easyocr==1.7.0",
        "requests==2.31.0"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            for model in models[:3]:
                print(f"   - {model.get('name', 'unknown')}")
            return True
        else:
            print("⚠️  Ollama is installed but not responding correctly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Ollama is not running or not installed")
        return False

def install_ollama():
    """Provide instructions for installing Ollama"""
    system = platform.system().lower()
    
    print("\n🤖 Ollama Installation Instructions:")
    print("=" * 50)
    
    if system == "windows":
        print("1. Download Ollama from: https://ollama.ai/download")
        print("2. Run the installer")
        print("3. Ollama will start automatically as a service")
    elif system == "darwin":  # macOS
        print("Option 1 - Using Homebrew:")
        print("   brew install ollama")
        print("\nOption 2 - Direct download:")
        print("   Download from: https://ollama.ai/download")
    else:  # Linux
        print("Run this command:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
    
    print("\n4. After installation, pull a model:")
    print("   ollama pull llama2")
    print("\n5. Verify installation:")
    print("   ollama list")
    
    return False

def pull_recommended_model():
    """Pull a recommended model if Ollama is available"""
    if not check_ollama_installation():
        return False
    
    print("\n🔄 Pulling recommended model (llama2)...")
    if run_command("ollama pull llama2", "Pulling llama2 model"):
        print("✅ Model llama2 is ready for use")
        return True
    else:
        print("⚠️  Failed to pull model. You can try manually: ollama pull llama2")
        return False

def test_easyocr():
    """Test EasyOCR installation"""
    try:
        import easyocr
        print("✅ EasyOCR is installed and ready")
        return True
    except ImportError:
        print("❌ EasyOCR is not installed")
        return False

def test_system_integration():
    """Test the system integration"""
    try:
        response = requests.get("http://localhost:8000/api/v1/system/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("\n📊 System Status:")
            print("=" * 30)
            
            # AI Status
            ai_status = status.get('services', {}).get('ai', {})
            ollama_status = ai_status.get('ollama', {})
            openai_status = ai_status.get('openai', {})
            
            print(f"🤖 Ollama: {'✅' if ollama_status.get('available') else '❌'}")
            if ollama_status.get('models'):
                print(f"   Models: {', '.join(ollama_status['models'])}")
            
            print(f"🔗 OpenAI: {'✅' if openai_status.get('available') else '❌'}")
            
            # OCR Status
            ocr_status = status.get('services', {}).get('ocr', {})
            print(f"👁️  OCR Engine: {ocr_status.get('primary_engine', 'None')}")
            print(f"   EasyOCR: {'✅' if ocr_status.get('easyocr_available') else '❌'}")
            print(f"   Tesseract: {'✅' if ocr_status.get('tesseract_available') else '❌'}")
            
            return True
        else:
            print("⚠️  Backend is not responding correctly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend is not running. Start it with: uvicorn app.main:app --reload")
        return False

def main():
    """Main installation function"""
    print("🚀 Career Intelligence System - Local AI Setup")
    print("=" * 60)
    
    # Install Python packages
    print("\n1. Installing Python packages...")
    if not install_python_packages():
        print("❌ Failed to install Python packages")
        return False
    
    # Test EasyOCR
    print("\n2. Testing EasyOCR...")
    test_easyocr()
    
    # Check Ollama
    print("\n3. Checking Ollama installation...")
    if not check_ollama_installation():
        install_ollama()
        print("\n⏸️  Please install Ollama and run this script again")
        return False
    
    # Pull model
    print("\n4. Setting up AI model...")
    pull_recommended_model()
    
    # Test integration
    print("\n5. Testing system integration...")
    if test_system_integration():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. The system is ready to use local AI")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Access the application: http://localhost:5173")
        print("4. Check system status: http://localhost:8000/api/v1/system/status")
    else:
        print("\n⚠️  System integration test failed")
        print("Make sure the backend is running: uvicorn app.main:app --reload")
    
    return True

if __name__ == "__main__":
    main()
