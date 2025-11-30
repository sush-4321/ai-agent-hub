"""
AI Agent Hub - Main Streamlit Application
Sales, Marketing & Support Intelligence
"""

import streamlit as st
from agents.support_agent import SupportAgent
from agents.product_agent import ProductAgent
from agents.social_agent import SocialAgent
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Agent Hub",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'active_agent' not in st.session_state:
    st.session_state.active_agent = 'support'

# Initialize agents
@st.cache_resource
def load_agents():
    return {
        'support': SupportAgent(),
        'product': ProductAgent(),
        'social': SocialAgent()
    }

agents = load_agents()

# Custom CSS
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

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Agent Hub</h1>
    <p>Sales, Marketing & Support Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Agent selection
col1, col2, col3 = st.columns(3)

agent_info = {
    'support': {
        'name': '💬 Support Assistant',
        'desc': 'FAQs & Escalations',
        'col': col1
    },
    'product': {
        'name': '🛍️ Product Recommender',
        'desc': 'Smart Suggestions',
        'col': col2
    },
    'social': {
        'name': '📱 Social Media Agent',
        'desc': 'Content Generation',
        'col': col3
    }
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

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display additional data
        if "data" in message:
            if message["data"].get("type") == "recommendations":
                st.markdown("---")
                for product in message["data"].get("products", []):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{product['name']}**")
                        st.caption(" | ".join(product.get('features', [])))
                    with col2:
                        st.markdown(f"**${product['price']}**")
                        st.caption(f"⭐ {product.get('rating', 'N/A')}")
                    st.markdown("")
            
            elif message["data"].get("type") == "social_content":
                st.markdown("---")
                for idea in message["data"].get("ideas", []):
                    st.info(f"**Idea #{idea['id']}**\n\n{idea['content']}")
            
            if message["data"].get("escalate"):
                st.warning(f"🎫 **Ticket Created:** {message['data'].get('ticket_number', 'N/A')}")

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Get agent response
    with st.spinner("Processing..."):
        response = agents[st.session_state.active_agent].process_query(prompt)
    
    # Add bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['response'],
        "data": response
    })
    
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("Active Agent", agent_info[st.session_state.active_agent]['name'])
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    # Quick action buttons based on active agent
    if st.session_state.active_agent == 'support':
        actions = ['Shipping info', 'Return policy', 'Track order', 'Payment methods']
    elif st.session_state.active_agent == 'product':
        actions = ['Show electronics', 'Fashion items', 'Home goods', 'Budget options']
    else:
        actions = ['Product launch', 'Engagement post', 'Sale promo', 'Content ideas']
    
    for action in actions:
        if st.button(action, key=f"quick_{action}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": action})
            response = agents[st.session_state.active_agent].process_query(action)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['response'],
                "data": response
            })
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    **AI Agent Hub** provides intelligent automation for:
    
    - Customer Support
    - Product Recommendations
    - Social Media Content
    
    Built with Python & Streamlit
    """)