#!/usr/bin/env python3
"""
Virtual Robotic Arm - Quick Setup Script
Automatically installs dependencies and sets up the environment
"""
import sys
import subprocess
import os

def main():
    """Setup the Virtual Robotic Arm environment"""
    print("🔧 Virtual Robotic Arm - Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    print("✅ requirements.txt found")
    
    # Install dependencies
    print("\n🚀 Installing dependencies...")
    try:
        cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully!")
        
        # Test imports
        print("\n🧪 Testing imports...")
        test_packages = ['pybullet', 'numpy', 'matplotlib', 'cv2', 'PIL']
        
        for package in test_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"⚠️  {package} (optional)")
        
        print("\n🎉 Setup complete!")
        print("\nTo start the application, run:")
        print("  python main.py")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)