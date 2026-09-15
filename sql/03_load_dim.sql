
-- dim_campaign_name 
INSERT INTO dim_campaign_name (campaign_name)
SELECT DISTINCT campaign_name
FROM vw_staging_norm
ON CONFLICT (campaign_name) DO NOTHING;

-- dim_location 
INSERT INTO dim_location (name_location)
SELECT DISTINCT location
FROM vw_staging_norm
ON CONFLICT (name_location) DO NOTHING;

-- dim_device 
INSERT INTO dim_device (device)
SELECT DISTINCT device
FROM vw_staging_norm
ON CONFLICT (device) DO NOTHING;

-- dim_keyword 
INSERT INTO dim_keyword (keyword)
SELECT DISTINCT keyword
FROM vw_staging_norm
ON CONFLICT (keyword) DO NOTHING;