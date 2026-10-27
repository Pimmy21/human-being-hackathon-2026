-- ONE-TIME ADMINISTRATOR SETUP. Do not run automatically or against existing objects.
-- Inspect your Zetaris version/schema and obtain account-owner permission first.
-- No AWS resource provisioning and no modification of the government source.
-- If the database already exists, skip its CREATE statement.
CREATE LIGHTNING DATABASE DONATION_FEASIBILITY_20261022 DESCRIBE BY "Historical public CRA 2024 charity background";

-- Historical Ontario animal organizations. This connector statement was live-validated.
CREATE LIGHTNING REST TABLE ontario_animal_directory FROM DONATION_FEASIBILITY_20261022 REQUEST (
 endpoint 'https://open.canada.ca/data/api/action/datastore_search?resource_id=694fdc72-eae4-4ee0-83eb-832ab7b230e3&filters=%7B%22Category%22%3A%220180%22%2C%22Province%22%3A%22ON%22%7D&limit=1000&fields=BN%2CLegal+Name%2CAccount+Name%2CCity%2CProvince%2CCategory',
 method 'get', response_type 'json', http_encoding 'URLENCODED', insecure_ssl 'false'
) HEADER () BODY ();

-- Equivalent template for the already existing fixed identity diagnostic connector.
-- Template supplied for reproduction; creation of this equivalent statement was not re-run.
CREATE LIGHTNING REST TABLE tcr_identity FROM DONATION_FEASIBILITY_20261022 REQUEST (
 endpoint 'https://open.canada.ca/data/api/action/datastore_search?resource_id=694fdc72-eae4-4ee0-83eb-832ab7b230e3&filters=%7B%22BN%22%3A%22720884691RR0001%22%7D&limit=1',
 method 'get', response_type 'json', http_encoding 'URLENCODED', insecure_ssl 'false'
) HEADER () BODY ();

-- Read-only checks, after inspecting inferred schema.
SELECT fact.BN, fact.`Legal Name`, fact.`Account Name`, fact.City, fact.Province, fact.Category, result.total
FROM DONATION_FEASIBILITY_20261022.ontario_animal_directory
LATERAL VIEW explode(result.records) AS fact;
SELECT fact.BN, fact.`Legal Name`, fact.City, fact.Province
FROM DONATION_FEASIBILITY_20261022.tcr_identity
LATERAL VIEW explode(result.records) AS fact;
