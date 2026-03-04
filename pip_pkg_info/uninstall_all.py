import sys

try:
    from .pkg_info import pip_pkg_info
    from .uninstall import uninstall_pkg
except:
    from pkg_info import pip_pkg_info
    from uninstall import uninstall_pkg

def remove_all(self_keep:bool=True):
    pkg_info = pip_pkg_info()
    white_list = ["pip"] # 保持不能删除的东西

    if self_keep:
        white_list.append("pip-pkg-info")

    # 统计总共需要删除多少个包，失败了多少个包
    total_cnt = 0
    fail_cnt = 0

    for term, details in sorted(pkg_info.items()):
        if term in white_list:
            continue

        total_cnt += 1
        
        try:
            uninstall_pkg(term)
        except Exception as e:
            sys.stderr.write(f"Unexpected exception happend when uninstalling {term}.")
            fail_cnt += 1
    
    if fail_cnt != 0:
        sys.stderr.write(f"Uninstalling total {total_cnt} packages, {fail_cnt} failed.")

if __name__ == "__main__":
    remove_all()
