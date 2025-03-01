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

    markdown_text =  "AI-Driven Personalized Travel Recommendation Systems: Innovations and Applications (2025/03/01)SummaryThis collection of academic papers and research focuses on the development and application of AI-driven personalized travel recommendation systems. The content explores how artificial intelligence, wearable devices, and real-time social media data analysis are being integrated to create more tailored and context-aware travel experiences for tourists.INDIANA Platform OverviewThe INDIANA platform, detailed in the arXiv paper (2411.12227), represents a comprehensive approach to personalized travel recommendations. The system leverages multiple data sources to enhance the tourist experience:Data Integration: Combines information from wearable devices, user preferences, current location, weather forecasts, and activity historyReal-time Recommendations: Provides context-aware suggestions based on the user's current situation and environmental factorsDual Beneficiaries: Serves both individual tourists looking to maximize their travel experiences and tourism professionals seeking insights to improve service deliveryTechnology Stack: Integrates AI, IoT, and wearable analytics to create a seamless and engaging experienceThis position paper, accepted at the 8th International Workshop on Chatbots and Human-Centred AI (CONVERSATIONS 2024), highlights how modern technologies can be combined to create more personalized travel experiences.Social Media Analysis for Travel RecommendationsThe ResearchGate article by Tafura Khatun explores how AI can analyze social media data in real-time to provide tailored travel recommendations. Key aspects include:Data-Driven Insights: Using AI to process vast amounts of social media data to identify trends, preferences, and potential destinationsReal-Time Analysis: Leveraging current social media activity to make dynamic recommendations that reflect shifting trends and real-world conditionsMachine Learning Applications: Employing Natural Language Processing (NLP) and other AI techniques to understand user preferences and predict suitable travel optionsEnhanced Planning Process: Creating a more efficient and personalized approach to travel planning through automated analysis of social dataThe research cites multiple studies on how social media analysis can be combined with AI to transform the travel industry, including work by Li & Wang (2021) on real-time analysis for personalized recommendations and Patel & Kopp (2023) on leveraging social media data for dynamic suggestions.Emerging Technologies and Future DirectionsBoth sources point to expanding applications of AI in travel recommendation systems:Augmented Reality Integration: Research by Zhang & Kim (2024) suggests combining AR with AI-driven social media insights for enhanced travel planningEthical Considerations: Both papers acknowledge the importance of data privacy and ethical AI use in handling personal informationIndustry Transformation: The travel industry is experiencing rapid evolution driven by these technological innovations, with changing consumer behaviors leading to demand for more personalized experiencesConclusionThe research presented across these sources demonstrates significant progress in creating more intelligent, responsive travel recommendation systems. By integrating multiple data sources—from wearable devices to social media—AI systems can provide increasingly personalized and context-aware travel suggestions. These developments not only enhance individual travel experiences but also provide valuable insights for the broader tourism industry, potentially transforming how travel services are delivered and experienced."

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