# AI Hedge Fund


用 7 個 AI Agent 分工來模擬的避險基金（hedge fund) 
基於 langchainai 開發，其中透過底下這6個 AI Agent 來實現這個 hedge fund ：

1. 市場資料分析師 - 收集和預先處理市場資料
2. 估值 Agent - 計算股票的內在價值，分析公司獲利能力、成長性、財務健康狀況和估值並產生交易信號
3. 情緒 Agent - 分析市場情緒並產生交易信號
4. 基本面 Agent - 分析基本面數據並產生交易信號
5. 技術分析師 - 分析技術指標（如 MACD、RSI、Bollinger Bands）等並產生交易信號
6. 風險管理員 - 計算風險指標（如波動率、最大回撤等）並設定持倉限制
7. 投資組合經理 - 作出最終交易決策並產生訂單

每個 agent 都會展示其推理過程，讓你清楚了解它們的運作方式
   
This system employs several agents working together:

1. Market Data Analyst - Gathers and preprocesses market data
2. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
3. Sentiment Agent - Analyzes market sentiment and generates trading signals
4. Fundamentals Agent - Analyzes fundamental data and generates trading signals
5. Technical Analyst - Analyzes technical indicators and generates trading signals
6. Risk Manager - Calculates risk metrics and sets position limits
7. Portfolio Manager - Makes final trading decisions and generates orders

