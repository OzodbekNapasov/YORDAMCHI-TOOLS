-- ============================================================
-- SUPABASE SQL MIGRATION FOR AMALIYOT MODULE
-- Run this in your Supabase SQL Editor: 
-- https://supabase.com/dashboard/project/rsrrrkkpvfjyfnzikiiy/sql
-- ============================================================

-- 1. FOLDERS TABLE (Papkalar Ierarxiyasi)
CREATE TABLE IF NOT EXISTS public.atlas_amaliyot_folders (
    id BIGSERIAL PRIMARY KEY,
    parent_id BIGINT REFERENCES public.atlas_amaliyot_folders(id) ON DELETE CASCADE,
    folder_type TEXT NOT NULL, -- 'year', 'direction', 'groups', 'semester'
    name TEXT NOT NULL,
    extra_data JSONB DEFAULT '{}'::jsonb,
    order_num INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. SURVEYS TABLE (Talabalar So'rovnomasi)
CREATE TABLE IF NOT EXISTS public.atlas_amaliyot_surveys (
    id BIGSERIAL PRIMARY KEY,
    folder_id BIGINT REFERENCES public.atlas_amaliyot_folders(id) ON DELETE CASCADE,
    guruhi TEXT NOT NULL,
    fio TEXT NOT NULL,
    tumani TEXT DEFAULT 'Shahrisabz shahar',
    start_date TEXT DEFAULT '08.06.2026',
    end_date TEXT DEFAULT '06.07.2026',
    phone TEXT,
    organization TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. ORDERS TABLE (Generatsiya Qilingan Buyruqlar Arxivi)
CREATE TABLE IF NOT EXISTS public.atlas_amaliyot_orders (
    id BIGSERIAL PRIMARY KEY,
    folder_id BIGINT REFERENCES public.atlas_amaliyot_folders(id) ON DELETE CASCADE,
    tumani TEXT NOT NULL,
    buyruq_raqami TEXT,
    buyruq_sanasi TEXT,
    shu_tuman_shifokori TEXT,
    oquv_yili TEXT,
    kursi TEXT,
    guruhlar TEXT,
    amaliyot_muddati TEXT,
    start_date TEXT,
    end_date TEXT,
    docx_path TEXT,
    students_count INTEGER DEFAULT 0,
    students JSONB DEFAULT '[]'::jsonb,
    students_json TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS POLICIES (Barcha operatsiyalarga to'liq ruxsat berish)
ALTER TABLE public.atlas_amaliyot_folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_amaliyot_surveys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atlas_amaliyot_orders ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all access to atlas_amaliyot_folders" ON public.atlas_amaliyot_folders;
DROP POLICY IF EXISTS "Allow all access to atlas_amaliyot_surveys" ON public.atlas_amaliyot_surveys;
DROP POLICY IF EXISTS "Allow all access to atlas_amaliyot_orders" ON public.atlas_amaliyot_orders;

CREATE POLICY "Allow all access to atlas_amaliyot_folders" ON public.atlas_amaliyot_folders FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access to atlas_amaliyot_surveys" ON public.atlas_amaliyot_surveys FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all access to atlas_amaliyot_orders" ON public.atlas_amaliyot_orders FOR ALL USING (true) WITH CHECK (true);
