import sys
import time


def test_ansi():
    # Colors
    print("\033[31mRed Text\033[0m")
    print("\033[32mGreen Text\033[0m")
    print("\033[33mYellow Text\033[0m")
    print("\033[34mBlue Text\033[0m")
    print("\033[35mMagenta Text\033[0m")
    print("\033[36mCyan Text\033[0m")
    print("\033[37mWhite Text\033[0m")

    # Bright Colors
    print("\033[91mBright Red Text\033[0m")
    print("\033[92mBright Green Text\033[0m")
    print("\033[93mBright Yellow Text\033[0m")
    print("\033[94mBright Blue Text\033[0m")
    print("\033[95mBright Magenta Text\033[0m")
    print("\033[96mBright Cyan Text\033[0m")
    print("\033[97mBright White Text\033[0m")

    # Background Colors
    print("\033[41mRed Background\033[0m")
    print("\033[42mGreen Background\033[0m")
    print("\033[101mBright Red Background\033[0m")

    # Styles
    print("\033[1mBold Text\033[0m")
    print("\033[3mItalic Text\033[0m")
    print("\033[4mUnderlined Text\033[0m")

    # Combined
    print("\033[1;31;42mBold Red on Green Background\033[0m")

    # Cursor movement and clearing (basic)
    print("This will be cleared in 1 second...")
    sys.stdout.flush()
    time.sleep(1)
    print("\033[1A\033[KCleared line above!")


if __name__ == "__main__":
    test_ansi()
