"""
Tests for PortfolioOptimizer class.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from src.config import PortfolioConfig
from src.portfolio_optimizer import PortfolioOptimizer


class TestPortfolioOptimizer:
    """Test cases for PortfolioOptimizer class."""
    
    @pytest.fixture
    def sample_config(self):
        """Create a sample configuration for testing."""
        return PortfolioConfig(
            benchmark_tickers=["^GSPC"],
            portfolio_tickers=['AAPL', 'GOOG'],
            start_date="2020-01-01",
            end_date="2021-01-01",
            number_of_scenarios=100
        )
    
    @pytest.fixture
    def sample_benchmark_data(self):
        """Create sample benchmark data."""
        dates = pd.date_range('2020-01-01', '2021-01-01', freq='D')
        prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.01)
        return pd.DataFrame({'Close': prices}, index=dates)
    
    @pytest.fixture
    def sample_portfolio_data(self):
        """Create sample portfolio data."""
        dates = pd.date_range('2020-01-01', '2021-01-01', freq='D')
        prices_aapl = 150 + np.cumsum(np.random.randn(len(dates)) * 0.01)
        prices_goog = 2000 + np.cumsum(np.random.randn(len(dates)) * 0.01)
        
        return pd.DataFrame({
            'Close': np.column_stack([prices_aapl, prices_goog])
        }, index=dates)
    
    def test_initialization(self, sample_config):
        """Test PortfolioOptimizer initialization."""
        optimizer = PortfolioOptimizer(sample_config)
        
        assert optimizer.config == sample_config
        assert optimizer.benchmark_data is None
        assert optimizer.portfolio_data is None
        assert optimizer.optimal_portfolio is None
        assert optimizer.results == {}
    
    @patch('src.portfolio_optimizer.download_ticker_data')
    @patch('src.portfolio_optimizer.clean_and_match_data')
    def test_download_data(self, mock_clean_data, mock_download, sample_config, 
                          sample_benchmark_data, sample_portfolio_data):
        """Test data download functionality."""
        # Setup mocks
        mock_download.side_effect = [sample_benchmark_data, sample_portfolio_data]
        mock_clean_data.return_value = (sample_benchmark_data, sample_portfolio_data)
        
        optimizer = PortfolioOptimizer(sample_config)
        optimizer.download_data()
        
        # Verify data was downloaded and stored
        assert optimizer.benchmark_data is not None
        assert optimizer.portfolio_data is not None
        assert mock_download.call_count == 2
        assert mock_clean_data.call_count == 1
    
    def test_analyze_benchmark(self, sample_config, sample_benchmark_data):
        """Test benchmark analysis."""
        optimizer = PortfolioOptimizer(sample_config)
        optimizer.benchmark_data = sample_benchmark_data
        
        optimizer.analyze_benchmark()
        
        # Verify benchmark metrics were calculated
        assert optimizer.benchmark_return is not None
        assert optimizer.benchmark_risk is not None
        assert isinstance(optimizer.benchmark_return, float)
        assert isinstance(optimizer.benchmark_risk, float)
    
    def test_simulate_portfolios(self, sample_config, sample_portfolio_data):
        """Test portfolio simulation."""
        optimizer = PortfolioOptimizer(sample_config)
        optimizer.portfolio_data = sample_portfolio_data
        
        optimizer.simulate_portfolios()
        
        # Verify simulation results
        assert 'returns' in optimizer.portfolio_scenarios
        assert 'risks' in optimizer.portfolio_scenarios
        assert 'weights' in optimizer.portfolio_scenarios
        
        # Check that we have the expected number of scenarios + benchmark
        expected_scenarios = sample_config.number_of_scenarios + 1
        assert len(optimizer.portfolio_scenarios['returns']) == expected_scenarios
        assert len(optimizer.portfolio_scenarios['risks']) == expected_scenarios
        assert len(optimizer.portfolio_scenarios['weights']) == sample_config.number_of_scenarios
    
    def test_optimize_portfolio(self, sample_config):
        """Test portfolio optimization."""
        optimizer = PortfolioOptimizer(sample_config)
        
        # Setup mock data
        optimizer.benchmark_return = 0.001
        optimizer.benchmark_risk = 0.02
        optimizer.portfolio_scenarios = {
            'returns': np.array([0.001, 0.002, 0.0015, 0.003]),
            'risks': np.array([0.02, 0.015, 0.025, 0.018]),
            'weights': [
                np.array([0.5, 0.5]),
                np.array([0.3, 0.7]),
                np.array([0.7, 0.3]),
                np.array([0.4, 0.6])
            ]
        }
        
        optimizer.optimize_portfolio()
        
        # Verify optimization results
        assert optimizer.optimal_portfolio is not None
        assert optimizer.optimal_weights is not None
        assert 'risk_boundaries' in optimizer.__dict__
        
        # Check that optimal portfolio has expected structure
        assert len(optimizer.optimal_portfolio) == 2  # [return, risk]
        assert len(optimizer.optimal_weights) == len(sample_config.portfolio_tickers)
    
    def test_generate_results(self, sample_config):
        """Test results generation."""
        optimizer = PortfolioOptimizer(sample_config)
        
        # Setup mock data
        optimizer.benchmark_return = 0.001
        optimizer.benchmark_risk = 0.02
        optimizer.optimal_portfolio = np.array([0.002, 0.015])
        optimizer.optimal_weights = np.array([0.6, 0.4])
        optimizer.risk_boundaries = {
            'min_risk': 0.01,
            'max_risk': 0.025,
            'risk_gap': [0.01, 0.025]
        }
        optimizer.portfolio_scenarios = {
            'returns': np.array([0.001, 0.002, 0.0015]),
            'risks': np.array([0.02, 0.015, 0.025])
        }
        
        results = optimizer.generate_results()
        
        # Verify results structure
        assert 'optimal_portfolio' in results
        assert 'benchmark' in results
        assert 'risk_boundaries' in results
        assert 'simulation_stats' in results
        
        # Check optimal portfolio results
        optimal = results['optimal_portfolio']
        assert 'daily_return' in optimal
        assert 'daily_risk' in optimal
        assert 'annual_return' in optimal
        assert 'annual_risk' in optimal
        assert 'weights' in optimal
        
        # Check that weights are properly formatted
        assert len(optimal['weights']) == len(sample_config.portfolio_tickers)
    
    @patch('src.portfolio_optimizer.download_ticker_data')
    @patch('src.portfolio_optimizer.clean_and_match_data')
    def test_run_optimization(self, mock_clean_data, mock_download, sample_config,
                             sample_benchmark_data, sample_portfolio_data):
        """Test complete optimization workflow."""
        # Setup mocks
        mock_download.side_effect = [sample_benchmark_data, sample_portfolio_data]
        mock_clean_data.return_value = (sample_benchmark_data, sample_portfolio_data)
        
        optimizer = PortfolioOptimizer(sample_config)
        results = optimizer.run_optimization()
        
        # Verify complete workflow
        assert results is not None
        assert 'optimal_portfolio' in results
        assert 'benchmark' in results
        assert optimizer.benchmark_data is not None
        assert optimizer.portfolio_data is not None
        assert optimizer.optimal_portfolio is not None
    
    def test_get_portfolio_performance_summary(self, sample_config):
        """Test performance summary generation."""
        optimizer = PortfolioOptimizer(sample_config)
        
        # Setup mock results
        optimizer.results = {
            'optimal_portfolio': {
                'annual_return': 0.15,
                'annual_risk': 0.20,
                'weights': {'AAPL': 0.6, 'GOOG': 0.4}
            },
            'benchmark': {
                'annual_return': 0.10,
                'annual_risk': 0.18
            }
        }
        
        summary = optimizer.get_portfolio_performance_summary()
        
        assert isinstance(summary, str)
        assert "Portfolio Optimization Results" in summary
        assert "15.00%" in summary  # Annual return
        assert "20.00%" in summary  # Annual risk
        assert "AAPL" in summary
        assert "GOOG" in summary
    
    def test_get_portfolio_performance_summary_no_results(self, sample_config):
        """Test performance summary when no results are available."""
        optimizer = PortfolioOptimizer(sample_config)
        
        summary = optimizer.get_portfolio_performance_summary()
        
        assert summary == "No results available. Run optimization first."