from llama_index.core import SimpleDirectoryReader

class DocumentLoader:
    @staticmethod
    def extract_file_paths_from_gradio_input(file_objs):
        if not file_objs:
            return []
        return [file_obj.name for file_obj in file_objs]

    def load_documents(self, file_objs):
        file_paths = self.extract_file_paths_from_gradio_input(file_objs)
        documents = []
        for file_path in file_paths:
            documents.extend(SimpleDirectoryReader(input_files=[file_path]).load_data())
        return documents, len(documents), len(file_paths)