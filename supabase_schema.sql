-- ============================================================
-- ATLAS Universal Bot Platform — Supabase Cloud Database Schema
-- Run this in your Supabase SQL Editor (1-Click Setup)
-- ============================================================

-- 1. Generated Documents Table (300 DPI Certificates & Orders Archive)
CREATE TABLE IF NOT EXISTS public.atlas_generated_docs (
    id BIGSERIAL PRIMARY KEY,
    template_id TEXT NOT NULL,
    template_name TEXT NOT NULL,
    recipient_fio TEXT NOT NULL,
    data_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    file_type TEXT DEFAULT 'png',
    file_url TEXT,
    storage_path TEXT,
    created_by TEXT DEFAULT 'web_admin',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Telegram Users Table
CREATE TABLE IF NOT EXISTS public.atlas_users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    role TEXT DEFAULT 'user',
    status TEXT DEFAULT 'active',
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Audit Logs Table
CREATE TABLE IF NOT EXISTS public.atlas_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    actor TEXT NOT NULL,
    module TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT DEFAULT 'success',
    details_json JSONB DEFAULT '{}'::jsonb,
    ip_address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 4. Student Academic Groups Table (O'quv guruhlari)
CREATE TABLE IF NOT EXISTS public.atlas_student_groups (
    id BIGSERIAL PRIMARY KEY,
    group_name TEXT UNIQUE NOT NULL,
    course_level INT DEFAULT 1,
    direction TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 5. Contract Sessions Table (Kontrakt Yangilanish Tarixi)
CREATE TABLE IF NOT EXISTS public.atlas_contract_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    filename TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    total_income NUMERIC DEFAULT 0,
    updated_count INT DEFAULT 0,
    unmatched_count INT DEFAULT 0,
    excel_url TEXT,
    xulosa_url TEXT,
    metrics_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 6. Enable Row Level Security & Allow Service Role Full Access
ALTER TABLE public.atlas_generated_docs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_student_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_contract_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow service_role full access to atlas_generated_docs" ON public.atlas_generated_docs FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_users" ON public.atlas_users FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_audit_logs" ON public.atlas_audit_logs FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_student_groups" ON public.atlas_student_groups FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_contract_sessions" ON public.atlas_contract_sessions FOR ALL TO service_role USING (true);

-- Allow public read access to generated documents, groups, and contract sessions
CREATE POLICY "Allow public read access to atlas_generated_docs" ON public.atlas_generated_docs FOR SELECT USING (true);
CREATE POLICY "Allow public read access to atlas_student_groups" ON public.atlas_student_groups FOR SELECT USING (true);
CREATE POLICY "Allow public read access to atlas_contract_sessions" ON public.atlas_contract_sessions FOR SELECT USING (true);

