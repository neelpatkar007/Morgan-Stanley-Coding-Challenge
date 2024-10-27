# Morgan Stanley Trading Game

This repository hosts the code and strategy developed for the Morgan Stanley Trading Game. The game challenges participants to navigate FX trading for a $1M portfolio between EUR and GBP while managing risks associated with simulated Brexit-driven events. This README provides an overview of the approach, setup, and insights gained.

## 📘 Game Overview

The goal is to maximize profits by trading EUR and GBP in response to two main events: a simulated crash and a bounce in GBP value. During each event:
- **Crash:** The value of GBP drops, making EUR relatively more valuable.
- **Bounce:** GBP regains value, reversing the previous trend.

Our objective is to leverage these events by strategically timing trades to optimize currency holdings and profit margins.

## ⚙️ Rules Summary
- **Trade Volume**: Limited to 100,000 shares per transaction.
- **Frequency Limit**: No more than one trade per second.
- **Currency Holding Requirement**: 30% minimum in EUR at the end.
- **Goal**: Maximize profitability.

## 🧠 Strategy

The core strategy is based on detecting and reacting to GBP’s crash and bounce events using a mix of moving averages and threshold-based signal detection.

### Key Steps
1. **API Setup**: Initialize API access for price feeds and trade placements.
2. **Signal Detection**:
   - Use moving averages to smooth price fluctuations and identify trend reversals.
   - Implement thresholds for detecting sharp price changes associated with crash and bounce events.
3. **Automated Trades**:
   - Place orders as soon as signals for significant price movement (crash or bounce) are detected.
   - Sell GBP for EUR during a crash, then buy back GBP during the bounce.
4. **Portfolio Management**:
   - Track holdings to maintain at least 30% EUR.
   - Log trades and price data for real-time analysis.

### Considerations
- **Data Logging**: Continuous logging of price feeds helps to track strategy effectiveness and refine signal detection.
- **Trade Frequency**: Ensure no trades exceed the frequency limit by implementing delay mechanisms between orders.

## 🏆 Outcome Goals
The main outcomes pursued are:
- **Profit Maximization**: Exploit volatility to increase portfolio value.
- **Best Strategy**: Achieve a robust, clean trading strategy and implementation.

## 💡 Insights

- **Event-Based Trading**: Focused on identifying crash and bounce patterns to capture high-profit trades.
- **Balancing Simplicity and Accuracy**: A straightforward approach using moving averages offers clear signals without overfitting to random price noise.
