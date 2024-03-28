from faster_whisper import WhisperModel

# Initialize the Whisper model
model = WhisperModel("large-v3", device="cpu")

def transcript(uploaded_file):
    if uploaded_file is not None:
        try:
            segments, _ = model.transcribe(uploaded_file, vad_filter=True)

            # Convert generator to a list and concatenate all segments
            all_segments = list(segments)
            response = "".join([segment.text for segment in all_segments])
            return response

        except Exception as e:
            return f"Error in transcription: {e}"
