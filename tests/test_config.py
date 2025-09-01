"""
Tests for configuration module.
"""

import pytest
import os
from src.config import PortfolioConfig, DEFAULT_CONFIG, load_config_from_env


class TestPortfolioConfig:
    """Test cases for PortfolioConfig class."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = PortfolioConfig(
            benchmark_tickers=["^GSPC"],
            portfolio_tickers=['AAPL', 'GOOG', 'AMZN'],
            start_date="2017-01-01",
            end_date="2022-03-31"
        )
        
        assert config.benchmark_tickers == ["^GSPC"]
        assert config.portfolio_tickers == ['AAPL', 'GOOG', 'AMZN']
        assert config.start_date == "2017-01-01"
        assert config.end_date == "2022-03-31"
        assert config.number_of_scenarios == 10000
        assert config.delta_risk == 0.05
        assert config.trade_days_per_year == 252
    
    def test_config_validation(self):
        """Test configuration parameter validation."""
        # Test negative scenarios
        with pytest.raises(ValueError, match="number_of_scenarios must be positive"):
            PortfolioConfig(
                benchmark_tickers=["^GSPC"],
                portfolio_tickers=['AAPL'],
                start_date="2020-01-01",
                end_date="2021-01-01",
                number_of_scenarios=-1
            )
        
        # Test invalid delta_risk
        with pytest.raises(ValueError, match="delta_risk must be between 0 and 1"):
            PortfolioConfig(
                benchmark_tickers=["^GSPC"],
                portfolio_tickers=['AAPL'],
                start_date="2020-01-01",
                end_date="2021-01-01",
                delta_risk=1.5
            )
        
        # Test negative trade days
        with pytest.raises(ValueError, match="trade_days_per_year must be positive"):
            PortfolioConfig(
                benchmark_tickers=["^GSPC"],
                portfolio_tickers=['AAPL'],
                start_date="2020-01-01",
                end_date="2021-01-01",
                trade_days_per_year=0
            )
    
    def test_default_config_object(self):
        """Test DEFAULT_CONFIG object."""
        assert isinstance(DEFAULT_CONFIG, PortfolioConfig)
        assert DEFAULT_CONFIG.benchmark_tickers == ["^GSPC"]
        assert DEFAULT_CONFIG.portfolio_tickers == ['AAPL', 'GOOG', 'AMZN']


class TestLoadConfigFromEnv:
    """Test cases for loading configuration from environment variables."""
    
    def test_load_config_with_defaults(self):
        """Test loading config with default values."""
        # Clear environment variables
        env_vars = [
            'BENCHMARK_TICKERS', 'PORTFOLIO_TICKERS', 'START_DATE', 
            'END_DATE', 'NUMBER_OF_SCENARIOS', 'DELTA_RISK', 'TRADE_DAYS_PER_YEAR'
        ]
        
        original_values = {}
        for var in env_vars:
            original_values[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]
        
        try:
            config = load_config_from_env()
            assert config.benchmark_tickers == ['^GSPC']
            assert config.portfolio_tickers == ['AAPL', 'GOOG', 'AMZN']
            assert config.start_date == '2017-01-01'
            assert config.end_date == '2022-03-31'
        finally:
            # Restore original environment variables
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value
                elif var in os.environ:
                    del os.environ[var]
    
    def test_load_config_with_env_vars(self):
        """Test loading config with environment variables set."""
        # Set environment variables
        os.environ['BENCHMARK_TICKERS'] = '^DJI'
        os.environ['PORTFOLIO_TICKERS'] = 'MSFT,TSLA'
        os.environ['START_DATE'] = '2020-01-01'
        os.environ['END_DATE'] = '2023-01-01'
        os.environ['NUMBER_OF_SCENARIOS'] = '5000'
        os.environ['DELTA_RISK'] = '0.1'
        os.environ['TRADE_DAYS_PER_YEAR'] = '250'
        
        try:
            config = load_config_from_env()
            assert config.benchmark_tickers == ['^DJI']
            assert config.portfolio_tickers == ['MSFT', 'TSLA']
            assert config.start_date == '2020-01-01'
            assert config.end_date == '2023-01-01'
            assert config.number_of_scenarios == 5000
            assert config.delta_risk == 0.1
            assert config.trade_days_per_year == 250
        finally:
            # Clean up environment variables
            for var in ['BENCHMARK_TICKERS', 'PORTFOLIO_TICKERS', 'START_DATE', 
                       'END_DATE', 'NUMBER_OF_SCENARIOS', 'DELTA_RISK', 'TRADE_DAYS_PER_YEAR']:
                if var in os.environ:
                    del os.environ[var]