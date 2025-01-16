from langchain_core.messages import HumanMessage
from agents.state import AgentState, show_agent_reasoning
from tools.api import get_insider_trades, get_news_sentiment
import pandas as pd
import numpy as np
import json


##### Sentiment Agent #####
def sentiment_agent(state: AgentState):
    """Analyzes market sentiment and generates trading signals."""
    data = state["data"]
    insider_trades = data.get("insider_trades", [])
    ticker = data["ticker"]
    show_reasoning = state["metadata"].get("show_reasoning", False)

    # Analyze insider trades
    transaction_shares = pd.Series([t['transaction_shares'] for t in insider_trades]).dropna()
    bearish_condition = transaction_shares < 0
    signals = np.where(bearish_condition, "bearish", "bullish").tolist()

    bullish_signals = signals.count("bullish")
    bearish_signals = signals.count("bearish")

    if bullish_signals > bearish_signals:
        insider_signal = "bullish"
    elif bearish_signals > bullish_signals:
        insider_signal = "bearish"
    else:
        insider_signal = "neutral"

    # Calculate confidence level based on insider signals
    total_signals = len(signals)
    confidence = max(bullish_signals, bearish_signals) / total_signals if total_signals > 0 else 0

    insider_analysis = {
        "signal": insider_signal,
        "confidence": f"{round(confidence * 100)}%",
        "reasoning": f"Bullish signals: {bullish_signals}, Bearish signals: {bearish_signals}"
    }

    # Analyze news sentiment
    try:
        news_data = get_news_sentiment(ticker, limit=100)
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

        for news in news_data:
            sentiment = news.get("sentiment", "neutral")
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

        total_news = sum(sentiment_counts.values())
        if sentiment_counts["positive"] > sentiment_counts["negative"]:
            news_signal = "bullish"
        elif sentiment_counts["negative"] > sentiment_counts["positive"]:
            news_signal = "bearish"
        else:
            news_signal = "neutral"

        news_confidence = max(sentiment_counts.values()) / total_news if total_news > 0 else 0
        news_analysis = {
            "signal": news_signal,
            "confidence": f"{round(news_confidence * 100)}%",
            "reasoning": f"Positive: {sentiment_counts['positive']}, Neutral: {sentiment_counts['neutral']}, Negative: {sentiment_counts['negative']}"
        }
    except Exception as e:
        news_analysis = {
            "signal": "neutral",
            "confidence": "0%",
            "reasoning": f"Error fetching news sentiment: {str(e)}"
        }

    # Combine insider and news signals
    combined_signals = [insider_analysis["signal"], news_analysis["signal"]]
    if combined_signals.count("bullish") > combined_signals.count("bearish"):
        overall_signal = "bullish"
    elif combined_signals.count("bearish") > combined_signals.count("bullish"):
        overall_signal = "bearish"
    else:
        overall_signal = "neutral"

    combined_confidence = (float(insider_analysis["confidence"].strip('%')) + float(
        news_analysis["confidence"].strip('%'))) / 200

    message_content = {
        "signal": overall_signal,
        "confidence": f"{round(combined_confidence * 100)}%",
        "reasoning": {
            "insider_analysis": insider_analysis,
            "news_analysis": news_analysis
        }
    }

    if show_reasoning:
        show_agent_reasoning(message_content, "Sentiment Analysis Agent")

    message = HumanMessage(
        content=json.dumps(message_content),
        name="sentiment_agent",
    )

    return {
        "messages": [message],
        "data": data,
    }
