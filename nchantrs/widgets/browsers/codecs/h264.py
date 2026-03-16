# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, expandvars, expanduser
import datetime as dt

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
import os

import requests
import bz2
import hashlib
from pathlib import Path
from typing import Optional, Tuple
import ctypes
import platform
from typing import Optional
import os
import platform
import requests
import bz2
import tempfile
import ctypes
from pathlib import Path
from typing import Optional, Tuple

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class OpenH264Downloader:
    """Handles runtime downloading and extraction of OpenH264 codec."""

    BASE_URL = "http://ciscobinary.openh264.org/"
    VERSION = "2.5.1"

    def __init__(self, app_data_dir: Optional[str] = None):
        """Initialize OpenH264Downloader."""
        self.app_name = "nchantdoffice"  # None
        self.app_data_dir = Path(app_data_dir or self._get_app_data_dir())
        self.codec_dir = self.app_data_dir / "openh264"
        self.codec_dir.mkdir(parents=True, exist_ok=True)

    def _get_app_data_dir(self) -> str:
        """Get platform-specific application data directory."""
        system = platform.system().lower()
        if system == "windows":
            return expandvars(rf"%APPDATA%\{self.app_name}")
        elif system == "darwin":
            return expanduser(f"~/Library/Application Support/{self.app_name}")
        else:  # Linux and others
            return expanduser(f"~/.local/share/{self.app_name}")

    def _get_platform_info(self) -> Tuple[str, str]:
        """Determine platform-specific binary name and file extension."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "windows":
            arch = "win64" if machine in ("amd64", "x86_64") else "win32"
            ext = "dll"
        elif system == "darwin":
            arch = "osx64"
            ext = "dylib"
        elif system == "linux":
            if machine in ("amd64", "x86_64"):
                arch = "linux64"
            elif machine in ("aarch64", "arm64"):
                arch = "linuxarm64"
            else:
                arch = "linux32"
            ext = "so"
        else:
            raise OSError(f"Unsupported platform: {system}")

        return arch, ext

    def _get_binary_url_and_filename(self) -> Tuple[str, str, str]:
        """Get download URL and filenames for the current platform."""
        arch, ext = self._get_platform_info()
        if platform.system().lower() == "windows":
            filename = f"openh264-{self.VERSION}-{arch}.7.{ext}"
        else:
            filename = f"libopenh264-{self.VERSION}-{arch}.7.{ext}"
        compressed_filename = f"{filename}.bz2"
        url = f"{self.BASE_URL}{compressed_filename}"
        return url, compressed_filename, filename

    def download_and_extract(self) -> str:
        """Download and extract OpenH264 binary. Returns path to extracted file."""
        url, compressed_filename, filename = self._get_binary_url_and_filename()
        compressed_path = self.codec_dir / compressed_filename
        extracted_path = self.codec_dir / filename
        # Check if already downloaded and extracted
        if extracted_path.exists():
            logma.info(f"OpenH264 already exists at: {extracted_path}")
            return str(extracted_path)
        logma.info(f"Downloading OpenH264 from: {url}")
        try:
            # Download compressed binary
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(compressed_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logma.info(f"Downloaded to: {compressed_path}")
            # Extract bz2 file
            with bz2.BZ2File(compressed_path, "rb") as src, open(extracted_path, "wb") as dst:
                dst.write(src.read())
            logma.info(f"Extracted to: {extracted_path}")
            # Make executable on Unix systems
            if platform.system().lower() != "windows":
                os.chmod(extracted_path, 0o755)
            # Clean up compressed file
            compressed_path.unlink()
            return str(extracted_path)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to download OpenH264: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract OpenH264: {e}")

    def is_available(self) -> bool:
        """Check if OpenH264 is available locally."""
        _, _, filename = self._get_binary_url_and_filename()
        return (self.codec_dir / filename).exists()

    def get_library_path(self) -> Optional[str]:
        """Get path to OpenH264 library if available."""
        if self.is_available():
            _, _, filename = self._get_binary_url_and_filename()
            return str(self.codec_dir / filename)
        return None

    def test(self):
        """"""
        if self.is_available():
            logma.info("OpenH264 is available locally")
            return True
        else:
            logma.info("OpenH264 is not available locally")
        return False


class OpenH264Loader:
    """Manual OpenH264 library loader for advanced usage."""

    def __init__(self, library_path: str):
        self.library_path = library_path
        self.library: Optional[ctypes.CDLL] = None

    def load_library(self) -> bool:
        """Load OpenH264 library manually."""
        try:
            if platform.system().lower() == "windows":
                self.library = ctypes.CDLL(self.library_path)
            else:
                self.library = ctypes.CDLL(self.library_path)
            # Verify essential functions exist
            if hasattr(self.library, "WelsCreateDecoder") and hasattr(self.library, "WelsCreateEncoder"):
                logma.info(f"OpenH264 library loaded successfully: {self.library_path}")
                return True
            else:
                logma.info("OpenH264 library loaded but missing expected functions")
                return False
        except OSError as e:
            logma.info(f"Failed to load OpenH264 library: {e}")
            return False

    def is_loaded(self) -> bool:
        """Check if library is loaded."""
        return self.library is not None

    def get_version(self) -> Optional[str]:
        """Get OpenH264 version if available."""
        if not self.is_loaded():
            return None
        try:
            # This is a simplified version - actual implementation would need proper C structures
            return "OpenH264 loaded"
        except Exception:
            return None


class OpenH264Manager:
    """Manages OpenH264 codec downloading and integration for QWebEngineView."""

    BASE_URL = "http://ciscobinary.openh264.org/"
    VERSION = "2.5.1"

    def __init__(self, app_instance):
        self.app = app_instance
        self.app_data_dir = self._get_app_data_dir()
        self.codec_dir = self.app_data_dir / "codecs" / "openh264"
        self.codec_dir.mkdir(parents=True, exist_ok=True)

    def download_and_setup(self) -> Optional[str]:
        """Download and setup OpenH264 codec. Returns library path on success."""
        if self.is_codec_available():
            return self.get_library_path()

        try:
            url, compressed_filename, filename = self._get_binary_info()

            print(f"Downloading OpenH264 from: {url}")

            # Download to temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix=".bz2") as tmp_file:
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()

                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rDownloading: {percent:.1f}%", end="")

                tmp_path = tmp_file.name

            print("\nExtracting...")

            # Extract to final location
            final_path = self.codec_dir / filename

            with bz2.BZ2File(tmp_path, "rb") as src, open(final_path, "wb") as dst:
                dst.write(src.read())

            # Make executable on Unix systems
            if platform.system().lower() != "windows":
                os.chmod(final_path, 0o755)

            # Clean up temporary file
            os.unlink(tmp_path)

            # Verify the library can be loaded
            if self._verify_library_linux(final_path):
                print(f"OpenH264 extracted and verified: {final_path}")
                self._setup_linux_integration(final_path)
                return str(final_path)
            else:
                print("OpenH264 library verification failed")
                return None

        except Exception as e:
            print(f"Failed to download/setup OpenH264: {e}")
            return None

    def get_library_path(self) -> Optional[str]:
        """Get path to codec library if available."""
        if self.is_codec_available():
            _, _, filename = self._get_binary_info()
            return str(self.codec_dir / filename)
        return None

    def is_codec_available(self) -> bool:
        """Check if codec is already downloaded and available."""
        _, _, filename = self._get_binary_info()
        library_path = self.codec_dir / filename
        return library_path.exists() and library_path.stat().st_size > 0

    def _get_app_data_dir(self) -> Path:
        """Get application-specific data directory."""
        if self.app and hasattr(self.app, "slug"):
            app_name = self.app.slug
        else:
            app_name = "nchantdoffice"  # Use your actual app name from the logs

        system = platform.system().lower()
        if system == "windows":
            base_dir = os.path.expandvars(r"%APPDATA%")
        elif system == "darwin":
            base_dir = os.path.expanduser("~/Library/Application Support")
        else:  # Linux and others
            base_dir = os.path.expanduser("~/.local/share")

        return Path(base_dir) / app_name

    def _get_binary_info(self) -> Tuple[str, str, str]:
        """Get download URL and filenames for current platform."""
        arch, ext = self._get_platform_info()

        if platform.system().lower() == "windows":
            filename = f"openh264-{self.VERSION}-{arch}.{ext}"
        else:
            filename = f"libopenh264-{self.VERSION}-{arch}.{ext}"

        compressed_filename = f"{filename}.bz2"
        url = f"{self.BASE_URL}{compressed_filename}"

        return url, compressed_filename, filename

    def _get_platform_info(self) -> Tuple[str, str]:
        """Determine platform-specific binary name and extension."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "linux":
            if machine in ("amd64", "x86_64"):
                arch = "linux64"
            elif machine in ("aarch64", "arm64"):
                arch = "linuxarm64"
            else:
                arch = "linux32"
            ext = "so"
        elif system == "windows":
            arch = "win64" if machine in ("amd64", "x86_64") else "win32"
            ext = "dll"
        elif system == "darwin":
            arch = "osx64"
            ext = "dylib"
        else:
            raise OSError(f"Unsupported platform: {system}")

        return arch, ext

    def _setup_linux_integration(self, library_path: str):
        """Setup Linux-specific codec integration."""
        try:
            # Create GStreamer plugin cache entry if directory exists
            gst_plugin_dirs = [
                Path.home() / ".cache" / "gstreamer-1.0",
                Path("/usr/lib/x86_64-linux-gnu/gstreamer-1.0"),
                Path("/usr/local/lib/gstreamer-1.0"),
            ]

            for plugin_dir in gst_plugin_dirs:
                if plugin_dir.exists() and os.access(plugin_dir.parent, os.W_OK):
                    try:
                        symlink_path = plugin_dir / "libopenh264.so"
                        if not symlink_path.exists():
                            os.symlink(library_path, symlink_path)
                            print(f"Created GStreamer plugin symlink: {symlink_path}")
                            break
                    except (OSError, PermissionError):
                        continue

            # Set LD_LIBRARY_PATH to include our codec directory
            codec_dir_str = str(self.codec_dir)
            current_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
            if codec_dir_str not in current_ld_path:
                new_ld_path = f"{codec_dir_str}:{current_ld_path}" if current_ld_path else codec_dir_str
                os.environ["LD_LIBRARY_PATH"] = new_ld_path
                print(f"Updated LD_LIBRARY_PATH: {new_ld_path}")

        except Exception as e:
            print(f"Linux integration setup failed (non-fatal): {e}")

    def _verify_library_linux(self, library_path: str) -> bool:
        """Verify OpenH264 library on Linux."""
        try:
            # Use ldd to check library dependencies
            import subprocess

            result = subprocess.run(["ldd", library_path], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"ldd check failed: {result.stderr}")
                return False

            # Check for unresolved dependencies
            if "not found" in result.stdout:
                print("Warning: Some dependencies not found:")
                print(result.stdout)
                # Continue anyway, might still work

            # Try to load with ctypes
            lib = ctypes.CDLL(library_path)

            # Check for essential functions
            required_functions = ["WelsCreateDecoder", "WelsCreateEncoder"]
            for func_name in required_functions:
                if not hasattr(lib, func_name):
                    print(f"Missing function {func_name}")
                    return False

            print("Library verification successful")
            return True

        except Exception as e:
            print(f"Library verification failed: {e}")
            return False


