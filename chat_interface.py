class ChatInterface:
    def __init__(self, query_processor):
        self.query_processor = query_processor
        self.history = []

    def chat(self, message):
        response = self.query_processor.process_query(message)
        self.history.append((message, str(response)))
        return self.history

    def stream_chat(self, message):
        partial_response = ""
        for text in self.query_processor.stream_response(message):
            partial_response += text
            yield self.history + [(message, partial_response)]
        self.history.append((message, partial_response))

    def clear_history(self):
        self.history = []
