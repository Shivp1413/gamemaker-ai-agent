from datetime import datetime

class CodeVersion:
    def __init__(self, code, description, version_number, run_instructions):
        self.code = code
        self.description = description
        self.version_number = version_number
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.run_instructions = run_instructions