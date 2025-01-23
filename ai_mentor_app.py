 
import streamlit as st
import google.generativeai as genai
# Add the app title and subheading at the top of the main page
st.title("AI Mentor")
st.subheader("Your personalized AI-powered learning companion.")



# Add a styled link to redirect to the Google AI Studio API key page
st.sidebar.markdown(
    """
    <a href="https://aistudio.google.com/app/apikey" target="_blank" style="text-decoration: none;">
        <button style="background-color: #007bff; color: white; border: none; padding: 8px 16px; 
                       text-align: center; font-size: 14px; border-radius: 5px; cursor: pointer;">
            Get Google AI API Key
        </button>
    </a>
    """,
    unsafe_allow_html=True,
)

# API Key Input
api_key = st.sidebar.text_input("Enter your Google AI Studio API Key", type="password")

# Configure the Google Generative AI client if API key is provided
if api_key:
    genai.configure(api_key=api_key)

# Initialize session state for chain of thought
if "current_topic" not in st.session_state:
    st.session_state["current_topic"] = None
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "question_counter" not in st.session_state:
    st.session_state["question_counter"] = 0

# Function to interact with Google AI Studio
def call_google_ai(prompt):
    if not api_key:
        st.warning("Please enter your Google AI Studio API key to generate content.")
        return None
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Main Navigation
page = st.sidebar.radio("Navigate", ["Learn Any Topic", "Prepare for Interview"])

# Footer with Personal Branding (Enhanced - Absolutely No Gap)
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <h3 style="margin: 0; line-height: 1;">Pranav Sharma</h3>
        <a href="https://www.linkedin.com/in/pranav-sharma-7b45531b8/" target="_blank" 
           style="text-decoration: none; font-size: 20px; font-weight: bold; color: #0077b5; margin: 0; line-height: 1;">
            LinkedIn Profile
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)



# Page 1: Learn Any Topic
if page == "Learn Any Topic":
    st.title("Learn Any Topic")
    topic = st.text_input("Enter the topic/tool you want to learn:")
    profile = st.text_input("Write the profile for which you want to study this topic/tool (e.g., Data Analyst):")
    learning_mode = st.radio("How do you want to learn?", ["Learn from scratch", "Write a subtopic to focus on"])
    
    if learning_mode == "Write a subtopic to focus on":
        subtopic = st.text_input("Enter the specific subtopic you want to learn:")
    else:
        subtopic = None

    # Start Learning
    if st.button("Start Learning"):
        if topic and profile:
            st.session_state["current_topic"] = topic
            st.session_state["conversation_history"] = []  # Reset history for new topic

            if subtopic:
                st.write(f"Teaching the subtopic: {subtopic} for {profile}...")
                learning_prompt = f"""
                You are an expert tutor specializing in {topic}. Focus on the subtopic '{subtopic}' 
                and explain it in detail, tailored for a {profile}. Provide examples and practical applications.
                """
            else:
                st.write(f"Teaching the topic: {topic} tailored for {profile}...")
                learning_prompt = f"""
                You are an expert tutor specializing in {topic}. Explain the topic from the basics, tailored for a {profile}.
                Break the content into easy-to-follow steps, provide examples with in-depth explanations, 
                and suggest practical applications.
                """
            
            response = call_google_ai(learning_prompt)
            if response:
                st.session_state["conversation_history"].append({"role": "system", "content": response})
                st.write(response)
        else:
            st.warning("Please enter a topic and your learning profile.")

    # Chat Bar for Custom Queries
    st.write("---")
    user_query = st.text_input("Ask a question to continue learning:")
    if st.button("Submit Query"):
        if user_query:
            chat_prompt = f"""
            Continue teaching the topic '{st.session_state.get('current_topic', 'the topic')}'.
            Based on the user's query: {user_query}, provide a detailed response while maintaining the context of
            previous explanations: {st.session_state.get('conversation_history', [{'content': ''}])[-1]['content']}
            """
            response = call_google_ai(chat_prompt)
            if response:
                st.session_state["conversation_history"].append({"role": "user", "content": user_query})
                st.session_state["conversation_history"].append({"role": "system", "content": response})
                st.write(response)

# Page 2: Prepare for Interview
elif page == "Prepare for Interview":
    st.title("Prepare for Interview")
    job_profile = st.text_input("Enter your job profile:")
    job_description = st.text_area("Paste the job description:")
    prep_mode = st.radio("What do you want to prepare?", ["All Questions", "Topic/Tool-Specific Questions"])
    
    if prep_mode == "Topic/Tool-Specific Questions":
        selected_tool = st.text_input("Enter the topic/tool to focus on:")
        if st.button("Generate Tool-Specific Questions"):
            if selected_tool:
                tool_specific_prompt = f"""
                You are an expert interviewer preparing candidates for a {job_profile} role. 
                Based on this job description: {job_description}, and the focus on {selected_tool}, 
                generate a list of expected interview questions specific to this topic/tool. 
                Provide detailed answers with explanations.
                """
                response = call_google_ai(tool_specific_prompt)
                if response:
                    st.session_state["conversation_history"].append({"role": "system", "content": response})
                    st.write(response)
            else:
                st.warning("Please enter the topic/tool to focus on.")

    if st.button("More Questions"):
        if st.session_state.get("conversation_history"):
            question_prompt = f"""
            Continue generating more interview questions for the job profile '{job_profile}' 
            with a focus on '{selected_tool}' or the job description provided. Include detailed answers and explanations.
            """
            response = call_google_ai(question_prompt)
            if response:
                st.session_state["conversation_history"].append({"role": "system", "content": response})
                st.write(response)

    # Chat Bar for Custom Interview Queries
    st.write("---")
    user_query = st.text_input("Ask a specific interview-related question:")
    if st.button("Submit Query for Interview"):
        if user_query:
            chat_prompt = f"""
            Based on the job description '{job_description}' and job profile '{job_profile}', respond to the user's query:
            {user_query}. Include relevant examples and in-depth explanations.
            """
            response = call_google_ai(chat_prompt)
            if response:
                st.write(response)


