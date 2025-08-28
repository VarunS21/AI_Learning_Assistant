from dotenv import load_dotenv
from tasks.content_search_task import content_search_task
from tasks.quiz_generate_task import quiz_task
from crew import agent_crew

load_dotenv()

def run(topic: str):
    # Run the Crew
    result = agent_crew.kickoff(inputs={'topic': topic})

    print('-' * 150)
    
    print("----- Content Search Output -----")
    print(content_search_task.output.raw)
    
    print("----- Quiz Generation Output -----")
    print(quiz_task.output.raw)
    
    print("----- Ouiz Evaluation Output -----")
    print(result.raw)
    
    print('-' * 150)


if __name__ == '__main__':
    topic = 'AI Agents'
    run(topic)
