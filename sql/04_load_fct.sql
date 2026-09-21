INSERT INTO fct_anuncio (
    id_anuncio,
    id_campaign_name,
    id_location,
    id_device,
    id_keyword,
    clicks,
    impressions,
    cost,
    leads,
    conversions,
    sale_amount,
    ad_date,
    flag_inconsistencia_funil
)
SELECT
    s.ad_id,
    dc.id_campaign_name,
    dl.id_location,
    dd.id_device,
    dk.id_keyword,
    COALESCE(s.clicks, 0),
    COALESCE(s.impressions, 0),
    s.cost,              
    COALESCE(s.leads, 0),
    COALESCE(s.conversions, 0),
    s.sale_amount,        
    s.ad_date,
    s.flag_inconsistencia_funil
FROM vw_staging_norm s
JOIN dim_campaign_name dc ON dc.campaign_name = s.campaign_name
JOIN dim_location      dl ON dl.name_location  = s.location
JOIN dim_device        dd ON dd.device         = s.device
JOIN dim_keyword       dk ON dk.keyword        = s.keyword
ON CONFLICT (id_anuncio) DO NOTHING;

ALTER TABLE fct_anuncio ALTER COLUMN ad_date SET NOT NULL;

ALTER TABLE fct_anuncio
ADD CONSTRAINT fk_fct_calendario
FOREIGN KEY (ad_date) REFERENCES dim_calendario(id_calendario);