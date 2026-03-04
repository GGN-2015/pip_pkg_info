import subprocess
import sys
from typing import Tuple, Optional

def _check_package_installed(package_name: str) -> bool:
    """
    Helper function to check if a package is currently installed.
    
    Args:
        package_name (str): Name of the package to check
    
    Returns:
        bool: True if installed, False if not (or if check fails)
    """
    try:
        # Use pip show to check package existence (silent output)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        # pip show returns 0 exit code only if package exists
        return result.returncode == 0
    except Exception:
        return False

def _uninstall_package(package_name: str) -> Tuple[bool, str]:
    """
    Helper function to uninstall a package (silent, auto-confirm).
    
    Args:
        package_name (str): Name of the package to uninstall
    
    Returns:
        Tuple[bool, str]: (Success flag, message)
    """
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package_name],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return True, f"Uninstalled existing package: {package_name}"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to uninstall {package_name}: {e.stderr.strip()[:200]}"
    except Exception as e:
        return False, f"Unexpected error during uninstall: {str(e)}"

def install_pkg(package_name: str, version: Optional[str] = None) -> Tuple[bool, str]:
    """
    Install a package with a "clean" workflow:
    1. Check if the package is already installed
    2. Uninstall it (if present)
    3. Install the specified version (or latest version if no version is provided)
    
    Args:
        package_name (str): Name of the package to install (e.g., "requests", "numpy")
        version (Optional[str]): Specific version to install (e.g., "2.31.0") 
                                 If None, installs the latest version (default: None)
    
    Returns:
        Tuple[bool, str]: 
            - First value: Boolean (True = full workflow succeeded, False = failed)
            - Second value: Human-readable log of the workflow
    """
    # Validate input
    if not package_name or not isinstance(package_name, str):
        return False, "Error: Invalid package name (must be a non-empty string)"
    
    # Build package spec (name + optional version)
    package_spec = package_name
    if version:
        if not isinstance(version, str):
            return False, "Error: Version must be a string (e.g., '2.31.0')"
        package_spec = f"{package_name}=={version}"
    
    # Step 1: Check if package is installed
    install_log = []
    is_installed = _check_package_installed(package_name)
    
    if is_installed:
        install_log.append(f"Package '{package_name}' is currently installed")
        
        # Step 2: Uninstall existing package
        uninstall_success, uninstall_msg = _uninstall_package(package_name)
        if not uninstall_success:
            install_log.append(f"❌ Uninstall failed: {uninstall_msg}")
            return False, "\n".join(install_log)
        install_log.append(f"✅ {uninstall_msg}")
    else:
        install_log.append(f"Package '{package_name}' is not installed (skipping uninstall)")
    
    # Step 3: Install target version
    install_log.append(f"Installing target version: {package_spec}")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_spec],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        install_log.append(f"✅ Successfully installed {package_spec}")
        return True, "\n".join(install_log)
    
    except subprocess.CalledProcessError as e:
        error_details = e.stderr.strip()[:300]
        install_log.append(f"❌ Failed to install {package_spec}: {error_details}")
        return False, "\n".join(install_log)
    except Exception as e:
        install_log.append(f"❌ Unexpected install error: {str(e)}")
        return False, "\n".join(install_log)

# Example Usage
if __name__ == "__main__":
    # Example 1: Install latest version (clean install)
    print("=== Clean Install: Latest Requests ===")
    success, log = install_pkg("requests")
    print(log)
    print(f"\nOverall Result: {'✅ SUCCESS' if success else '❌ FAILURE'}\n")

    # Example 2: Install specific version (clean install)
    print("=== Clean Install: pd-code-rotate 0.0.1 ===")
    success, log = install_pkg("pd-code-rotate", version="0.0.1")
    print(log)
    print(f"\nOverall Result: {'✅ SUCCESS' if success else '❌ FAILURE'}")
