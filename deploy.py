import os
import shutil
import subprocess
import sys
import platform

def check_environment():
    """
    Verifies the Python environment and required packages are properly set up.
    This helps ensure we have the correct versions before starting deployment.
    """
    print("Checking environment...")
    
    # Check Python version
    python_version = platform.python_version()
    print(f"Python version: {python_version}")
    
    # Check Pygbag version
    try:
        import pygbag
        print(f"Pygbag version: {pygbag.__version__}")
    except ImportError:
        print("Pygbag not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag==0.8.3"])
        import pygbag
        print(f"Installed Pygbag version: {pygbag.__version__}")

def create_web_directory():
    """
    Creates and prepares the web directory structure with all necessary files.
    This ensures all required files are in place before running Pygbag.
    """
    print("Setting up web directory...")
    
    # Clean up existing directories
    for dir_name in ['web', 'build']:
        if os.path.exists(dir_name):
            print(f"Removing existing {dir_name} directory")
            shutil.rmtree(dir_name)
    
    # Create new directories
    os.makedirs('web')
    print("Created new web directory")
    
    # Create __init__.py files
    for path in ['web', 'web/utils']:
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, '__init__.py')
        with open(init_file, 'w') as f:
            pass
        print(f"Created {init_file}")
    
    # Copy required files
    files_to_copy = [
        'main.py',
        'markov.py',
        'game.py',          
        'menu_system.py',   
        'utils/settings.py',
        'utils/button.py',  
    ]
    
    for file_path in files_to_copy:
        dest_path = os.path.join('web', file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if os.path.exists(file_path):
            shutil.copy2(file_path, dest_path)
            print(f"Copied {file_path} to {dest_path}")
        else:
            print(f"Warning: {file_path} not found")

def run_pygbag():
    """
    Runs Pygbag with the correct arguments for version 0.8.3.
    Uses simplified argument syntax to avoid compatibility issues.
    """
    print("\nStarting Pygbag...")
    try:
        # Using simplified arguments that are known to work with 0.8.3
        subprocess.run([
            sys.executable,
            "-m",
            "pygbag",
            "--port", "8000",
            "--bind", "0.0.0.0",
            "--cache", "no",
            "web"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Pygbag: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)

def main():
    """
    Main deployment process that coordinates all steps of the deployment.
    Provides clear feedback at each stage of the process.
    """
    print("Starting deployment process...")
    
    check_environment()
    create_web_directory()
    run_pygbag()

if __name__ == "__main__":
    main()