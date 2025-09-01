# Portfolio Optimization

A comprehensive Python package for portfolio optimization using Monte Carlo simulation. This tool helps investors find optimal portfolio allocations by simulating thousands of random portfolio combinations and selecting the best performer based on risk-return criteria.

## Features

- **Monte Carlo Simulation**: Generate thousands of random portfolio combinations
- **Risk-Return Analysis**: Optimize portfolios based on risk constraints
- **Benchmark Comparison**: Compare portfolio performance against market benchmarks
- **Visualization**: Create scatter plots showing portfolio scenarios and optimal selection
- **Flexible Configuration**: Customize tickers, date ranges, and optimization parameters
- **Command Line Interface**: Easy-to-use CLI for quick analysis
- **Comprehensive Testing**: Full test coverage with pytest

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/portfolio-optimization.git
cd portfolio-optimization
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Using pip (when published)

```bash
pip install portfolio-optimization
```

## Quick Start

### Command Line Usage

Run with default configuration (AAPL, GOOG, AMZN from 2017-2022):
```bash
python src/main.py
```

Run with custom portfolio and parameters:
```bash
python src/main.py --portfolio AAPL,GOOG,MSFT,TSLA --start-date 2020-01-01 --end-date 2023-12-31 --scenarios 20000
```

### Python API Usage

```python
from src.config import PortfolioConfig
from src.portfolio_optimizer import PortfolioOptimizer

# Create configuration
config = PortfolioConfig(
    benchmark_tickers=["^GSPC"],
    portfolio_tickers=['AAPL', 'GOOG', 'AMZN', 'MSFT'],
    start_date="2020-01-01",
    end_date="2023-12-31",
    number_of_scenarios=10000
)

# Run optimization
optimizer = PortfolioOptimizer(config)
results = optimizer.run_optimization()

# Print results
print(optimizer.get_portfolio_performance_summary())

# Create visualization
fig = optimizer.create_visualization()
fig.show()

# Get portfolio allocation table
table = optimizer.create_summary_table()
print(table)
```

## Configuration

### PortfolioConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `benchmark_tickers` | List[str] | `["^GSPC"]` | Benchmark ticker symbols |
| `portfolio_tickers` | List[str] | `['AAPL', 'GOOG', 'AMZN']` | Portfolio ticker symbols |
| `start_date` | str | `"2017-01-01"` | Start date (YYYY-MM-DD) |
| `end_date` | str | `"2022-03-31"` | End date (YYYY-MM-DD) |
| `number_of_scenarios` | int | `10000` | Number of Monte Carlo scenarios |
| `delta_risk` | float | `0.05` | Risk tolerance delta (0-1) |
| `trade_days_per_year` | int | `252` | Trading days per year |

### Environment Variables

You can also configure the optimizer using environment variables:

```bash
export BENCHMARK_TICKERS="^GSPC"
export PORTFOLIO_TICKERS="AAPL,GOOG,MSFT"
export START_DATE="2020-01-01"
export END_DATE="2023-12-31"
export NUMBER_OF_SCENARIOS="15000"
export DELTA_RISK="0.03"
```

## Command Line Options

```bash
python src/main.py --help
```

### Available Options

- `--benchmark`: Benchmark ticker symbols (comma-separated)
- `--portfolio`: Portfolio ticker symbols (comma-separated)
- `--start-date`: Start date (YYYY-MM-DD)
- `--end-date`: End date (YYYY-MM-DD)
- `--scenarios`: Number of Monte Carlo scenarios
- `--delta-risk`: Risk tolerance delta (0-1)
- `--trade-days`: Trading days per year
- `--output-dir`: Output directory for results
- `--save-results`: Save results to CSV file
- `--show-plot`: Display optimization plot
- `--save-plot`: Save optimization plot to file
- `--verbose`: Enable verbose logging

## Project Structure

```
portfolio-optimization/
├── src/                          # Source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── portfolio_optimizer.py    # Main optimization class
│   ├── utils.py                  # Utility functions
│   └── main.py                   # Command line interface
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_utils.py
│   └── test_portfolio_optimizer.py
├── docs/                         # Documentation
├── data/                         # Data storage
├── requirements.txt              # Dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

## Algorithm

The portfolio optimization uses the following approach:

1. **Data Collection**: Download historical price data for benchmark and portfolio assets
2. **Benchmark Analysis**: Calculate benchmark return and risk metrics
3. **Monte Carlo Simulation**: Generate random portfolio weights using Dirichlet distribution
4. **Portfolio Evaluation**: Calculate return and risk for each simulated portfolio
5. **Optimization**: Select optimal portfolio based on risk constraints:
   - If portfolios exist within risk tolerance: select highest return
   - Otherwise: select highest return among minimum risk portfolios
6. **Results**: Generate comprehensive analysis and visualization

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_portfolio_optimizer.py
```

## Development

### Setting up Development Environment

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e .[dev]
```

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Run formatting and linting:
```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Dependencies

### Core Dependencies
- `yfinance`: Yahoo Finance data download
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `matplotlib`: Data visualization

### Optional Dependencies
- `scipy`: Scientific computing
- `seaborn`: Statistical data visualization
- `plotly`: Interactive plots

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational and research purposes only. It should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment decisions.

## Acknowledgments

- Yahoo Finance for providing free financial data
- The Python community for excellent open-source libraries
- Modern Portfolio Theory for the theoretical foundation

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/portfolio-optimization/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## Changelog

### Version 1.0.0
- Initial release
- Monte Carlo portfolio optimization
- Command line interface
- Comprehensive test suite
- Documentation and examples