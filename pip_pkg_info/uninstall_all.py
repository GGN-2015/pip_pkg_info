import sys

# Safely import tqdm; use progress bar only if available (no error)
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    tqdm = None
    TQDM_AVAILABLE = False

try:
    from .pkg_info import pip_pkg_info
    from .uninstall import uninstall_pkg
except:
    from pkg_info import pip_pkg_info
    from uninstall import uninstall_pkg

def remove_all(self_keep: bool = True, local_keep: bool = True):
    pkg_info = pip_pkg_info()
    white_list = ["pip"]  # Essential packages that must NOT be removed

    # Keep all locally installed packages
    if local_keep:
        for pkg_name in pkg_info:
            pkg_item = pkg_info[pkg_name]
            if pkg_item["local"] and (pkg_name not in white_list):
                white_list.append(pkg_name)

    # Ensure pip_pkg_info itself is not uninstalled
    if self_keep:
        white_list.append("pip-pkg-info")
    
    # Skip uninstalling tqdm itself to avoid runtime errors
    if TQDM_AVAILABLE:
        white_list.append("tqdm")
        white_list.append("colorama")

    # Collect all packages to uninstall
    uninstall_pkgs = []
    for term, details in sorted(pkg_info.items()):
        if term not in white_list:
            uninstall_pkgs.append(term)

    total_cnt = len(uninstall_pkgs)
    fail_cnt = 0

    # Use tqdm progress bar if available
    if TQDM_AVAILABLE:
        assert tqdm is not None
        pkg_iter = tqdm(
            uninstall_pkgs,
            desc="Uninstalling packages",
            unit="pkg",
            file=sys.stdout
        )
    else:
        pkg_iter = uninstall_pkgs

    # Perform uninstallation
    for term in pkg_iter:
        try:
            uninstall_pkg(term)
        except Exception as e:
            # Avoid messy output when progress bar is active
            if not TQDM_AVAILABLE:
                sys.stderr.write(f"Unexpected exception happened when uninstalling {term}.\n")
            fail_cnt += 1

    # Print final result
    if fail_cnt != 0:
        sys.stderr.write(f"\nUninstalling total {total_cnt} packages, {fail_cnt} failed.\n")
    else:
        if TQDM_AVAILABLE:
            sys.stdout.write(f"\nAll {total_cnt} packages uninstalled successfully!\n")

if __name__ == "__main__":
    remove_all()