from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

from agents.state import AgentState, show_agent_reasoning


##### Portfolio Management Agent #####
def portfolio_management_agent(state: AgentState):
    """Makes final trading decisions and generates orders"""
    show_reasoning = state["metadata"]["show_reasoning"]
    portfolio = state["data"]["portfolio"]

    # Get the technical analyst, fundamentals agent, and risk management agent messages
    technical_message = next(msg for msg in state["messages"] if msg.name == "technical_analyst_agent")
    fundamentals_message = next(msg for msg in state["messages"] if msg.name == "fundamentals_agent")
    sentiment_message = next(msg for msg in state["messages"] if msg.name == "sentiment_agent")
    valuation_message = next(msg for msg in state["messages"] if msg.name == "valuation_agent")
    #risk_message = next(msg for msg in state["messages"] if msg.name == "risk_management_agent") #不考慮risk

    # Create the prompt template
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a portfolio manager making final trading decisions.
                Your job is to make a trading decision based on the team's analysis.

                When weighing the different signals for direction and timing:
                1. Valuation Analysis (35% weight)
                   - Primary driver of fair value assessment
                   - Determines if price offers good entry/exit point
                
                2. Fundamental Analysis (30% weight)
                   - Business quality and growth assessment
                   - Determines conviction in long-term potential
                
                3. Technical Analysis (25% weight)
                   - Secondary confirmation
                   - Helps with entry/exit timing
                
                4. Sentiment Analysis (10% weight)
                   - Final consideration
                   - Helps gauge market mood
                
                The decision process should be:
                1. First evaluate fundamentals signal
                2. Then evaluate valuation signal
                3. Use technical analysis for timing
                4. Consider sentiment for final adjustment
                
                Provide the following in your output:
                - "action": "buy" | "sell" | "hold",
                - "quantity": <positive integer>
                - "confidence": <float between 0 and 1>
                - "agent_signals": <list of agent signals including agent name, signal (bullish | bearish | neutral), and their confidence>
                - "reasoning": <concise explanation of the decision including how you weighted the signals>

                Trading Rules:
                - Go long if there is a “buy” signal and go short if there is a “sell” signal."""
            ),
            (
                "human",
                """Based on the team's analysis below, make your trading decision.

                Technical Analysis Trading Signal: {technical_message}
                Fundamental Analysis Trading Signal: {fundamentals_message}
                Sentiment Analysis Trading Signal: {sentiment_message}
                Valuation Analysis Trading Signal: {valuation_message}
                

                Here is the current portfolio:
                Portfolio:
                Cash: {portfolio_cash}
                Current Position: {portfolio_stock} shares

                Only include the action, quantity, reasoning, confidence, and agent_signals in your output as JSON.  Do not include any JSON markdown.

                Remember, the action must be either buy, sell, or hold.
                Go long if there is a “buy” signal and go short if there is a “sell” signal.
                """
            ),
        ]
    )

    # Generate the prompt
    prompt = template.invoke(
        {
            "technical_message": technical_message.content, 
            "fundamentals_message": fundamentals_message.content,
            "sentiment_message": sentiment_message.content,
            "valuation_message": valuation_message.content,

            "portfolio_cash": f"{portfolio['cash']:.2f}",
            "portfolio_stock": portfolio["stock"]
        }
    )
    # Invoke the LLM
    llm = ChatOpenAI(model="gpt-4o")
    result = llm.invoke(prompt)

    # Create the portfolio management message
    message = HumanMessage(
        content=result.content,
        name="portfolio_management",
    )

    # Print the decision if the flag is set
    if show_reasoning:
        show_agent_reasoning(message.content, "Portfolio Management Agent")

    return {"messages": state["messages"] + [message]}