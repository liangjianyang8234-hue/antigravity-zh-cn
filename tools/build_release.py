"""Build on Windows x64 with the project's build dependencies installed."""
from pathlib import Path
import hashlib
import importlib.metadata
import platform
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0'
NAME = f'Antigravity-ZH-CN-v{VERSION}-windows-x64'


def main():
    if sys.platform != 'win32' or platform.machine().lower() not in ('amd64','x86_64'):
        raise SystemExit('Build this release on Windows x64.')
    output = ROOT/'release'
    bundle = output/NAME
    bundle.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onefile','--console',
        '--name','Antigravity-ZH-CN','--distpath',str(output/'bin'),
        '--workpath',str(ROOT/'build/pyinstaller'),'--specpath',str(ROOT/'build'),
        '--add-data',str(ROOT/'src/ui-zh-cn.js')+';.',str(ROOT/'src/patcher.py'),
    ],check=True,cwd=ROOT)
    shutil.copy2(output/'bin/Antigravity-ZH-CN.exe',bundle/'Antigravity-ZH-CN.exe')
    for name in ['README.md','LICENSE','CHANGELOG.md']:
        shutil.copy2(ROOT/name,bundle/name)
    (bundle/'使用说明.txt').write_text(
        'Antigravity 中文界面补丁 v'+VERSION+'\n\n'
        '仅限 Windows x64 / 已验证的 Antigravity 2.34.0 构建。\n'
        '完全退出 Antigravity，双击 Antigravity-ZH-CN.exe。\n'
        '输入 1 安装，输入 2 恢复英文，输入 3 检查状态。无需安装 Python。\n'
        '请阅读 README.md 的支持范围与备份说明。\n'
        '本工具是非官方补丁，部分文案仍可能为英文。\n'
        '觉得实用，欢迎给你下载此工具的 GitHub 仓库点 Star ⭐！\n',encoding='utf-8')
    licenses = bundle/'licenses'
    licenses.mkdir(exist_ok=True)
    python_license = Path(sys.base_prefix)/'LICENSE.txt'
    if not python_license.is_file():
        raise SystemExit('CPython LICENSE.txt not found; refusing to publish without notices.')
    shutil.copy2(python_license,licenses/'CPython-LICENSE.txt')
    distribution = importlib.metadata.distribution('pyinstaller')
    count = 0
    for item in distribution.files or []:
        if item.name in ('COPYING.txt','LICENSE','LICENSE.txt'):
            path = Path(distribution.locate_file(item))
            if path.is_file():
                shutil.copy2(path,licenses/('PyInstaller-'+path.name))
                count += 1
    if not count:
        raise SystemExit('PyInstaller license not found; refusing to publish without notices.')
    (licenses/'NOTICE.txt').write_text(
        'The executable bundles CPython and the PyInstaller bootloader.\n'
        'See included license texts. The patch source uses the repository MIT license.\n'
        'Antigravity itself is not included.\n',encoding='utf-8')
    archive = output/(NAME+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as handle:
        for file in sorted(bundle.rglob('*')):
            if file.is_file():
                handle.write(file,Path(NAME)/file.relative_to(bundle))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n',encoding='ascii')
    print(f'Release: {archive}\nSHA-256: {digest}')


if __name__=='__main__':
    main()
