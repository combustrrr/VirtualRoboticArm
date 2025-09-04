"""
Interactive 3D JCB Robotic Arm Mini Project
Main entry point for the Virtual Robotic Arm simulation
"""
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
            cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("✅ All dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
            print("\n📝 You can try installing manually with:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during installation: {e}")
            return False
    else:
        print("✅ All dependencies are already installed!")
        return True


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("INTERACTIVE 3D JCB ROBOTIC ARM MINI PROJECT")
    print("=" * 60)
    print("Enhanced Web-Based Interface with Integrated Features")
    print()
    
    # Check and install dependencies first
    if not check_and_install_dependencies():
        print("\n❌ Failed to install required dependencies.")
        print("Please install them manually and try again.")
        return
    
    print("\n🎉 All dependencies are ready!")
    print("Starting the application...")
    
    while True:
        print("\nSelect interface mode:")
        print("1. Enhanced Web-Based Interface (Comprehensive)")
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
    """Run Enhanced Web Interactive Arm"""
    print("\n" + "=" * 50)
    print("LAUNCHING ENHANCED WEB-BASED INTERFACE")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'web_interactive_arm.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import web_interactive_arm
            web_interactive_arm.main()
        except Exception as e:
            print(f"Error running Enhanced Web Interactive Arm: {e}")
            print("You can also run it directly with:")
            print("python src/web_interactive_arm.py")
    else:
        print(f"Enhanced Web Interactive Arm script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting Virtual Robotic Arm simulation...")
        sys.exit(0)