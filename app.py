"""
AI Agent Hub - Main Streamlit Application
Sales, Marketing & Support Intelligence
"""

import streamlit as st
from agents.support_agent import SupportAgent
from agents.product_agent import ProductAgent
from agents.social_agent import SocialAgent
from agents.analytics_agent import AnalyticsAgent
from datetime import datetime
import time
import json

# -------------------------
# NEW: Conversation summarizer
# -------------------------
from utils.summarizer import ConversationSummarizer

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="AI Agent Hub",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Initialize session state
# -------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'active_agent' not in st.session_state:
    st.session_state.active_agent = 'support'

# -------------------------
# Initialize agents
# -------------------------
@st.cache_resource
def load_agents():
    return {
        'support': SupportAgent(),
        'product': ProductAgent(),
        'social': SocialAgent(),
        'analytics': AnalyticsAgent()
    }

agents = load_agents()

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Hub</h1>
    <p>Sales, Marketing & Support Intelligence</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Agent selection
# -------------------------
col1, col2, col3, col4 = st.columns(4)
agent_info = {
    'support': {'name': '💬 Support Assistant', 'desc': 'FAQs & Escalations', 'col': col1},
    'product': {'name': '🛍️ Product Recommender', 'desc': 'Smart Suggestions', 'col': col2},
    'social': {'name': '📱 Social Media Agent', 'desc': 'Content Generation', 'col': col3},
    'analytics': {'name': '📊 Analytics Dashboard', 'desc': 'Insights & Metrics', 'col': col4}
}

for agent_id, info in agent_info.items():
    with info['col']:
        if st.button(
            f"{info['name']}\n{info['desc']}",
            key=agent_id,
            use_container_width=True,
            type="primary" if st.session_state.active_agent == agent_id else "secondary"
        ):
            st.session_state.active_agent = agent_id
            st.session_state.messages = []
            st.rerun()

st.markdown("---")

# -------------------------
# Display chat messages
# -------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sentiment if available
        if "data" in message and "sentiment" in message["data"]:
            sentiment = message["data"]["sentiment"]
            st.caption(f"{sentiment['emoji']} Sentiment: {sentiment['sentiment']} (Score: {sentiment['score']})")

        # Show response time if available
        if "response_time_ms" in message:
            st.caption(f"⚡ Response time: {message['response_time_ms']}ms")

        # Show additional data (products / analytics / tickets)
        if "data" in message:
            data = message["data"]

            if data.get("type") == "recommendations":
                st.markdown("---")
                for product in data.get("products", []):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{product['name']}**")
                        st.caption(" | ".join(product.get('features', [])))
                    with c2:
                        st.markdown(f"**${product['price']}**")
                        st.caption(f"⭐ {product.get('rating', 'N/A')}")

            elif data.get("type") == "analytics":
                st.markdown("---")
                metrics = data.get("metrics", {})
                agent_type = data.get("agent_type", 'all')

                if agent_type in ['all', 'support']:
                    st.subheader("💬 Support Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Total Queries", metrics['support']['total_queries'])
                    with c2:
                        st.metric("Resolved", metrics['support']['resolved'])
                    with c3:
                        st.metric("Avg Response Time", f"{metrics['support']['avg_response_time']}min")
                    with c4:
                        st.metric("Satisfaction", f"{metrics['support']['satisfaction_rate']}%")

                if agent_type in ['all', 'products']:
                    st.subheader("🛍️ Product Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Recommendations", metrics['products']['recommendations_made'])
                    with c2:
                        st.metric("Conversion Rate", f"{metrics['products']['conversion_rate']}%")
                    with c3:
                        st.metric("Avg Order Value", f"${metrics['products']['avg_order_value']}")
                    with c4:
                        st.metric("Top Category", metrics['products']['top_category'])

                if agent_type in ['all', 'social']:
                    st.subheader("📱 Social Media Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Posts Generated", metrics['social']['posts_generated'])
                    with c2:
                        st.metric("Engagement Rate", f"{metrics['social']['engagement_rate']}%")
                    with c3:
                        st.metric("Reach", f"{metrics['social']['reach']:,}")
                    with c4:
                        st.metric("Best Performing", metrics['social']['best_performing'])

            if data.get("escalate"):
                st.warning(f"🎫 **Ticket Created:** {data.get('ticket_number', 'N/A')}")

# -------------------------
# Chat input with typing animation
# -------------------------
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Placeholder for typing animation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        typing_messages = ["🤖 Thinking", "🤖 Thinking.", "🤖 Thinking..", "🤖 Thinking..."]
        for msg in typing_messages:
            message_placeholder.markdown(msg)
            time.sleep(0.2)

        # Get response
        start_time = time.time()
        response = agents[st.session_state.active_agent].process_query(prompt)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)

        # Show actual response
        message_placeholder.markdown(response['response'])

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['response'],
        "data": response,
        "response_time_ms": response_time
    })
    st.rerun()

# -------------------------
# Smart suggestions
# -------------------------
st.markdown("### 💡 Suggested Queries")
suggestions = {
    'support': ["What's your return policy?", "How can I track my order?", "This product arrived damaged", "What payment methods do you accept?"],
    'product': ["Show me budget electronics", "Recommend premium products", "What's in the fashion category?", "Show me top-rated items"],
    'social': ["Create a product launch post", "Give me engagement ideas", "Write a sale promotion", "Generate contest content"],
    'analytics': ["Show overall metrics", "Support agent performance", "Product recommendation stats", "Social media engagement"]
}

cols = st.columns(2)
for idx, suggestion in enumerate(suggestions[st.session_state.active_agent]):
    with cols[idx % 2]:
        if st.button(f"💬 {suggestion}", key=f"suggest_{idx}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            start_time = time.time()
            response = agents[st.session_state.active_agent].process_query(suggestion)
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['response'],
                "data": response,
                "response_time_ms": response_time
            })
            st.rerun()

st.markdown("---")

# -------------------------
# Sidebar: Statistics, Summary, Export, Theme
# -------------------------
with st.sidebar:
    st.markdown("## 📊 Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("Active Agent", agent_info[st.session_state.active_agent]['name'])

    # -------------------------
    # Conversation Summary
    # -------------------------
    if st.session_state.messages:
        st.markdown("---")
        st.markdown("### 📝 Conversation Summary")
        summary = ConversationSummarizer.summarize(st.session_state.messages)

        st.metric("User Messages", summary['user_messages'])
        st.metric("Bot Messages", summary['bot_messages'])

        if summary['topics']:
            st.write("**Topics Discussed:**")
            for topic in summary['topics']:
                st.write(f"• {topic.title()}")

        st.write(f"**Overall Sentiment:** {summary['sentiment_overview']}")

    # -------------------------
    # Clear chat
    # -------------------------
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # -------------------------
    # Export data
    # -------------------------
    st.markdown("---")
    st.markdown("### 📥 Export Data")
    if st.button("📄 Export Chat History", use_container_width=True):
        if st.session_state.messages:
            export_data = {
                'agent': st.session_state.active_agent,
                'timestamp': datetime.now().isoformat(),
                'messages': st.session_state.messages
            }
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No messages to export yet!")

    # -------------------------
    # Theme toggle
    # -------------------------
    st.markdown("---")
    st.markdown("### 🎨 Settings")
    theme = st.selectbox("Theme", ["Dark", "Light", "Auto"], index=0)
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "Light":
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #0c0c0c;
        }
        </style>
        """, unsafe_allow_html=True)
