# Present.ly

Present.ly is a Streamlit attendance app that uses AI-assisted face and voice recognition to make classroom attendance faster. Teachers can manage subjects, run attendance analysis, and review attendance records. Students can create a face profile, optionally enroll a voice profile, join subjects, and view attendance progress.

## Features

- Teacher registration and password login
- Student FaceID login and profile registration
- Optional voice enrollment for students
- Face attendance from one or more classroom photos
- Voice attendance from recorded or uploaded audio
- Subject creation and student enrollment using a share code
- Attendance review before saving results
- Teacher attendance records and student attendance statistics
- Supabase-backed data storage

## Requirements

- Python 3.10 or newer
- A Supabase project
- A browser with camera and microphone access for live capture
- HTTPS or `localhost` for browser microphone access

## Setup

1. Clone the repository and open its directory:

   ```powershell
   git clone <repository-url>
   cd Present.ly
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.streamlit/secrets.toml`:

   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-key"
   ```

   Keep this file private and do not commit it.

5. Configure the Supabase database with the tables and columns used by the application:

   - `teachers`
   - `students`
   - `subjects`
   - `subject_students`
   - `attendance_logs`

   Then run [`supabase_permissions.sql`](supabase_permissions.sql) in the Supabase SQL Editor to enable the API permissions required by the app.

## Run the app

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Typical workflow

### Teacher

1. Register or log in.
2. Create a subject.
3. Share the subject code with students.
4. Use classroom photos or voice audio to analyze attendance.
5. Review the results and confirm them.
6. View saved attendance in **Attendance Records**.

### Student

1. Choose student login and capture a face image.
2. Create a profile if the face is not recognized.
3. Optionally record a short voice sample.
4. Enroll in a subject using its share code.
5. View enrolled subjects and attendance statistics.

A share link containing `?join-code=<code>` opens the student enrollment flow automatically after student login.

## Tests

Run the test suite with:

```bash
pytest
```

## Project structure

```text
app.py                         Streamlit entry point
src/components/                Dialogs and reusable UI components
src/database/                  Supabase client and database operations
src/pipeline/                  Face and voice recognition pipelines
src/screens/                   Home, teacher, and student screens
src/ui/                        Shared layout and styling
tests/                         Automated tests
```

## Notes

- The first face or voice analysis may take longer while the recognition models load.
- Students need a stored face profile for face recognition and a stored voice profile for voice attendance.
- Review attendance results before confirming them because confirmed logs are written to Supabase.
- Review the policies in `supabase_permissions.sql` for your deployment. The included policies are intentionally permissive and should be tightened before using the app with sensitive or production data.
