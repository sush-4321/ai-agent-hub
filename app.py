"""
AI Agent Hub - Light Theme Version
"""

import streamlit as st
from agents.support_agent import SupportAgent
from agents.product_agent import ProductAgent
from agents.social_agent import SocialAgent
from agents.analytics_agent import AnalyticsAgent
from datetime import datetime
import time
import json
from utils.summarizer import ConversationSummarizer

# Page config
st.set_page_config(page_title="AI Agent Hub", page_icon="🤖", layout="wide")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'active_agent' not in st.session_state:
    st.session_state.active_agent = 'support'

# Load agents
@st.cache_resource
def load_agents():
    return {
        'support': SupportAgent(),
        'product': ProductAgent(),
        'social': SocialAgent(),
        'analytics': AnalyticsAgent()
    }

agents = load_agents()

# Simple CSS for better visibility
st.markdown("""
<style>
    /* Main header */
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.8rem;
        margin: 0;
        font-weight: 800;
    }
    
    .main-header p {
        color: white !important;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Larger buttons */
    .stButton > button {
        min-height: 100px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
    }
    
    /* Subheaders with color */
    .stMarkdown h2, .stMarkdown h3 {
        color: #667eea !important;
    }
    
    /* Metrics with better contrast */
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #262730 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Hub</h1>
    <p>Sales, Marketing & Support Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Agent selection
st.markdown("## 🎯 Select Your AI Agent")

col1, col2, col3, col4 = st.columns(4)

agents_info = {
    'support': ('💬 Support Assistant', 'FAQs & Escalations', col1),
    'product': ('🛍️ Product Recommender', 'Smart Suggestions', col2),
    'social': ('📱 Social Media Agent', 'Content Generation', col3),
    'analytics': ('📊 Analytics Dashboard', 'Insights & Metrics', col4)
}

for agent_id, (name, desc, col) in agents_info.items():
    with col:
        button_type = "primary" if st.session_state.active_agent == agent_id else "secondary"
        if st.button(f"**{name}**\n\n{desc}", key=f"agent_{agent_id}", type=button_type, use_container_width=True):
            st.session_state.active_agent = agent_id
            st.rerun()

st.divider()

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if "data" in message and message["data"].get("sentiment"):
            sentiment = message["data"]["sentiment"]
            st.caption(f"{sentiment['emoji']} **Sentiment:** {sentiment['sentiment']} | **Score:** {sentiment['score']}")
        
        if "response_time_ms" in message:
            st.caption(f"⚡ **Response time:** {message['response_time_ms']}ms")
        
        if "data" in message:
            data = message["data"]
            
            # Product recommendations
            if data.get("type") == "recommendations":
                st.divider()
                st.markdown("### 🛍️ Recommended Products")
                for product in data.get("products", []):
                    with st.expander(f"**{product['name']}** - ${product['price']}", expanded=True):
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            st.write(f"**Category:** {product['category']}")
                            st.write(f"**Features:** {', '.join(product.get('features', []))}")
                        with col_b:
                            st.metric("Price", f"${product['price']}")
                            st.write(f"**Rating:** {'⭐' * int(product.get('rating', 0))}")
            
            # Social media content
            elif data.get("type") == "social_content":
                st.divider()
                st.markdown("### 📱 Social Media Posts")
                for idea in data.get("ideas", []):
                    st.info(f"**{idea.get('platform', 'Platform')} - {idea.get('type', 'Post')}**\n\n{idea['content']}")
            
            # Analytics dashboard
            elif data.get("type") == "analytics":
                st.divider()
                metrics = data.get("metrics", {})
                agent_type = data.get("agent_type", 'all')
                
                if agent_type in ['all', 'support']:
                    st.markdown("### 💬 Support Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("**Total Queries**", metrics['support']['total_queries'])
                    with c2:
                        st.metric("**Resolved**", metrics['support']['resolved'])
                    with c3:
                        st.metric("**Avg Response Time**", f"{metrics['support']['avg_response_time']}min")
                    with c4:
                        st.metric("**Satisfaction**", f"{metrics['support']['satisfaction_rate']}%")
                
                if agent_type in ['all', 'products']:
                    st.markdown("### 🛍️ Product Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("**Recommendations**", metrics['products']['recommendations_made'])
                    with c2:
                        st.metric("**Conversion Rate**", f"{metrics['products']['conversion_rate']}%")
                    with c3:
                        st.metric("**Avg Order Value**", f"${metrics['products']['avg_order_value']}")
                    with c4:
                        st.metric("**Top Category**", metrics['products']['top_category'])
                
                if agent_type in ['all', 'social']:
                    st.markdown("### 📱 Social Media Metrics")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("**Posts Generated**", metrics['social']['posts_generated'])
                    with c2:
                        st.metric("**Engagement Rate**", f"{metrics['social']['engagement_rate']}%")
                    with c3:
                        st.metric("**Reach**", f"{metrics['social']['reach']:,}")
                    with c4:
                        st.metric("**Best Performing**", metrics['social']['best_performing'])
            
            if data.get("escalate"):
                st.warning(f"🎫 **Ticket Created:** {data.get('ticket_number', 'N/A')}")

# Chat input
if prompt := st.chat_input("💬 Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        for msg in ["🤖 Thinking", "🤖 Thinking.", "🤖 Thinking..", "🤖 Thinking..."]:
            message_placeholder.markdown(msg)
            time.sleep(0.2)
        
        start_time = time.time()
        response = agents[st.session_state.active_agent].process_query(prompt)
        response_time = round((time.time() - start_time) * 1000, 2)
        message_placeholder.markdown(response['response'])
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['response'],
        "data": response,
        "response_time_ms": response_time
    })
    st.rerun()

# Suggested queries
st.divider()
st.markdown("## 💡 Quick Actions - Try These Queries")

suggestions = {
    'support': [
        "📦 What's your return policy?",
        "🚚 How can I track my order?",
        "⚠️ This product arrived damaged",
        "💳 What payment methods do you accept?"
    ],
    'product': [
        "💻 Show me budget electronics",
        "⭐ Recommend premium products",
        "👔 What's in the fashion category?",
        "🔥 Show me top-rated items"
    ],
    'social': [
        "🚀 Create a product launch post",
        "💬 Give me engagement ideas",
        "💰 Write a sale promotion",
        "🎁 Generate contest content"
    ],
    'analytics': [
        "📊 Show overall metrics",
        "💬 Support agent performance",
        "🛍️ Product recommendation stats",
        "📱 Social media engagement"
    ]
}

cols = st.columns(2)
for idx, suggestion in enumerate(suggestions[st.session_state.active_agent]):
    with cols[idx % 2]:
        if st.button(suggestion, key=f"quick_{idx}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            start_time = time.time()
            response = agents[st.session_state.active_agent].process_query(suggestion)
            response_time = round((time.time() - start_time) * 1000, 2)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['response'],
                "data": response,
                "response_time_ms": response_time
            })
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("# 📊 Dashboard")
    
    st.metric("📨 Total Messages", len(st.session_state.messages))
    
    active_names = {
        'support': '💬 Support Assistant',
        'product': '🛍️ Product Recommender',
        'social': '📱 Social Media Agent',
        'analytics': '📊 Analytics Dashboard'
    }
    st.metric("🤖 Active Agent", active_names[st.session_state.active_agent])
    
    if st.session_state.messages:
        st.divider()
        st.markdown("## 📝 Session Summary")
        summary = ConversationSummarizer.summarize(st.session_state.messages)
        
        st.metric("👤 User Messages", summary['user_messages'])
        st.metric("🤖 Bot Messages", summary['bot_messages'])
        
        if summary['topics']:
            st.markdown("**📌 Topics Discussed:**")
            for topic in summary['topics']:
                st.write(f"• {topic.title()}")
        
        st.markdown(f"**😊 Overall Sentiment:** {summary['sentiment_overview']}")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("## 📥 Export Data")
    
    if st.button("📄 Export Chat", use_container_width=True):
        if st.session_state.messages:
            export_data = {
                'agent': st.session_state.active_agent,
                'timestamp': datetime.now().isoformat(),
                'total_messages': len(st.session_state.messages),
                'messages': st.session_state.messages
            }
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name=f"ai_agent_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("💡 Start a conversation to export!")
    
    st.divider()
    st.caption("🤖 AI Agent Hub v1.0")
    st.caption("Built with Streamlit")