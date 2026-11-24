from typing import Any

from dify_plugin import ToolProvider


class TrainHornSplProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # This plugin requires no credentials and performs no network calls.
        return
