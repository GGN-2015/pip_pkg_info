import sys

# 安全导入 tqdm，不存在则不使用进度条（不报错）
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

def remove_all(self_keep:bool=True):
    pkg_info = pip_pkg_info()
    white_list = ["pip"]  # 保持不能删除的基础包

    if self_keep:
        white_list.append("pip-pkg-info")
    
    # 关键：跳过卸载 tqdm 自身，避免进度条库被删导致异常
    if TQDM_AVAILABLE:
        white_list.append("tqdm")
        white_list.append("colorama")

    # 筛选出所有需要卸载的包列表
    uninstall_pkgs = []
    for term, details in sorted(pkg_info.items()):
        if term not in white_list:
            uninstall_pkgs.append(term)

    total_cnt = len(uninstall_pkgs)
    fail_cnt = 0

    # 使用 tqdm 进度条遍历卸载（有则用，无则普通循环）
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

    # 执行卸载
    for term in pkg_iter:
        try:
            uninstall_pkg(term)
        except Exception as e:
            # 进度条模式下不输出杂乱信息，保持进度条整洁
            if not TQDM_AVAILABLE:
                sys.stderr.write(f"Unexpected exception happened when uninstalling {term}.\n")
            fail_cnt += 1

    # 最终结果输出
    if fail_cnt != 0:
        sys.stderr.write(f"\nUninstalling total {total_cnt} packages, {fail_cnt} failed.\n")
    else:
        if TQDM_AVAILABLE:
            sys.stdout.write(f"\nAll {total_cnt} packages uninstalled successfully!\n")

if __name__ == "__main__":
    remove_all()