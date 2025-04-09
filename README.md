# 🍔🥦 Food and Grocery Delivery Support System 🚀

A **modular, extensible system** for handling food and grocery delivery customer support queries using **LangGraph, OpenAI, and computer vision** capabilities. 🛒📦

---

## ✨ Features

✅ **AI-powered classification** of customer complaints 🤖📊  
✅ **Automated refund processing** with receipt verification 💳✅  
✅ **Vision-based verification** of issues and bill amounts 🖼️📄  
✅ **Conversational agent** for customer support 🗣️💬  
✅ **Estimated delivery time** information ⏳🚚  
✅ **Service complaint handling** 📝❗  
✅ **Human escalation path** for complex issues 🆘👨‍💻  

---

## 📁 Project Structure

```
food_delivery_support/
├── config.py           # ⚙️ Configuration settings and constants
├── models.py           # 🤖 Model setup for LLMs and vision models
├── schemas.py          # 📜 Type definitions and data schemas
├── nodes.py            # 🔄 Node implementation functions
├── conditionals.py     # 🔀 Conditional routing functions
├── graph.py            # 🕸️ Graph construction logic
├── main.py             # 🚀 Main application entry point
├── setup.py            # 🔧 Installation and setup script
└── README.md           # 📖 Project documentation
```

---

## ⚡ Installation

1️⃣ Run the setup script to install required packages and configure the environment:

```bash
python setup.py
```

2️⃣ Enter your **OpenAI API key** when prompted. 🔑

---

## 🚀 Usage

Run the main application to start the support agent:

```bash
python main.py
```

Follow the prompts to interact with the support system. 🤝

---

## 🔄 Workflow

1️⃣ **User submits an initial complaint** 📝  
2️⃣ **System classifies the complaint** as refundable or non-refundable 🏷️  
3️⃣ **For refundable issues**:
   - ✅ System verifies the problem with **image proof** 📷
   - ✅ System verifies **bill amount** with **receipt image** 🧾
   - ✅ System **processes the refund** 💸
4️⃣ **For non-refundable issues**, such as **estimated delivery time inquiries** or **registering a complaint about rude service**, the system **provides relevant responses and records historical context** 🕰️📜.


