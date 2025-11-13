import os
import time
import subprocess
import pytest
import pyautogui

from config import settings  # your YAML-loaded settings object
from src.driver.gui_driver import GuiDriver


def pytest_configure(config):
    # Ensure report directories exist
    os.makedirs(settings.reports.html_dir, exist_ok=True)
    os.makedirs(settings.reports.screenshots_dir, exist_ok=True)


@pytest.fixture(scope='session')
def config():
    """Provide loaded framework settings."""
    return settings


@pytest.fixture(scope='session')
def driver(config):
    """
    Launch the application under test and initialize GuiDriver.

    Yields:
        GuiDriver instance for use in tests.
    """
    # Start the application
    exe = config.application.exe
    args = config.application.launch_args.split()
    proc = subprocess.Popen([exe, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Initialize the GUI driver
    gui = GuiDriver(config.driver)

    # Wait for main window or a known element
    gui.wait_for(config.application.launch_marker_image, timeout=config.application.launch_timeout)

    yield gui

    # Teardown: close the application
    proc.terminate()
    proc.wait(timeout=10)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        # Determine filename
        ts = time.strftime('%Y%m%d_%H%M%S')
        name = item.name
        fname = os.path.join(settings.reports.screenshots_dir, f"FAIL_{name}_{ts}.png")

        # Use driver if available, else fallback to PyAutoGUI
        drv = item.funcargs.get('driver')
        if drv:
            drv.screenshot(fname)
        else:
            pyautogui.screenshot(fname)

        # Optionally attach to pytest-html report
        if hasattr(rep, 'extra'):
            rep.extra.append(pytest_html.extras.image(fname))


@pytest.fixture(autouse=True)
def clear_logs(config):
    """
    Truncate the log file before each test for clean output.
    """
    log_file = config.logging.file
    open(log_file, 'w').close()
    yield
