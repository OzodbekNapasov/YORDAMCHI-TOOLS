-- ============================================================
-- ATLAS Universal Bot Platform — Supabase Cloud Database Schema
-- Run this in your Supabase SQL Editor (1-Click Setup)
-- ============================================================

-- 1. Generated Documents Table (300 DPI Certificates Archive)
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

-- 4. Enable Row Level Security & Allow Service Role Full Access
ALTER TABLE public.atlas_generated_docs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow service_role full access to atlas_generated_docs" ON public.atlas_generated_docs FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_users" ON public.atlas_users FOR ALL TO service_role USING (true);
CREATE POLICY "Allow service_role full access to atlas_audit_logs" ON public.atlas_audit_logs FOR ALL TO service_role USING (true);

-- Allow public read access to generated documents if public
CREATE POLICY "Allow public read access to atlas_generated_docs" ON public.atlas_generated_docs FOR SELECT USING (true);
