# utils/app_launcher.py
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Sequence, Tuple


try:
    import pyautogui
    _HAVE_PYAUTOGUI = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.2
except Exception:
    _HAVE_PYAUTOGUI = False


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app_launcher.log", mode="w"), logging.StreamHandler(sys.stdout)],
)

def _wait_image(
    img_path: Path,
    timeout: int = 120,
    confidence: float = 0.9,
    region: Optional[Tuple[int, int, int, int]] = None,
):
    """
    Wait until an image appears on screen. Requires pyautogui + opencv.
    Keep Windows display scaling and app zoom at 100% for accurate matching.
    """
    if not _HAVE_PYAUTOGUI:
        raise RuntimeError("PyAutoGUI not available. Install 'pyautogui' and 'opencv-python' to use wait_img.")

    end = time.time() + timeout
    while time.time() < end:
        box = pyautogui.locateOnScreen(str(img_path), confidence=confidence, region=region)
        if box:
            logging.info(f"[ready-check] Found image: {img_path} @ {box}")
            return True
        time.sleep(0.3)
    raise TimeoutError(f"[ready-check] Image not found within {timeout}s: {img_path}")

def open_application(
    app_path: str,
    args: Optional[Sequence[str]] = None,
    *,
    cwd: Optional[str] = None,
    wait_img: Optional[str] = None,
    timeout: int = 120,
    confidence: float = 0.9,
    region: Optional[Tuple[int, int, int, int]] = None,) -> subprocess.Popen:
    """
    Launches a desktop application and optionally waits for a specific UI image.

    Parameters
    ----------
    app_path : str
        Full path to the executable (e.g., r"C:\\Program Files\\PTC\\Creo...\\parametric.exe")
    args : list[str], optional
        Extra command-line arguments for the application.
    cwd : str, optional
        Working directory to launch from.
    wait_img : str, optional
        Path to a reference PNG on disk that uniquely indicates the app is ready.
        (Capture at 100% scaling. No resizing.)
    timeout : int
        Seconds to wait for the ready image (if provided).
    confidence : float
        Matching confidence for the image (0.0–1.0). 0.9 is a good start.
    region : (left, top, width, height), optional
        Search region to speed up and reduce false positives.

    Returns
    -------
    subprocess.Popen
        A process handle you can keep and later close.
    """
    exe = Path(app_path)
    if not exe.exists():
        raise FileNotFoundError(f"Executable not found: {exe}")

    cmd = [str(exe)]
    if args:
        cmd.extend(args)

    logging.info(f"[launch] Starting application: {cmd} (cwd={cwd or 'inherit'})")
    proc = subprocess.Popen(
        cmd,
        cwd=cwd or None,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
    )

    if wait_img:
        img_path = Path(wait_img)
        if not img_path.exists():
            raise FileNotFoundError(f"wait_img not found: {img_path}")
        _wait_image(img_path, timeout=timeout, confidence=confidence, region=region)

    return proc

def close_application(proc: subprocess.Popen, kill_after: int = 5) -> None:
    """
    Try to exit the app gracefully; if still alive after `kill_after` seconds, kill it.
    """
    if proc and proc.poll() is None:
        logging.info("[shutdown] Terminating application...")
        proc.terminate()
        try:
            proc.wait(timeout=kill_after)
        except subprocess.TimeoutExpired:
            logging.warning("[shutdown] Force-killing application...")
            proc.kill()
