import sys
import time
import logging
from pathlib import Path
from typing import Optional, Tuple
import pyautogui

pyautogui.FAILSAFE = True            
pyautogui.PAUSE = 0.20

DEFAULT_TIMEOUT = 25                
DEFAULT_RETRY_EVERY = 0.5
DEFAULT_CONFIDENCE = 0.88           
IMG_DIR = Path(__file__).parent / "images"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

def wait_for_image(name, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE,
                   region: Optional[Tuple[int,int,int,int]] = None):
    p = str(IMG_DIR / name)
    t0 = time.time()
    while time.time() - t0 < timeout:
        box = pyautogui.locateOnScreen(p, confidence=confidence, region=region)
        if box:
            return box
        time.sleep(DEFAULT_RETRY_EVERY)
    return None

def click_image(name, timeout=DEFAULT_TIMEOUT, confidence=DEFAULT_CONFIDENCE,
                clicks=1, interval=0.12, button="left",
                region: Optional[Tuple[int,int,int,int]] = None):
    box = wait_for_image(name, timeout, confidence, region)
    if not box:
        raise RuntimeError(f"Could not find image: {name}")
    x, y = pyautogui.center(box)
    pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)

def type_text(text: str, interval=0.02):
    pyautogui.write(text, interval=interval)

def hotkey(*keys, interval=0.06):
    pyautogui.hotkey(*keys, interval=interval)

def focus_cero():
    """
    Bring Cero to foreground:
    - Windows: Win+S, type 'Cero', Enter (fallback)
    - Or click its taskbar icon image if you provide one.
    """
   
    if wait_for_image("cero_taskbar.png", timeout=2, confidence=0.85):
        click_image("cero_taskbar.png", confidence=0.85)
        time.sleep(0.8)
        return

    if sys.platform.startswith("win"):
        hotkey('win', 's')
        type_text("Cero")
        time.sleep(0.6)
        pyautogui.press('enter')
    elif sys.platform == "darwin":
        hotkey('command', 'space')
        type_text("Cero")
        time.sleep(0.6)
        pyautogui.press('enter')
    time.sleep(2.0)

def run_cero_flow(username: str, password: str, export_dir: str, dry: bool = False):
    """
    Example flow for Cero:
      1) Launch / focus app
      2) Log in
      3) Open Reports > Sales Summary
      4) Export (CSV)
      5) Log out
    """
    logging.info("Starting Cero automation" + (" (dry run)" if dry else ""))


    logging.info("3s to cancel (move mouse to top-left).")
    time.sleep(3)

   
    focus_cero()


    dash = wait_for_image("cero_dashboard_marker.png", timeout=4, confidence=0.83)
    if not dash:
        
        click_image("login_username.png", timeout=15)
        if not dry:
            type_text(username)

        click_image("login_password.png")
        if not dry:
            type_text(password)

        if dry:
            wait_for_image("login_button.png")
        else:
            click_image("login_button.png")

 
        dash = wait_for_image("cero_dashboard_marker.png", timeout=30, confidence=0.83)
        if not dash:
            raise RuntimeError("Login likely failed; dashboard marker not found.")


    top_bar = (0, 0, pyautogui.size().width, 140)
    click_image("menu_reports.png", region=top_bar)
    time.sleep(0.4)
    click_image("reports_sales_summary.png")
    wait_for_image("sales_summary_loaded.png", timeout=30, confidence=0.85)

    if wait_for_image("date_from_field.png", timeout=2, confidence=0.85):
        click_image("date_from_field.png")
        if not dry:
            hotkey('ctrl', 'a' if not sys.platform == "darwin" else 'command')
            type_text("2025-01-01")
    if wait_for_image("date_to_field.png", timeout=2, confidence=0.85):
        click_image("date_to_field.png")
        if not dry:
            hotkey('ctrl', 'a' if not sys.platform == "darwin" else 'command')
            # type_text("2025-08-14")

    click_image("btn_export.png", timeout=15)
    time.sleep(0.6)
    click_image("export_csv.png", timeout=10)

    if wait_for_image("file_dialog_name_field.png", timeout=10, confidence=0.85):
        click_image("file_dialog_name_field.png")
        if not dry:
            type_text(f"{export_dir}")

        if sys.platform.startswith("win"):
            pyautogui.press('enter')
        else:
            pyautogui.press('enter')


    wait_for_image("toast_export_success.png", timeout=15, confidence=0.8)

    click_image("user_menu.png", region=top_bar)
    if wait_for_image("menu_logout.png", timeout=5, confidence=0.85):
        click_image("menu_logout.png")

    logging.info("Cero flow complete.")

if __name__ == "__main__":
    
    args = sys.argv[1:]
    dry = ("--dry" in args)
    if dry:
        run_cero_flow("user", "pass", "C:\\Exports\\cero_sales.csv", dry=True)
    else:
        if len(args) < 3:
            print("Usage: python cero_automation.py <username> <password> <export_path>")
            sys.exit(1)
        run_cero_flow(args[0], args[1], args[2], dry=False)
