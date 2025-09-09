import streamlit as st
from openai import OpenAI

# --- Load secret key ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Your Streamlit app code ---
st.title("AI Virtual Teacher")

st.write("Welcome! Ask me anything about AI.")

user_input = st.text_input("Your Question:")

if user_input:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",   # modern replacement for text-davinci-003
        messages=[
            {"role": "system", "content": "You are a helpful AI teacher."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=100
    )
    st.write(response.choices[0].message.content)

import streamlit as st
import pandas as pd
from gtts import gTTS
import os
import io
import base64
import random
import time
import numpy as np
from PIL import Image

# Configure the app
st.set_page_config(
    page_title="🤖 AI Virtual Teacher for Kids",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== DATA SECTION ===================

# Complete Lesson Content
lessons = {
    "lesson1": {
        "title": "🤖 What is AI?",
        "content": [
            "🤖 AI stands for Artificial Intelligence - it's like a super-smart robot brain!",
            "💡 Just like you learn from books and games, AI learns from lots and lots of examples",
            "📺 AI helps Netflix know what cartoons you'll love to watch",
            "🎯 AI is everywhere - in games, phones, cars, and even your favorite apps!",
            "🧠 But remember: AI is very smart, but it's not exactly like a human brain"
        ],
        "fun_fact": "🎮 Did you know? AI can play video games and sometimes beat the best human players!",
        "demo": "story",
        "emoji": "🤖"
    },
    "lesson2": {
        "title": "🏠 Where do we find AI?",
        "content": [
            "🏠 AI is in your home - smart speakers like Alexa, phones, tablets",
            "🚗 AI helps cars drive safely and find the best routes to places",
            "🏥 AI helps doctors see inside your body with special X-ray cameras",
            "🎮 AI makes video game characters smart and fun to play with",
            "📱 AI helps your camera take better photos and recognize your face!"
        ],
        "fun_fact": "📸 Your phone's camera uses AI to automatically find and focus on your pet's face!",
        "demo": "picture_spotting",
        "emoji": "🏠"
    },
    "lesson3": {
        "title": "🎓 How does AI Learn?",
        "content": [
            "👀 AI learns by looking at thousands and thousands of pictures",
            "🐱🐶 To tell cats from dogs, AI looks at 10,000+ photos of cats and dogs",
            "🧩 AI finds patterns - like 'cats have pointy ears, dogs have floppy ears'",
            "📚 The more examples AI sees, the smarter it gets!",
            "⚡ AI can learn much faster than humans, but it needs lots of examples"
        ],
        "fun_fact": "🔢 Some AI systems look at millions of pictures to learn just one simple thing!",
        "demo": "cat_vs_dog",
        "emoji": "🎓"
    },
    "lesson4": {
        "title": "🧠 AI vs Human Brain",
        "content": [
            "💭 Human brains have feelings, imagination, and creativity",
            "🤖 AI brains are very fast at math and remembering things",
            "❤️ Humans can love, feel sad, get excited - AI cannot feel emotions",
            "🎨 Humans can create art from imagination - AI copies patterns it learned",
            "👥 Humans are great at understanding other people's feelings"
        ],
        "fun_fact": "🌟 Humans only use about 10% of their brain, but that's still more creative than any AI!",
        "demo": "spot_difference",
        "emoji": "🧠"
    },
    "lesson5": {
        "title": "🔧 Types of AI",
        "content": [
            "👂 Some AI can listen and talk to you (like Siri or Google Assistant)",
            "👁️ Some AI can see and recognize pictures and faces",
            "🎯 Some AI can recommend things you might like (like YouTube suggestions)",
            "🎮 Some AI can play games and solve puzzles",
            "🚗 Some AI can control robots and self-driving cars"
        ],
        "fun_fact": "🎵 AI can even make music! But it learns by listening to songs humans already made!",
        "demo": "chatbot_recommender",
        "emoji": "🔧"
    },
    "lesson6": {
        "title": "⚖️ Good AI vs Bad AI",
        "content": [
            "😊 Good AI helps people: finding medicine, making life easier, learning new things",
            "😟 Bad AI can happen when people use it for mean things",
            "🛡️ That's why we need smart people like YOU to help make AI good!",
            "📏 AI should always be fair to everyone, no matter who they are",
            "🤝 The best AI is when humans and AI work together as a team!"
        ],
        "fun_fact": "🦸‍♂️ You could be an AI superhero by learning how to make AI helpful for everyone!",
        "demo": "ethics_story",
        "emoji": "⚖️"
    }
}

# Quiz Questions
quiz_data = {
    "lesson1": [
        {
            "question": "🤖 What does AI stand for?",
            "options": ["Artificial Intelligence", "Amazing Internet", "Automatic Ideas"],
            "correct": 0,
            "explanation": "Great! AI stands for Artificial Intelligence - like a smart robot brain! 🧠"
        },
        {
            "question": "🎯 How does AI learn?",
            "options": ["From one picture", "From lots of examples", "It doesn't learn"],
            "correct": 1,
            "explanation": "Exactly! AI learns by looking at many, many examples! 📚"
        },
        {
            "question": "📺 Where can we find AI?",
            "options": ["Only in robots", "In phones and apps", "Nowhere"],
            "correct": 1,
            "explanation": "Yes! AI is in phones, apps, games, and many places around us! 📱"
        }
    ],
    "lesson2": [
        {
            "question": "🏠 Where do we find AI at home?",
            "options": ["Smart speakers", "Only in computers", "In the kitchen only"],
            "correct": 0,
            "explanation": "Perfect! Smart speakers like Alexa use AI to understand you! 🔊"
        },
        {
            "question": "🚗 How does AI help cars?",
            "options": ["Makes them faster", "Helps them drive safely", "Changes their color"],
            "correct": 1,
            "explanation": "Great! AI helps cars drive safely and find good routes! 🛣️"
        }
    ]
}

# =================== HELPER FUNCTIONS ===================

def text_to_speech_for_kids(text, language='en', slow=False):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception as e:
        return None

def create_audio_player(audio_bytes):
    """Create HTML audio player"""
    if audio_bytes:
        b64 = base64.b64encode(audio_bytes).decode()
        html = f"""
        <audio controls style="width: 100%; max-width: 400px; margin: 10px 0;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        return html
    return None

# =================== AI CHATBOT CLASS ===================

class KidsAIChatbot:
    def __init__(self):
        self.responses = {
            "what is ai": [
                "🤖 AI is like a super-smart computer brain that can learn things!",
                "AI stands for Artificial Intelligence - it's like having a really smart robot friend!",
                "Think of AI as a computer that can think and learn, just like you do but much faster!"
            ],
            "how does ai work": [
                "🧠 AI learns by looking at lots and lots of examples, just like how you learned to recognize your friends!",
                "AI finds patterns in things - like noticing that cats have pointy ears and dogs have floppy ears!",
                "AI practices over and over again until it gets really good at something!"
            ],
            "where is ai": [
                "🏠 AI is everywhere! In your phone, games, YouTube, and even smart speakers like Alexa!",
                "AI helps Netflix pick movies you might like, and helps cars drive safely!",
                "Look around - AI might be in your tablet, TV, or even your toy robot!"
            ],
            "are you real": [
                "🤖 I'm an AI chatbot - I'm real computer code, but I don't have a body like you!",
                "I exist in the computer, kind of like how video game characters exist in games!"
            ],
            "tell me a joke": [
                "🤖 Why did the robot go to school? To improve its AI-Q! Get it? Like IQ but AI-Q! 😄",
                "What do you call a robot who takes the long way around? R2-Detour! 🤖",
                "Why don't robots ever panic? Because they have nerves of steel! ⚡"
            ],
            "can ai feel": [
                "❤️ No, AI doesn't have feelings like happiness or sadness like you do!",
                "AI is super smart at some things, but only humans have real emotions!"
            ],
            "am i smart": [
                "🌟 You're super smart! You're learning about AI, and that makes you really clever!",
                "🧠 Of course you're smart! Smart kids ask good questions, just like you're doing!"
            ]
        }
        
        self.fallback_responses = [
            "🤔 That's a great question! Ask me about AI - like 'What is AI?' or 'How does AI work?'",
            "🌟 Wow, you're curious! Try asking me about where we find AI!",
            "🤖 I love your questions! Ask me anything about AI and robots!"
        ]

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Handle greetings
        if any(greeting in user_input for greeting in ["hi", "hello", "hey"]):
            return "🎉 Hello there, smart kid! I'm your AI teacher! Ask me anything about AI!"
        
        # Handle goodbyes
        if any(goodbye in user_input for goodbye in ["bye", "goodbye", "thanks"]):
            return "👋 Bye bye! Keep being curious and learning new things! You're awesome!"
        
        # Find matching response
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)
        
        return random.choice(self.fallback_responses)

# =================== SESSION STATE INITIALIZATION ===================

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = KidsAIChatbot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'lesson_progress' not in st.session_state:
    st.session_state.lesson_progress = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_question_index' not in st.session_state:
    st.session_state.quiz_question_index = 0

# =================== CUSTOM CSS ===================

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 6px #cccccc;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .lesson-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .lesson-card:hover {
        transform: translateY(-5px);
    }
    
    .chat-bubble-ai {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #2E8B57;
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        border-left: 5px solid #2196F3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-box {
        background: linear-gradient(45deg, #FFE0B2, #FFCC02);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 3px solid #FF9800;
    }
    
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .progress-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stButton > button {
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# =================== MAIN FUNCTION ===================

def main():
    st.markdown('<h1 class="main-header">🤖 AI Virtual Teacher for Kids! 🎉</h1>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.markdown("### 🌟 Your Learning Adventure")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "🎯 Choose your adventure:",
        [
            "🏠 Welcome Home", 
            "📖 Learn About AI", 
            "🤖 Chat with AI Teacher", 
            "🎮 Play AI Games", 
            "🧠 Take Smart Quiz", 
            "🏆 My Progress", 
            "👨‍👩‍👧‍👦 For Parents"
        ]
    )
    
    # Sidebar Progress
    completed_lessons = len([k for k, v in st.session_state.lesson_progress.items() if v])
    total_lessons = len(lessons)
    progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
    
    st.sidebar.markdown("### 📊 Your Progress")
    st.sidebar.progress(progress_percentage / 100)
    st.sidebar.write(f"🎯 {completed_lessons}/{total_lessons} lessons completed!")
    st.sidebar.write(f"💬 {len(st.session_state.chat_history)//2} AI conversations")
    
    # Navigation
    if page == "🏠 Welcome Home":
        show_home()
    elif page == "📖 Learn About AI":
        show_lessons()
    elif page == "🤖 Chat with AI Teacher":
        show_chat()
    elif page == "🎮 Play AI Games":
        show_games()
    elif page == "🧠 Take Smart Quiz":
        show_quiz()
    elif page == "🏆 My Progress":
        show_progress()
    elif page == "👨‍👩‍👧‍👦 For Parents":
        show_parents()

# =================== PAGE FUNCTIONS ===================

def show_home():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("## 🌟 Welcome to Your AI Learning Adventure!")
        st.markdown("### Ready to become an AI expert?")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Feature showcase
    st.markdown("### 🎯 What Amazing Things Will You Learn Today?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📚 Learn")
        st.write("• 🤖 What is AI?")
        st.write("• 🏠 Where we find AI")
        st.write("• 🎓 How AI learns")
        st.write("• 🧠 AI vs Human brains")
    
    with col2:
        st.markdown("#### 🎮 Play")
        st.write("• 🐱🐶 Cat vs Dog game")
        st.write("• 🎬 Cartoon recommender")
        st.write("• 🎨 Drawing guesser")
        st.write("• 🧠 AI quiz challenges")
    
    with col3:
        st.markdown("#### 💬 Chat")
        st.write("• 🤖 Ask AI anything")
        st.write("• 🔊 Listen to answers")
        st.write("• 😄 Hear AI jokes")
        st.write("• 🌟 Get encouragement")
    
    st.markdown("---")
    
    # Big start button
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 START MY AI ADVENTURE!", key="big_start", help="Begin your amazing AI learning journey!"):
            st.balloons()
            st.success("🎉 Amazing! Choose something from the left menu to start!")
            
            # Welcome audio
            welcome_text = "Welcome to your AI learning adventure! You're going to discover amazing things about artificial intelligence!"
            welcome_audio = text_to_speech_for_kids(welcome_text)
            if welcome_audio:
                st.markdown("🔊 **Your welcome message:**")
                audio_html = create_audio_player(welcome_audio)
                st.markdown(audio_html, unsafe_allow_html=True)

def show_lessons():
    st.header("📖 AI Lessons for Future Geniuses!")
    
    # Progress indicator
    completed_lessons = len([k for k, v in st.session_state.lesson_progress.items() if v])
    st.info(f"🎯 Your progress: {completed_lessons}/{len(lessons)} lessons completed!")
    
    # Lesson selection
    st.markdown("### 🎯 Choose Your Lesson:")
    
    lesson_options = ["Choose a lesson..."] + [f"{lessons[key]['emoji']} {lessons[key]['title']}" for key in lessons.keys()]
    lesson_choice = st.selectbox("Pick your adventure:", lesson_options, key="lesson_selector")
    
    if lesson_choice != "Choose a lesson...":
        # Find selected lesson
        selected_key = None
        for key in lessons.keys():
            if lessons[key]['title'] in lesson_choice:
                selected_key = key
                break
        
        if selected_key:
            lesson = lessons[selected_key]
            
            # Display lesson in beautiful card
            st.markdown(f'<div class="lesson-card">', unsafe_allow_html=True)
            st.markdown(f"## {lesson['title']}")
            st.markdown("---")
            
            for i, point in enumerate(lesson['content'], 1):
                st.markdown(f"### {i}. {point}")
                st.write("")
            
            st.markdown("---")
            st.markdown(f"**🤔 Fun Fact:** {lesson['fun_fact']}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"🔊 Listen to Lesson", key=f"listen_{selected_key}"):
                    lesson_text = f"{lesson['title']}. " + " ".join(lesson['content']) + f" Fun fact: {lesson['fun_fact']}"
                    
                    with st.spinner("🎵 Creating your audio lesson..."):
                        audio_bytes = text_to_speech_for_kids(lesson_text, slow=True)
                        
                    if audio_bytes:
                        st.success("🎵 Here's your lesson audio!")
                        audio_html = create_audio_player(audio_bytes)
                        st.markdown(audio_html, unsafe_allow_html=True)
                    else:
                        st.error("🔧 Audio is being prepared!")
            
            with col2:
                if st.button(f"✅ Mark Complete", key=f"complete_{selected_key}"):
                    st.session_state.lesson_progress[selected_key] = True
                    st.success("🎉 Awesome! Lesson completed!")
                    st.balloons()
                    
                    # Achievement audio
                    achievement_text = "Great job! You completed another lesson! You're becoming an AI expert!"
                    achievement_audio = text_to_speech_for_kids(achievement_text)
                    if achievement_audio:
                        audio_html = create_audio_player(achievement_audio)
                        st.markdown(audio_html, unsafe_allow_html=True)
            
            with col3:
                if selected_key in quiz_data:
                    if st.button(f"🧠 Take Quiz", key=f"quiz_{selected_key}"):
                        st.session_state.current_quiz = selected_key
                        st.session_state.quiz_question_index = 0
                        st.experimental_rerun()

def show_chat():
    st.header("🤖 Chat with Your AI Teacher!")
    st.markdown("### Ask me anything about AI! I love curious kids like you! 🎉")
    
    # Chat interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "💭 What's your question?", 
            placeholder="What is AI? How does it work? Tell me a joke!",
            key="main_chat_input"
        )
    
    with col2:
        ask_button = st.button("🚀 Ask!", key="main_ask_btn")
    
    # Process question
    if ask_button and user_question:
        with st.spinner("🤖 AI Teacher is thinking..."):
            time.sleep(1)  # Add realistic thinking time
            
            # Get AI response
            ai_response = st.session_state.chatbot.get_response(user_question)
            
            # Add to chat history
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("AI Teacher", ai_response))
            
            # Create and play audio
            audio_bytes = text_to_speech_for_kids(ai_response)
            if audio_bytes:
                st.success("🔊 Listen to my answer!")
                audio_html = create_audio_player(audio_bytes)
                st.markdown(audio_html, unsafe_allow_html=True)
    
    # Quick question buttons
    st.markdown("### 🎯 Try These Questions:")
    quick_questions = [
        "What is AI?", 
        "How does AI work?", 
        "Tell me a joke!", 
        "Can I build AI?", 
        "Where is AI?", 
        "Are you real?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(quick_questions):
        col_index = i % 3
        if cols[col_index].button(question, key=f"quick_{i}"):
            # Process quick question
            ai_response = st.session_state.chatbot.get_response(question)
            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("AI Teacher", ai_response))
            
            # Play audio for quick question
            audio_bytes = text_to_speech_for_kids(ai_response)
            if audio_bytes:
                audio_html = create_audio_player(audio_bytes)
                st.markdown(audio_html, unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Our Amazing Conversation:")
        
        # Show recent messages (last 10)
        recent_messages = st.session_state.chat_history[-10:]
        
        for speaker, message in recent_messages:
            if speaker == "You":
                st.markdown(f'<div class="chat-bubble-user"><strong>👦 You:</strong> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai"><strong>🤖 AI Teacher:</strong> {message}</div>', unsafe_allow_html=True)
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Start New Conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.experimental_rerun()

def show_games():
    st.header("🎮 Amazing AI Games for Smart Kids!")
    
    # Game tabs
    game_tabs = st.tabs(["🐱🐶 Pet Guesser", "🎬 Show Picker", "🎨 Draw & Guess", "🧠 Quick Quiz"])
    
    # Cat vs Dog Game
    with game_tabs[0]:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🐱🐶 AI Pet Guesser!")
        st.markdown("**Upload a picture and I'll guess if it's a cat or dog!**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "📁 Choose a cute pet picture:",
                type=['png', 'jpg', 'jpeg', 'webp'],
                key="pet_uploader"
            )
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Your awesome pet! 📸", width=350)
                
                if st.button("🔍 Let AI Guess!", key="guess_pet"):
                    with st.spinner("🤖 AI is analyzing your picture..."):
                        time.sleep(2)
                        
                        # Enhanced guessing logic
                        guesses = [
                            {"result": "🐱 CUTE CAT", "message": "I think this is a beautiful cat! Cats are amazing! 🐱", "confidence": random.randint(85, 95)},
                            {"result": "🐶 AWESOME DOG", "message": "I think this is a fantastic dog! Dogs are wonderful! 🐶", "confidence": random.randint(85, 95)},
                            {"result": "🥰 ADORABLE PET", "message": "I see an absolutely adorable pet! Is it a cat or dog? 🥰", "confidence": random.randint(75, 85)}
                        ]
                        
                        result = random.choice(guesses)
                        
                        st.success(f"🎯 **My AI Guess:** {result['result']}")
                        st.info(result['message'])
                        
                        # Progress bar for confidence
                        st.write(f"**AI Confidence:** {result['confidence']}%")
                        st.progress(result['confidence'] / 100)
                        
                        if result['confidence'] > 80:
                            st.balloons()
                            
                        # Educational note
                        st.markdown("---")
                        st.info("🤖 **How AI Does This:** AI looks at shapes, colors, and patterns in your picture and compares them to thousands of cat and dog photos it learned from!")
        
        with col2:
            st.markdown("### 🤖 How AI Recognizes Pets:")
            st.write("1. 👀 **Looks** at your picture")
            st.write("2. 🔍 **Finds** shapes and patterns")
            st.write("3. 🧠 **Compares** to training data")
            st.write("4. 🎯 **Makes** its best guess!")
            
            st.info("💡 **Amazing Fact:** AI needs to see thousands of pictures to learn the difference!")
    
    # Cartoon Recommender
    with game_tabs[1]:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🎬 AI Show Recommender!")
        st.markdown("**Tell me what you like and get perfect show suggestions!**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 🎯 What kind of shows do you love most?")
        
        preference = st.radio(
            "Pick your favorite type:",
            [
                "🗡️ Adventure and action shows!", 
                "😂 Funny and silly cartoons!", 
                "📚 Educational and learning shows!", 
                "🦸‍♂️ Superhero adventures!", 
                "🦁 Animal and nature shows!"
            ],
            key="show_preference"
        )
        
        if st.button("🌟 Get My Perfect Shows!", key="get_shows"):
            with st.spinner("🤖 AI is finding perfect shows for you..."):
                time.sleep(1)
                
                # Show recommendations database
                recommendations = {
                    "🗡️ Adventure and action shows!": [
                        {"name": "🦸‍♀️ Avatar: The Last Airbender", "why": "Epic adventures with amazing powers and great characters!"},
                        {"name": "🗡️ Adventure Time", "why": "Crazy fun adventures in magical lands with Finn and Jake!"},
                        {"name": "🌟 Steven Universe", "why": "Magical gem warriors with heart and friendship!"}
                    ],
                    "😂 Funny and silly cartoons!": [
                        {"name": "🧽 SpongeBob SquarePants", "why": "The funniest underwater adventures with SpongeBob!"},
                        {"name": "🐻 We Bare Bears", "why": "Three hilarious bear brothers and their silly adventures!"},
                        {"name": "🐱 The Amazing World of Gumball", "why": "The most creative and funny cat family ever!"}
                    ],
                    "📚 Educational and learning shows!": [
                        {"name": "🔬 Bill Nye the Science Guy", "why": "Learn amazing science with fun experiments!"},
                        {"name": "🌍 Wild Kratts", "why": "Discover incredible animals and nature!"},
                        {"name": "🧮 Cyberchase", "why": "Learn math while solving cool mysteries!"}
                    ],
                    "🦸‍♂️ Superhero adventures!": [
                        {"name": "🕷️ Ultimate Spider-Man", "why": "Amazing web-slinging superhero action!"},
                        {"name": "⚡ Teen Titans", "why": "Awesome teen superheroes saving the world!"},
                        {"name": "🔥 Ben 10", "why": "Transform into incredible aliens with cool powers!"}
                    ],
                    "🦁 Animal and nature shows!": [
                        {"name": "🦁 The Lion King", "why": "Epic story of Simba and the Pride Lands!"},
                        {"name": "🐧 Madagascar", "why": "Zoo animals on the most fun adventures!"},
                        {"name": "🐠 Finding Nemo", "why": "Underwater family adventure with beautiful fish!"}
                    ]
                }
                
                shows = recommendations.get(preference, recommendations["🗡️ Adventure and action shows!"])
                
                st.success("🎉 Here are your perfect shows!")
                
                for i, show in enumerate(shows, 1):
                    st.markdown(f"### {i}. {show['name']}")
                    st.write(f"   💡 **Why you'll love it:** {show['why']}")
                    st.write("")
                
                st.balloons()
                
                # AI explanation
                st.markdown("---")
                st.info("🤖 **How AI Recommends:** AI looks at what you enjoy and finds shows with similar themes, characters, and story types that match your interests!")
    
    # Drawing Game
    with game_tabs[2]:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🎨 Draw & Guess Game!")
        st.markdown("**Describe your drawing and I'll try to guess what it is!**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            drawing_description = st.text_area(
                "🖊️ Tell me about your drawing:",
                placeholder="I drew something round like the sun with rays coming out...",
                height=100,
                key="drawing_input"
            )
            
            if st.button("🤖 Let AI Guess My Art!", key="guess_drawing") and drawing_description:
                with st.spinner("🎨 AI is thinking about your masterpiece..."):
                    time.sleep(1)
                    
                    description = drawing_description.lower()
                    
                    # Smart guessing logic
                    if any(word in description for word in ['round', 'circle', 'ball', 'sun']):
                        possible_guesses = ["sun ☀️", "ball ⚽", "clock 🕐", "moon 🌙", "wheel 🎡"]
                    elif any(word in description for word in ['square', 'box', 'rectangle']):
                        possible_guesses = ["present 🎁", "window 🪟", "book 📚", "TV 📺"]
                    elif any(word in description for word in ['triangle', 'pointy', 'sharp']):
                        possible_guesses = ["mountain ⛰️", "tree 🌲", "house roof 🏠", "arrow 🏹"]
                    elif any(word in description for word in ['long', 'line', 'straight']):
                        possible_guesses = ["road 🛣️", "pencil ✏️", "stick 🥢", "ruler 📏"]
                    else:
                        possible_guesses = ["amazing artwork", "creative masterpiece", "beautiful drawing", "fantastic creation"]
                    
                    guess = random.choice(possible_guesses)
                    
                    encouragements = [
                        "🎨 Wow! That sounds like incredible artwork!",
                        "✨ You're such a creative and talented artist!",
                        "🌟 I love your imagination and artistic skills!",
                        "🏆 That's absolutely fantastic drawing!",
                        "💫 Your creativity is truly amazing!"
                    ]
                    
                    encouragement = random.choice(encouragements)
                    
                    st.success(f"🤖 I think you drew a **{guess}**!")
                    st.info(encouragement)
                    st.balloons()
                    
                    # Audio response
                    audio_text = f"I think you drew a {guess}! {encouragement}"
                    audio_bytes = text_to_speech_for_kids(audio_text)
                    if audio_bytes:
                        st.markdown("🔊 **Listen to my guess:**")
                        audio_html = create_audio_player(audio_bytes)
                        st.markdown(audio_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Drawing Ideas:")
            st.write("🔵 **Circles:** sun, ball, clock, moon")
            st.write("🔲 **Squares:** house, present, window") 
            st.write("🔺 **Triangles:** mountain, tree, roof")
            st.write("➖ **Lines:** road, pencil, stick")
            st.write("🌈 **Curves:** rainbow, smile, snake")
            
            st.info("💡 **AI Art Fact:** Real AI can now create amazing artwork by learning from millions of pictures!")
    
    # Quick Quiz
    with game_tabs[3]:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.subheader("🧠 Lightning Quick AI Quiz!")
        st.markdown("**Test your AI knowledge with fun questions!**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick quiz questions
        quick_quiz = [
            {
                "question": "🤖 What does AI stand for?",
                "options": ["Artificial Intelligence", "Amazing Internet", "Automatic Ideas"],
                "correct": 0,
                "explanation": "Perfect! AI stands for Artificial Intelligence! 🧠"
            },
            {
                "question": "🎓 How does AI learn best?",
                "options": ["From one example", "From many examples", "It doesn't learn"],
                "correct": 1,
                "explanation": "Exactly right! AI learns from lots and lots of examples! 📚"
            },
            {
                "question": "🏠 Where can we find AI today?",
                "options": ["Only in robots", "In phones and apps", "Nowhere"],
                "correct": 1,
                "explanation": "Yes! AI is in phones, apps, games, and many places! 📱"
            }
        ]
        
        if 'quick_quiz_index' not in st.session_state:
            st.session_state.quick_quiz_index = 0
        if 'quick_quiz_score' not in st.session_state:
            st.session_state.quick_quiz_score = 0
        
        if st.session_state.quick_quiz_index < len(quick_quiz):
            current_q = quick_quiz[st.session_state.quick_quiz_index]
            
            st.markdown(f"### Question {st.session_state.quick_quiz_index + 1}: {current_q['question']}")
            
            answer = st.radio(
                "Choose your answer:",
                current_q['options'],
                key=f"quick_quiz_{st.session_state.quick_quiz_index}"
            )
            
            if st.button("✅ Submit Answer", key=f"submit_quick_{st.session_state.quick_quiz_index}"):
                correct_idx = current_q['correct']
                
                if current_q['options'].index(answer) == correct_idx:
                    st.success(f"🎉 Correct! {current_q['explanation']}")
                    st.session_state.quick_quiz_score += 1
                    st.balloons()
                    
                    # Correct answer audio
                    audio_bytes = text_to_speech_for_kids(f"Correct! {current_q['explanation']}")
                    if audio_bytes:
                        audio_html = create_audio_player(audio_bytes)
                        st.markdown(audio_html, unsafe_allow_html=True)
                else:
                    st.error(f"Not quite right! {current_q['explanation']}")
                    
                    # Try again audio
                    audio_bytes = text_to_speech_for_kids(f"Good try! {current_q['explanation']}")
                    if audio_bytes:
                        audio_html = create_audio_player(audio_bytes)
                        st.markdown(audio_html, unsafe_allow_html=True)
                
                st.session_state.quick_quiz_index += 1
                time.sleep(2)
                st.experimental_rerun()
        else:
            # Quiz completed
            score_percent = (st.session_state.quick_quiz_score / len(quick_quiz)) * 100
            
            st.markdown(f'<div class="progress-card">', unsafe_allow_html=True)
            st.markdown(f"## 🏆 Quiz Complete!")
            st.markdown(f"### Your Score: {st.session_state.quick_quiz_score}/{len(quick_quiz)} ({score_percent:.0f}%)")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if score_percent == 100:
                st.success("🌟 Perfect score! You're an AI genius!")
                st.balloons()
            elif score_percent >= 70:
                st.success("🎯 Excellent work! You know a lot about AI!")
            else:
                st.info("🤗 Good effort! Keep learning about AI!")
            
            if st.button("🔄 Play Again"):
                st.session_state.quick_quiz_score = 0
                st.session_state.quick_quiz_index = 0
                st.experimental_rerun()

def show_quiz():
    st.header("🧠 Complete AI Knowledge Quiz!")
    
    if st.session_state.current_quiz is None:
        st.markdown("### 📚 Choose a lesson to quiz yourself on:")
        
        for lesson_key, lesson_data in lessons.items():
            if lesson_key in quiz_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{lesson_data['emoji']} **{lesson_data['title']}**")
                with col2:
                    if st.button(f"Take Quiz", key=f"start_quiz_{lesson_key}"):
                        st.session_state.current_quiz = lesson_key
                        st.session_state.quiz_question_index = 0
                        st.experimental_rerun()
    else:
        # Show quiz
        lesson_key = st.session_state.current_quiz
        questions = quiz_data[lesson_key]
        
        if st.session_state.quiz_question_index < len(questions):
            current_q = questions[st.session_state.quiz_question_index]
            
            st.markdown(f"## Quiz: {lessons[lesson_key]['title']}")
            st.markdown(f"### Question {st.session_state.quiz_question_index + 1}/{len(questions)}")
            st.markdown(f"### {current_q['question']}")
            
            answer = st.radio(
                "Choose your answer:",
                current_q['options'],
                key=f"quiz_answer_{lesson_key}_{st.session_state.quiz_question_index}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Submit", key="submit_quiz_answer"):
                    if current_q['options'].index(answer) == current_q['correct']:
                        st.success(current_q['explanation'])
                        st.balloons()
                    else:
                        st.error(f"Try again! {current_q['explanation']}")
                    
                    st.session_state.quiz_question_index += 1
                    time.sleep(2)
                    st.experimental_rerun()
            
            with col2:
                if st.button("🚪 Exit Quiz", key="exit_quiz"):
                    st.session_state.current_quiz = None
                    st.session_state.quiz_question_index = 0
                    st.experimental_rerun()
        else:
            st.success(f"🎉 Quiz completed for {lessons[lesson_key]['title']}!")
            st.balloons()
            
            if st.button("🏠 Back to Quiz Menu"):
                st.session_state.current_quiz = None
                st.session_state.quiz_question_index = 0
                st.experimental_rerun()

def show_progress():
    st.header("🏆 Your Amazing Learning Journey!")
    
    # Progress metrics
    completed_lessons = len([k for k, v in st.session_state.lesson_progress.items() if v])
    total_lessons = len(lessons)
    chat_messages = len(st.session_state.chat_history) // 2
    
    # Progress cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        st.metric("📚 Lessons Completed", f"{completed_lessons}/{total_lessons}")
        progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        st.progress(progress / 100)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        st.metric("💬 AI Conversations", chat_messages)
        st.write("Keep asking questions!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        completion_rate = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        st.metric("🎯 Overall Progress", f"{completion_rate:.0f}%")
        if completion_rate == 100:
            st.write("🌟 AI Expert!")
        elif completion_rate >= 75:
            st.write("🚀 Almost there!")
        elif completion_rate >= 50:
            st.write("📈 Great progress!")
        else:
            st.write("🌱 Keep learning!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Achievements
    st.markdown("### 🏅 Your Achievements:")
    
    achievements = []
    if completed_lessons > 0:
        achievements.append("🎓 First Lesson Complete")
    if completed_lessons >= 3:
        achievements.append("📚 Knowledge Seeker")
    if completed_lessons >= 5:
        achievements.append("🧠 AI Expert")
    if chat_messages >= 5:
        achievements.append("💬 Curious Conversationalist")
    if chat_messages >= 10:
        achievements.append("🤖 AI Friend")
    
    if achievements:
        for achievement in achievements:
            st.success(f"✅ {achievement}")
    else:
        st.info("🌟 Complete lessons and chat with AI to earn achievements!")
    
    # Learning path
    st.markdown("### 🗺️ Your Learning Path:")
    
    for i, (lesson_key, lesson_data) in enumerate(lessons.items(), 1):
        status = "✅" if lesson_key in st.session_state.lesson_progress and st.session_state.lesson_progress[lesson_key] else "⭕"
        st.write(f"{status} **Lesson {i}:** {lesson_data['emoji']} {lesson_data['title']}")

def show_parents():
    st.header("👨‍👩‍👧‍👦 Information for Parents & Teachers")
    
    # Safety and privacy
    st.markdown("### 🛡️ Safety & Privacy First")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ **Privacy Protected**")
        st.write("• No personal data collected")
        st.write("• No photos stored")
        st.write("• Safe, educational content only")
        st.write("• No external links or ads")
    
    with col2:
        st.success("✅ **Educational Standards**")
        st.write("• Age-appropriate content (5-10 years)")
        st.write("• Curriculum-aligned concepts")
        st.write("• Interactive learning approach")
        st.write("• Progress tracking available")
    
    # Learning objectives
    st.markdown("### 🎯 Learning Objectives")
    
    objectives = [
        "🤖 **Basic AI Understanding**: What AI is and how it works",
        "🏠 **Real-world Applications**: Where kids encounter AI daily", 
        "🎓 **Learning Concepts**: How AI learns from examples",
        "🧠 **Human vs AI**: Understanding differences and similarities",
        "🔧 **AI Types**: Different kinds of AI and their purposes",
        "⚖️ **Ethics & Responsibility**: Using AI for good"
    ]
    
    for objective in objectives:
        st.write(f"• {objective}")
    
    # Technical details
    st.markdown("### 🔧 Technical Information")
    
    tech_info = {
        "Platform": "Web-based Streamlit application",
        "AI Features": "Text-to-speech, chatbot, simple image recognition",
        "Accessibility": "Audio support, large fonts, emoji-rich interface",
        "Data Storage": "Session-based only, no permanent data storage",
        "Requirements": "Modern web browser, internet connection for audio"
    }
    
    for key, value in tech_info.items():
        st.write(f"**{key}:** {value}")
    
    # Tips for parents
    st.markdown("### 💡 Tips for Parents & Teachers")
    
    tips = [
        "👥 **Learn Together**: Explore the lessons alongside your child",
        "🗣️ **Discuss Learning**: Talk about what they discovered",
        "🎯 **Encourage Questions**: Foster curiosity about technology",
        "🎮 **Use Games**: Learning through play is most effective",
        "📱 **Real-world Connections**: Point out AI in daily life",
        "⏰ **Set Learning Time**: 15-20 minutes sessions work best"
    ]
    
    for tip in tips:
        st.info(tip)
    
    # Contact and feedback
    st.markdown("### 📞 Feedback & Support")
    st.write("This AI Virtual Teacher was created as an educational prototype.")
    st.write("For questions about child digital literacy or AI education, consult your school's technology coordinator.")
    
    if st.button("📊 View Child's Progress Summary"):
        completed = len([k for k, v in st.session_state.lesson_progress.items() if v])
        total = len(lessons)
        chats = len(st.session_state.chat_history) // 2
        
        summary = f"""
        ## 📈 Learning Progress Summary
        
        **Lessons Completed:** {completed} out of {total} ({(completed/total*100):.0f}%)
        **AI Conversations:** {chats} exchanges
        **Engagement Level:** {'High' if chats > 5 else 'Good' if chats > 0 else 'Starting'}
        **Recommended Next Steps:** {'Take more quizzes' if completed > 3 else 'Continue with lessons'}
        
        **Skills Developed:**
        • Basic AI concept understanding ✅
        • Technology curiosity ✅ 
        • Interactive learning ✅
        """
        
        st.markdown(summary)

# =================== RUN THE APP ===================

if __name__ == "__main__":
    main()
