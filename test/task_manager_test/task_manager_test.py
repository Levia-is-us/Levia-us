import os
import sys
import dotenv
import pytest

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
print(project_root)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from engine.flow.executor.task_manager import TaskManager


@pytest.mark.parametrize(
    "plan",
    [[
        {
            "step": "Web Scraping Tool",
            "intent": "Gather today's football news from reliable sports websites",
            "Description": "Extract current football news articles and updates from major sports news websites and trusted sources",
            "Reason": "To collect the most recent and relevant football news content from multiple sources",
        },
        {
            "step": "Content Filtering Engine",
            "intent": "Filter and organize collected news",
            "Description": "Process the gathered news to filter out duplicates and organize content by relevance and timestamp",
            "Reason": "To ensure the user receives unique, relevant, and timely football news without redundancy",
        },
        {
            "step": "Content Categorization System",
            "intent": "Categorize news by topics",
            "Description": "Organize filtered news into categories such as transfers, match results, injuries, and team updates",
            "Reason": "To provide structured and easily navigable news content for better user experience",
        },
        {
            "step": "News Presentation Interface",
            "intent": "Display organized news content",
            "Description": "Present the categorized news in a user-friendly format with headlines, summaries, and links to full articles",
            "Reason": "To deliver the news in an accessible and engaging format for the user to consume",
        },
    ]],
)
def test_task_manager(plan):
    task_manager = TaskManager()
    task_manager.init_tasks(plan)
    assert task_manager.get_current_task()["step"] == plan[0]["step"]
    assert task_manager.get_next_task()["step"] == plan[1]["step"]
    assert task_manager.get_next_task()["step"] == plan[2]["step"]
    assert task_manager.get_next_task()["step"] == plan[3]["step"]
    assert len(task_manager.get_all_tasks()) == 4
    assert task_manager.get_current_task_index() == 3
    assert task_manager.get_total_tasks() == 4
    assert task_manager.get_task_by_index(0)["step"] == plan[0]["step"]


