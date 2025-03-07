import os
import shutil
import subprocess
import sys
import platform

def check_environment():
    """
    Verifies the Python environment and required packages are properly set up.
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

def rename_config_file():
    """
    Ensure the pygbag config file has the correct name.
    """
    if os.path.exists('pybag.config.json') and not os.path.exists('pygbag.config.json'):
        print("Renaming pybag.config.json to pygbag.config.json")
        shutil.copy2('pybag.config.json', 'pygbag.config.json')

def prepare_build_directory():
    """
    Creates a clean build directory with all necessary files.
    """
    print("Setting up build directory...")
    
    # Define the build directory path
    build_dir = 'clean_build'
    
    # Clean up existing build directory if it exists
    if os.path.exists(build_dir):
        print(f"Removing existing {build_dir} directory")
        shutil.rmtree(build_dir)
    
    # Create new build directory
    os.makedirs(build_dir)
    print(f"Created new {build_dir} directory")
    
    # Copy all Python files
    python_files = [
        'main.py', 
        'markov.py', 
        'game.py', 
        'menu_system.py', 
        '__init__.py'
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            shutil.copy2(file_path, os.path.join(build_dir, file_path))
            print(f"Copied {file_path} to {build_dir}")
        else:
            print(f"Warning: {file_path} not found")
    
    # Copy pygbag.config.json
    if os.path.exists('pygbag.config.json'):
        shutil.copy2('pygbag.config.json', os.path.join(build_dir, 'pygbag.config.json'))
        print(f"Copied pygbag.config.json to {build_dir}")
    
    # Copy directories
    directories = ['assets', 'utils', 'examples']
    
    for directory in directories:
        if os.path.exists(directory):
            dest_dir = os.path.join(build_dir, directory)
            shutil.copytree(directory, dest_dir)
            print(f"Copied {directory} directory to {build_dir}")
        else:
            print(f"Warning: {directory} directory not found")
            # Create empty directories that might be needed
            if directory in ['utils']:
                os.makedirs(os.path.join(build_dir, directory), exist_ok=True)
                with open(os.path.join(build_dir, directory, '__init__.py'), 'w') as f:
                    pass
                print(f"Created empty {directory} directory with __init__.py")
    
    return build_dir

def run_pygbag_build(build_dir):
    """
    Runs Pygbag build command on the prepared directory.
    """
    print("\nRunning Pygbag build...")
    
    try:
        # Change to the build directory
        original_dir = os.getcwd()
        os.chdir(build_dir)
        
        # Run pygbag build command
        subprocess.run([
            sys.executable,
            "-m",
            "pygbag",
            "--build",
            "--ume_block", "0",
            "--app_name", "Markov Shapes",
            "--title", "Markov Shapes",
            "."  # Build from current directory
        ], check=True)
        
        # Move back to original directory
        os.chdir(original_dir)
        
        # Check if build was successful
        if os.path.exists(os.path.join(build_dir, 'build', 'web')):
            print("\nBuild completed successfully!")
            
            # Copy the build artifacts to a more accessible location
            if os.path.exists('web_build'):
                shutil.rmtree('web_build')
            
            shutil.copytree(
                os.path.join(build_dir, 'build', 'web'), 
                'web_build'
            )
            
            print("\nDeployable files are available in the 'web_build' directory.")
            print("To deploy to itch.io:")
            print("1. Go to your project page on itch.io")
            print("2. Click 'Upload files' or 'Edit game'")
            print("3. Choose 'HTML' as the project type")
            print("4. Upload all files from the 'web_build' directory")
            print("5. Check 'This file will be played in the browser'")
        else:
            print("\nBuild process completed but build directory not found.")
            print("Check for errors in the build process.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error running Pygbag: {e}")
        return False
    
    return True

def main():
    """
    Main deployment function.
    """
    print("=== Markov Shapes Deployment Process ===")
    
    check_environment()
    rename_config_file()
    build_dir = prepare_build_directory()
    success = run_pygbag_build(build_dir)
    
    if success:
        print("\nDeployment process completed successfully.")
    else:
        print("\nDeployment process encountered errors.")

if __name__ == "__main__":
    main()