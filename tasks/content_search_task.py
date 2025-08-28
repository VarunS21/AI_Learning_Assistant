import textwrap
from crewai import Task
from agents.content_agent import content_search_agent

content_search_task = Task(
    agent= content_search_agent,
    description = textwrap.dedent("""
        Conduct a comprehensive search on the topic {topic} and provide a clear, beginner-friendly explanation.
        Your tasks:
        Search and gather the most relevant and accurate information about the topic from trusted sources.
        Extract key points, definitions, and any recent developments related to the topic.
        Summarize the complex content into a simple, easy-to-understand explanation suitable for beginners.
        Provide one real-world use case or practical example to make the concept more relatable and understandable."""),
    
    expected_output= textwrap.dedent("""
        A clear, concise, and beginner-friendly explanation of the topic {topic}, including:
        A simple and accurate definition
        Key points and important highlights
        Any recent developments (if available)
        One real-world example demonstrating its application """),
    response_format="markdown",
    return_output = True
    )