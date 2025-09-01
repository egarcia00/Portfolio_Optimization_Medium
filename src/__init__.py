"""
Portfolio Optimization Package.

A comprehensive Python package for portfolio optimization using Monte Carlo simulation.
"""

__version__ = "1.0.0"
__author__ = "Eduardo Garcia"
__email__ = "eduardo@datafrankfurt.de"

from .config import PortfolioConfig, DEFAULT_CONFIG, load_config_from_env
from .portfolio_optimizer import PortfolioOptimizer
from .utils import (
    download_ticker_data, clean_and_match_data, calculate_returns_and_risk,
    generate_random_portfolio_weights, calculate_portfolio_metrics,
    annualize_metrics, find_optimal_portfolio, create_portfolio_visualization,
    create_portfolio_summary_table
)

__all__ = [
    'PortfolioConfig',
    'DEFAULT_CONFIG', 
    'load_config_from_env',
    'PortfolioOptimizer',
    'download_ticker_data',
    'clean_and_match_data',
    'calculate_returns_and_risk',
    'generate_random_portfolio_weights',
    'calculate_portfolio_metrics',
    'annualize_metrics',
    'find_optimal_portfolio',
    'create_portfolio_visualization',
    'create_portfolio_summary_table'
]
