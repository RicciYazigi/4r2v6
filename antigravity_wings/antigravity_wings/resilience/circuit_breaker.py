import time
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional, TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitOpenError(Exception):
    """Error lanzado cuando el circuito está abierto."""
    pass

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_sec: float = 30.0
    max_latency_sec: float = 10.0

@dataclass
class CircuitMetrics:
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[float] = None

class CircuitBreaker:
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.metrics = CircuitMetrics()

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        self._check_state()
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            latency = time.time() - start_time
            
            if latency > self.config.max_latency_sec:
                logger.warning(f"[{self.name}] High latency: {latency:.2f}s")
                self._record_failure()
                raise TimeoutError(f"Latency {latency:.2f}s exceeded max {self.config.max_latency_sec}s")
            else:
                self._record_success()
            
            return result
        except Exception as e:
            logger.error(f"[{self.name}] Protected call failed: {e}")
            self._record_failure()
            raise

    def _check_state(self):
        if self.metrics.state == CircuitState.OPEN:
            elapsed = time.time() - (self.metrics.last_failure_time or 0)
            if elapsed > self.config.recovery_timeout_sec:
                logger.info(f"[{self.name}] Switching to HALF_OPEN for recovery probe.")
                self.metrics.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(f"Circuit '{self.name}' is OPEN. Cooling down.")

    def _record_failure(self):
        self.metrics.failure_count += 1
        self.metrics.last_failure_time = time.time()
        
        if self.metrics.failure_count >= self.config.failure_threshold:
            if self.metrics.state != CircuitState.OPEN:
                logger.error(f"[{self.name}] FAILURE THRESHOLD REACHED. Circuit OPEN.")
                self.metrics.state = CircuitState.OPEN

    def _record_success(self):
        if self.metrics.state == CircuitState.HALF_OPEN:
            logger.info(f"[{self.name}] Probing success. Closing circuit.")
        self.metrics.state = CircuitState.CLOSED
        self.metrics.failure_count = 0
