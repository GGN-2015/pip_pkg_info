import subprocess
import sys

try:
    from .pip_version import get_pip_version
except:
    from pip_version import get_pip_version

def pip_pkg_info() -> dict:
    """
    Execute 'pip freeze' via subprocess and return detailed package information
    as a nested dictionary with 'version' and 'local' flags for each package.
    
    Returns:
        dict: Nested dictionary in format {package_name: {"version": str, "local": bool}}
              Returns empty dict if execution/parsing fails.
    """

    # Main dictionary to store package info
    package_details = {
        "pip":{"version":get_pip_version()[1], "local":False}
    }
    
    try:
        # Execute pip freeze using current Python interpreter (avoids environment mismatch)
        command = [sys.executable, "-m", "pip", "freeze"]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        # Parse each line of the command output
        for line in result.stdout.splitlines():
            clean_line = line.strip()
            
            # Skip empty lines
            if not clean_line:
                continue
            
            # Case 1: Standard package with version (package==x.y.z)
            if '==' in clean_line:
                pkg_name, pkg_version = clean_line.split('==', 1)
                package_details[pkg_name.strip()] = {
                    "version": pkg_version.strip(),
                    "local": False
                }
            
            # Case 2: Locally installed package (package@ file:///path)
            elif '@' in clean_line:
                pkg_name = clean_line.split('@')[0].strip()
                package_details[pkg_name] = {
                    "version": "local_install",
                    "local": True
                }
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing pip freeze command: {e}")
        print(f"Error output from pip: {e.stderr.strip()}")
    except Exception as e:
        print(f"Unexpected error during package parsing: {str(e)}")
    
    return package_details

# Example usage
if __name__ == "__main__":
    print("Installed Python Packages (with version and local status):")
    print("-" * 85)
    
    packages = pip_pkg_info()
    
    if packages:
        # Print packages in alphabetical order with formatted output
        for pkg_name, details in sorted(packages.items()):
            print(f"Package: {pkg_name:<25} | Version: {details['version']:<15} | Local Install: {details['local']}")
    else:
        print("Failed to retrieve package information.")
