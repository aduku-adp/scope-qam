DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
        CREATE ROLE postgres LOGIN PASSWORD 'postgres';
    ELSE
        ALTER ROLE postgres WITH LOGIN PASSWORD 'postgres';
    END IF;
END
$$;

SELECT 'CREATE DATABASE qam_db OWNER postgres'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'qam_db'
)\gexec
