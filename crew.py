from crewai import Crew

from agents.content_agent import content_search_agent
from agents.quiz_generate_agent import quiz_agent
from agents.evaluation_agent import evaluation_agent
from tasks.content_search_task import content_search_task
from tasks.quiz_generate_task import quiz_task
from tasks.evaluation_task import evaluation_task

# agent_crew = Crew(
#     agents = [content_search_agent,quiz_agent,evaluation_agent],
#     tasks = [content_search_task,quiz_task,evaluation_task],
#     verbose = True
# )
# Content Generation Crew
content_crew = Crew(
    agents=[content_search_agent],
    tasks=[content_search_task],
    verbose=True
)

# Quiz Generation Crew
quiz_crew = Crew(
    agents=[quiz_agent],
    tasks=[quiz_task],
    verbose=True
)

# Evaluation Crew
evaluation_crew = Crew(
    agents=[evaluation_agent],
    tasks=[evaluation_task],
    verbose=True
)
