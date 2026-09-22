CREATE OR REPLACE VIEW vw_staging_norm AS
SELECT
    s.ad_id,
    CASE
        WHEN LOWER(TRIM(s.campaign_name)) IN (
            'data anlytics corse',
            'dataanalyticscourse',
            'data analytics corse',
            'data analytcis course',
            'data analytics course'
        ) THEN 'Data Analytics Course'
        ELSE COALESCE(NULLIF(INITCAP(TRIM(s.campaign_name)), ''), 'UNKNOWN')
    END AS campaign_name,

    CASE
        WHEN LOWER(TRIM(s.location)) IN (
            'hyderbad',
            'haiderbad',
            'hyderabad',
            'hydrebad'
        ) THEN 'Hyderabad'
        ELSE COALESCE(NULLIF(INITCAP(TRIM(s.location)), ''), 'UNKNOWN')
    END AS location,

    COALESCE(
            NULLIF(
                REGEXP_REPLACE(LOWER(TRIM(s.keyword)), 'ana[a-z]{0,3}tic[a-z]{0,3}', 'analytics', 'gi'),
            ''),
            'UNKNOWN'
        ) AS keyword,

    COALESCE(NULLIF(UPPER(TRIM(s.device)), ''), 'UNKNOWN') AS device,
    
    CASE
        WHEN s.clicks      > 0 AND (s.impressions = 0 OR s.impressions IS NULL) THEN 'clique_sem_impressao'
        WHEN s.leads        > 0 AND (s.clicks      = 0 OR s.clicks      IS NULL) THEN 'lead_sem_clique'
        WHEN s.conversions  > 0 AND (s.leads        = 0 OR s.leads        IS NULL) THEN 'conversao_sem_lead'
        ELSE NULL
    END AS flag_inconsistencia_funil,

    s.clicks,
    s.impressions,
    s.cost,
    s.leads,
    s.conversions,
    s.sale_amount,
    s.ad_date
FROM staging_ads s;