import threading
import logging
import time
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, Dict, Any, List, Tuple
from datetime import datetime
import functools
from concurrent.futures import ThreadPoolExecutor
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ConvergenceCriterion(Enum):
    ABSOLUTE_CHANGE = "absolute_change"
    RELATIVE_CHANGE = "relative_change"
    GRADIENT_NORM = "gradient_norm"
    COMBINED = "combined"


class LearningRateSchedule(Enum):
    CONSTANT = "constant"
    EXPONENTIAL_DECAY = "exponential_decay"
    POLYNOMIAL_DECAY = "polynomial_decay"
    ADAPTIVE = "adaptive"


@dataclass
class OptimizationConfig:
    max_iterations: int = 10000
    convergence_criterion: ConvergenceCriterion = ConvergenceCriterion.COMBINED
    absolute_tolerance: float = 1e-6
    relative_tolerance: float = 1e-6
    gradient_tolerance: float = 1e-5
    initial_learning_rate: float = 0.01
    learning_rate_schedule: LearningRateSchedule = LearningRateSchedule.ADAPTIVE
    decay_rate: float = 0.95
    decay_steps: int = 100
    min_learning_rate: float = 1e-8
    max_learning_rate: float = 1.0
    gradient_clip_value: float = 10.0
    numerical_stability_eps: float = 1e-10
    max_function_calls: int = 100000
    timeout_seconds: float = 300.0
    validate_inputs: bool = True
    early_stopping_patience: int = 50
    momentum: float = 0.9
    use_momentum: bool = False

    def validate(self) -> None:
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        if self.absolute_tolerance < 0:
            raise ValueError("absolute_tolerance must be non-negative")
        if self.relative_tolerance < 0:
            raise ValueError("relative_tolerance must be non-negative")
        if self.gradient_tolerance < 0:
            raise ValueError("gradient_tolerance must be non-negative")
        if self.initial_learning_rate <= 0:
            raise ValueError("initial_learning_rate must be positive")
        if self.min_learning_rate < 0:
            raise ValueError("min_learning_rate must be non-negative")
        if self.max_learning_rate <= 0:
            raise ValueError("max_learning_rate must be positive")
        if self.min_learning_rate > self.max_learning_rate:
            raise ValueError("min_learning_rate must be <= max_learning_rate")
        if self.gradient_clip_value <= 0:
            raise ValueError("gradient_clip_value must be positive")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.momentum < 0 or self.momentum >= 1:
            raise ValueError("momentum must be in [0, 1)")


@dataclass
class OptimizationState:
    iteration: int = 0
    current_point: Optional[List[float]] = None
    current_value: float = 0.0
    previous_value: float = 0.0
    gradient: Optional[List[float]] = None
    learning_rate: float = 0.0
    function_calls: int = 0
    convergence_achieved: bool = False
    convergence_reason: str = ""
    elapsed_time: float = 0.0
    history: List[Dict[str, Any]] = field(default_factory=list)
    velocity: Optional[List[float]] = None
    improvement_count: int = 0
    no_improvement_count: int = 0


@dataclass
class OptimizationResult:
    success: bool
    optimal_point: List[float]
    optimal_value: float
    iterations: int
    function_calls: int
    convergence_criterion_met: str
    elapsed_time: float
    history: List[Dict[str, Any]]
    error_message: Optional[str] = None


class GradientComputationError(Exception):
    pass


class NumericalInstabilityError(Exception):
    pass


class TimeoutError(Exception):
    pass


class FunctionCallLimitExceededError(Exception):
    pass


class GradientComputer(ABC):
    @abstractmethod
    def compute(self, func: Callable, point: List[float], eps: float) -> List[float]:
        pass


