
''' 
from crewai import Crew, Process
from agents import researcher, writer, proof_reader
from tasks import research_task, write_task, proof_read_task

crew = Crew(
    agents=[researcher, writer, proof_reader],
    tasks=[research_task, write_task, proof_read_task],
    process=Process.sequential
)


topic="Artifical Intelligence in Finance"
result=crew.kickoff(inputs={"topic":topic})
print(result)

'''

# Streamlit APP

import streamlit as st
import time
from datetime import datetime, timedelta

# Import with error handling
try:
    from crewai import Crew, Process
    from agents import researcher, writer, proof_reader
    from tasks import research_task, write_task, proof_read_task
    IMPORTS_SUCCESS = True
    IMPORT_ERROR = None
except ImportError as e:
    IMPORTS_SUCCESS = False
    IMPORT_ERROR = str(e)

# Page configuration
st.set_page_config(
    page_title="ArticleCraft AI",
    page_icon="🤖",
    layout="centered"
)

# Minimal CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .agent-card {
        background: linear-gradient(125deg, #667eea 0%, #764ba2 100%);;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 0.75rem;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: #007bff;
        color: white;
        border: none;
        padding: 0.75rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: #0056b3;
    }
    
    .stButton > button:disabled {
        background: #6c757d;
        cursor: not-allowed;
    }
    
    .result-box {
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .rate-limit-info {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: #856404;
    }
    
    .success-info {
        background: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'crew_result' not in st.session_state:
    st.session_state.crew_result = None
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = None

# Rate limiting - 1 minute between requests
RATE_LIMIT_SECONDS = 60

def get_time_until_next_request():
    """Calculate seconds until next request is allowed"""
    if not st.session_state.last_request_time:
        return 0
    
    time_passed = (datetime.now() - st.session_state.last_request_time).total_seconds()
    time_remaining = RATE_LIMIT_SECONDS - time_passed
    return max(0, time_remaining)

def format_time_remaining(seconds):
    """Format remaining time as MM:SS"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def can_make_request():
    """Check if enough time has passed since last request"""
    return get_time_until_next_request() == 0

# Header
st.markdown('<h1 class="main-title">🤖 ArticleCraft AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Multi-Agent Content Creation</p>', unsafe_allow_html=True)

# Check for import errors
if not IMPORTS_SUCCESS:
    st.error(f"Import Error: {IMPORT_ERROR}")
    st.info("Install: `pip install crewai crewai-tools python-dotenv langchain-groq`")
    st.stop()

# Sidebar with agent info
with st.sidebar:
    st.markdown("### 🤖 AI Agent Crew")
    
    st.markdown("""
    <div class="agent-card">
        <strong>🔍 Researcher</strong><br>
        <small>Gathers data and identifies trends using Google search</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="agent-card">
        <strong>✍️ Writer</strong><br>
        <small>Creates engaging, well-structured articles</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="agent-card">
        <strong>📝 Proof Reader</strong><br>
        <small>Ensures quality and adds proper citations</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Process:** Sequential workflow")

# Main content
st.markdown("### Enter Topic")

# Topic input
topic = st.text_input(
    "",
    placeholder="e.g., AI in Healthcare, Space Technology, Climate Solutions...",
    label_visibility="collapsed"
)

# Rate limit status
time_remaining = get_time_until_next_request()
if time_remaining > 0:
    st.markdown(f"""
    <div class="rate-limit-info">
        ⏱️ <strong>Rate limit active</strong><br>
        Next request available in: <strong>{format_time_remaining(time_remaining)}</strong>
    </div>
    """, unsafe_allow_html=True)

# Generate button
button_disabled = not can_make_request() or st.session_state.is_processing
button_text = "🚀 Generate Article"

if time_remaining > 0:
    button_text = f"⏱️ Wait {format_time_remaining(time_remaining)}"
elif st.session_state.is_processing:
    button_text = "🔄 Processing..."

if topic and st.button(button_text, disabled=button_disabled):
    if not st.session_state.is_processing and can_make_request():
        st.session_state.is_processing = True
        st.session_state.last_request_time = datetime.now()
        
        # Progress tracking with longer delays
        with st.status("Processing with AI agents...", expanded=True) as status:
            st.write("🔍 Researcher analyzing topic...")
            time.sleep(5)
            
            try:
                # Initialize crew
                crew = Crew(
                    agents=[researcher, writer, proof_reader],
                    tasks=[research_task, write_task, proof_read_task],
                    process=Process.sequential
                )
                
                st.write("✍️ Writer creating content...")
                time.sleep(5)
                
                st.write("📝 Proof reader finalizing...")
                time.sleep(5)
                
                # Execute crew
                result = crew.kickoff(inputs={"topic": topic})
                st.session_state.crew_result = result
                
                status.update(label="✅ Article generated successfully!", state="complete")
                
                # Show next available time
                next_time = datetime.now() + timedelta(seconds=RATE_LIMIT_SECONDS)
                st.markdown(f"""
                <div class="success-info">
                    ✅ <strong>Content generated!</strong><br>
                    Next request available at: <strong>{next_time.strftime('%I:%M %p')}</strong>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                status.update(label="❌ Generation failed", state="error")
                # Reset last request time on error so user can try again
                st.session_state.last_request_time = None
            
            finally:
                st.session_state.is_processing = False

# Display result
if st.session_state.crew_result:
    st.markdown("### Generated Article")
    
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(st.session_state.crew_result)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download and reset options
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            "📄 Download Article",
            data=str(st.session_state.crew_result),
            file_name=f"{topic.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Clear Result", use_container_width=True):
            st.session_state.crew_result = None
            st.rerun()

# Auto-refresh when rate limited
if time_remaining > 0 and not st.session_state.is_processing:
    time.sleep(10)
    st.rerun()