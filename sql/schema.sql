CREATE TABLE IF NOT EXISTS cves (
    cve_id       TEXT PRIMARY KEY,
    published    TIMESTAMP NOT NULL,
    status       TEXT,
    cvss_version TEXT,
    score        NUMERIC(3,1),
    severity     TEXT NOT NULL,
    description  TEXT,
    loaded_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);