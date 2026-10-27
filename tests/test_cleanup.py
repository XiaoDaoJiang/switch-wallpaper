import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import wallpaper_changer as changer


class CleanupTests(unittest.TestCase):
    def test_dates_protection_and_unrelated_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            names = ['bing_wallpaper_20260927.jpg', 'bing_wallpaper_20260928.jpg',
                     'bing_wallpaper_20261027.jpg', 'bing_wallpaper_20260101.jpg',
                     'bing_wallpaper_20260230.jpg', 'photo.jpg', 'wallpaper_changer.log']
            for name in names:
                (root / name).write_bytes(b'test')
            nested = root / 'nested'
            nested.mkdir()
            (nested / names[0]).write_bytes(b'test')
            changer.cleanup_old_wallpapers(folder, str(root / names[3]), date(2026, 10, 27))
            self.assertFalse((root / names[0]).exists())
            for name in names[1:]:
                self.assertTrue((root / name).exists(), name)
            self.assertTrue((nested / names[0]).exists())

    def test_delete_failure_does_not_interrupt(self):
        with tempfile.TemporaryDirectory() as folder:
            old = Path(folder) / 'bing_wallpaper_20200101.jpg'
            old.write_bytes(b'test')
            with patch.object(changer.os, 'remove', side_effect=PermissionError('locked')):
                changer.cleanup_old_wallpapers(folder, str(Path(folder) / 'current.jpg'))
            self.assertTrue(old.exists())

    def test_successful_paths_and_failed_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            current = Path(folder) / f"bing_wallpaper_{datetime.now():%Y%m%d}.jpg"
            current.write_bytes(b'test')
            with patch.object(changer, 'get_wallpaper_folder', return_value=folder), \
                 patch.object(changer, 'set_wallpaper', return_value=True), \
                 patch.object(changer, 'cleanup_old_wallpapers') as cleanup:
                changer.change_wallpaper()
                cleanup.assert_called_once_with(folder, str(current))
            with patch.object(changer, 'set_wallpaper', return_value=True), \
                 patch.object(changer, 'cleanup_old_wallpapers') as cleanup:
                changer.use_fallback_wallpaper(folder)
                cleanup.assert_called_once_with(folder, str(current))
            with patch.object(changer, 'set_wallpaper', return_value=False), \
                 patch.object(changer, 'cleanup_old_wallpapers') as cleanup:
                changer.use_fallback_wallpaper(folder)
                cleanup.assert_not_called()
            current.unlink()
            def download(path):
                Path(path).write_bytes(b'test')
                return True
            with patch.object(changer, 'get_wallpaper_folder', return_value=folder), \
                 patch.object(changer, 'download_bing_wallpaper', side_effect=download), \
                 patch('time.sleep'), \
                 patch.object(changer, 'set_wallpaper', return_value=True), \
                 patch.object(changer, 'cleanup_old_wallpapers') as cleanup:
                changer.change_wallpaper()
                cleanup.assert_called_once_with(folder, str(current))


if __name__ == '__main__':
    unittest.main()
