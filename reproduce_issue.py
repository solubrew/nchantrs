import sys
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser


def test_browser():
    app = pyqt.QApplication(sys.argv)
    browser = NchantdWebBrowser()
    browser.initWidget("https://www.google.com")
    browser.show()

    print("Browser initialized successfully")
    # We don't actually run the exec_() because we are in a headless/non-interactive env
    # but we checked that it can be instantiated and initialized.
    return True


if __name__ == "__main__":
    try:
        test_browser()
        print("Test passed")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
