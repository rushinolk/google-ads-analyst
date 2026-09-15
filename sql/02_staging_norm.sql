
CREATE OR REPLACE VIEW vw_staging_norm AS
SELECT
    ad_id,
    COALESCE(NULLIF(INITCAP(TRIM(campaign_name)), ''), 'UNKNOWN') AS campaign_name,
    COALESCE(NULLIF(INITCAP(TRIM(location)), ''), 'UNKNOWN')      AS location,
    COALESCE(NULLIF(UPPER(TRIM(device)), ''), 'UNKNOWN')        AS device,
    COALESCE(NULLIF(LOWER(TRIM(keyword)), ''), 'UNKNOWN')       AS keyword,

    clicks,
    impressions,
    cost,
    leads,
    conversions,
    sale_amount,
    ad_date
FROM staging_ads;