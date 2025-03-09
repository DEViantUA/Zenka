class ZZZError(Exception):
    def __init__(self, error_message: dict):
        super().__init__(error_message["text"])
        self.code = error_message["code"]
        self.text = error_message["text"]