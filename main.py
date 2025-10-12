"""Entry point for the Virtual Robotic Arm toolkit."""
import sys
import os
import subprocess
import importlib

def _get_requirements_file_path():
    """Get the path to requirements.txt file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')


def _read_requirements_file(requirements_path):
    """Read and parse requirements from requirements.txt file."""
    if not os.path.exists(requirements_path):
        print("WARNING: requirements.txt not found. Skipping dependency check.")
        return None
    
    try:
        with open(requirements_path, 'r') as f:
            requirements = [line.strip() for line in f.readlines() 
                          if line.strip() and not line.strip().startswith('#')]
        return requirements
    except Exception as e:
        print(f"ERROR: Failed to read requirements.txt: {e}")
        return False


def _extract_package_name(requirement):
    """Extract package name from requirement string, handling version specifiers."""
    if not requirement:
        return None
        
    # Extract package name (handle version specifiers)
    package_name = requirement.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
    
    # Special handling for opencv-python
    if package_name == 'opencv-python':
        package_name = 'cv2'
    
    return package_name


def _check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def _find_missing_packages(requirements):
    """Find packages that are missing from the current environment."""
    missing_packages = []
    
    for requirement in requirements:
        package_name = _extract_package_name(requirement)
        if not package_name:
            continue
            
        if _check_package_installed(package_name):
            print(f"FOUND: {package_name} is already installed")
        else:
            print(f"MISSING: {package_name} is not installed")
            missing_packages.append(requirement)
    
    return missing_packages


def _handle_installation_timeout(missing_packages):
    """Handle installation timeout gracefully."""
    print("WARNING: Installation timed out. This may be due to network issues.")
    print("MANUAL INSTALLATION: Please try installing manually with:")
    print(f"pip install {' '.join(missing_packages)}")
    print("\nCONTINUING: Proceeding with available dependencies...")
    return True


def _handle_network_error(missing_packages):
    """Handle network-related installation errors."""
    print("WARNING: Network connectivity issue detected during installation.")
    print("MANUAL INSTALLATION: Please check your internet connection and try installing manually with:")
    print(f"pip install {' '.join(missing_packages)}")
    print("\nCONTINUING: Proceeding with available dependencies...")
    return True


def _handle_installation_error(e, missing_packages):
    """Handle general installation errors."""
    error_msg = e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)
    print(f"ERROR: Failed to install dependencies: {e}")
    print(f"Error details: {error_msg}")
    print("\nMANUAL INSTALLATION: You can try installing manually with:")
    print(f"pip install {' '.join(missing_packages)}")
    return False


def _is_network_error(error_msg):
    """Check if error message indicates a network-related issue."""
    network_keywords = ['timeout', 'connection', 'network', 'http']
    return any(keyword in error_msg.lower() for keyword in network_keywords)


def _install_missing_packages(missing_packages):
    """Install missing packages using pip."""
    print(f"\nINSTALLING: Installing {len(missing_packages)} missing dependencies...")
    print("This may take a few minutes...")
    
    try:
        cmd = [sys.executable, '-m', 'pip', 'install', '--timeout', '60'] + missing_packages
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
        print("SUCCESS: All dependencies installed successfully!")
        return True
        
    except subprocess.TimeoutExpired:
        return _handle_installation_timeout(missing_packages)
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        if _is_network_error(error_msg):
            return _handle_network_error(missing_packages)
        else:
            return _handle_installation_error(e, missing_packages)
            
    except Exception as e:
        print(f"ERROR: Unexpected error during installation: {e}")
        print("\nMANUAL INSTALLATION: You can try installing manually with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False


def check_and_install_dependencies():
    """Check for required dependencies and install them if missing."""
    print("Checking dependencies...")
    
    requirements_path = _get_requirements_file_path()
    requirements = _read_requirements_file(requirements_path)
    
    if requirements is None:
        return True
    elif requirements is False:
        return False
    
    missing_packages = _find_missing_packages(requirements)
    
    if missing_packages:
        return _install_missing_packages(missing_packages)
    else:
        print("SUCCESS: All dependencies are already installed!")
        return True


def _print_header():
    """Print the application header."""
    print("=" * 60)
    print("PUMA 560 VIRTUAL ROBOTIC ARM")
    print("=" * 60)
    print("Streamlit-driven digital twin with cinematic 3D rendering")
    print()


def _print_dependency_status(deps_result):
    """Print dependency check results."""
    if deps_result:
        print("\nREADY: All dependencies are ready!")
    else:
        print("\nWARNING: Some dependencies may be missing, but continuing...")
        print("The application will run with reduced functionality.")


def _get_user_choice():
    """Get user's menu choice with error handling."""
    print("\nSelect interface mode:")
    print("1. Launch Streamlit interface")
    print("2. Exit")
    
    try:
        choice = input("\nEnter your choice (1-2): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


def _handle_menu_choice(choice):
    """Handle the user's menu choice."""
    if choice == "1":
        launch_streamlit_interface()
        return False  # Continue menu loop
    elif choice == "2":
        print("Goodbye!")
        return True   # Exit menu loop
    else:
        print("Invalid choice. Please enter 1-2.")
        return False  # Continue menu loop


def _run_main_menu():
    """Run the main application menu loop."""
    while True:
        choice = _get_user_choice()
        should_exit = _handle_menu_choice(choice)
        if should_exit:
            break


def main():
    """Main application entry point."""
    _print_header()
    
    # Check and install dependencies first
    deps_result = check_and_install_dependencies()
    _print_dependency_status(deps_result)
    
    print("Starting the application...")
    _run_main_menu()


def _get_streamlit_app_path():
    """Get the path to the Streamlit application."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                       'src', 'streamlit_puma_interface.py')


def _launch_streamlit_process(src_path):
    """Launch the Streamlit process."""
    print("Starting Streamlit server...")
    print(f"Command: streamlit run {src_path}")
    print("The application will open in your default web browser.")
    print("Press Ctrl+C to stop the server.")
    print()
    
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', src_path], check=True)


def _handle_streamlit_error(e, src_path):
    """Handle Streamlit launch errors."""
    print(f"Error launching Streamlit: {e}")
    print("You can also launch it manually with:")
    print(f"streamlit run {src_path}")


def launch_streamlit_interface():
    """Launch the Streamlit-based PUMA 560 interface."""
    print("\n" + "=" * 50)
    print("LAUNCHING STREAMLIT INTERFACE")
    print("=" * 50)
    
    src_path = _get_streamlit_app_path()
    
    if not os.path.exists(src_path):
        print(f"Streamlit application not found at: {src_path}")
        print("Please ensure all source files are properly installed.")
        return
    
    try:
        _launch_streamlit_process(src_path)
    except subprocess.CalledProcessError as e:
        _handle_streamlit_error(e, src_path)
    except KeyboardInterrupt:
        print("\nStopping Streamlit server...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting Virtual Robotic Arm simulation...")
        sys.exit(0)