import sys
import time
import logging
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

# ---------- Global Settings ----------
pyautogui.FAILSAFE = True          
pyautogui.PAUSE = 0.25            

# Tune these to your liking
DEFAULT_TIMEOUT = 20               
DEFAULT_RETRY_EVERY = 0.5          
DEFAULT_CONFIDENCE = 0.9           
IMG_DIR = Path(__file__).parent / "images"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

# ---------- Helpers ----------
def wait_for_image(
    image_name: str,
    timeout: float = DEFAULT_TIMEOUT,
    confidence: float = DEFAULT_CONFIDENCE,
    region: Optional[Tuple[int,int,int,int]] = None
):
    """
    Block until an image appears on screen (returns Box) or timeout (returns None).
    `region` is (left, top, width, height) to speed up matches.
    """
    img_path = str(IMG_DIR / image_name)
    logging.info(f"Waiting for image: {image_name}")
    t0 = time.time()
    while time.time() - t0 < timeout:
        loc = pyautogui.locateOnScreen(img_path, confidence=confidence, region=region)
        if loc is not None:
            logging.info(f"Found {image_name} at {loc}")
            return loc
        time.sleep(DEFAULT_RETRY_EVERY)
    logging.error(f"Timed out waiting for {image_name}")
    return None


def click_image_center(
    image_name: str,
    timeout: float = DEFAULT_TIMEOUT,
    confidence: float = DEFAULT_CONFIDENCE,
    clicks: int = 1,
    interval: float = 0.1,
    button: str = "left",
    region: Optional[Tuple[int,int,int,int]] = None
):
    """Wait for image, then click its center."""
    loc = wait_for_image(image_name, timeout, confidence, region)
    if not loc:
        raise RuntimeError(f"Could not find image: {image_name}")
    x, y = pyautogui.center(loc)
    pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
    logging.info(f"Clicked {image_name} at ({x},{y})")


def click_coords(
    x: int, y: int,
    clicks: int = 1,
    interval: float = 0.1,
    button: str = "left"
):
    """Coordinate fallback if you cannot or don’t want to use templates."""
    pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
    logging.info(f"Clicked coords ({x},{y})")


def type_text(text: str, interval: float = 0.02):
    pyautogui.write(text, interval=interval)
    logging.info(f"Typed text: {text!r}")


def press(keys, interval: float = 0.05):
    """Press a single key or a sequence like ['ctrl','s']."""
    if isinstance(keys, (list, tuple)):
        pyautogui.hotkey(*keys, interval=interval)
        logging.info(f"Hotkey: {'+'.join(keys)}")
    else:
        pyautogui.press(keys)
        logging.info(f"Key: {keys}")


def ensure_window_in_front(app_image: Optional[str] = None, timeout: float = 10):
    """
    Best-effort: bring the app into focus by clicking a known element
    (e.g., its toolbar/logo) or using Alt+Tab/Cmd+Tab.
    """
    try:
        if app_image:
            click_image_center(app_image, timeout=timeout)
        else:
            if sys.platform == "darwin":
                press(['command', 'tab'])
            else:
                press(['alt', 'tab'])
        time.sleep(0.5)
        logging.info("Attempted to focus the app.")
    except Exception as e:
        logging.warning(f"Could not ensure window focus: {e}")



def run_flow(dry_run: bool = False):
    """
    Example: open a file via the app's menu, type into a field, save, and close.
    Replace image names with your own assets under ./images
    """
    logging.info("Starting automation flow" + (" (dry run)" if dry_run else ""))

    # 0) Safety: give yourself 2 seconds to wiggle the mouse to abort
    logging.info("You have 2 seconds to move the mouse to the top-left to abort.")
    time.sleep(2)

    if dry_run:
        logging.info("Dry run: not clicking or typing; only locating images.")
    
    # 1) Bring app to front via a known UI element (e.g., app_toolbar.png)
    ensure_window_in_front(app_image="app_toolbar.png")

    # 2) Open menu
    if dry_run:
        wait_for_image("menu_file.png")
    else:
        click_image_center("menu_file.png")

    # 3) Click 'Open…'
    if dry_run:
        wait_for_image("menu_open.png")
    else:
        click_image_center("menu_open.png")

    # 4) In file dialog: click filename field, type path, press Enter
    if dry_run:
        wait_for_image("file_name_field.png")
    else:
        click_image_center("file_name_field.png")
        type_text(r"C:\path\to\your\file.txt" if sys.platform.startswith("win") else "/Users/you/file.txt")
        press('enter')

    # 5) Wait for document body (e.g., editor_area.png) and type something
    if dry_run:
        wait_for_image("editor_area.png", timeout=30)
    else:
        click_image_center("editor_area.png", timeout=30)  # place caret
        type_text("Automated line 1\nAutomated line 2\n")
    
    # 6) Save (Ctrl/Cmd+S)
    if not dry_run:
        if sys.platform == "darwin":
            press(['command', 's'])
        else:
            press(['ctrl', 's'])

    # 7) Close the document (Ctrl/Cmd+W) and optionally confirm save dialogs
    if not dry_run:
        if sys.platform == "darwin":
            press(['command', 'w'])
        else:
            press(['ctrl', 'w'])
        # Example: confirm dialog
        try:
            click_image_center("dialog_ok.png", timeout=3, confidence=0.85)
        except Exception:
            pass

    logging.info("Flow complete.")


# ---------- Entry Point ----------
if __name__ == "__main__":
    # Usage: python automation.py [--dry]
    dry = "--dry" in sys.argv
    try:
        run_flow(dry_run=dry)
    except pyautogui.FailSafeException:
        logging.error("Fail-safe triggered (mouse moved to top-left). Exiting.")
    except Exception as e:
        logging.exception(f"Automation failed: {e}")
