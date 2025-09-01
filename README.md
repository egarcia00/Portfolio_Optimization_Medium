<<<<<<< Current (Your changes)
# Portfolio_Optimization_Medium
A code that helps you run scenarios to assess which stock create the best portfolio at minimum risk and maximum return with past information.
---

If you don't have any Idea how to create a stock portfolio, this will help you.
Big disclosure, I'm not any financial advice. 
This is an exercise on how to create a portfolio testing 10,000 combination of stocks, and finding if there was one combination that has:
Better Returns than the Market
Has the Same or lower Risk

For this we need 
Market Benchmark: We need to define what we will consider as our market benchmark. This will be the financial asset we will compare returns and risk against our portfolio. 
Portfolio of Stocks: we will use any list of stocks, commodities, etc. In my case, I will use some random stocks that I know. Again, this list is no financial advice. (I promise this is the last "warning" over this😅)

Let's start our journey.
Tools to use
We will be working with Python and the following packages:

Packages used for this projectAlso we need a function called download you can check the link of the website from Analyzing Alpha. 

Step 1: Setting Up our Variables
Now we need to set some key variables. 
Benchmark: in this case S&P 500 that is represented by "^GSPC"
Portfolio: List of stocks we're analyzing.
Start Date: When do we want to start analyzing the data
End Date: When do we want to finish analyzing the data
Number of Scenarios: How many random combinations we want to test. 
Output Lists: We need a place to store our Return, Risk, and Portfolios Distribution (Combinations). 

Technical disclaimer: All this exercise can be done with functions or classes, it's a WIPStep 2: Downloading and Cleaning the Data
We will download all the financial data from our benchmark (df) and portfolio (df2) from the start to end date.
After downloading the data, we need to drop all empty values. I did it this way for simplicity, but you could have a different approach if you want.

Step 3: Analyzing our Market Benchmark
Now with our clean data we select the variable we want. To familiarize yourself with the data, let me show you what download function recovers from any stock:
In this case we will be using "Close" which is the last price traded of this stock at the end of a day.
Now we procede to select the information, calculate our daily returns and add the Benchmark Return and Risk to our lists:

The daily returns are the variation of the Close price between two days. 
Step 4: Analyze our Portfolio Data
We follow the same procedure as the previous step but with 2 extras.
We need to create a loop/sequence that will do this exercise 10,000 times.
We need to create a random distribution for generating each portfolio and making it unique.

You can do this with the following code:

Step 5: Select the Best Portfolio
The criterion for the best portfolio is to have the minimum risk, meaning that the stock is at least as volatile as the market. For understanding the risk we've being using the Standard Deviation. I leave you a link to Investopedia that can help.
And once we have calculated this "minimum risk" we will find the highest return possible. This way we are finding a porfolio that in the past has performed better than the market.
Step 6: Let's do some visuals
We're going to plot the risk on the x-axis and the return on the y-axis
In this next image, you can see the market performing (red dot) and then the maximum return at the minimum risk. Meaning that if you would've held that portfolio between start and end date, you would've had a better portfolio than the market benchmark.
This graph will depend to the stocks that you want to analyze. For example if we choose only Apple, Google and Amazon Stocks, our exercise looks like this:
Where the stocks we selected had higher returns (y-axis) but also higher risk (x-axis)

---

As mentioned, this is not a tool to start your analysis on the portfolio you want to build, and is only showing what happened in the past, not trying to find what is happening in the future.
The optimization power of a simple code is what really amazed me while going through this exercise, because we can map and evaluate complex decisions in a brief period.
=======
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
>>>>>>> Incoming (Background Agent changes)
