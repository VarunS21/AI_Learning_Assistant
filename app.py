import streamlit as st
import json
from crew import content_crew, quiz_crew, evaluation_crew
import re

# Initialize session state
if "content" not in st.session_state:
    st.session_state.content = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None 
    
st.set_page_config(page_title="AI-Study Assistant", layout="wide")

st.title("📘 AI Learning Assistant")
st.subheader("🧠 Get started on a new topic. Our AI will guide you with a summary, a quiz, and a detailed evaluation of your progress.")
# --------------------------
# Generate Summarized Content
# --------------------------
st.markdown("")
st.markdown("")
topic = st.text_input("Enter a topic to learn:", placeholder="e.g., Machine Learning")
st.markdown("")
if st.button("Generate Content"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("🔎 Fetching content..."):
            # Call the content_crew, which only needs the topic
            content_output = content_crew.kickoff(inputs={"topic": topic})

            # Fetch the summary directly from the crew output
            st.session_state.content = content_output.raw if content_output else "No summary found!"

# Show the content summary if available
if "content" in st.session_state and st.session_state.content:
    st.subheader("📄 Simplified Content Summary")
    st.write(st.session_state.content)
    
# --------------------------
# Quiz Generation Section
# --------------------------
# Button to start quiz
if st.button("🎯 Attend Quiz"):
    if not st.session_state.content:
        st.warning("⚠️ Please generate content first.")
    else:
        with st.spinner("🧠 Generating quiz..."):
            # Call the quiz_crew, which needs the topic and content
            raw_quiz = quiz_crew.kickoff(inputs={
                "topic": topic,
                "content": st.session_state.content
            }).raw
    
            if raw_quiz:
                try:
                    # Extract JSON only (ignore extra text if LLM adds)
                    match = re.search(r'\{.*\}', raw_quiz, re.DOTALL)
                    if match:
                        raw_quiz = match.group()

                    # Parse the cleaned JSON
                    st.session_state.quiz = json.loads(raw_quiz)
                    
                    # Validate JSON structure
                    if "questions" not in st.session_state.quiz or not isinstance(st.session_state.quiz["questions"], list):
                        raise ValueError("Invalid quiz format")
                    
                    # Reset evaluation state when a new quiz is generated
                    st.session_state.evaluation = None

                except (json.JSONDecodeError, ValueError) as e:
                    st.session_state.quiz = None
                    st.error(f"⚠️ Quiz data is invalid. Please try again. Error: {e}")
            else:
                st.session_state.quiz = None
                st.warning("⚠️ No quiz generated.")

# 📝 Show Quiz if Available
if st.session_state.quiz and "questions" in st.session_state.quiz:
    st.subheader("📝 Quiz Time")
    
    # Initialize user_answers state if not already done
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    for i, q in enumerate(st.session_state.quiz["questions"]):
        # Extra safety check for missing keys
        question_text = q.get("question", f"Question {i+1}")
        options = q.get("options", [])

        if not options or len(options) < 2:
            st.warning(f"⚠️ Skipping Q{i+1}: Invalid options")
            continue

        st.write(f"**Q{i+1}. {question_text}**")
        selected = st.radio(
            f"Select answer for Q{i+1}",
            options,
            key=f"q_{i}",
            index=None
        )
        st.session_state.user_answers[i] = selected
    
    # --------------------------
    # Quiz Evaluation Section
    # --------------------------
    if st.button("✅ Check Answers"):
        with st.spinner("🧠 Evaluating your answers..."):
            user_data = {
                "quiz": st.session_state.quiz,
                "user_answers": st.session_state.user_answers
            }
            
            try:
                evaluation_output = evaluation_crew.kickoff(inputs={
                    "topic": topic,
                    "quiz_data": json.dumps(user_data["quiz"]),
                    "user_answers": json.dumps(user_data["user_answers"])
                }).raw
                
                match = re.search(r'\{.*\}', evaluation_output, re.DOTALL)
                if match:
                    st.session_state.evaluation = json.loads(match.group())
                    st.success("Evaluation complete!")
                else:
                    st.session_state.evaluation = None
                    st.error("⚠️ Failed to parse evaluation data from the agent's output.")

            except Exception as e:
                st.session_state.evaluation = None
                st.error(f"An error occurred during evaluation: {e}")

# Display the evaluation results
if st.session_state.evaluation:
    st.subheader("📊 Your Evaluation")
    
    if isinstance(st.session_state.evaluation, dict) and "overall_score" in st.session_state.evaluation:
        overall_score = st.session_state.evaluation.get("overall_score", "N/A")
        overall_feedback = st.session_state.evaluation.get("overall_feedback", "No feedback available.")
        
        st.metric(label="Overall Score", value=overall_score)
        st.write(f"**Overall Feedback:** {overall_feedback}")
        
        st.write("---")
        st.subheader("Detailed Breakdown")
        
        for i, q_eval in enumerate(st.session_state.evaluation.get("evaluation_details", [])):
            question_text = q_eval.get("question", f"Question {i+1}")
            user_ans = q_eval.get("user_answer", "Not answered")
            # is_correct = q_eval.get("is_correct", False)
            correct_ans = q_eval.get("correct_answer", "N/A")
            feedback = q_eval.get("feedback", "")

            is_correct_local = user_ans.strip().lower() == correct_ans.strip().lower()
            
            st.write(f"**Q{i+1}:** {question_text}")
            st.write(f"Your Answer: **{user_ans}**")
            
            if is_correct_local:
                st.success(f"✅ Correct! The correct answer is: {correct_ans}")
            else:
                st.error(f"❌ Incorrect. The correct answer is: {correct_ans}")
                
            # st.info(f"Feedback: {feedback}")

    else:
        st.error("⚠️ Invalid evaluation data received. Please try again.")