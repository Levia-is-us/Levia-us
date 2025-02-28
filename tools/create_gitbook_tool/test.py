import os
import sys


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
from engine.tool_framework.tool_registry import ToolRegistry
from engine.tool_framework.tool_caller import ToolCaller


def main():
    registry = ToolRegistry()
    
    # Use absolute path
    tools_dir = os.path.join(project_root, "tools")
    registry.scan_directory(tools_dir)  # Scan tools directory

    # Create ToolCaller instance
    caller = ToolCaller(registry)

    markdown_text =  "\n\n```markdown\n### Title: Recent Bitcoin Developments Since October 2023 (2023/12/27; 2023/12/12; 2024/03/05)\n**Summary:**  \nThis collection of news reports details Bitcoin's resurgence in late 2023 and early 2024, driven by macroeconomic shifts, regulatory developments, and institutional adoption. Below are the key themes and events:\n\n#### **1. Bitcoin's 2023 Rally and Related Stock Surges (CNBC, 2023/12/27)**  \n- **Price Performance**: Bitcoin rose over 150% in 2023, surpassing $42,683 by December, though still 38% below its 2021 peak. Stocks tied to Bitcoin outperformed significantly: Marathon Digital (+688%), Coinbase (+386%), MicroStrategy (+327%), and Grayscale Bitcoin Trust (+330%).  \n- **Drivers**:  \n  - **Spot ETF Optimism**: Anticipation of SEC approval for spot Bitcoin ETFs (e.g., BlackRock, Fidelity) fueled buying. Grayscale’s GBTC discount to NAV narrowed to 5.6% amid ETF conversion hopes.  \n  - **Halving Event**: The May 2024 halving (reducing mining rewards) tightened supply expectations.  \n  - **Institutional Moves**: MicroStrategy acquired an additional 14,620 BTC ($615M) in Q4 2023, totaling 189,150 BTC ($7.4B). Marathon expanded mining capacity by 56% via acquisitions.  \n  - **Regulatory Shifts**: Easing Fed rate hikes and mark-to-market accounting rules (effective 2025) boosted risk appetite.  \n\n#### **2. Market Recovery and Regulatory Fallout (Reuters, 2023/12/12)**  \n- **Crypto Market Growth**: Total crypto market cap rebounded to $1.7T (from $871B in 2022), with Bitcoin dominance rising to 50%.  \n- **Legal Developments**:  \n  - Binance’s $4.3B settlement with DOJ and CZ’s resignation.  \n  - Sam Bankman-Fried’s fraud conviction.  \n  - Ripple’s partial legal victory over XRP’s non-security status.  \n- **ETF Impact**: Analysts projected $3B inflows into spot ETFs post-approval, though JPMorgan warned adoption might underperform bullish estimates.  \n\n#### **3. Record Highs and ETF-Driven Momentum (CBS, 2024/03/05)**  \n- **Price Surge**: Bitcoin hit $68,818 in March 2024, driven by $7.35B inflows into spot ETFs post-SEC approval (January 2024).  \n- **Institutional Adoption**: BlackRock and Fidelity’s ETFs dominated inflows, attracting traditional investors seeking regulated exposure.  \n- **Volatility Warnings**: Despite gains, analysts cautioned about Bitcoin’s inherent volatility, referencing the 2022 crash (FTX collapse, -60% price drop).  \n\n#### **Mixed Sentiment and Future Outlook**  \n- **Bullish Voices**: Galaxy Digital’s Michael Novogratz predicted Bitcoin surpassing its $69K record, citing scarcity and institutional demand.  \n- **Bearish Concerns**: JPMorgan CEO Jamie Dimon criticized Bitcoin’s use cases (e.g., “criminals, tax avoidance”), while short sellers lost $6.3B betting against crypto stocks in 2023.  \n- **Halving and ETFs**: The 2024 halving and ETF approvals are seen as pivotal for sustained growth, though corrections are expected amid speculative trading.  \n\n**Conclusion**: Bitcoin’s 2023–2024 rally reflects renewed institutional confidence, regulatory milestones, and macroeconomic tailwinds, though volatility and regulatory risks persist. The interplay of ETF adoption, halving dynamics, and global monetary policy will shape its trajectory in 2024.\n```"
    

    result = caller.call_tool(tool_name="SaveMarkdownToGitbook", method="save_markdown_to_gitbook", kwargs={"content":markdown_text})
    
    if result:
        if "error" in result:
            print(f"Tool execution error: {result['error']}")
        else:
            print(f"response info: {result}")
    else:
        print("Tool call failed, no result returned")


if __name__ == "__main__":
    main()