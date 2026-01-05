# 🎬 LangChain Streamlit Media Summarizer

Repo: https://github.com/iceyisaak/langchain-streamlit-media-summarizer

StreamlitUI: https://langchain-media-summarizer.streamlit.app/ 

---

An AI-powered web application that generates concise, intelligent summaries of various media sources, including YouTube videos and web articles. Built with **LangChain**, **Streamlit**, and **Large Language Models (LLMs)**.

## 🚀 Features

* **YouTube Summarization**: Extract transcripts from YouTube videos and summarize the core message.
* **Webpage Summarization**: Scrape and condense long-form articles or blog posts from any URL.
* **Interactive UI**: Clean and simple dashboard built with Streamlit for a seamless user experience.
* **Customizable Summaries**: Leveraging LangChain's summarization chains (Map-Reduce/Stuff) to handle long-form content efficiently.
* **API Integration**: Compatible with OpenAI, Groq, or local models via Ollama.

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **LLM Framework**: [LangChain](https://www.langchain.com/)
* **Orchestration**: Python
* **Data Loading**: `YoutubeLoader`, `UnstructuredURLLoader`

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/iceyisaak/langchain-streamlit-media-summarizer.git
cd langchain-streamlit-media-summarizer

```


2. **Create a virtual environment:**
```bash
conda env create -f environment.yml

conda activate mlangchain-streamlit-media-summarizer

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```



## 🚦 Usage

Run the Streamlit app with the following command:

```bash
streamlit run app.py

```

**Enter your Groq API Key in the sidebar**


1. Enter the **URL** (YouTube or Website) in the input field.
2. Select your preferred model or summarization length (if applicable).
3. Click **Summarize** to generate the content.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---