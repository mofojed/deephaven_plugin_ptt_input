from __future__ import annotations
from typing import Callable, Union
import logging

from deephaven.plugin.object_type import MessageStream

logger = logging.getLogger(__name__)

class DeephavenPluginPttInputObject:
    """
    This is a simple object that demonstrates how to send messages to the client.
    When the object is created, it will be passed a connection to the client.
    This connection can be used to send messages back to the client.

    Attributes:
        _connection: MessageStream: The connection to the client
    """
    def __init__(self, on_text: Union[Callable[[str], None], None] = None, on_error: Union[Callable[[str], None], None] = None) -> None:
        self._connection: MessageStream = None
        self.on_text = on_text
        self.on_error = on_error


    def send_message(self, message: str) -> None:
        """
        Send a message to the client

        Args:
            message: The message to send
        """
        if self._connection:
            self._connection.send_message(message)

    def _set_connection(self, connection: MessageStream) -> None:
        """
        Set the connection to the client.
        This is called on the object when it is created.

        Args:
            connection: The connection to the client
        """
        self._connection = connection




