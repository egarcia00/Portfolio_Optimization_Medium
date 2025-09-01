"""
Utility functions for portfolio optimization.

This module contains helper functions for data processing, calculations,
and visualization used in portfolio optimization.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_ticker_data(
    tickers: List[str], 
    start: Optional[str] = None, 
    end: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Download historical data for given tickers.
    
    Args:
        tickers: List of ticker symbols to download
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        **kwargs: Additional parameters for yfinance download
        
    Returns:
        DataFrame with historical data
        
    Raises:
        ValueError: If no data is downloaded
    """
    try:
        logger.info(f"Downloading data for tickers: {tickers}")
        df = yf.download(tickers, start=start, end=end, **kwargs)
        
        if df.empty:
            raise ValueError(f"No data downloaded for tickers: {tickers}")
            
        # Clean rows with no values
        df = df.dropna(axis=0)
        logger.info(f"Downloaded {len(df)} rows of data")
        
        return df
        
    except Exception as e:
        logger.error(f"Error downloading data: {e}")
        raise


def clean_and_match_data(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean and match two dataframes to have the same date index.
    
    Args:
        df1: First dataframe (benchmark)
        df2: Second dataframe (portfolio)
        
    Returns:
        Tuple of cleaned and matched dataframes
    """
    # Clean rows with no values
    df1_clean = df1.dropna(axis=0)
    df2_clean = df2.dropna(axis=0)
    
    # Match the days
    common_dates = df1_clean.index.intersection(df2_clean.index)
    df1_matched = df1_clean[df1_clean.index.isin(common_dates)]
    df2_matched = df2_clean[df2_clean.index.isin(common_dates)]
    
    logger.info(f"Matched {len(common_dates)} common trading days")
    
    return df1_matched, df2_matched


def calculate_returns_and_risk(prices: np.ndarray) -> Tuple[float, float]:
    """
    Calculate average return and risk (standard deviation) from price data.
    
    Args:
        prices: Array of closing prices
        
    Returns:
        Tuple of (average_return, risk)
    """
    # Calculate daily returns
    returns = np.diff(prices) / prices[1:]
    
    # Calculate average return and risk
    avg_return = np.average(returns)
    risk = np.std(returns)
    
    return avg_return, risk


def generate_random_portfolio_weights(n_assets: int) -> np.ndarray:
    """
    Generate random portfolio weights using Dirichlet distribution.
    
    Args:
        n_assets: Number of assets in the portfolio
        
    Returns:
        Array of portfolio weights that sum to 1
    """
    return np.random.dirichlet(np.ones(n_assets), size=1)[0]


def calculate_portfolio_metrics(
    weights: np.ndarray, 
    asset_prices: np.ndarray
) -> Tuple[float, float]:
    """
    Calculate portfolio return and risk given weights and asset prices.
    
    Args:
        weights: Portfolio weights
        asset_prices: Asset price matrix (n_assets x n_days)
        
    Returns:
        Tuple of (portfolio_return, portfolio_risk)
    """
    # Calculate weighted portfolio prices
    portfolio_prices = np.matmul(weights, asset_prices.T)
    
    # Calculate daily returns
    portfolio_returns = np.diff(portfolio_prices) / portfolio_prices[1:]
    
    # Calculate metrics
    portfolio_return = np.average(portfolio_returns)
    portfolio_risk = np.std(portfolio_returns)
    
    return portfolio_return, portfolio_risk


def annualize_metrics(return_rate: float, risk: float, trade_days: int = 252) -> Tuple[float, float]:
    """
    Annualize return and risk metrics.
    
    Args:
        return_rate: Daily return rate
        risk: Daily risk (standard deviation)
        trade_days: Number of trading days per year
        
    Returns:
        Tuple of (annualized_return, annualized_risk)
    """
    annualized_return = return_rate * trade_days
    annualized_risk = risk * trade_days
    
    return annualized_return, annualized_risk


def find_optimal_portfolio(
    portfolio_array: np.ndarray, 
    max_risk: float, 
    min_risk: float
) -> Tuple[np.ndarray, int]:
    """
    Find the optimal portfolio based on risk constraints.
    
    Args:
        portfolio_array: Array of [return, risk] pairs
        max_risk: Maximum acceptable risk
        min_risk: Minimum risk in the dataset
        
    Returns:
        Tuple of (best_portfolio_metrics, portfolio_index)
    """
    # Find portfolios within risk constraint
    acceptable_portfolios = np.where(portfolio_array[:, 1] <= max_risk)[0]
    
    if len(acceptable_portfolios) > 1:
        # Select from acceptable portfolios
        candidate_portfolios = portfolio_array[acceptable_portfolios]
        best_idx = np.argmax(candidate_portfolios[:, 0])
        portfolio_idx = acceptable_portfolios[best_idx]
        best_portfolio = candidate_portfolios[best_idx]
    else:
        # Select minimum risk portfolio
        min_risk_portfolios = np.where(portfolio_array[:, 1] == min_risk)[0]
        candidate_portfolios = portfolio_array[min_risk_portfolios]
        best_idx = np.argmax(candidate_portfolios[:, 0])
        portfolio_idx = min_risk_portfolios[best_idx]
        best_portfolio = candidate_portfolios[best_idx]
    
    return best_portfolio, portfolio_idx


def create_portfolio_visualization(
    risk_vector: np.ndarray,
    return_vector: np.ndarray,
    benchmark_risk: float,
    benchmark_return: float,
    best_portfolio: np.ndarray,
    risk_gap: List[float],
    trade_days_per_year: int = 252
) -> plt.Figure:
    """
    Create a scatter plot visualization of portfolio optimization results.
    
    Args:
        risk_vector: Array of portfolio risks
        return_vector: Array of portfolio returns
        benchmark_risk: Benchmark risk
        benchmark_return: Benchmark return
        best_portfolio: Best portfolio [return, risk]
        risk_gap: [min_risk, max_risk] for visualization
        trade_days_per_year: Trading days per year for annualization
        
    Returns:
        Matplotlib figure object
    """
    # Annualize metrics
    risk_gap_annual = np.array(risk_gap) * trade_days_per_year
    best_portfolio_annual = best_portfolio.copy()
    best_portfolio_annual[0] *= trade_days_per_year
    best_portfolio_annual[1] *= trade_days_per_year
    
    x = np.array(risk_vector) * trade_days_per_year
    y = np.array(return_vector) * trade_days_per_year
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot portfolio scenarios
    ax.scatter(x, y, alpha=0.5, linewidths=0.1, edgecolors='black', 
               label='Portfolio Scenarios')
    
    # Plot benchmark
    ax.scatter(benchmark_risk * trade_days_per_year, 
               benchmark_return * trade_days_per_year,
               color='red', linewidths=1, edgecolors='black', 
               label='Market Proxy Values')
    
    # Plot best portfolio
    ax.scatter(best_portfolio_annual[1], best_portfolio_annual[0],
               color='green', linewidths=1, edgecolors='black', 
               label='Best Performer')
    
    # Add risk zone
    ax.axvspan(risk_gap_annual[0], risk_gap_annual[1], 
               color='red', alpha=0.08, label='Accepted Risk Zone')
    
    # Formatting
    ax.set_ylabel("Yearly Portfolio Average Return (%)")
    ax.set_xlabel("Yearly Portfolio Standard Deviation")
    ax.axhline(y=0, color='black', alpha=0.5)
    ax.legend(loc=0)
    
    # Format y-axis as percentage
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    
    plt.tight_layout()
    return fig


def create_portfolio_summary_table(
    portfolio_tickers: List[str],
    best_weights: List[float]
) -> pd.DataFrame:
    """
    Create a summary table of the optimal portfolio allocation.
    
    Args:
        portfolio_tickers: List of ticker symbols
        best_weights: Optimal portfolio weights
        
    Returns:
        Formatted DataFrame with portfolio allocation
    """
    df = pd.DataFrame({
        "Stock Name": portfolio_tickers,
        "Stock % in Portfolio": best_weights
    })
    
    # Sort by allocation percentage (descending)
    df = df.sort_values(by=["Stock % in Portfolio"], ascending=False)
    
    return df