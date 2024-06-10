"""llm-api errors"""


class LlmApiError(Exception):
    """llm-api base error"""

    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super().__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:  # pylint: disable=broad-exception-caught
                http_body = "<Could not decode body as utf-8.>"

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code

    def __str__(self):
        msg = self._message or "<empty message>"
        return msg

    @property
    def user_message(self):
        """user message"""
        return self._message

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(message={self._message},"
            f" http_status={self.http_status}, request_id={self.request_id})"
        )


class APIError(LlmApiError):
    """General llm-api error"""


class TryAgain(LlmApiError):
    """Retriable error"""


class Timeout(LlmApiError):
    """Timeout error"""


class APIConnectionError(LlmApiError):
    """Connection error"""

    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super().__init__(message, http_body, http_status, json_body, headers, code)
        self.should_retry = should_retry


class InvalidRequestError(LlmApiError):
    """Invalid request error"""


class AuthenticationError(LlmApiError):
    """Authentication error"""


class PermissionError(LlmApiError):  # pylint: disable=redefined-builtin
    """Permission error"""


class RateLimitError(LlmApiError):
    """Rate limit error"""


class ServiceUnavailableError(LlmApiError):
    """Service unavailable error"""


class InvalidAPIType(LlmApiError):
    """Invalid API type error"""