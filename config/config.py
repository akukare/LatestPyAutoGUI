# config/__init__.py

import yaml
from pathlib import Path
from dataclasses import dataclass

# 1️⃣ Define dataclasses matching your YAML structure
@dataclass
class DriverConfig:
    pause_between_actions: float
    fail_safe: bool
    exists_timeout: float
    confidence: float

@dataclass
class ApplicationConfig:
    exe: str
    launch_args: str
    launch_timeout: float
    launch_marker_image: str  # name of an image under assets/

@dataclass
class ReportsConfig:
    html_dir: str
    screenshots_dir: str

@dataclass
class RetryConfig:
    max_retries: int
    backoff_factor: float

@dataclass
class Settings:
    driver: DriverConfig
    application: ApplicationConfig
    reports: ReportsConfig
    retry: RetryConfig

# 2️⃣ Load your default.yaml
_config_path = Path(__file__).with_name("default.yaml")
_data = yaml.safe_load(_config_path.read_text())

# 3️⃣ Instantiate
settings = Settings(
    driver=DriverConfig(**_data["driver"]),
    application=ApplicationConfig(**_data["application"]),
    reports=ReportsConfig(**_data["reports"]),
    retry=RetryConfig(**_data["retry"]),
)
