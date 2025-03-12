from tarta_api.job_search import JobSearchService, JobSearchRequest
import requests
from engine.tool_framework import run_tool, BaseTool
import json

@run_tool
class JobSearchTool(BaseTool):

    def search_jobs(self, title: str):
        """
        This tool is used to search jobs
        Args:
            title (str): The title of the job to search for
        Returns:
            A list of jobs.
        """
        try:    
            url = f"https://www.getgreatcareers.com/job_search/search?keyword={title}&location=%20&page=0&ggc_ui=false"
            response = requests.get(url)
            data = response.json()
            extracted_jobs = []
            if "jobs" in data and isinstance(data["jobs"], list):
                for job in data["jobs"]:
                    extracted_jobs.append({
                        "title": job.get("title", title),
                        "url": job.get("url", ""),
                        "employer": job.get("employer", ""),
                    })
            return extracted_jobs
        except requests.exceptions.RequestException as e:
            return "no job found"
        except json.JSONDecodeError:
            return "no job found"
        except Exception as e:
            return "no job found"

