# hybrid_driver.py
import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Tuple

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- Logging (rewrite each run) --------------------
LOG_PATH = Path("hybrid.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, mode="w"), logging.StreamHandler(sys.stdout)],
)

# -------------------- Selenium factory --------------------
def make_webdriver(headless: bool = False) -> webdriver.Chrome:
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    if headless:
   
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    driver.set_page_load_timeout(60)
    return driver

# -------------------- Hybrid driver --------------------
class HybridDriver:
    def __init__(self, driver: webdriver.Chrome, image_root: Path = Path("images")):
        self.driver = driver
        self.image_root = image_root
        pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
        pyautogui.PAUSE = 0.2


    def wait_dom(self, by: By, value: str, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def click_dom(self, by: By, value: str, timeout: int = 10):
        el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
        el.click()
        logging.info(f"DOM click: ({by}, {value})")
        return True


    def _img_path(self, name_or_path: str) -> Path:
        p = Path(name_or_path)
        return p if p.exists() else (self.image_root / name_or_path)

    def wait_image(
        self,
        img: str,
        timeout: int = 10,
        confidence: float = 0.9,
        region: Optional[Tuple[int, int, int, int]] = None,
    ):
        """Wait until an image appears; requires opencv installed for confidence."""
        path = self._img_path(img)
        end = time.time() + timeout
        while time.time() < end:
            box = pyautogui.locateOnScreen(str(path), confidence=confidence, region=region)
            if box:
                logging.info(f"Image found: {path} @ {box}")
                return box
        raise TimeoutError(f"Image not found within {timeout}s: {path}")

    def click_image(
        self,
        img: str,
        timeout: int = 10,
        confidence: float = 0.9,
        region: Optional[Tuple[int, int, int, int]] = None,
    ):
        box = self.wait_image(img, timeout=timeout, confidence=confidence, region=region)
        center = pyautogui.center(box)
        pyautogui.moveTo(center.x, center.y, duration=0.15)
        pyautogui.click()
        logging.info(f"GUI click: {img}")
        return True

    def type_text(self, text: str, press_enter: bool = False):
        pyautogui.typewrite(text, interval=0.02)
        if press_enter:
            pyautogui.press("enter")
        logging.info(f"Typed text (enter={press_enter}): {text}")

   
    def click(
        self,
        by: Optional[By] = None,
        value: Optional[str] = None,
        *,
        img: Optional[str] = None,
        dom_timeout: int = 5,
        gui_timeout: int = 8,
        region: Optional[Tuple[int, int, int, int]] = None,
        confidence: float = 0.9,
    ):
        """
        Try DOM click first; if not clickable/visible in dom_timeout,
        fall back to GUI-image click.
        """
        try:
            if by and value:
                return self.click_dom(by, value, timeout=dom_timeout)
        except Exception as e:
            logging.warning(f"DOM click failed: ({by}, {value}) -> {e}")

        if img is None:
            raise RuntimeError("Hybrid click fallback requires 'img' path when DOM locator fails.")
        return self.click_image(img, timeout=gui_timeout, confidence=confidence, region=region)

    def wait_ready(self):
        
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def screenshot(self, name: str = "screen.png"):
        out = Path(name)
        self.driver.save_screenshot(str(out))
        logging.info(f"Saved Selenium screenshot: {out}")


    def handle_save_dialog(self, filename: str, folder: Optional[str] = None):
        """
        Assumes the native 'Save As' dialog is already open.
        Strategy: focus filename field -> type full path -> press Save.
        You may need template images like 'save_button.png' if Enter isn't enough.
        """
     
        pyautogui.hotkey("alt", "n")
        time.sleep(0.2)
        fullpath = Path(folder).expanduser() / filename if folder else Path(filename)
        pyautogui.typewrite(str(fullpath), interval=0.02)
        pyautogui.press("enter")
        logging.info(f"Handled Save dialog -> {fullpath}")


if __name__ == "__main__":
    drv = make_webdriver(headless=False)  # Must be headful for PyAutoGUI
    hybrid = HybridDriver(drv)
    try:
        drv.get("https:")
        hybrid.wait_ready()
        # Try DOM click first; provide an img fallback in case a native dialog appears
        hybrid.click(By.XPATH, "//a[contains(@href, 'w3css_templates.zip')]", img="download_link.png")
        # If your browser prompts a native Save dialog, use:
        # hybrid.handle_save_dialog("template.zip", folder="C:/Users/Public/Downloads")
        time.sleep(2)
        hybrid.screenshot("after_click.png")
    finally:
        drv.quit()
