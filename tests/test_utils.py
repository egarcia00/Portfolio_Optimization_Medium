"""
Tests for utility functions.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from src.utils import (
    calculate_returns_and_risk, generate_random_portfolio_weights,
    calculate_portfolio_metrics, annualize_metrics, find_optimal_portfolio
)


class TestCalculateReturnsAndRisk:
    """Test cases for calculate_returns_and_risk function."""
    
    def test_calculate_returns_and_risk_basic(self):
        """Test basic calculation of returns and risk."""
        # Create simple price data
        prices = np.array([100, 105, 102, 108, 110])
        
        return_rate, risk = calculate_returns_and_risk(prices)
        
        # Calculate expected returns manually
        expected_returns = np.array([0.05, -0.02857, 0.05882, 0.01852])
        expected_return = np.mean(expected_returns)
        expected_risk = np.std(expected_returns)
        
        assert abs(return_rate - expected_return) < 1e-6
        assert abs(risk - expected_risk) < 1e-6
    
    def test_calculate_returns_and_risk_constant_prices(self):
        """Test calculation with constant prices (no returns)."""
        prices = np.array([100, 100, 100, 100])
        
        return_rate, risk = calculate_returns_and_risk(prices)
        
        assert return_rate == 0.0
        assert risk == 0.0


class TestGenerateRandomPortfolioWeights:
    """Test cases for generate_random_portfolio_weights function."""
    
    def test_generate_random_portfolio_weights(self):
        """Test random portfolio weight generation."""
        n_assets = 3
        weights = generate_random_portfolio_weights(n_assets)
        
        # Check that weights sum to 1
        assert abs(np.sum(weights) - 1.0) < 1e-10
        
        # Check that all weights are positive
        assert np.all(weights >= 0)
        
        # Check correct number of assets
        assert len(weights) == n_assets
    
    def test_generate_random_portfolio_weights_single_asset(self):
        """Test weight generation for single asset."""
        weights = generate_random_portfolio_weights(1)
        
        assert len(weights) == 1
        assert abs(weights[0] - 1.0) < 1e-10


class TestCalculatePortfolioMetrics:
    """Test cases for calculate_portfolio_metrics function."""
    
    def test_calculate_portfolio_metrics(self):
        """Test portfolio metrics calculation."""
        # Create simple test data
        weights = np.array([0.5, 0.5])
        asset_prices = np.array([
            [100, 105, 102, 108],  # Asset 1
            [200, 210, 204, 216]   # Asset 2
        ])
        
        portfolio_return, portfolio_risk = calculate_portfolio_metrics(weights, asset_prices)
        
        # Calculate expected portfolio prices
        expected_portfolio_prices = np.array([150, 157.5, 153, 162])
        expected_returns = np.array([0.05, -0.02857, 0.05882])
        
        expected_return = np.mean(expected_returns)
        expected_risk = np.std(expected_returns)
        
        assert abs(portfolio_return - expected_return) < 1e-6
        assert abs(portfolio_risk - expected_risk) < 1e-6


class TestAnnualizeMetrics:
    """Test cases for annualize_metrics function."""
    
    def test_annualize_metrics(self):
        """Test annualization of metrics."""
        daily_return = 0.001
        daily_risk = 0.02
        trade_days = 252
        
        annual_return, annual_risk = annualize_metrics(daily_return, daily_risk, trade_days)
        
        assert annual_return == daily_return * trade_days
        assert annual_risk == daily_risk * trade_days
    
    def test_annualize_metrics_custom_trade_days(self):
        """Test annualization with custom trade days."""
        daily_return = 0.001
        daily_risk = 0.02
        trade_days = 250
        
        annual_return, annual_risk = annualize_metrics(daily_return, daily_risk, trade_days)
        
        assert annual_return == 0.25
        assert annual_risk == 5.0


class TestFindOptimalPortfolio:
    """Test cases for find_optimal_portfolio function."""
    
    def test_find_optimal_portfolio_with_acceptable_risk(self):
        """Test finding optimal portfolio when risk constraint is satisfied."""
        # Create test data with some portfolios within risk constraint
        portfolio_array = np.array([
            [0.1, 0.05],  # High return, low risk
            [0.08, 0.03], # Medium return, very low risk
            [0.12, 0.08], # High return, high risk
            [0.06, 0.04], # Low return, medium risk
        ])
        
        max_risk = 0.06
        min_risk = 0.03
        
        best_portfolio, portfolio_idx = find_optimal_portfolio(portfolio_array, max_risk, min_risk)
        
        # Should select portfolio with highest return within risk constraint
        assert portfolio_idx == 0  # [0.1, 0.05] has highest return within constraint
        assert np.array_equal(best_portfolio, portfolio_array[0])
    
    def test_find_optimal_portfolio_no_acceptable_risk(self):
        """Test finding optimal portfolio when no portfolios meet risk constraint."""
        # Create test data with all portfolios exceeding risk constraint
        portfolio_array = np.array([
            [0.1, 0.08],  # High return, high risk
            [0.08, 0.07], # Medium return, high risk
            [0.12, 0.09], # High return, very high risk
            [0.06, 0.08], # Low return, high risk
        ])
        
        max_risk = 0.05
        min_risk = 0.07
        
        best_portfolio, portfolio_idx = find_optimal_portfolio(portfolio_array, max_risk, min_risk)
        
        # Should select minimum risk portfolio with highest return
        assert portfolio_idx == 1  # [0.08, 0.07] has highest return among min risk portfolios
        assert np.array_equal(best_portfolio, portfolio_array[1])
