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
    print("Enhanced Web-Based Interface with Integrated Features")
    print()
    
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