import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

st.set_page_config(page_title="Langchain: Summarize Text from Webpage")
st.title("Langchain-Streamlit: Media Summarizer")
st.subheader("Summarize URL")

# Get Groq API Key and URL
with st.sidebar:
    api_key = st.text_input("HuggingFace Access Token", value="", type="password")


###############################################

# Get URL Input
generic_url = st.text_input("URL", label_visibility="collapsed")

# 1. Map Prompt: Summarize individual chunks
map_prompt_template = """
    Write a concise summary of the following text:
    "{text}"
    CONCISE SUMMARY:
"""
map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

# 2. Combine Prompt: Merge those summaries into a final 500-word piece
combine_prompt_template = """
    Write a summary of the following content in approximately 500 words:
    "{text}"
    FINAL SUMMARY:
"""
combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])



#######################################################

if st.button("Summarize the Content from URL"):

    if not api_key.strip() or not generic_url.strip():
        st.error("Please provide both the GROQ API Key and the URL to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (e.g. Youtube URL or Website URL)")
    else:
        try:
            with st.spinner("Processing..."):
                # 1. Initialize LLM
                # llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
                llm_base=HuggingFaceEndpoint(
                    repo_id="HuggingFaceH4/zephyr-7b-beta",
                    max_new_tokens=512,
                    temperature=0.7,
                    huggingfacehub_api_token=api_key,
                    task="conversational",
                    # provider="auto"
                )

                llm = ChatHuggingFace(llm=llm_base)

                # 2. Loading the URL data
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url, 
                        add_video_info=False, 
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={ 
                             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        })
                
                docs = loader.load()

               # We use len (character count) as the length_function to avoid the 'transformers' requirement
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=3500, 
                    chunk_overlap=300,
                    length_function=len 
                )
                split_docs = text_splitter.split_documents(docs)

                # 3. Summarization chain
               # Using map_reduce to handle the large input across multiple API calls
                summarization_chain = load_summarize_chain(
                    llm=llm,
                    chain_type="map_reduce",
                    map_prompt=map_prompt,
                    combine_prompt=combine_prompt,
                    verbose=True
                )
                
                # Invoke chain
                output_summary = summarization_chain.invoke(split_docs)

                st.success(output_summary['output_text'])

        except Exception as e:
            st.error(f"An error occurred: {e}")