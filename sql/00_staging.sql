CREATE TABLE IF NOT EXISTS staging_ads (
    ad_id           TEXT,
    campaign_name   TEXT,
    clicks          NUMERIC,
    impressions     NUMERIC,
    cost            NUMERIC,
    leads           NUMERIC,
    conversions     NUMERIC,
    sale_amount     NUMERIC,
    ad_date         DATE,
    location        TEXT,
    device          TEXT,
    keyword         TEXT
);