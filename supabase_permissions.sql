-- Required for the teacher dashboard query in src/database/db.py.
-- Run this in the Supabase SQL Editor for the project used by the app.
grant usage on schema public to anon;
grant usage on schema public to authenticated;

grant select on table
    public.subjects,
    public.subject_students,
    public.attendance_logs
to anon, authenticated;

grant insert on table public.subjects to anon, authenticated;
grant insert on table public.subject_students to anon;
grant insert on table public.subject_students to authenticated;
grant insert on table public.attendance_logs to anon, authenticated;
grant delete on table public.subject_students to anon;
grant delete on table public.subject_students to authenticated;

drop policy if exists "api_can_read_subjects" on public.subjects;
create policy "api_can_read_subjects"
on public.subjects
for select
to public
using (true);

drop policy if exists "api_can_read_subject_students" on public.subject_students;
create policy "api_can_read_subject_students"
on public.subject_students
for select
to public
using (true);

drop policy if exists "api_can_read_attendance_logs" on public.attendance_logs;
create policy "api_can_read_attendance_logs"
on public.attendance_logs
for select
to public
using (true);

drop policy if exists "api_can_insert_attendance_logs" on public.attendance_logs;
create policy "api_can_insert_attendance_logs"
on public.attendance_logs
for insert
to public
with check (true);

drop policy if exists "api_can_insert_subjects" on public.subjects;
drop policy if exists "anon_can_insert_subjects" on public.subjects;
create policy "api_can_insert_subjects"
on public.subjects
for insert
to public
with check (true);

drop policy if exists "api_can_insert_subject_students" on public.subject_students;
create policy "api_can_insert_subject_students"
on public.subject_students
for insert
to public
with check (true);

drop policy if exists "api_can_delete_subject_students" on public.subject_students;
create policy "api_can_delete_subject_students"
on public.subject_students
for delete
to public
using (true);