# config/__init__.py

import yaml
from pathlib import Path
from dataclasses import dataclass

# ─── Define dataclasses to mirror your default.yaml structure ─────────────────

@dataclass
class DriverTimeoutConfig:
    click: float
    exists: float

@dataclass
class DriverConfig:
    timeout: DriverTimeoutConfig
    pause_between_actions: float
    fail_safe: bool
    confidence: float

@dataclass
class RetryConfig:
    max_retries: int
    backoff_factor: float

@dataclass
class ReportsConfig:
    html_dir: str
    screenshots_dir: str

@dataclass
class ApplicationConfig:
    exe: str
    launch_args: str
    launch_timeout: float
    launch_marker_image: str

@dataclass
class Settings:
    driver: DriverConfig
    retry: RetryConfig
    reports: ReportsConfig
    application: ApplicationConfig

# ─── Load default.yaml and instantiate Settings ──────────────────────────────

_yaml_path = Path(__file__).with_name("default.yaml")
_raw = yaml.safe_load(_yaml_path.read_text())

settings = Settings(
    driver=DriverConfig(
        timeout=DriverTimeoutConfig(**_raw["driver"]["timeout"]),
        pause_between_actions=_raw["driver"]["pause_between_actions"],
        fail_safe=_raw["driver"]["fail_safe"],
        confidence=_raw["driver"]["confidence"],
    ),
    retry=RetryConfig(**_raw["retry"]),
    reports=ReportsConfig(**_raw["reports"]),
    application=ApplicationConfig(**_raw["application"]),
)
