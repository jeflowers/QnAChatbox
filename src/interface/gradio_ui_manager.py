# gradio_ui_manager.py

import gradio as gr

class GradioUIManager:
    def __init__(self, document_loader, load_documents_func, get_chat_interface_func):
        self.document_loader = document_loader
        self.load_documents_func = load_documents_func
        self.get_chat_interface_func = get_chat_interface_func

    def create_ui(self):
        with gr.Blocks() as demo:
            gr.Markdown("# RAG Q&E Chat Application")

            with gr.Row():
                file_input = gr.File(label="Select file to load", file_count="multiple")
                load_btn = gr.Button("Load Documents")

            load_output = gr.Textbox(label="Load Status")

            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Enter your question", interactive=True)
            clear = gr.Button("Clear")

            load_btn.click(self.load_documents_func, inputs=[file_input], outputs=[load_output])
            msg.submit(self.chat, inputs=[msg], outputs=[chatbot])
            msg.submit(lambda: "", outputs=[msg])
            clear.click(self.clear_chat, outputs=[chatbot])

        return demo

    def chat(self, message):
        chat_interface = self.get_chat_interface_func()
        return chat_interface.stream_chat(message)

    def clear_chat(self):
        chat_interface = self.get_chat_interface_func()
        chat_interface.clear_history()
        return None

    def launch(self):
        demo = self.create_ui()
        demo.launch()