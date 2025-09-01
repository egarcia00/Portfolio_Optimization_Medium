"""
Portfolio Optimization Engine.

This module contains the main PortfolioOptimizer class that orchestrates
the portfolio optimization process using Monte Carlo simulation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional
import logging

from .config import PortfolioConfig
from .utils import (
    download_ticker_data, clean_and_match_data, calculate_returns_and_risk,
    generate_random_portfolio_weights, calculate_portfolio_metrics,
    annualize_metrics, find_optimal_portfolio, create_portfolio_visualization,
    create_portfolio_summary_table
)

logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """
    Main class for portfolio optimization using Monte Carlo simulation.
    
    This class handles the complete portfolio optimization workflow:
    1. Data download and preprocessing
    2. Benchmark analysis
    3. Portfolio simulation
    4. Optimization and selection
    5. Results visualization and reporting
    """
    
    def __init__(self, config: PortfolioConfig):
        """
        Initialize the PortfolioOptimizer.
        
        Args:
            config: PortfolioConfig object containing optimization parameters
        """
        self.config = config
        self.benchmark_data = None
        self.portfolio_data = None
        self.benchmark_return = None
        self.benchmark_risk = None
        self.portfolio_scenarios = []
        self.optimal_portfolio = None
        self.optimal_weights = None
        self.results = {}
        
        logger.info("PortfolioOptimizer initialized")
    
    def download_data(self) -> None:
        """Download and prepare benchmark and portfolio data."""
        logger.info("Starting data download...")
        
        # Download benchmark data
        self.benchmark_data = download_ticker_data(
            self.config.benchmark_tickers,
            start=self.config.start_date,
            end=self.config.end_date,
            interval=self.config.interval,
            auto_adjust=self.config.auto_adjust,
            back_adjust=self.config.back_adjust,
            prepost=self.config.prepost,
            actions=self.config.actions,
            threads=self.config.threads,
            group_by=self.config.group_by,
            progress=self.config.progress,
            show_errors=self.config.show_errors,
            rounding=self.config.rounding,
            timeout=self.config.timeout
        )
        
        # Download portfolio data
        self.portfolio_data = download_ticker_data(
            self.config.portfolio_tickers,
            start=self.config.start_date,
            end=self.config.end_date,
            interval=self.config.interval,
            auto_adjust=self.config.auto_adjust,
            back_adjust=self.config.back_adjust,
            prepost=self.config.prepost,
            actions=self.config.actions,
            threads=self.config.threads,
            group_by=self.config.group_by,
            progress=self.config.progress,
            show_errors=self.config.show_errors,
            rounding=self.config.rounding,
            timeout=self.config.timeout
        )
        
        # Clean and match data
        self.benchmark_data, self.portfolio_data = clean_and_match_data(
            self.benchmark_data, self.portfolio_data
        )
        
        logger.info("Data download completed successfully")
    
    def analyze_benchmark(self) -> None:
        """Analyze benchmark performance."""
        logger.info("Analyzing benchmark...")
        
        # Extract closing prices
        benchmark_prices = np.array(self.benchmark_data['Close'])
        
        # Calculate returns and risk
        self.benchmark_return, self.benchmark_risk = calculate_returns_and_risk(
            benchmark_prices
        )
        
        logger.info(f"Benchmark - Return: {self.benchmark_return:.4f}, Risk: {self.benchmark_risk:.4f}")
    
    def simulate_portfolios(self) -> None:
        """Run Monte Carlo simulation to generate portfolio scenarios."""
        logger.info(f"Starting Monte Carlo simulation with {self.config.number_of_scenarios} scenarios...")
        
        # Extract portfolio prices
        portfolio_prices = np.array(self.portfolio_data['Close'])
        
        # Initialize results storage
        return_vector = [self.benchmark_return]
        risk_vector = [self.benchmark_risk]
        weight_vector = []
        
        # Run simulation
        for i in range(self.config.number_of_scenarios):
            if (i + 1) % 1000 == 0:
                logger.info(f"Completed {i + 1} scenarios...")
            
            # Generate random portfolio weights
            weights = generate_random_portfolio_weights(len(self.config.portfolio_tickers))
            weight_vector.append(weights)
            
            # Calculate portfolio metrics
            portfolio_return, portfolio_risk = calculate_portfolio_metrics(
                weights, portfolio_prices
            )
            
            # Store results
            return_vector.append(portfolio_return)
            risk_vector.append(portfolio_risk)
        
        # Store results
        self.portfolio_scenarios = {
            'returns': np.array(return_vector),
            'risks': np.array(risk_vector),
            'weights': weight_vector
        }
        
        logger.info("Monte Carlo simulation completed")
    
    def optimize_portfolio(self) -> None:
        """Find the optimal portfolio based on risk constraints."""
        logger.info("Optimizing portfolio...")
        
        # Create portfolio array (excluding benchmark)
        portfolio_array = np.column_stack((
            self.portfolio_scenarios['returns'][1:],
            self.portfolio_scenarios['risks'][1:]
        ))
        
        # Calculate risk boundaries
        min_risk = np.min(self.portfolio_scenarios['risks'][1:])
        max_risk = self.benchmark_risk * (1 + self.config.delta_risk)
        
        # Find optimal portfolio
        best_portfolio, portfolio_idx = find_optimal_portfolio(
            portfolio_array, max_risk, min_risk
        )
        
        # Store results
        self.optimal_portfolio = best_portfolio
        self.optimal_weights = self.portfolio_scenarios['weights'][portfolio_idx]
        
        # Store risk boundaries
        self.risk_boundaries = {
            'min_risk': min_risk,
            'max_risk': max_risk,
            'risk_gap': [min_risk, max_risk]
        }
        
        logger.info(f"Optimal portfolio found - Return: {best_portfolio[0]:.4f}, Risk: {best_portfolio[1]:.4f}")
    
    def create_visualization(self) -> plt.Figure:
        """Create portfolio optimization visualization."""
        logger.info("Creating visualization...")
        
        fig = create_portfolio_visualization(
            risk_vector=self.portfolio_scenarios['risks'],
            return_vector=self.portfolio_scenarios['returns'],
            benchmark_risk=self.benchmark_risk,
            benchmark_return=self.benchmark_return,
            best_portfolio=self.optimal_portfolio,
            risk_gap=self.risk_boundaries['risk_gap'],
            trade_days_per_year=self.config.trade_days_per_year
        )
        
        return fig
    
    def create_summary_table(self) -> pd.DataFrame:
        """Create portfolio allocation summary table."""
        logger.info("Creating summary table...")
        
        table = create_portfolio_summary_table(
            portfolio_tickers=self.config.portfolio_tickers,
            best_weights=self.optimal_weights.tolist()
        )
        
        return table
    
    def generate_results(self) -> Dict[str, Any]:
        """Generate comprehensive optimization results."""
        logger.info("Generating results summary...")
        
        # Annualize metrics
        annual_return, annual_risk = annualize_metrics(
            self.optimal_portfolio[0], 
            self.optimal_portfolio[1], 
            self.config.trade_days_per_year
        )
        
        annual_benchmark_return, annual_benchmark_risk = annualize_metrics(
            self.benchmark_return, 
            self.benchmark_risk, 
            self.config.trade_days_per_year
        )
        
        self.results = {
            'optimal_portfolio': {
                'daily_return': self.optimal_portfolio[0],
                'daily_risk': self.optimal_portfolio[1],
                'annual_return': annual_return,
                'annual_risk': annual_risk,
                'weights': dict(zip(self.config.portfolio_tickers, self.optimal_weights))
            },
            'benchmark': {
                'daily_return': self.benchmark_return,
                'daily_risk': self.benchmark_risk,
                'annual_return': annual_benchmark_return,
                'annual_risk': annual_benchmark_risk
            },
            'risk_boundaries': self.risk_boundaries,
            'simulation_stats': {
                'total_scenarios': self.config.number_of_scenarios,
                'min_risk': np.min(self.portfolio_scenarios['risks'][1:]),
                'max_risk': np.max(self.portfolio_scenarios['risks'][1:]),
                'min_return': np.min(self.portfolio_scenarios['returns'][1:]),
                'max_return': np.max(self.portfolio_scenarios['returns'][1:])
            }
        }
        
        return self.results
    
    def run_optimization(self) -> Dict[str, Any]:
        """
        Run the complete portfolio optimization workflow.
        
        Returns:
            Dictionary containing all optimization results
        """
        logger.info("Starting portfolio optimization workflow...")
        
        try:
            # Step 1: Download data
            self.download_data()
            
            # Step 2: Analyze benchmark
            self.analyze_benchmark()
            
            # Step 3: Simulate portfolios
            self.simulate_portfolios()
            
            # Step 4: Optimize portfolio
            self.optimize_portfolio()
            
            # Step 5: Generate results
            results = self.generate_results()
            
            logger.info("Portfolio optimization completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error during optimization: {e}")
            raise
    
    def save_results(self, filename: str = "portfolio_results.csv") -> None:
        """Save optimization results to CSV file."""
        if not self.results:
            raise ValueError("No results to save. Run optimization first.")
        
        # Create results DataFrame
        results_data = []
        
        # Add optimal portfolio
        for ticker, weight in self.results['optimal_portfolio']['weights'].items():
            results_data.append({
                'Type': 'Optimal Portfolio',
                'Asset': ticker,
                'Weight': weight,
                'Daily_Return': self.results['optimal_portfolio']['daily_return'],
                'Daily_Risk': self.results['optimal_portfolio']['daily_risk'],
                'Annual_Return': self.results['optimal_portfolio']['annual_return'],
                'Annual_Risk': self.results['optimal_portfolio']['annual_risk']
            })
        
        # Add benchmark
        results_data.append({
            'Type': 'Benchmark',
            'Asset': self.config.benchmark_tickers[0],
            'Weight': 1.0,
            'Daily_Return': self.results['benchmark']['daily_return'],
            'Daily_Risk': self.results['benchmark']['daily_risk'],
            'Annual_Return': self.results['benchmark']['annual_return'],
            'Annual_Risk': self.results['benchmark']['annual_risk']
        })
        
        df = pd.DataFrame(results_data)
        df.to_csv(filename, index=False)
        logger.info(f"Results saved to {filename}")
    
    def get_portfolio_performance_summary(self) -> str:
        """Get a formatted string summary of portfolio performance."""
        if not self.results:
            return "No results available. Run optimization first."
        
        optimal = self.results['optimal_portfolio']
        benchmark = self.results['benchmark']
        
        summary = f"""
Portfolio Optimization Results
==============================

Optimal Portfolio:
  Annual Return: {optimal['annual_return']:.2%}
  Annual Risk: {optimal['annual_risk']:.2%}
  
Benchmark ({self.config.benchmark_tickers[0]}):
  Annual Return: {benchmark['annual_return']:.2%}
  Annual Risk: {benchmark['annual_risk']:.2%}

Portfolio Allocation:
"""
        
        for ticker, weight in optimal['weights'].items():
            summary += f"  {ticker}: {weight:.2%}\n"
        
        return summary
