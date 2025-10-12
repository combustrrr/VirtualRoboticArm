"""Entry point for the Virtual Robotic Arm toolkit."""
import sys
import os
import subprocess
import importlib

def check_and_install_dependencies():
    """Check for required dependencies and install them if missing"""
    print("🔍 Checking dependencies...")
    
    # Get the requirements file path
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print("⚠️  requirements.txt not found. Skipping dependency check.")
        return True
    
    # Read requirements
    try:
        with open(requirements_path, 'r') as f:
            requirements = [line.strip() for line in f.readlines() 
                          if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False
    
    missing_packages = []
    
    # Check each requirement
    for requirement in requirements:
        if not requirement:
            continue
            
        # Extract package name (handle version specifiers)
        package_name = requirement.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
        
        # Special handling for opencv-python
        if package_name == 'opencv-python':
            package_name = 'cv2'
        
        try:
            importlib.import_module(package_name)
            print(f"✅ {package_name} is already installed")
        except ImportError:
            print(f"❌ {package_name} is missing")
            missing_packages.append(requirement)
    
    # Install missing packages
    if missing_packages:
        print(f"\n🚀 Installing {len(missing_packages)} missing dependencies...")
        print("This may take a few minutes...")
        
        try:
            # Install all missing packages at once
            cmd = [sys.executable, '-m', 'pip', 'install', '--timeout', '60'] + missing_packages
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
            
            print("✅ All dependencies installed successfully!")
            return True
            
        except subprocess.TimeoutExpired:
            print("⚠️  Installation timed out. This may be due to network issues.")
            print("📝 Please try installing manually with:")
            print(f"pip install {' '.join(missing_packages)}")
            
            # Continue anyway - the app might still work with degraded functionality
            print("\n🔄 Continuing with available dependencies...")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            
            # Check for common network-related errors
            if any(keyword in error_msg.lower() for keyword in ['timeout', 'connection', 'network', 'http']):
                print("⚠️  Network connectivity issue detected during installation.")
                print("📝 Please check your internet connection and try installing manually with:")
                print(f"pip install {' '.join(missing_packages)}")
                
                # Continue anyway - the app might still work with degraded functionality
                print("\n🔄 Continuing with available dependencies...")
                return True
            else:
                print(f"❌ Error installing dependencies: {e}")
                print(f"Error details: {error_msg}")
                print("\n📝 You can try installing manually with:")
                print(f"pip install {' '.join(missing_packages)}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error during installation: {e}")
            print("\n📝 You can try installing manually with:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ All dependencies are already installed!")
        return True


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("PUMA 560 VIRTUAL ROBOTIC ARM")
    print("=" * 60)
    print("Streamlit-driven digital twin with cinematic 3D rendering")
    print()
    
    # Check and install dependencies first
    deps_result = check_and_install_dependencies()
    
    if deps_result:
        print("\n🎉 All dependencies are ready!")
    else:
        print("\n⚠️  Some dependencies may be missing, but continuing...")
        print("The application will run with reduced functionality.")
    
    print("Starting the application...")
    
    while True:
        print("\nSelect interface mode:")
        print("1. Launch Streamlit interface")
        print("2. Exit")
        
        try:
            choice = input("\nEnter your choice (1-2): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            run_web_interactive_arm()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-2.")


def run_web_interactive_arm():
    """Launch the Streamlit-based experience."""
    print("\n" + "=" * 50)
    print("LAUNCHING STREAMLIT INTERFACE")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'streamlit_puma_interface.py')
    
    if os.path.exists(src_path):
        try:
            import subprocess
            print("Starting Streamlit server...")
            print(f"Command: streamlit run {src_path}")
            print("The application will open in your default web browser.")
            print("Press Ctrl+C to stop the server.")
            print()
            
            # Launch streamlit
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', src_path], 
                         check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error launching Streamlit: {e}")
            print("You can also launch it manually with:")
            print(f"streamlit run {src_path}")
        except KeyboardInterrupt:
            print("\nStopping Streamlit server...")
    else:
        print(f"Streamlit application not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting Virtual Robotic Arm simulation...")
        sys.exit(0)