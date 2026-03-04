import sys
import json
from . import *

def main():
    argv_list = json.loads(json.dumps(sys.argv[1:]))
    
    if argv_list == []:
        print(json.dumps(pip_pkg_info()))

    elif argv_list == ["remove_all"]:
        remove_all()
        print("All package removed.")

    else:
        sys.stderr.write(f"pip-pkg-info: Unknown command list: {argv_list}")

main()
