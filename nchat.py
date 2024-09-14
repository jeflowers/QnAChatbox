# Necessary Import Libraries
import os
import gradio as gr
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

# configure settngs for the application
Settings.text_splitter = SentenceSplitter(chunk_size=500)
Settings.embed_model = NVIDIAEmbedding("NV-Embed-QA", truncate="END")
Settings.llm = NVIDIA(model="meta/llama-3.1-405b-instruct")

# check if NVIDIA API key is set as an env variable
if os.getenv('NVIDIA_API_KEY') is None:
    raise ValueError("NVIDIA_API_KEY environment variableis not set")

# initialize global variables for index and query
# initialized when documents are loaded
index = None
query_engine = None

# Function to get name from file obj
# extract names from file objects
def get_files_from_input(file_objs):
    if not file_objs:
        return[]
    return [file_obj.name for file_obj in file_objs]

# load documents and create the index
# handles document loading where it:
# 1. reads file
# 2. creates the index using milvus vector store
#
def load_documents(file_objs):
    global index, query_engine
    try:
        if not file_objs:
            return "Error: No files selected."
        file_paths = get_files_from_input(file_objs)
        documents = []
        for file_path in file_paths:
            directory = os.path.dirname(file_path)
            documents.extend(SimpleDirectoryReader(input_files=[file_path]).load_data())

        if not documents:
            return f"No documents found in the selected files."

        # creat a Milvus vector store and storage context
        vector_store = MilvusVectorStore(uri="./milvus_demo.db", dim=1024, overwrite=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # create the index form the documents
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        # create tje query engine
        query_engine = index.as_query_engine(similar_top_k=20, streaming=True)
        return f"Successfully loaded {len(documents)} documents from {len(file_paths)} files."
    except Exception as e:
        return f"Error loading documents: {str(e)}"

# Function to handle chat interactions
# handles basic question answering
def chat(message, history):
    global query_engine
    if query_engine is None:
        return history + [("Please load documents first.", None)]
    try:
        response = query_engine.query(message)
        return history + [(message, response)]
    except Exception as e:
        return history + [(message, f"Error processing query: {str(e)}")]
    
# Function handles stream response
def stream_response(message, history):
    global query_engine
    if query_engine is None:
        yield history + [("Please load documents first.", None)]
        return
    
    try:
        response = query_engine.query(message)
        partial_response = ""
        for text in response.response_gen:
            partial_response += text
            yield history + [(message, partial_response)]
    except Exception as e:
        yield history + [(message, f"Error processing query: {str(e)}")]

# create friendly web interface using Gradio
with gr.Blocks() as demo:
    gr.Markdown("# RAG Q&E Chat Application")

    with gr.Row():
        file_input = gr.File(label="Select file to laod", file_count="multiple")
        load_btn = gr.Button("Load Documents")

    load_output = gr.Textbox(label="Load Status")

    # initialize chatbot request.
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Enter your question", interactive=True)
    # clear button to reset history
    clear = gr.Button("Clear")

    # event handler to connect interface with respective functions
    load_btn.click(load_documents, inputs=[file_input], outputs=[load_output])
    # initialize straming response.
    msg.submit(stream_response, inputs=[msg, chatbot], outputs=[chatbot])
    msg.submit(lambda: "", outputs=[msg])
    # clear button to reset history
    clear.click(lambda: None, None, chatbot, queue=False)

#Launch Gradio
if __name__ == "__main__":
    demo.launch()

