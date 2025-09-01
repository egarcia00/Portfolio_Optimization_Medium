"""
Configuration management for Portfolio Optimization.

This module contains configuration classes and constants used throughout
the portfolio optimization system.
"""

from dataclasses import dataclass
from typing import List, Optional
import os


@dataclass
class PortfolioConfig:
    """Configuration class for portfolio optimization parameters."""
    
    # Portfolio assets
    benchmark_tickers: List[str]
    portfolio_tickers: List[str]
    
    # Date range
    start_date: str
    end_date: str
    
    # Optimization parameters
    number_of_scenarios: int = 10000
    delta_risk: float = 0.05
    trade_days_per_year: int = 252
    
    # Data parameters
    interval: str = "1d"
    auto_adjust: bool = False
    back_adjust: bool = False
    prepost: bool = False
    actions: bool = False
    threads: bool = True
    group_by: str = "column"
    progress: bool = True
    show_errors: bool = True
    rounding: bool = False
    timeout: Optional[float] = None
    
    def __post_init__(self):
        """Validate configuration parameters after initialization."""
        if self.number_of_scenarios <= 0:
            raise ValueError("number_of_scenarios must be positive")
        if self.delta_risk <= 0 or self.delta_risk >= 1:
            raise ValueError("delta_risk must be between 0 and 1")
        if self.trade_days_per_year <= 0:
            raise ValueError("trade_days_per_year must be positive")


# Default configuration
DEFAULT_CONFIG = PortfolioConfig(
    benchmark_tickers=["^GSPC"],
    portfolio_tickers=['AAPL', 'GOOG', 'AMZN'],
    start_date="2017-01-01",
    end_date="2022-03-31"
)


def load_config_from_env() -> PortfolioConfig:
    """Load configuration from environment variables."""
    return PortfolioConfig(
        benchmark_tickers=os.getenv('BENCHMARK_TICKERS', '^GSPC').split(','),
        portfolio_tickers=os.getenv('PORTFOLIO_TICKERS', 'AAPL,GOOG,AMZN').split(','),
        start_date=os.getenv('START_DATE', '2017-01-01'),
        end_date=os.getenv('END_DATE', '2022-03-31'),
        number_of_scenarios=int(os.getenv('NUMBER_OF_SCENARIOS', '10000')),
        delta_risk=float(os.getenv('DELTA_RISK', '0.05')),
        trade_days_per_year=int(os.getenv('TRADE_DAYS_PER_YEAR', '252'))
    )
