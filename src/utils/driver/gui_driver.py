import time
import pyautogui
from pathlib import Path

from config import settings
from src.utils.retry import retry

from src.utils.logger import get_logger

# Initialize the module-level logger
driver_logger = get_logger(__name__)

class GuiDriver:
    """
    A wrapper around PyAutoGUI that adds retries, timeouts, and logging.
    """

    def __init__(self, driver_config=None):
        # Load driver-specific settings or use defaults
        self.config = driver_config or settings.driver

        # Configure PyAutoGUI
        pyautogui.PAUSE = self.config.pause_between_actions
        pyautogui.FAILSAFE = self.config.fail_safe
        self.exists_timeout = self.config.timeout.exists
        self.click_timeout = self.config.timeout.click
        self.default_confidence = self.config.confidence

        driver_logger.info(f"GuiDriver initialized: pause={pyautogui.PAUSE}, failsafe={pyautogui.FAILSAFE}")

    @retry(max_attempts=settings.retry.max_retries, backoff=settings.retry.backoff_factor)
    def wait_for(self, image_path: str, timeout: float = None, confidence: float = None):
        """
        Wait until the given image appears on screen and return its location box.
        """
        timeout = timeout or self.exists_timeout
        confidence = confidence or self.default_confidence
        end = time.time() + timeout
        driver_logger.debug(f"Waiting for '{image_path}' up to {timeout}s (confidence={confidence})")

        while time.time() < end:
            loc = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if loc:
                driver_logger.debug(f"Found '{image_path}' at {loc}")
                return loc
            time.sleep(0.5)

        raise TimeoutError(f"Element '{image_path}' not found after {timeout}s")

    @retry(max_attempts=settings.retry.max_retries, backoff=settings.retry.backoff_factor)
    def click(self, image_path: str, timeout: float = None, confidence: float = None):
        """
        Locate the image on screen and click its center.
        """
        box = self.wait_for(image_path, timeout, confidence)
        x, y = pyautogui.center(box)
        pyautogui.click(x, y)
        driver_logger.info(f"Clicked '{image_path}' @ ({x}, {y})")

    def type(self, text: str, interval: float = None):
        """
        Type text with the configured pause interval.
        """
        iv = interval or self.config.pause_between_actions
        pyautogui.write(text, interval=iv)
        driver_logger.info(f"Typed text: {text}")

    def screenshot(self, dest: str):
        """
        Capture a screenshot to the given destination path.
        """
        path = Path(dest)
        path.parent.mkdir(parents=True, exist_ok=True)
        pyautogui.screenshot(str(path))
        driver_logger.info(f"Screenshot saved: {path}")
