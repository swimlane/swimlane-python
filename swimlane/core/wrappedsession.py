import requests
from typing import Any, Optional


class WrappedSession(requests.Session):
    """A wrapper for requests.Session to override 'verify' property, ignoring REQUESTS_CA_BUNDLE environment variable.

    This is a workaround for https://github.com/kennethreitz/requests/issues/3829 (will be fixed in requests 3.0.0)
    """
    def merge_environment_settings(self, url: str, proxies: Any, stream: Optional[bool], verify: bool, *args: Any, **kwargs: Any) -> Any:
        if self.verify is False:
            verify = False

        return super(WrappedSession, self).merge_environment_settings(url, proxies, stream, verify, *args, **kwargs)