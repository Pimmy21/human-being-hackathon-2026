-- One new REST connector in the existing approved database. No new AWS resource.
-- Public CRA2024 annual-return identity records, Ontario animal category only.
-- Historical background, never current registration or case qualification.
CREATE LIGHTNING REST TABLE ontario_animal_directory FROM DONATION_FEASIBILITY_20261022 REQUEST (
  endpoint 'https://open.canada.ca/data/api/action/datastore_search?resource_id=694fdc72-eae4-4ee0-83eb-832ab7b230e3&filters=%7B%22Category%22%3A%220180%22%2C%22Province%22%3A%22ON%22%7D&limit=1000&fields=BN%2CLegal+Name%2CAccount+Name%2CCity%2CProvince%2CCategory',
  method 'get', response_type 'json', http_encoding 'URLENCODED', insecure_ssl 'false'
) HEADER () BODY ();
