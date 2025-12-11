# Build Fellowship Final Project
## SMA Trend-Following Strategy with External VIX CSV Data (QuantConnect)
### By Madhumitha Bharadwaj

## 1. Project Overview

This project implements a simple and interpretable trend-following strategy using QuantConnect’s Lean engine.  
The strategy trades SPY based on the relationship between two moving averages:

- SMA 50 (fast)
- SMA 200 (slow)

Trading Logic:
- Enter a long position when SMA 50 crosses above SMA 200.
- Exit the position when SMA 50 crosses below SMA 200.
- Apply a 5 percent stop-loss to manage risk.
- Load external VIX data from a CSV file using a custom PythonData class.


## 2. Trading Thesis

Markets tend to exhibit long-term trends. A basic and widely used approach to capture these trends is comparing short-term and long-term moving averages.

Thesis:  
When the 50-day moving average is above the 200-day moving average, the market is in a long-term uptrend. In an uptrend, the strategy holds SPY. When the trend weakens, the strategy exits to protect capital.

## 3. External Data Used (VIX CSV)

To satisfy the requirement for integrating external data, this project includes:
- A custom dataset: vix_daily.csv
- A PythonData class: custom_data_vix.py

Purpose of external data:  
Although the final strategy does not enforce a VIX filter, the custom CSV data integration demonstrates the ability to load, parse, and use external data files safely.

CSV Format Example:
date,value  
2018-01-02,9.77  
2020-03-16,82.69

## 4. Failure-Mode Preparation

The algorithm includes several mechanisms to handle potential failures:

1. Missing CSV file  
   The algorithm disables VIX usage and continues running.

2. Invalid CSV rows  
   Rows with incorrect formatting are skipped without stopping the strategy.

3. Missing daily VIX value  
   The strategy uses the most recent known value or defaults to continuing without applying a filter.

4. Indicator warm-up  
   The algorithm waits until SMA indicators are fully ready before trading.

5. Drawdown risk control  
   A 5 percent stop-loss ensures large losses are avoided.

## 5. File Structure

week-final-madhumitha/  
    main.py  
    custom_data_vix.py  
    Pensive Blue Seahorse.json  
    README.md  
    data/  
        vix_daily.csv  

## 6. Backtest Summary (2018–2024)

Metrics from the QuantConnect backtest:

Net Profit: approximately 5,858 USD  
Total Return: approximately 25.13 percent  
Sharpe Ratio: approximately 0.099  
Sortino Ratio: approximately 0.078  
Maximum Drawdown: approximately 40.50 percent  
Win Rate: approximately 43 percent  
Number of Trades: 15  
Profit/Loss Ratio: 1.89  
Portfolio Turnover: 0.66 percent  

These results show that the strategy follows long-term trends, limits exposure during downtrends, and provides interpretable performance.  
The full backtest export is included in the file: Report.pdf
## 7. Strategy Logic (Simplified)

1. If SMA50 > SMA200  
   Enter a long position in SPY.

2. If SMA50 < SMA200  
   Exit the position.

3. If unrealized loss exceeds 5 percent  
   Trigger stop-loss and exit.

External VIX data is loaded and processed but does not restrict trades in the final submission for stability.

## 8. How External Data Is Integrated

The file custom_data_vix.py defines a PythonData class that tells Lean how to read the CSV file.  
The system reads:

- Date  
- VIX value  

and maps it to a custom data symbol.  
The algorithm handles errors and missing data safely.

## 9. Limitations and Future Improvements

Limitations:
- SMA signals can lag during volatile markets.
- The return is modest but stable.
- The CSV dataset is small and intended for demonstration.
- Stop-losses may trigger during sharp market pullbacks.

Potential improvements:
- Use exponential moving averages instead of SMAs.
- Improve volatility-based position sizing.
- Use a complete VIX historical dataset.
- Add additional trend filters or exit conditions.

## 10. Conclusion

This project demonstrates practical algorithmic trading concepts including:
- A clear trading logic  
- Integration of external data  
- Robust failure handling  
- A complete backtest  
- Clean code structure  

