# -*- coding: utf-8 -*-
"""一键复现全部结果：按顺序执行 notebook 目录下的 4 个 notebook。

用法：
    python run_all.py                      # 顺序执行 01→04，任一失败立即停止
    python run_all.py --dry-run            # 只列出将要执行的 notebook，不运行
    python run_all.py --only 02            # 只执行编号 02 的 notebook（"2" 也认）
    python run_all.py --continue-on-error  # 某个失败后仍继续跑后面的
    python run_all.py --timeout 900        # 单个 cell 超时（秒），默认 1800

说明：
    - 只有执行成功的 notebook 才会写回 .ipynb（先写临时文件再原子替换）；
      执行失败时原文件保持不动，避免把已保存的图表输出覆盖成带报错的残缺版本。
    - 执行时 cwd 指向 notebook 所在目录，notebook 内部会向上查找含 data/ 的目录
      作为项目根，故不要求从项目根启动。
    - 论文 docx 不由本脚本生成（项目不保留 build/ 目录）。
    - 随机种子统一为 42（见各 notebook 首段），结果可复现。
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(os.getcwd()).resolve() 
FIG_DIR = ROOT / "outputs" / "figures"
TAB_DIR = ROOT / "outputs" / "tables"
EXPECT_FIGS = 27                            # fig01–fig27
NB_DIR_CANDIDATES = ("code")   

def find_nb_dir(explicit=None):
    if explicit:
        d = Path(explicit)
        d = d if d.is_absolute() else (ROOT / d)
        return d if d.is_dir() else None
    return ROOT / "code"

def match_only(name, only):
    keys = [only]
    if only.isdigit():
        keys.append(only.zfill(2))
    return any(name.startswith(k) for k in keys) or only in name


def check_deps():
    missing = []
    for mod in ("nbformat", "nbclient"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print("缺少依赖：%s" % "、".join(missing))
        print("请先执行：pip install -r requirements.txt")
        return False
    return True


def kernel_warning(name):
    try:
        from jupyter_client.kernelspec import KernelSpecManager
        specs = KernelSpecManager().find_kernel_specs()
    except Exception:                                          # noqa: BLE001
        return None
    if name in specs:
        return None
    return "未找到名为 %s 的 kernel（现有：%s）" % (name, "、".join(sorted(specs)) or "无")


def first_error_cell(nb):
    for i, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "error":
                return i
    return None


def run_notebook(path, timeout, kernel):
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(str(path), as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name=kernel,
        allow_errors=False,
        resources={"metadata": {"path": str(path.parent)}},
    )
    t0 = time.time()
    ok = True
    try:
        client.execute()
    except Exception as e:                                     # noqa: BLE001
        ok = False
        print("  [失败] %s: %s" % (type(e).__name__, str(e)[:1200]))
        idx = first_error_cell(nb)
        if idx is not None:
            print("  出错位置：第 %d 个 code cell（0 起计）" % idx)

    if ok:
        tmp = path.with_name(path.name + ".tmp")
        try:
            nbformat.write(nb, str(tmp))
            os.replace(str(tmp), str(path))
        finally:
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
    else:
        print("  原 notebook 未被改动：%s" % path.name)

    print("  %-6s %6.1fs  %s" % ("OK" if ok else "FAIL", time.time() - t0, path.name))
    return ok, time.time() - t0


def verify_outputs():
    figs = sorted(FIG_DIR.glob("fig*.png"))
    tabs = sorted(TAB_DIR.glob("*.csv")) + sorted(TAB_DIR.glob("*.json"))
    dash = ROOT / "outputs" / "dashboard"
    htmls = sorted(dash.glob("*.html")) if dash.is_dir() else []

    print("\n产出核对：")
    print("  图表 %2d 张  %s" % (len(figs), FIG_DIR))
    print("  结果表 %2d 个  %s" % (len(tabs), TAB_DIR))
    print("  大屏 %2d 个   %s" % (len(htmls), dash))

    nums = set()
    for p in figs:
        m = re.match(r"fig(\d{2})", p.name)
        if m:
            nums.add(int(m.group(1)))
    missing = [n for n in range(1, EXPECT_FIGS + 1) if n not in nums]
    if missing:
        head = "、".join("fig%02d" % n for n in missing[:6])
        print("  [提示] 缺 %d 张：%s%s" % (
            len(missing), head, " 等" if len(missing) > 6 else ""))
        if EXPECT_FIGS in missing:
            print("         fig27 是交互大屏截图，需本机装有 Chrome 或 Edge 才能生成。")
    else:
        print("  fig01–fig%02d 齐全。" % EXPECT_FIGS)


def main():
    ap = argparse.ArgumentParser(description="一键执行 Superstore 分析 notebook")
    ap.add_argument("--only", default=None, help="只执行指定编号，如 02（也认 2）")
    ap.add_argument("--dry-run", action="store_true", help="只列出待执行 notebook，不运行")
    ap.add_argument("--continue-on-error", action="store_true", help="失败后继续执行其余 notebook")
    ap.add_argument("--timeout", type=int, default=1800, help="单 cell 超时秒数，默认 1800")
    ap.add_argument("--kernel", default="python3", help="jupyter kernel 名称，默认 python3")
    ap.add_argument("--nb-dir", default=None, help="notebook 目录，默认自动识别 notebooks/ 或 code/")
    args = ap.parse_args()

    nb_dir = find_nb_dir(args.nb_dir)
    if nb_dir is None:
        print("找不到 notebook 目录（已尝试 notebooks/、code/）：", ROOT)
        return 1

    nbs = sorted(p for p in nb_dir.glob("*.ipynb")
                 if not p.name.startswith(".") and not p.name.endswith(".tmp"))
    if args.only:
        nbs = [p for p in nbs if match_only(p.name, args.only)]
    if not nbs:
        print("没有匹配的 notebook（目录：%s）。" % nb_dir)
        return 1

    print("项目根：", ROOT)
    print("notebook 目录：", nb_dir)
    print("待执行 %d 个 notebook（按文件名排序）" % len(nbs))
    for p in nbs:
        print("  -", p.name)

    if args.dry_run:
        print("\n--dry-run：未执行任何 notebook。")
        return 0

    if not check_deps():
        return 1

    warn = kernel_warning(args.kernel)
    if warn:
        print("\n[注意]", warn)

    print("")
    t_all = time.time()
    results = []
    for p in nbs:
        ok, cost = run_notebook(p, args.timeout, args.kernel)
        results.append((p.name, ok, cost))
        if not ok and not args.continue_on_error:
            print("\n已停止：%s 执行失败。修好后可只补跑它：--only %s"
                  % (p.name, p.name[:2]))
            break

    print("\n总耗时 %.1fs" % (time.time() - t_all))
    failed = [n for n, ok, _ in results if not ok]
    if failed:
        print("执行失败：", "、".join(failed))
        return 1

    done = {n for n, _, _ in results}
    skipped = [p.name for p in nbs if p.name not in done]
    if skipped:
        print("未执行（因前序失败）：", "、".join(skipped))
        return 1

    verify_outputs()
    return 0


if __name__ == "__main__":
    sys.exit(main())
