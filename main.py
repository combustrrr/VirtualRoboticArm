"""
Interactive 3D JCB Robotic Arm Mini Project
Main entry point for the Virtual Robotic Arm simulation
"""
import sys
import os

def main():
    """Main demonstration function"""
    print("=" * 60)
    print("INTERACTIVE 3D JCB ROBOTIC ARM MINI PROJECT")
    print("=" * 60)
    
    while True:
        print("\nSelect simulation mode:")
        print("1. Enhanced CAD Interactive Arm (Recommended)")
        print("2. Web-Based Interface")
        print("3. Real CAD Integration")
        print("4. Matplotlib Visualization")
        print("5. Realistic Texture Demo")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            run_enhanced_cad_interactive_arm()
        elif choice == "2":
            run_web_interactive_arm()
        elif choice == "3":
            run_real_cad_integration()
        elif choice == "4":
            run_matplotlib_visualization()
        elif choice == "5":
            run_realistic_texture_demo()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


def run_enhanced_cad_interactive_arm():
    """Run Enhanced CAD Interactive Arm"""
    print("\n" + "=" * 50)
    print("LAUNCHING ENHANCED CAD INTERACTIVE ARM")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'enhanced_cad_interactive_arm.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import enhanced_cad_interactive_arm
            enhanced_cad_interactive_arm.main()
        except Exception as e:
            print(f"Error running Enhanced CAD Interactive Arm: {e}")
            print("You can also run it directly with:")
            print("python src/enhanced_cad_interactive_arm.py")
    else:
        print(f"Enhanced CAD Interactive Arm script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


def run_web_interactive_arm():
    """Run Web Interactive Arm"""
    print("\n" + "=" * 50)
    print("LAUNCHING WEB-BASED INTERFACE")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'web_interactive_arm.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import web_interactive_arm
            web_interactive_arm.main()
        except Exception as e:
            print(f"Error running Web Interactive Arm: {e}")
            print("You can also run it directly with:")
            print("python src/web_interactive_arm.py")
    else:
        print(f"Web Interactive Arm script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


def run_real_cad_integration():
    """Run Real CAD Integration"""
    print("\n" + "=" * 50)
    print("LAUNCHING REAL CAD INTEGRATION")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'real_cad_integration.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import real_cad_integration
            real_cad_integration.main()
        except Exception as e:
            print(f"Error running Real CAD Integration: {e}")
            print("You can also run it directly with:")
            print("python src/real_cad_integration.py")
    else:
        print(f"Real CAD Integration script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


def run_matplotlib_visualization():
    """Run Matplotlib Visualization"""
    print("\n" + "=" * 50)
    print("LAUNCHING MATPLOTLIB VISUALIZATION")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'interactive_matplotlib_arm.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import interactive_matplotlib_arm
            interactive_matplotlib_arm.main()
        except Exception as e:
            print(f"Error running Matplotlib Visualization: {e}")
            print("You can also run it directly with:")
            print("python src/interactive_matplotlib_arm.py")
    else:
        print(f"Matplotlib Visualization script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


def run_realistic_texture_demo():
    """Run Realistic Texture Demo"""
    print("\n" + "=" * 50)
    print("LAUNCHING REALISTIC TEXTURE DEMO")
    print("=" * 50)
    
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           'src', 'realistic_texture_system.py')
    
    if os.path.exists(src_path):
        try:
            sys.path.insert(0, os.path.dirname(src_path))
            import realistic_texture_system
            realistic_texture_system.main()
        except Exception as e:
            print(f"Error running Realistic Texture Demo: {e}")
            print("You can also run it directly with:")
            print("python src/realistic_texture_system.py")
    else:
        print(f"Realistic Texture Demo script not found at: {src_path}")
        print("Please ensure all source files are properly installed.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting Virtual Robotic Arm simulation...")
        sys.exit(0)