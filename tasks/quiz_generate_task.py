import textwrap
from crewai import Task
from agents.content_agent import content_search_agent
from agents.quiz_generate_agent import quiz_agent
from tasks.content_search_task import content_search_task

quiz_task = Task(
    agent= quiz_agent,
    description=textwrap.dedent("""
        Create a comprehensive quiz on the topic {topic}.

        ### Steps to follow:
        1. Read and understand the content provided by the `content_search_agent` about the topic.
        2. Generate 5 multiple-choice questions (MCQs) based on:
            - The topic provided.
            - The summarized content from `content_search_agent`.
        3. Each question must have exactly 4 unique options and 1 correct answer.
        4. Ensure the questions are beginner-friendly but slightly challenging.
        5. Make sure the questions are accurate, clear, and free from ambiguity.
    """), 
    context=[content_search_task],
    expected_output=textwrap.dedent("""
        The output must strictly be in JSON format as follows:
        {
        "topic": "<topic>",
        "questions": [
            {
            "question": "What is AI?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
            },
            {
            "question": "Which of the following is a type of Machine Learning?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option B"
            }
        ]
        }

        ⚠️ Exactly 5 questions should be generated.
    """),
    return_output=True    
)