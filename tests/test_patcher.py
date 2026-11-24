import importlib.util
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('patcher', ROOT/'src/patcher.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def archive(version='2.34.0'):
    files = {
        'package.json': json.dumps({'name':'antigravity','version':version}).encode(),
        'dist/preload.js': b'// original bridge\n',
        'dist/keep.js': b'function originalFeature() {return 42;}\n',
    }
    tree, offset, bodies = {'files':{}}, 0, []
    for name, body in files.items():
        node = tree
        parts = name.split('/')
        for part in parts[:-1]:
            node = node['files'].setdefault(part, {'files':{}})
        node['files'][parts[-1]] = {'offset':str(offset),'size':len(body),
            'integrity':{'algorithm':'SHA256','hash':p.sha(body),'blockSize':4194304,'blocks':[p.sha(body)]}}
        offset += len(body)
        bodies.append(body)
    header = json.dumps(tree).encode()
    padding = b'\0' * (-len(header)%4)
    n = 4+len(header)+len(padding)
    return struct.pack('<4I',4,n+4,n,len(header))+header+padding+b''.join(bodies)


class PatcherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name)/'app.asar'
        self.state = Path(self.tmp.name)/'backups'
        self.original = archive()
        self.target.write_bytes(self.original)
        self.support = patch.object(p,'SUPPORTED_SHA256',p.sha(self.original))
        self.support.start()
        self.addCleanup(self.support.stop)

    def test_roundtrip_and_other_entries_unchanged(self):
        output, count = p.build(self.original, b'// translation')
        self.assertEqual(count, 2)
        old = p.contents(self.original,*p.unpack(self.original))
        new = p.contents(output,*p.unpack(output))
        self.assertEqual(set(old),set(new))
        self.assertEqual(new['dist/keep.js'], old['dist/keep.js'])
        self.assertEqual(new['package.json'], old['package.json'])
        self.assertEqual(new[p.ENTRY],old[p.ENTRY]+p.MARKER+b'// translation')
        p.install(self.target,self.state,b'// translation')
        p.restore(self.target,self.state)
        self.assertEqual(self.target.read_bytes(),self.original)

    def test_dry_run_leaves_no_backup_or_changes(self):
        p.install(self.target,self.state,b'// translation',True)
        self.assertEqual(self.target.read_bytes(),self.original)
        self.assertFalse(self.state.exists())

    def test_repeated_install_does_not_append_again(self):
        p.install(self.target,self.state,b'// translation')
        installed = self.target.read_bytes()
        p.install(self.target,self.state,b'// translation')
        self.assertEqual(self.target.read_bytes(),installed)

    def test_unknown_build_is_rejected(self):
        self.target.write_bytes(self.original+b'unknown build')
        before = self.target.read_bytes()
        with self.assertRaises(p.PatchError):
            p.install(self.target,self.state,b'// translation')
        self.assertEqual(self.target.read_bytes(),before)
        self.assertFalse(self.state.exists())

    def test_wrong_version_even_with_allowlisted_hash(self):
        data = archive('9.0.0')
        with patch.object(p,'SUPPORTED_SHA256',p.sha(data)):
            with self.assertRaises(p.PatchError):
                p.build(data,b'// translation')

    def test_restore_refuses_to_overwrite_updated_app(self):
        p.install(self.target,self.state,b'// translation')
        self.target.write_bytes(b'newer application')
        with self.assertRaises(p.PatchError):
            p.restore(self.target,self.state)
        self.assertEqual(self.target.read_bytes(),b'newer application')

    def test_restore_rejects_corrupt_backup(self):
        p.install(self.target,self.state,b'// translation')
        before = self.target.read_bytes()
        (self.state/'app.asar.original').write_bytes(b'corrupt')
        with self.assertRaises(p.PatchError):
            p.restore(self.target,self.state)
        self.assertEqual(self.target.read_bytes(),before)

    def test_unmanaged_patch_requires_old_restore_tool(self):
        result,_ = p.build(self.original,b'// translation')
        self.target.write_bytes(result)
        with self.assertRaises(p.PatchError):
            p.install(self.target,self.state,b'// translation')
        self.assertFalse(self.state.exists())

    def test_atomic_replace_failure_keeps_original(self):
        with patch.object(p.os,'replace',side_effect=PermissionError('locked')):
            with self.assertRaises(PermissionError):
                p.atomic_write(self.target,b'changed')
        self.assertEqual(self.target.read_bytes(),self.original)
        self.assertEqual(list(self.target.parent.glob('.agy-zh-*')),[])

    def test_running_process_blocks_mutation(self):
        completed = type('Result',(),{'returncode':0,'stdout':b'"Antigravity.exe","123"'})()
        with patch.object(p.sys,'platform','win32'), patch.object(p.subprocess,'run',return_value=completed):
            with self.assertRaises(p.PatchError):
                p.ensure_closed()

    def test_invalid_archive_is_rejected(self):
        with self.assertRaises(p.PatchError):
            p.unpack(b'not an archive')

    @unittest.skipUnless(os.environ.get('AGY_TEST_ORIGINAL'),'Optional: provide a local original archive')
    def test_real_archive_roundtrip_in_temporary_directory(self):
        original = Path(os.environ['AGY_TEST_ORIGINAL']).read_bytes()
        with patch.object(p,'SUPPORTED_SHA256','8934adef0622c9271c92eea950a71848764a66f7b10023ccbd82e54b959adb0e'):
            self.target.write_bytes(original)
            output,count = p.build(original,(ROOT/'src/ui-zh-cn.js').read_bytes())
            self.assertEqual(count,788)
            p.install(self.target,self.state,(ROOT/'src/ui-zh-cn.js').read_bytes())
            self.assertEqual(self.target.read_bytes(),output)
            p.restore(self.target,self.state)
            self.assertEqual(self.target.read_bytes(),original)


if __name__=='__main__':
    unittest.main()