class FiniteDifferenceGradient(GradientComputer):
    def __init__(self, method: str = "central", eps: float = 1e-5):
        if method not in ["forward", "backward", "central"]:
            raise ValueError(f"Invalid method: {method}")
        self.method = method
        self.eps = eps

    def compute(self, func: Callable, point: List[float], eps: float = None) -> List[float]:
        if eps is None:
            eps = self.eps
        
        gradient = []
        
        for i in range(len(point)):
            if self.method == "central":
                point_plus = point.copy()
                point_minus = point.copy()
                point_plus[i] += eps
                point_minus[i] -= eps
                
                try:
                    grad = (func(point_plus) - func(point_minus)) / (2 * eps)
                except (ValueError, OverflowError, TypeError) as e:
                    raise GradientComputationError(f"Failed to compute gradient at dimension {i}: {str(e)}")
                
            elif self.method == "forward":
                point_plus = point.copy()
                point_plus[i] += eps
                
                try:
                    grad = (func(point_plus) - func(point)) / eps
                except (ValueError, OverflowError, TypeError) as e:
                    raise GradientComputationError(f"Failed to compute gradient at dimension {i}: {str(e)}")
                
            else:
                point_minus = point.copy()
                point_minus[i] -= eps
                
                try:
                    grad = (func(point) - func(point_minus)) / eps
                except (ValueError, OverflowError, TypeError) as e:
                    raise GradientComputationError(f"Failed to compute gradient at dimension {i}: {str(e)}")
            
            if not math.isfinite(grad):
                raise NumericalInstabilityError(f"Non-finite gradient at dimension {i}: {grad}")
            
            gradient.append(grad)
        
        return gradient


class LearningRateScheduler:
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.initial_lr = config.initial_learning_rate

    def get_learning_rate(self, iteration: int, gradient_norm: float = None) -> float:
        if self.config.learning_rate_schedule == LearningRateSchedule.CONSTANT:
            return self.initial_lr
        
        elif self.config.learning_rate_schedule == LearningRateSchedule.EXPONENTIAL_DECAY:
            decay = self.config.decay_rate ** (iteration / self.config.decay_steps)
            lr = self.initial_lr * decay
        
        elif self.config.learning_rate_schedule == LearningRateSchedule.POLYNOMIAL_DECAY:
            decay = (1 - iteration / self.config.max_iterations) ** 2
            lr = self.initial_lr * decay
        
        elif self.config.learning_rate_schedule == LearningRateSchedule.ADAPTIVE:
            if gradient_norm is None:
                return self.initial_lr
            adaptive_lr = 0.1 / (1 + gradient_norm)
            lr = min(max(adaptive_lr, self.config.min_learning_rate), self.config.max_learning_rate)
        
        else:
            lr = self.initial_lr
        
        return max(min(lr, self.config.max_learning_rate), self.config.min_learning_rate)


