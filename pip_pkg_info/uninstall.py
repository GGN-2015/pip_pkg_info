import subprocess
import sys
from typing import Tuple, Optional

def uninstall_pkg(package_name: str, skip_confirmation: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Uninstall a specified Python package using `python -m pip uninstall` via subprocess.
    
    Args:
        package_name (str): Name of the package to uninstall (e.g., "requests", "numpy==1.26.4")
        skip_confirmation (bool): If True, add `-y` flag to skip interactive confirmation (default: True)
    
    Returns:
        Tuple[bool, Optional[str]]: 
            - First value: Boolean indicating if uninstall succeeded (True) or failed (False)
            - Second value: Human-readable message (success/error details)
    """
    # Validate input
    if not package_name or not isinstance(package_name, str):
        return False, "Error: Invalid package name (must be non-empty string)"
    
    # Build the uninstall command
    cmd = [sys.executable, "-m", "pip", "uninstall"]
    if skip_confirmation:
        cmd.append("-y")  # Auto-confirm uninstall (no interactive prompt)
    cmd.append(package_name)
    
    try:
        # Execute the uninstall command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,  # Raise CalledProcessError if exit code != 0
            encoding='utf-8'
        )

        if (result.returncode != 0) or (result.stderr.strip() != ""):
            # Handle pip command errors (e.g., package not found, permission denied)
            error_msg = f"Failed to uninstall {package_name}: "
            if "not installed" in result.stderr.lower() or "no such package" in result.stderr.lower():
                error_msg += "Package is not installed"
            elif "permission denied" in result.stderr.lower() or "access denied" in result.stderr.lower():
                error_msg += "Permission denied (try running with admin/root privileges)"
            else:
                error_msg += f"Pip error: {result.stderr.strip()}"
            return False, error_msg
        
        # Success case: return True + success message
        success_msg = f"Successfully uninstalled package: {package_name}"
        # Include pip's output for verification (optional)
        # success_msg += f"\nPip output: {result.stdout.strip()}"
        return True, success_msg
    
    except subprocess.CalledProcessError as e:
        return False, f"Failed to uninstall {package_name}: {str(e)}"
    
    except Exception as e:
        # Handle unexpected errors (e.g., invalid command, encoding issues)
        return False, f"Unexpected error during uninstall: {str(e)}"

# Example Usage
if __name__ == "__main__":
    # Test uninstall (replace "test-package" with actual package name)
    package_to_remove = "test-package"
    
    # Call the uninstall function
    success, message = uninstall_pkg(package_to_remove)
    
    # Print results
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    # Example: Uninstall with interactive confirmation (skip_confirmation=False)
    # success, message = uninstall_package("another-package", skip_confirmation=False)