![Screenshot 2024-12-27 at 5 49 56 PM](https://github.com/user-attachments/assets/c281b8c3-d8e6-431e-a05e-d309d306e967)



## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Setup

Clone the repository:
```bash
git clone https://github.com/Investment-Analyst/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env

export OPENAI_API_KEY='your-api-key-here' # Get a key from https://platform.openai.com/
export FINANCIAL_DATASETS_API_KEY='your-api-key-here' # Get a key from https://financialdatasets.ai/
```

## Usage

### Running the Hedge Fund

```bash
poetry run python src/main.py --ticker AAPL
```

**Example Output:**
```
Final Result:
{
    "action": "hold",
    "quantity": 0,
    "confidence": 0.63,
    "agent_signals": [
        {
            "agent_name": "Valuation Analysis",
            "signal": "bearish",
            "confidence": 0.82
        },
        {
            "agent_name": "Fundamental Analysis",
            "signal": "bearish",
            "confidence": 0.5
        },
        {
            "agent_name": "Technical Analysis",
            "signal": "bullish",
            "confidence": 0.24
        },
        {
            "agent_name": "Sentiment Analysis",
            "signal": "bearish",
            "confidence": 1.0
        }
    ],
    "reasoning": "The risk management constraints require a bearish action, but since the current position is 0 shares, selling is 
not possible. Valuation Analysis provides a strong bearish signal with 82% confidence due to significant overvaluation. Fundamental
 Analysis also supports a bearish stance with concerns over growth and high price ratios. Sentiment is unanimously bearish with 100
% confidence. Technical Analysis is bullish but holds the least weight and confidence. Given these factors, the decision is to hold, with no buy or sell action possible due to portfolio constraints."
}
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
poetry run python src/main.py --ticker AAPL --show-reasoning
```

**Example Output:**
```

==========  Fundamental Analysis Agent  ==========
{
  "signal": "bearish",
  "confidence": "50%",
  "reasoning": {
    "profitability_signal": {
      "signal": "bullish",
      "details": "ROE: 137.90%, Net Margin: 24.00%, Op Margin: 31.58%"
    },
    "growth_signal": {
      "signal": "bearish",
      "details": "Revenue Growth: 1.41%, Earnings Growth: -8.06%"
    },
    "financial_health_signal": {
      "signal": "neutral",
      "details": "Current Ratio: 0.87, D/E: 5.41"
    },
    "price_ratios_signal": {
      "signal": "bearish",
      "details": "P/E: 36.95, P/B: 60.81, P/S: 8.86"
    }
  }
}

==========   Valuation Analysis Agent   ==========================================================

{
  "signal": "bearish",
  "confidence": "82%",
  "reasoning": {
    "dcf_analysis": {
      "signal": "bearish",
      "details": "Intrinsic Value: $1,066,951,000,140.94, Market Cap: $3,785,304,395,660.00, Gap: -71.8%"
    },
    "owner_earnings_analysis": {
      "signal": "bearish",
      "details": "Owner Earnings Value: $329,466,172,364.20, Market Cap: $3,785,304,395,660.00, Gap: -91.3%"
    }
  }
}
================================================

==========   Sentiment Analysis Agent   ==========
{
  "signal": "bearish",
  "confidence": "100%",
  "reasoning": "Bullish signals: 0, Bearish signals: 4"
}
================================================

==========      Technical Analyst       ==========
{
  "signal": "bullish",
  "confidence": "24%",
  "strategy_signals": {
    "trend_following": {
      "signal": "bullish",
      "confidence": "47%",
      "metrics": {
        "adx": 46.965186241303456,
        "trend_strength": 0.4696518624130346
      }
    },
    "mean_reversion": {
      "signal": "neutral",
      "confidence": "50%",
      "metrics": {
        "z_score": 1.1464485714115078,
        "price_vs_bb": 0.5301399395699092,
        "rsi_14": 53.982566877066404,
        "rsi_28": 70.35674880470765
      }
    },
    "momentum": {
      "signal": "neutral",
      "confidence": "50%",
      "metrics": {
        "momentum_1m": 0.054807993022794266,
        "momentum_3m": NaN,
        "momentum_6m": NaN,
        "volume_momentum": 0.7967340841582854
      }
    },
    "volatility": {
      "signal": "neutral",
      "confidence": "50%",
      "metrics": {
        "historical_volatility": 0.16263301280136414,
        "volatility_regime": NaN,
        "volatility_z_score": NaN,
        "atr_ratio": 0.017527696327312967
      }
    },
    "statistical_arbitrage": {
      "signal": "neutral",
      "confidence": "50%",
      "metrics": {
        "hurst_exponent": 4.686994974318529e-16,
        "skewness": NaN,
        "kurtosis": NaN
      }
    }
  }
}
================================================

==========    Risk Management Agent     ==========
{
  "max_position_size": 25000.0,
  "risk_score": 4,
  "trading_action": "bearish",
  "risk_metrics": {
    "volatility": 0.16928687183949434,
    "value_at_risk_95": -0.018062898239189856,
    "max_drawdown": -0.061189106901217816,
    "market_risk_score": 0,
    "stress_test_results": {
      "market_crash": {
        "potential_loss": -0.0,
        "portfolio_impact": -0.0
      },
      "moderate_decline": {
        "potential_loss": -0.0,
        "portfolio_impact": -0.0
      },
      "slight_decline": {
        "potential_loss": -0.0,
        "portfolio_impact": -0.0
      }
    }
  },
  "reasoning": "Risk Score 4/10: Market Risk=0, Volatility=16.93%, VaR=-1.81%, Max Drawdown=-6.12%"
}
================================================

==========  Portfolio Management Agent  ==========
{
  "action": "hold",
  "quantity": 0,
  "confidence": 0.1,
  "agent_signals": [
    {
      "agent_name": "Valuation Analysis",
      "signal": "bearish",
      "confidence": 0.82
    },
    {
      "agent_name": "Fundamental Analysis",
      "signal": "bearish",
      "confidence": 0.5
    },
    {
      "agent_name": "Technical Analysis",
      "signal": "bullish",
      "confidence": 0.24
    },
    {
      "agent_name": "Sentiment Analysis",
      "signal": "bearish",
      "confidence": 1.0
    }
  ],
  "reasoning": "Risk management constraints dictate a bearish action. Valuation, fundamental, and sentiment analyses are all bearish, outweighing the technical analysis' bullish signal. Without current shares to sell, holding is the most prudent action."        
}
================================================

Final Result:
{
    "action": "hold",
    "quantity": 0,
    "confidence": 0.1,
    "agent_signals": [
        {
            "agent_name": "Valuation Analysis",
            "signal": "bearish",
            "confidence": 0.82
        },
        {
            "agent_name": "Fundamental Analysis",
            "signal": "bearish",
            "confidence": 0.5
        },
        {
            "agent_name": "Technical Analysis",
            "signal": "bullish",
            "confidence": 0.24
        },
        {
            "agent_name": "Sentiment Analysis",
            "signal": "bearish",
            "confidence": 1.0
        }
    ],
    "reasoning": "Risk management constraints dictate a bearish action. Valuation, fundamental, and sentiment analyses are all bearish, outweighing the technical analysis' bullish signal. Without current shares to sell, holding is the most prudent action."      
}

```
You can optionally specify the start and end dates to make decisions for a specific time period.

```bash
poetry run python src/main.py --ticker AAPL --start-date 2024-01-01 --end-date 2025-01-01 
```

**Example Output:**
```

Final Result:
{
    "action": "hold",
    "quantity": 0,
    "confidence": 0.82,
    "agent_signals": [
        {
            "agent": "Technical Analysis",
            "signal": "bullish",
            "confidence": 0.24
        },
        {
            "agent": "Fundamental Analysis",
            "signal": "bearish",
            "confidence": 0.50
        },
        {
            "agent": "Sentiment Analysis",
            "signal": "bearish",
            "confidence": 1.00
        },
        {
            "agent": "Valuation Analysis",
            "signal": "bearish",
            "confidence": 0.82
        }
    ],
    "reasoning": "The risk management constraints require a 'hold' action. The dominant bearish signals from valuation (82% confide
nce) and sentiment (100% confidence) outweigh the bullish technical signal (24% confidence). Fundamental analysis is also bearish. Thus, despite the technical bullish signal, the overall bearish sentiment and valuation drive the decision to hold."

```
### Running the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL
```

**Example Output:**
```
Starting backtest...
Date         Ticker Action Quantity    Price         Cash    Stock  Total Value
----------------------------------------------------------------------
2024-01-01   AAPL   buy       519.0   192.53        76.93    519.0    100000.00
2024-01-02   AAPL   hold          0   185.64        76.93    519.0     96424.09
2024-01-03   AAPL   hold          0   184.25        76.93    519.0     95702.68
2024-01-04   AAPL   hold          0   181.91        76.93    519.0     94488.22
2024-01-05   AAPL   hold          0   181.18        76.93    519.0     94109.35
2024-01-08   AAPL   sell        519   185.56     96382.57      0.0     96382.57
2024-01-09   AAPL   buy       520.0   185.14       109.77    520.0     96382.57
```

You can optionally specify the start and end dates to backtest over a specific time period.

```bash
poetry run python src/backtester.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-03-01
```

## Project Structure 
```
ai-hedge-fund/
├── src/
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── fundamentals.py       # Fundamental analysis agent
│   │   ├── market_data.py        # Market data agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── state.py              # Agent state
│   │   ├── technicals.py         # Technical analysis agent
│   │   ├── valuation.py          # Valuation analysis agent
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py # Main entry point
├── pyproject.toml
├── ...
```

