"""
Main execution script for Portfolio Optimization.

This script provides a command-line interface and example usage
of the PortfolioOptimizer class.
"""

import argparse
import sys
import os
from pathlib import Path
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from config import PortfolioConfig, DEFAULT_CONFIG, load_config_from_env
from portfolio_optimizer import PortfolioOptimizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_custom_config(args) -> PortfolioConfig:
    """Create configuration from command line arguments."""
    config = PortfolioConfig(
        benchmark_tickers=args.benchmark.split(','),
        portfolio_tickers=args.portfolio.split(','),
        start_date=args.start_date,
        end_date=args.end_date,
        number_of_scenarios=args.scenarios,
        delta_risk=args.delta_risk,
        trade_days_per_year=args.trade_days
    )
    return config


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Portfolio Optimization using Monte Carlo Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default configuration
  python main.py
  
  # Custom portfolio and date range
  python main.py --portfolio AAPL,GOOG,MSFT --start-date 2020-01-01 --end-date 2023-12-31
  
  # More scenarios for better optimization
  python main.py --scenarios 50000 --delta-risk 0.03
        """
    )
    
    # Portfolio configuration
    parser.add_argument(
        '--benchmark', 
        default=','.join(DEFAULT_CONFIG.benchmark_tickers),
        help='Benchmark ticker symbols (comma-separated)'
    )
    parser.add_argument(
        '--portfolio', 
        default=','.join(DEFAULT_CONFIG.portfolio_tickers),
        help='Portfolio ticker symbols (comma-separated)'
    )
    parser.add_argument(
        '--start-date', 
        default=DEFAULT_CONFIG.start_date,
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--end-date', 
        default=DEFAULT_CONFIG.end_date,
        help='End date (YYYY-MM-DD)'
    )
    
    # Optimization parameters
    parser.add_argument(
        '--scenarios', 
        type=int, 
        default=DEFAULT_CONFIG.number_of_scenarios,
        help='Number of Monte Carlo scenarios'
    )
    parser.add_argument(
        '--delta-risk', 
        type=float, 
        default=DEFAULT_CONFIG.delta_risk,
        help='Risk tolerance delta (0-1)'
    )
    parser.add_argument(
        '--trade-days', 
        type=int, 
        default=DEFAULT_CONFIG.trade_days_per_year,
        help='Trading days per year'
    )
    
    # Output options
    parser.add_argument(
        '--output-dir', 
        default='output',
        help='Output directory for results'
    )
    parser.add_argument(
        '--save-results', 
        action='store_true',
        help='Save results to CSV file'
    )
    parser.add_argument(
        '--show-plot', 
        action='store_true',
        help='Display optimization plot'
    )
    parser.add_argument(
        '--save-plot', 
        action='store_true',
        help='Save optimization plot to file'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create configuration
        if args.portfolio != ','.join(DEFAULT_CONFIG.portfolio_tickers) or \
           args.start_date != DEFAULT_CONFIG.start_date or \
           args.end_date != DEFAULT_CONFIG.end_date:
            config = create_custom_config(args)
        else:
            config = DEFAULT_CONFIG
        
        logger.info("Starting Portfolio Optimization")
        logger.info(f"Configuration: {config}")
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Initialize optimizer
        optimizer = PortfolioOptimizer(config)
        
        # Run optimization
        results = optimizer.run_optimization()
        
        # Print results summary
        print(optimizer.get_portfolio_performance_summary())
        
        # Save results if requested
        if args.save_results:
            results_file = output_dir / "portfolio_results.csv"
            optimizer.save_results(str(results_file))
            logger.info(f"Results saved to {results_file}")
        
        # Create and handle visualization
        if args.show_plot or args.save_plot:
            fig = optimizer.create_visualization()
            
            if args.save_plot:
                plot_file = output_dir / "portfolio_optimization.png"
                fig.savefig(plot_file, dpi=300, bbox_inches='tight')
                logger.info(f"Plot saved to {plot_file}")
            
            if args.show_plot:
                import matplotlib.pyplot as plt
                plt.show()
        
        # Create summary table
        summary_table = optimizer.create_summary_table()
        print("\nPortfolio Allocation Summary:")
        print(summary_table.to_string(index=False, formatters={
            'Stock % in Portfolio': '{:.2%}'.format
        }))
        
        logger.info("Portfolio optimization completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Optimization interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
        sys.exit(1)


def run_example():
    """Run a simple example with default configuration."""
    print("Running Portfolio Optimization Example")
    print("=" * 50)
    
    # Use default configuration
    config = DEFAULT_CONFIG
    optimizer = PortfolioOptimizer(config)
    
    # Run optimization
    results = optimizer.run_optimization()
    
    # Print results
    print(optimizer.get_portfolio_performance_summary())
    
    # Create visualization
    fig = optimizer.create_visualization()
    
    # Create summary table
    summary_table = optimizer.create_summary_table()
    print("\nPortfolio Allocation Summary:")
    print(summary_table.to_string(index=False, formatters={
        'Stock % in Portfolio': '{:.2%}'.format
    }))
    
    return results


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run example
        run_example()
    else:
        # Run with command line arguments
        main()