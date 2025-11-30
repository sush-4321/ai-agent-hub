\# 🤖 AI Agent Hub



\*\*Sales, Marketing \& Support Intelligence System\*\*



A powerful multi-agent AI system built with Python and Streamlit for automating customer support, product recommendations, and social media content generation.



!\[Python](https://img.shields.io/badge/Python-3.14+-blue.svg)

!\[Streamlit](https://img.shields.io/badge/Streamlit-1.51+-red.svg)

!\[License](https://img.shields.io/badge/License-MIT-green.svg)



\## 🎯 Features



\### 💬 Support Assistant

\- ✅ Automated FAQ responses

\- ✅ Intelligent query routing

\- ✅ Escalation management with ticket generation

\- ✅ Handles shipping, returns, payments, tracking, warranty queries



\### 🛍️ Product Recommender

\- ✅ Smart product suggestions based on categories

\- ✅ Budget-friendly and premium filtering

\- ✅ Real-time product information with ratings

\- ✅ Electronics, Fashion, and Home products



\### 📱 Social Media Agent

\- ✅ Automated content generation

\- ✅ Platform-optimized templates

\- ✅ Product launch, engagement, and promotional content

\- ✅ Hashtag suggestions included



\## 📸 Screenshots



\### Main Interface

!\[Screenshot1](screenshots/Screenshot1.png)

\*Multi-agent dashboard with Support, Product, and Social Media agents\*



\### Support Assistant in Action

!\[Screenshot2](screenshots/Screenshot2.png)

\*Automated FAQ handling with intelligent escalation\*



\### Product Recommendations

!\[Screenshot3](screenshots/Screenshot3.png)

\*Smart product suggestions with ratings and pricing\*



\### Social Media Content Generation

!\[Screenshot4](screenshots/Screenshot4.png)

\*AI-powered content ideas for engagement and promotions\*



\## 🚀 Quick Start



\### Prerequisites

\- Python 3.11 or higher

\- pip package manager



\### Installation



\*\*1. Clone the repository\*\*

```bash

git clone https://github.com/sush-4321/ai-agent-hub.git

cd ai-agent-hub

```



\*\*2. Create virtual environment\*\*

```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# Mac/Linux

python3 -m venv venv

source venv/bin/activate

```



\*\*3. Install dependencies\*\*

```bash

pip install streamlit

```



\*\*4. Run the application\*\*

```bash

streamlit run app.py

```



\*\*5. Open browser\*\*

Navigate to `http://localhost:8501`



\## 📁 Project Structure

```

ai-agent-hub/

├── app.py                      # Main Streamlit application

├── agents/

│   ├── \_\_init\_\_.py

│   ├── base\_agent.py          # Base agent class

│   ├── support\_agent.py       # Support logic \& FAQ handling

│   ├── product\_agent.py       # Product recommendation engine

│   └── social\_agent.py        # Social media content generator

├── data/

│   ├── faqs.json              # FAQ knowledge base

│   ├── products.json          # Product catalog

│   └── social\_templates.json  # Content templates

├── .streamlit/

│   └── config.toml            # Streamlit theme configuration

└── README.md

```



\## 🎮 Usage Examples



\### Support Agent Queries

```

💬 "What's your shipping policy?"

💬 "How do I return an item?"

💬 "This product is damaged!"  → Triggers escalation with ticket

💬 "Track my order"

💬 "What payment methods do you accept?"

```



\### Product Agent Queries

```

🛍️ "Show me electronics"

🛍️ "Budget-friendly options"

🛍️ "Premium products"

🛍️ "Fashion items"

```



\### Social Media Agent Queries

```

📱 "Product launch ideas"

📱 "Engagement content"

📱 "Sale promotions"

📱 "Giveaway post"

```



\## 🛠️ Tech Stack



\- \*\*Framework\*\*: Streamlit 1.51+

\- \*\*Language\*\*: Python 3.14+

\- \*\*Architecture\*\*: Multi-agent object-oriented design

\- \*\*Data Storage\*\*: JSON-based knowledge bases

\- \*\*UI\*\*: Responsive web interface with custom CSS



\## ⚙️ Configuration



The app uses `.streamlit/config.toml` for theming:

\- Custom purple gradient header

\- Dark theme optimized

\- Responsive layout



\## 📈 Features Roadmap



\- \[ ] Integration with OpenAI GPT-4 / Anthropic Claude API

\- \[ ] Database persistence (PostgreSQL/MongoDB)

\- \[ ] User authentication \& session management

\- \[ ] Email/SMS notifications for escalations

\- \[ ] Analytics dashboard with metrics

\- \[ ] REST API endpoints

\- \[ ] Multi-language support

\- \[ ] CRM integration (Salesforce, HubSpot)

\- \[ ] Advanced sentiment analysis

\- \[ ] A/B testing for social content



\## 🎨 Customization



\### Modify FAQs

Edit `data/faqs.json` to add/update support responses



\### Add Products

Update `data/products.json` with your product catalog



\### Customize Templates

Modify `data/social\_templates.json` for brand-specific content



\### Change Theme

Edit `.streamlit/config.toml` for colors and styling



\## 📝 License



MIT License - feel free to use this project for learning and development.



\## 👤 Author



\*\*Sushmita\*\*

\- GitHub: \[@sush-4321](https://github.com/sush-4321)

\- Project: \[AI Agent Hub](https://github.com/sush-4321/ai-agent-hub)



\## 🤝 Contributing



Contributions, issues, and feature requests are welcome!



1\. Fork the project

2\. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3\. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4\. Push to the branch (`git push origin feature/AmazingFeature`)

5\. Open a Pull Request



\## ⭐ Show Your Support



Give a ⭐️ if this project helped you learn about multi-agent systems!



\## 📧 Contact



For questions or feedback, please open an issue on GitHub.



---



\*\*Built with ❤️ using Python and Streamlit\*\*

