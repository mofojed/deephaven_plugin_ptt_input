import React, { CSSProperties, useCallback, useEffect, useState } from "react";
import { useApi } from "@deephaven/jsapi-bootstrap";
import Log from "@deephaven/log";
import { WidgetComponentProps } from "@deephaven/plugin";
import type { dh } from "@deephaven/jsapi-types";
import { ActionButton, Button, TextField, View } from "@deephaven/components";

const log = Log.module(
  "deephaven-plugin-ptt-input.DeephavenPluginPttInputView"
);

// Create a custom style for the component
export const DeephavenPluginPttInputViewStyle: CSSProperties = {
  // CSS variables can be used to style the component according to the theme
  color: "var(--dh-color-purple-700)",
  fontSize: "x-large",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  height: "100%",
  width: "100%",
  flexDirection: "column",
};

export function DeephavenPluginPttInputView(
  props: WidgetComponentProps
): JSX.Element {
  const { fetch } = props;
  const [text, setText] = useState<string>(
    "Call send_message on the object and the message will appear here."
  );
  const [widget, setWidget] = useState<dh.Widget | null>(null);
  const [recorder, setRecorder] = useState<MediaRecorder | null>(null);
  const isRecording = recorder != null;
  const dh = useApi();

  useEffect(() => {
    async function init() {
      // Fetch the widget from the server
      const fetched_widget = (await fetch()) as dh.Widget;
      setWidget(fetched_widget);

      // Add an event listener to the widget to listen for messages from the server
      fetched_widget.addEventListener<dh.Widget>(
        dh.Widget.EVENT_MESSAGE,
        ({ detail }) => {
          // When a message is received, update the text in the component
          const text = detail.getDataAsString();
          if (text) {
            setText(text);
          }
        }
      );
    }

    init();
  }, [dh, fetch]);

  const startRecording = useCallback(async () => {
    try {
      // Open up the microphone and start recording
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      // TODO: Use a timeslice value here to send chunks as they come in rather than send it all at once
      // recorder.start(50);
      recorder.start();
      recorder.ondataavailable = (e) => {
        log.info("Recording data available");

        // Send the recorded audio to the server
        const reader = new FileReader();
        reader.onload = async () => {
          const data = reader.result as ArrayBuffer;
          const message = new Uint8Array(data);
          await widget?.sendMessage(message);
        };
        reader.readAsArrayBuffer(e.data);
      };

      recorder.onstop = async () => {
        log.info("Recording stopped");

        stream.getTracks().forEach((track) => track.stop());

        // Send an empty message to signal the end of the recording
        await widget?.sendMessage(new Uint8Array());
      };

      setRecorder(recorder);
    } catch (e) {
      log.error("Error starting recording", e);
    }
  }, [widget]);

  const stopRecording = useCallback(() => {
    if (!recorder) {
      return;
    }

    recorder.stop();
    setRecorder(null);
  }, [recorder]);

  return (
    <View>
      <ActionButton
        onPressStart={startRecording}
        onPressEnd={stopRecording}
        UNSAFE_style={{ backgroundColor: isRecording ? "red" : undefined }}
      >
        Record
      </ActionButton>
    </View>
  );
}

export default DeephavenPluginPttInputView;