class ConvergenceChecker:
    def __init__(self, config: OptimizationConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def check_convergence(self, state: OptimizationState) -> Tuple[bool, str]:
        if state.iteration == 0:
            return False, ""
        
        if self.config.convergence_criterion == ConvergenceCriterion.ABSOLUTE_CHANGE:
            if abs(state.current_value - state.previous_value) < self.config.absolute_tolerance:
                return True, "absolute_change"
        
        elif self.config.convergence_criterion == ConvergenceCriterion.RELATIVE_CHANGE:
            if abs(state.previous_value) < self.config.numerical_stability_eps:
                denominator = self.config.numerical_stability_eps
            else:
                denominator = abs(state.previous_value)
            
            relative_change = abs(state.current_value - state.previous_value) / denominator
            if relative_change < self.config.relative_tolerance:
                return True, "relative_change"
        
        elif self.config.convergence_criterion == ConvergenceCriterion.GRADIENT_NORM:
            if state.gradient:
                gradient_norm = math.sqrt(sum(g**2 for g in state.gradient))
                if gradient_norm < self.config.gradient_tolerance:
                    return True, "gradient_norm"
        
        elif self.config.convergence_criterion == ConvergenceCriterion.COMBINED:
            abs_change = abs(state.current_value - state.previous_value) < self.config.absolute_tolerance
            
            if abs(state.previous_value) < self.config.numerical_stability_eps:
                denominator = self.config.numerical_stability_eps
            else:
                denominator = abs(state.previous_value)
            rel_change = abs(state.current_value - state.previous_value) / denominator < self.config.relative_tolerance
            
            gradient_norm_small = False
            if state.gradient:
                gradient_norm = math.sqrt(sum(g**2 for g in state.gradient))
                gradient_norm_small = gradient_norm < self.config.gradient_tolerance
            
            if (abs_change or rel_change) and gradient_norm_small:
                return True, "combined_criteria"
        
        return False, ""

    def check_early_stopping(self, state: OptimizationState) -> bool:
        if state.no_improvement_count > self.config.early_stopping_patience:
            self.logger.info(f"Early stopping triggered after {state.no_improvement_count} iterations without improvement")
            return True
        return False


class GradientAscentOptimizer:
    def __init__(self, config: Optional[OptimizationConfig] = None, gradient_computer: Optional[GradientComputer] = None):
        self.config = config or OptimizationConfig()
        self.config.validate()
        self.gradient_computer = gradient_computer or FiniteDifferenceGradient()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.lock = threading.RLock()
        self._validate_function = self.config.validate_inputs
        self.lr_scheduler = LearningRateScheduler(self.config)
        self.convergence_checker = ConvergenceChecker(self.config, self.logger)

    def _validate_function_input(self, func: Callable, initial_point: List[float]) -> None:
        if not callable(func):
            raise TypeError("func must be callable")
        
        if not isinstance(initial_point, (list, tuple)):
            raise TypeError("initial_point must be a list or tuple")
        
        if len(initial_point) == 0:
            raise ValueError("initial_point cannot be empty")
        
        for i, val in enumerate(initial_point):
            if not isinstance(val, (int, float)):
                raise TypeError(f"initial_point[{i}] must be numeric")
            if not math.isfinite(val):
                raise ValueError(f"initial_point[{i}] must be finite")
        
        try:
            test_value = func(initial_point)
            if not isinstance(test_value, (int, float)):
                raise TypeError(f"Function must return numeric value, got {type(test_value)}")
            if not math.isfinite(test_value):
                raise ValueError(f"Function returned non-finite value: {test_value}")
        except Exception as e:
            raise ValueError(f"Function evaluation failed at initial_point: {str(e)}")

    def _clip_gradient(self, gradient: List[float]) -> List[float]:
        gradient_norm = math.sqrt(sum(g**2 for g in gradient))
        
        if gradient_norm > self.config.gradient_clip_value:
            scale = self.config.gradient_clip_value / gradient_norm
            gradient = [g * scale for g in gradient]
        
        return gradient

    def _apply_momentum(self, state: OptimizationState, gradient: List[float]) -> List[float]:
        if not self.config.use_momentum:
            return gradient
        
        if state.velocity is None:
            state.velocity = [0.0] * len(gradient)
        
        state.velocity = [
            self.config.momentum * v + (1 - self.config.momentum) * g
            for v, g in zip(state.velocity, gradient)
        ]
        
        return state.velocity

    def _update_point(self, current_point: List[float], gradient: List[float], learning_rate: float) -> List[float]:
        return [p + learning_rate * g for p, g in zip(current_point, gradient)]

    def _check_numerical_stability(self, point: List[float], value: float, gradient: List[float]) -> None:
        if not all(math.isfinite(p) for p in point):
            raise NumericalInstabilityError("Point contains non-finite values")
        
        if not math.isfinite(value):
            raise NumericalInstabilityError(f"Function value is non-finite: {value}")
        
        if not all(math.isfinite(g) for g in gradient):
            raise NumericalInstabilityError("Gradient contains non-finite values")

    def optimize(self, func: Callable, initial_point: List[float]) -> OptimizationResult:
        with self.lock:
            if self._validate_function:
                self._validate_function_input(func, initial_point)
        
        state = OptimizationState(
            current_point=initial_point.copy(),
            learning_rate=self.config.initial_learning_rate
        )
        
        start_time = time.time()
        
        try:
            state.current_value = func(state.current_point)
            state.function_calls += 1
            
            if not math.isfinite(state.current_value):
                raise NumericalInstabilityError(f"Initial function value is non-finite: {state.current_value}")
            
            self.logger.info(f"Starting optimization with initial value: {state.current_value}")
            
            while state.iteration < self.config.max_iterations:
                elapsed = time.time() - start_time
                state.elapsed_time = elapsed
                
                if elapsed > self.config.timeout_seconds:
                    raise TimeoutError(f"Optimization exceeded timeout of {self.config.timeout_seconds} seconds")
                
                if state.function_calls > self.config.max_function_calls:
                    raise FunctionCallLimitExceededError(
                        f"Optimization exceeded maximum function calls of {self.config.max_function_calls}"
                    )
                
                try:
                    state.gradient = self.gradient_computer.compute(func, state.current_point)
                    state.function_calls += 2
                