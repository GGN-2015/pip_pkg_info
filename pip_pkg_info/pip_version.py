import subprocess
import sys
from typing import Tuple, Optional

def get_pip_version() -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Query the version of pip associated with the current Python interpreter.
    
    Returns:
        Tuple[bool, Optional[str], Optional[str]]:
            - 1st value: Boolean (True = success, False = failure)
            - 2nd value: Pip version string (e.g., "24.0") if successful, None otherwise
            - 3rd value: Full raw output/error message (for debugging)
    """
    try:
        # Run `python -m pip --version` to get pip version (reliable cross-environment)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        # Parse raw output to extract only the version number
        # Raw output example: "pip 24.0 from /path/to/pip (python 3.11)"
        raw_output = result.stdout.strip()
        pip_version = None
        
        if raw_output.startswith("pip "):
            # Split on space and take the second element (version)
            version_part = raw_output.split()[1]
            # Clean version (remove any suffixes like "b1" for beta, keep core version if needed)
            pip_version = version_part.split()[0]  # Ensures we get just "24.0"
        
        return True, pip_version, raw_output
    
    except subprocess.CalledProcessError as e:
        # Handle pip command failure (e.g., pip not installed)
        error_msg = f"Pip command failed: {e.stderr.strip()}"
        return False, None, error_msg
    except Exception as e:
        # Handle unexpected errors (e.g., encoding issues)
        error_msg = f"Unexpected error: {str(e)}"
        return False, None, error_msg

# Example Usage
if __name__ == "__main__":
    # Get pip version
    success, version, details = get_pip_version()
    
    # Print results
    if success:
        print(f"✅ Pip Version: {version}")
        print(f"📝 Full Output: {details}")
    else:
        print(f"❌ Failed to get pip version: {details}")

    # ------------------------------
    # Alternative Method 1: Import pip directly (less reliable)
    # ------------------------------
    try:
        import pip
        print(f"\n📌 Alternative (import pip): pip.__version__ = {pip.__version__}")
    except ImportError:
        print("\n⚠️ Alternative method failed: Could not import pip (common in newer pip versions)")

    # ------------------------------
    # Alternative Method 2: Using `pip -V` (same as --version)
    # ------------------------------
    # Note: Less reliable than `-m pip` (may use wrong pip in virtual environments)
    # subprocess.run(["pip", "-V"], ...)