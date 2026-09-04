import streamlit as st
from src.pipeline.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd

from src.components.dialog_attendance_results import show_attendance_result

@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):
    st.write('Record audio of students saying I am Present. Then AI will recognize the students')

    audio_data = st.audio_input(
        "Record classroom audio",
        sample_rate=16000,
        key="voice_attendance_recorder",
        help="Microphone access requires HTTPS or localhost. If recording fails, upload a WAV file below.",
    )
    uploaded_audio = st.file_uploader(
        "Or upload classroom audio",
        type=["wav", "mp3", "m4a", "ogg", "webm"],
        key="voice_attendance_upload",
        help="Use this when the browser cannot access your microphone.",
    )

    if st.button('Analyze Audio', width='stretch', type = 'primary'):
        recording = audio_data or uploaded_audio
        if recording is None:
            st.warning('Please record or upload audio before analyzing.')
            return

        with st.spinner('Processing Audio data'):
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled in this course')
                return
            candidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.error('No enrolled students have voice profiles registerd')
                return

            audio_bytes = recording.getvalue()

            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = score > 0
                results.append({
                    "Name": student['name'],
                    "ID" : student['student_id'],
                    "Sources": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })
                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results

        show_attendance_result(df_results, logs)



