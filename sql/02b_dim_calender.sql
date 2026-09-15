

CREATE TABLE IF NOT EXISTS dim_calendario (
    id_calendario    DATE PRIMARY KEY,
    ano              INT  NOT NULL,
    trimestre        INT  NOT NULL,
    mes              INT  NOT NULL,
    nome_mes         TEXT NOT NULL,
    dia              INT  NOT NULL,
    dia_semana       INT  NOT NULL,
    nome_dia_semana  TEXT NOT NULL,
    semana_iso       INT  NOT NULL,
    ano_mes          TEXT NOT NULL,
    eh_fim_semana    BOOLEAN NOT NULL
);


INSERT INTO dim_calendario (
    id_calendario, ano, trimestre, mes, nome_mes, dia,
    dia_semana, nome_dia_semana, semana_iso, ano_mes, eh_fim_semana
)
SELECT
    d::DATE                                        AS id_calendario,
    EXTRACT(YEAR    FROM d)::INT                   AS ano,
    EXTRACT(QUARTER FROM d)::INT                   AS trimestre,
    EXTRACT(MONTH   FROM d)::INT                   AS mes,
    TO_CHAR(d, 'TMMonth')                          AS nome_mes,
    EXTRACT(DAY     FROM d)::INT                   AS dia,
    EXTRACT(DOW     FROM d)::INT                   AS dia_semana,
    TO_CHAR(d, 'TMDay')                            AS nome_dia_semana,
    EXTRACT(WEEK    FROM d)::INT                   AS semana_iso,
    TO_CHAR(d, 'YYYY-MM')                          AS ano_mes,
    EXTRACT(DOW FROM d) IN (0, 6)                  AS eh_fim_semana
FROM generate_series(
    (SELECT MIN(ad_date)::DATE FROM vw_staging_norm),
    (SELECT MAX(ad_date)::DATE FROM vw_staging_norm),
    INTERVAL '1 day'
) AS d
ON CONFLICT (id_calendario) DO NOTHING;