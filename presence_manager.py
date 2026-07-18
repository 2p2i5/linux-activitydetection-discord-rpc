import time
from typing import Optional, List, Dict

from pypresence import Presence


class PresenceManager:
    def __init__(self):
        self._rpc: Optional[Presence] = None
        self._client_id: Optional[str] = None
        self._start_timestamp: Optional[int] = None
        self.connected: bool = False

    def connect(self, client_id: str):
        """Connect (or reconnect, if client_id changed) to Discord."""
        if self.connected and self._client_id == client_id:
            return  # already connected with the same client_id

        self.disconnect()  # don't leave a stale socket hanging around

        self._rpc = Presence(client_id)
        self._rpc.connect()
        self._client_id = client_id
        self.connected = True

    def disconnect(self):
        if self._rpc is not None:
            try:
                self._rpc.close()
            except Exception:
                pass
        self._rpc = None
        self.connected = False

    def set_start_timestamp_now(self):
        self._start_timestamp = int(time.time())

    def clear_start_timestamp(self):
        self._start_timestamp = None

    def update(
        self,
        details: str = "",
        state: str = "",
        large_image: str = "",
        large_text: str = "",
        small_image: str = "",
        small_text: str = "",
        show_timestamp: bool = False,
        buttons: Optional[List[Dict[str, str]]] = None,
    ):
        if not self.connected or self._rpc is None:
            raise RuntimeError("Not connected to Discord. Call connect() first.")

        kwargs = {}
        if details:
            kwargs["details"] = details
        if state:
            kwargs["state"] = state
        if large_image:
            kwargs["large_image"] = large_image
        if large_text:
            kwargs["large_text"] = large_text
        if small_image:
            kwargs["small_image"] = small_image
        if small_text:
            kwargs["small_text"] = small_text
        if show_timestamp:
            if self._start_timestamp is None:
                self.set_start_timestamp_now()
            kwargs["start"] = self._start_timestamp
        if buttons:
            # Discord only accepts up to 2 buttons
            kwargs["buttons"] = buttons[:2]

        self._rpc.update(**kwargs)

    def clear(self):
        if self.connected and self._rpc is not None:
            try:
                self._rpc.clear()
            except Exception:
                pass
