from __future__ import annotations

from typing import Any
from deephaven.plugin.object_type import MessageStream, BidirectionalObjectType
import logging
import tempfile
import whisper

logger = logging.getLogger(__name__)

from .deephaven_plugin_ptt_input_object import DeephavenPluginPttInputObject

model = whisper.load_model("base")

# Create a custom message stream to send messages to the client

class DeephavenPluginPttInputMessageStream(MessageStream):
    """
    A custom MessageStream

    Attributes:
        _client_connection: MessageStream: The connection to the client
    """

    def __init__(self, obj: Any, client_connection: MessageStream):
        super().__init__()
        self._client_connection = client_connection

        # Start the message stream. All we do is send a blank message to start. Client will respond with the initial state.
        self._client_connection.on_data(b"", [])
        self.obj = obj

        obj._set_connection(self)

    def send_message(self, message: str) -> None:
        """
        Send a message to the client

        Args:
            message: The message to send
        """
        self._client_connection.on_data(message.encode(), [])

    def on_data(self, payload: bytes, references: list[Any]) -> None:
        """
        Handle a payload from the client.

        Args:
            payload: Payload to execute
            references: References to objects on the server

        Returns:
            The payload to send to the client and the references to send to the client
        """
        # This is where you would process the payload.
        # This is just an acknowledgement that the payload was received,
        # so print.
        if len(bytearray(payload)) == 0:
            logger.debug("Received empty stream payload")
            # print("Received empty stream payload")
            return
        
        # print(f"Received payload of type: {type(payload)}")

        # Decode the payload...
        try:
            import __main__

            # TODO: We shouldn't need to write to an intermediate file...
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, mode="bx") as f:
                f.write(payload)
                result = model.transcribe(f.name, fp16=False)
                logger.debug(f"Transcribed voice command: {result['text']}")
                self.obj.on_text(result['text'])
                f.close()
        except Exception as e:
            print(f"Error recognizing speech: {e}")

    def on_close(self) -> None:
        """
        Close the connection
        """
        pass

# The object type that will be registered with the plugin system.
# The object is bidirectional, meaning it can send messages to and from the client.
# A MessageStream is created for each object that is created. This needs to be saved and tied to the object.
# The value returned by name() should match supportedTypes in DeephavenPluginPttInputPlugin.ts
class DeephavenPluginPttInputType(BidirectionalObjectType):
    """
    Defines the Element type for the Deephaven plugin system.
    """

    @property
    def name(self) -> str:
        return "DeephavenPluginPttInput"

    def is_type(self, obj: Any) -> bool:
        return isinstance(obj, DeephavenPluginPttInputObject)

    def create_client_connection(
        self, obj: object, connection: MessageStream
    ) -> MessageStream:
        message_stream = DeephavenPluginPttInputMessageStream(obj, connection)
        return message_stream
