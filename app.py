import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

st.set_page_config(page_title="Langchain: Summarize Text from Webpage")
st.title("Langchain-Streamlit: Media Summarizer")
st.subheader("Summarize URL")

# Get Groq API Key and URL
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# Get URL Input
generic_url = st.text_input("URL", label_visibility="collapsed")

# Prompt Template
prompt_template = """
    Provide a summary of the following content in 500 words:
    Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])



#######################################################

if st.button("Summarize the Content from URL"):

    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both the GROQ API Key and the URL to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (e.g. Youtube URL or Website URL)")
    else:
        try:
            with st.spinner("Processing..."):
                # 1. Initialize LLM
                llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

                # 2. Loading the URL data
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    # loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url, 
                        add_video_info=True, 
                        # video_transformer_class=None  # Default transformer
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={ 
                             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        })
                
                doc = loader.load()

                # 3. Summarization chain
                summarization_chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                
                # Invoke chain
                output_summary = summarization_chain.invoke(doc)

                st.success(output_summary['output_text'])

        except Exception as e:
            st.error(f"An error occurred: {e}")