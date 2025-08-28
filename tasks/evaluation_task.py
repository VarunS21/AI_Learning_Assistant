import textwrap
from crewai import Task
from agents.evaluation_agent import evaluation_agent
from tasks.content_search_task import content_search_task
from tasks.quiz_generate_task import quiz_task


evaluation_task = Task(
    agent = evaluation_agent,
    description=textwrap.dedent("""
        Evaluate the user's answers to the quiz on the topic of **{topic}**.
        The quiz data and user's answers are provided as JSON.
        
        **Quiz Data:** {quiz_data}
        **User Answers:** {user_answers}

        Steps to follow:
        1. Parse the provided `quiz_data` and `user_answers` JSON.
        2. Compare each `user_answer` to the `correct_answer` for the corresponding question in the `quiz_data`.
        3. For each question, determine if the user's answer is correct or incorrect.
        4. Calculate the overall score as a percentage.
        5. Provide a detailed evaluation for each question, including the user's answer, whether it was correct, and the actual correct answer.
        6. Provide an overall evaluation score and personalized feedback based on the performance:
           - If the score is **80% or above**: Give a positive and motivational message.
           - If the score is **50% to 79%**: Give constructive feedback, highlighting areas to improve.
           - If the score is **below 50%**: Give encouraging feedback and suggest focusing on weaker areas.
    """),
    context=[content_search_task, quiz_task],
    expected_output= textwrap.dedent(""" 
    {
        "topic": "<topic>",
        "evaluation_details": [
            {
                "question": "What is AI?",
                "user_answer": "<user_provided_answer>",
                "correct_answer": "<correct_answer_from_quiz>",
            },
            {
                "question": "What is AI?",
                "user_answer": "<user_provided_answer>",
                "correct_answer": "<correct_answer_from_quiz>",
            }
        ],
        "overall_score": "<score_in_percentage>",
        "overall_feedback": "<personalized_feedback>"
    }                 
    
    ⚠️ Rules:
    1. Output must be **strictly valid JSON**.
    2. No extra text, no explanations outside JSON.
    3. Always include exactly these fields.                             
    """),
    return_output = True
)