"""Antigravity 中文界面补丁：Windows / 2.34.0，标准库实现。"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

VERSION = '0.1.0'
APP_VERSION = '2.34.0'
# Only the original archive actually verified during development is accepted.
SUPPORTED_SHA256 = '8934adef0622c9271c92eea950a71848764a66f7b10023ccbd82e54b959adb0e'
MARKER = b'\n// ANTIGRAVITY_ZH_LOCAL_V1\n'
ENTRY = 'dist/preload.js'


class PatchError(Exception):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unpack(data: bytes):
    try:
        if len(data) < 16:
            raise ValueError('short header')
        size_len, header_size, payload_size, json_size = struct.unpack('<4I', data[:16])
        if size_len != 4 or payload_size + 4 != header_size or not 0 < json_size <= payload_size - 4:
            raise ValueError('invalid header')
        base = 8 + header_size
        if base > len(data):
            raise ValueError('header out of bounds')
        tree = json.loads(data[16:16+json_size])
        if not isinstance(tree.get('files'), dict):
            raise ValueError('invalid file tree')
        return tree, base
    except (ValueError, TypeError, KeyError, struct.error, UnicodeError) as exc:
        raise PatchError('程序归档格式不受支持，未修改任何文件。') from exc


def entries(tree, prefix=''):
    for name, value in tree.get('files', {}).items():
        path = prefix + name
        if 'files' in value:
            yield from entries(value, path+'/')
        elif 'offset' in value:
            yield path, value


def contents(data, tree, base):
    result = {}
    for name, info in entries(tree):
        offset, size = int(info['offset']), int(info['size'])
        if offset < 0 or size < 0 or base + offset + size > len(data):
            raise PatchError('归档文件范围校验失败。')
        result[name] = data[base+offset:base+offset+size]
    return result


def build(original, script):
    if sha(original) != SUPPORTED_SHA256:
        raise PatchError('此安装包的版本或构建校验值不在支持列表中。为避免误改，已停止。')
    tree, base = unpack(original)
    files = contents(original, tree, base)
    package = json.loads(files['package.json'])
    if package.get('name') != 'antigravity' or package.get('version') != APP_VERSION:
        raise PatchError('仅支持已验证的 Antigravity 2.34.0 构建。')
    if MARKER in files[ENTRY]:
        raise PatchError('原始归档已包含补丁，无法重复添加。')
    changed = files[ENTRY] + MARKER + script
    patched = copy.deepcopy(tree)
    bodies, offset = [], 0
    for name, info in entries(patched):
        payload = changed if name == ENTRY else files[name]
        info['offset'], info['size'] = str(offset), len(payload)
        if name == ENTRY and 'integrity' in info:
            block = info['integrity'].get('blockSize', 4194304)
            info['integrity'] = {
                'algorithm': 'SHA256', 'hash': sha(payload), 'blockSize': block,
                'blocks': [sha(payload[i:i+block]) for i in range(0, len(payload), block)]}
        bodies.append(payload)
        offset += len(payload)
    header = json.dumps(patched, ensure_ascii=False, separators=(',', ':')).encode()
    padding = b'\0' * (-len(header) % 4)
    payload_size = 4 + len(header) + len(padding)
    output = (struct.pack('<4I', 4, 4+payload_size, payload_size, len(header))
              + header + padding + b''.join(bodies))
    new_tree, new_base = unpack(output)
    check = contents(output, new_tree, new_base)
    if set(check) != set(files) or check[ENTRY] != changed:
        raise PatchError('补丁构建校验失败。')
    if any(check[p] != body for p, body in files.items() if p != ENTRY):
        raise PatchError('检测到翻译脚本之外的文件发生变化，已停止。')
    return output, len(files)-1


def atomic_write(path: Path, data: bytes):
    # Same-directory temp + replace: a failed write leaves the original intact.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.agy-zh-', dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def script_bytes():
    return Path(__file__).with_name('ui-zh-cn.js').read_bytes()


def find_target(app_dir=None):
    if app_dir:
        candidate = Path(app_dir).expanduser().resolve() / 'resources' / 'app.asar'
        if not candidate.is_file():
            raise PatchError('--app-dir 必须指向包含 Antigravity.exe 和 resources 的安装目录。')
        if not (candidate.parent.parent/'Antigravity.exe').is_file():
            raise PatchError('选定目录没有 Antigravity.exe。')
        return candidate
    candidates = []
    for env, suffix in [('LOCALAPPDATA', 'Programs/antigravity'),
                        ('ProgramFiles', 'Antigravity'), ('ProgramFiles(x86)', 'Antigravity')]:
        root = os.environ.get(env)
        if root:
            path = Path(root)/suffix/'resources/app.asar'
            if path.is_file() and path not in candidates:
                candidates.append(path.resolve())
    if len(candidates) != 1:
        raise PatchError('未找到唯一安装目录。请通过 --app-dir "安装目录" 手动指定。')
    return candidates[0]


def state_path(target):
    root = os.environ.get('LOCALAPPDATA')
    if not root:
        raise PatchError('无法定位本地备份目录。')
    identity = hashlib.sha256(str(target.resolve()).casefold().encode()).hexdigest()[:20]
    return Path(root)/'AntigravityZhPatch'/'backups'/identity


def ensure_closed():
    if sys.platform != 'win32':
        raise PatchError('此版本仅支持 Windows。')
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Antigravity.exe', '/FO', 'CSV', '/NH'],
        capture_output=True, timeout=15,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        raise PatchError('无法检查 Antigravity 是否退出，未修改文件。')
    if b'"antigravity.exe"' in result.stdout.lower():
        raise PatchError('请先完全退出 Antigravity，然后重试。不会自动结束你的进程。')


def install(target, state, script, dry_run=False):
    original = target.read_bytes()
    tree, base = unpack(original)
    files = contents(original, tree, base)
    if ENTRY not in files:
        raise PatchError('未找到预期的界面预加载文件。')
    if MARKER in files[ENTRY]:
        manifest = state/'manifest.json'
        if manifest.is_file():
            record = json.loads(manifest.read_text('utf-8'))
            if record.get('patched_sha256') == sha(original):
                return '此补丁已安装，无需重复安装。'
        raise PatchError('检测到其他或旧版汉化补丁。请先用原补丁的恢复工具还原，再安装。')
    output, unchanged = build(original, script)
    if dry_run:
        return f'预检查通过：仅更改 {ENTRY}，其余 {unchanged} 个文件内容一致。未写入文件。'
    state.mkdir(parents=True, exist_ok=True)
    backup = state/'app.asar.original'
    if backup.exists() and sha(backup.read_bytes()) != sha(original):
        raise PatchError('已有不同的备份，已停止，避免覆盖。')
    atomic_write(backup, original)
    if sha(backup.read_bytes()) != sha(original):
        raise PatchError('原始备份校验失败，未替换程序。')
    record = {'patch_version': VERSION, 'app_version': APP_VERSION,
              'original_sha256': sha(original), 'patched_sha256': sha(output),
              'script_sha256': sha(script), 'unchanged_entries': unchanged}
    atomic_write(state/'manifest.json', json.dumps(record, indent=2).encode())
    # Recheck after preparing backup; do not overwrite a concurrent app update.
    if target.read_bytes() != original:
        raise PatchError('准备期间程序文件发生变化，已停止。')
    atomic_write(target, output)
    if sha(target.read_bytes()) != sha(output):
        raise PatchError('安装后的文件校验失败，请保留备份并运行恢复操作。')
    return f'中文补丁安装成功！请重新打开 Antigravity。\n原始备份：{state}\n如果有帮助，欢迎给 GitHub 仓库点一个 Star ⭐。'


def restore(target, state):
    backup, manifest = state/'app.asar.original', state/'manifest.json'
    if not backup.is_file() or not manifest.is_file():
        raise PatchError('没有找到本工具生成的备份，无法自动恢复。')
    record = json.loads(manifest.read_text('utf-8'))
    original = backup.read_bytes()
    if sha(original) != record['original_sha256']:
        raise PatchError('备份校验失败，未修改程序。')
    current = target.read_bytes()
    if sha(current) == record['original_sha256']:
        return '已经是原始版本，无需恢复。'
    if sha(current) != record['patched_sha256']:
        raise PatchError('程序已更新或被其他工具修改，拒绝用旧备份覆盖。')
    atomic_write(target, original)
    if sha(target.read_bytes()) != record['original_sha256']:
        raise PatchError('恢复后校验失败。请保留备份。')
    return '已恢复原始英文程序，校验一致。请重新打开 Antigravity。备份继续保留。'


def status(target, state):
    current = target.read_bytes()
    tree, base = unpack(current)
    files = contents(current, tree, base)
    patched = MARKER in files.get(ENTRY, b'')
    return (f'程序归档：{target}\n'
            f'检测到本系列汉化标记：{"是" if patched else "否"}\n'
            f'归档 SHA-256：{sha(current)}\n'
            f'原版构建受支持：{"是" if sha(current)==SUPPORTED_SHA256 else "否（也可能已安装补丁）"}\n'
            f'恢复备份：{"存在" if (state/"app.asar.original").is_file() else "不存在"}')


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', nargs='?', choices=['install', 'restore', 'status'])
    parser.add_argument('--app-dir', help='Antigravity.exe 所在目录')
    parser.add_argument('--dry-run', action='store_true', help='安装预检查，不写入任何文件')
    parser.add_argument('--version', action='version', version=VERSION)
    args = parser.parse_args()
    interactive = args.action is None
    code = 0
    try:
        action = args.action
        if interactive:
            print(f'Antigravity 中文界面补丁 v{VERSION}\n仅支持 Windows / 已验证的 2.34.0 构建\n')
            print('1. 安装中文补丁\n2. 恢复英文原版\n3. 检查状态\n0. 退出\n')
            choice = input('请输入选项：').strip()
            if choice == '0':
                return 0
            action = {'1':'install', '2':'restore', '3':'status'}.get(choice)
            if not action:
                raise PatchError('无效选项。')
        if args.dry_run and action != 'install':
            raise PatchError('--dry-run 仅适用于 install。')
        target = find_target(args.app_dir)
        state = state_path(target)
        if action != 'status' and not args.dry_run:
            ensure_closed()
        if action == 'install':
            print(install(target, state, script_bytes(), args.dry_run))
        elif action == 'restore':
            print(restore(target, state))
        else:
            print(status(target, state))
    except (PatchError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f'操作未完成：{exc}', file=sys.stderr)
        code = 1
    except (EOFError, KeyboardInterrupt):
        code = 1
    if interactive:
        try:
            input('\n按 Enter 关闭窗口…')
        except (EOFError, KeyboardInterrupt):
            pass
    return code


if __name__ == '__main__':
    sys.exit(main())
