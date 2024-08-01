import React, { useCallback, useEffect, useState } from "react";
import { useApi } from "@deephaven/jsapi-bootstrap";
import Log from "@deephaven/log";
import { WidgetComponentProps } from "@deephaven/plugin";
import type { dh } from "@deephaven/jsapi-types";
import {
  ActionButton,
  Icon,
  LoadingSpinner,
  View,
} from "@deephaven/components";
import { vsMic, vsMicFilled } from "@deephaven/icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const log = Log.module(
  "deephaven-plugin-ptt-input.DeephavenPluginPttInputView"
);

export function DeephavenPluginPttInputView(
  props: WidgetComponentProps
): JSX.Element {
  const { fetch } = props;
  const [widget, setWidget] = useState<dh.Widget | null>(null);
  const [recorder, setRecorder] = useState<MediaRecorder | null>(null);
  const [isPending, setIsPending] = useState(false);
  const isRecording = recorder != null;
  const dh = useApi();

  useEffect(() => {
    async function init() {
      // Fetch the widget from the server
      const fetched_widget = (await fetch()) as dh.Widget;
      setWidget(fetched_widget);
    }

    init();
  }, [dh, fetch]);

  const startRecording = useCallback(async () => {
    try {
      // Open up the microphone and start recording
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { sampleRate: 12000 },
      });
      const recorder = new MediaRecorder(stream);
      // TODO: Use a timeslice value here to send chunks as they come in rather than send it all at once
      // recorder.start(50);
      recorder.start();
      recorder.ondataavailable = (e) => {
        log.info("Recording data available");

        // Send the recorded audio to the server
        const reader = new FileReader();
        reader.onload = async () => {
          setIsPending(true);
          const data = reader.result as ArrayBuffer;
          // const message = new Uint16Array(data);
          await widget?.sendMessage(data);
          setIsPending(false);
        };
        reader.readAsArrayBuffer(e.data);
      };

      recorder.onstop = async () => {
        log.info("Recording stopped");

        stream.getTracks().forEach((track) => track.stop());
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

  useEffect(() => {
    if (!isPending) {
      // Send an empty message to signal the end of the recording
      widget?.sendMessage(new Uint8Array());
    }
  }, [isPending]);

  return (
    <View>
      <ActionButton
        aria-label="Voice command"
        onPressStart={startRecording}
        onPressEnd={stopRecording}
        onBlur={stopRecording}
        isDisabled={isPending}
        UNSAFE_style={{
          color: isRecording ? "var(--dh-color-visual-red)" : undefined,
        }}
      >
        {isPending ? (
          <LoadingSpinner />
        ) : (
          <Icon>
            <FontAwesomeIcon icon={isRecording ? vsMicFilled : vsMic} />
          </Icon>
        )}
      </ActionButton>
    </View>
  );
}

export default DeephavenPluginPttInputView;
