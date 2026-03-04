# pip_pkg_info
use this pkg to show all the packages installed by pip in JSON form.

## Install

```bash
pip install pip-pkg-info
```

## Usage

python usage:
```python
import pip_pkg_info

# install pkg
pip_pkg_info.install_pkg("<package-name>")
pip_pkg_info.install_pkg("<package-name>", "<version>")

# remove pkg
pip_pkg_info.uninstall_pkg("<package-name>")

# remove all pkg (will NOT remove pip)
pip_pkg_info.remove_all()
pip_pkg_info.remove_all(self_keep=False) # remove pip_pkg_info
```

command line usage:
```bash

# show packages info in JSON
python -m pip_pkg_info

# remove_all pkg (except pip and pip_pkg_info)
python -m pip_pkg_info remove_all
```