# Usage in your application:
def setup_advanced_codec(downloader: OpenH264Downloader):
    """Setup codec with manual loading verification."""
    if not downloader.is_available():
        library_path = downloader.download_and_extract()
    else:
        library_path = downloader.get_library_path()
    loader = OpenH264Loader(library_path)
    if loader.load_library():
        print("Advanced OpenH264 setup complete")
        return True
    else:
        print("Advanced OpenH264 setup failed")
        return False


def test_h264_playback():
    """Test H.264 video playback with a simple test page."""
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>H.264 Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            video { border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>H.264 Video Test</h1>
        <video width="640" height="360" controls preload="metadata">
            <source src="https://sample-videos.com/zip/10/mp4/mp4-480x270/SampleVideo_480x270_1mb.mp4" type="video/mp4">
            <p>Your browser does not support H.264 video.</p>
        </video>

        <div id="test-results"></div>

        <script>
            const video = document.querySelector('video');
            const results = document.getElementById('test-results');

            // Test codec support
            const h264Support = video.canPlayType('video/mp4; codecs="avc1.42E01E"');
            results.innerHTML = '<h2>Codec Support Test:</h2><p>H.264 Support: ' + h264Support + '</p>';

            // Add event listeners
            video.addEventListener('loadstart', () => console.log('Load started'));
            video.addEventListener('loadeddata', () => console.log('Data loaded'));
            video.addEventListener('canplay', () => console.log('Can play'));
            video.addEventListener('error', (e) => console.error('Video error:', e));

            console.log('Video test page loaded');
        </script>
    </body>
    </html>
    """

    # Use this HTML in one of your web views to test
    return test_html


def main():
    """Main application entry point."""
    # Set environment variables before creating QApplication
    setup_advanced_codec(OpenH264Downloader())


if __name__ == "__main__":
    main()

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
