class HinglishError:
    """Class to structure and format custom Hinglish tracebacks."""
    def __init__(self, error_type, line, message, suggestion=None):
        self.error_type = error_type
        self.line = line
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        # Format the error into the custom UI style
        trace = f"[{self.error_type.upper()}] Line {self.line}: {self.message}"
        if self.suggestion:
            trace += f"\n   -> Bhai, kya tera matlab '{self.suggestion}' tha?"
        return trace

class ErrorHandler:
    """Centralized manager for collecting compiler errors across passes."""
    def __init__(self):
        self.errors = []

    def add_error(self, error_type, line, message, suggestion=None):
        self.errors.append(HinglishError(error_type, line, message, suggestion))

    def has_errors(self):
        return len(self.errors) > 0

    def get_traceback(self):
        # Join all errors neatly for the IDE console
        return "\n".join(str(err) for err in self.errors)

    def clear(self):
        self.errors = []