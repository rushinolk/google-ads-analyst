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

    COALESCE(NULLIF(UPPER(TRIM(s.device)), ''), 'UNKNOWN') AS device,
    COALESCE(NULLIF(LOWER(TRIM(s.keyword)), ''), 'UNKNOWN') AS keyword,

    s.clicks, 
    s.impressions, 
    s.cost, 
    s.leads, 
    s.conversions, 
    s.sale_amount,
    
    s.ad_date
FROM staging_ads s;