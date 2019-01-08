ALTER TABLE census
 ALTER COLUMN geom TYPE geometry(GEOMETRY, 4326) USING ST_Transform(ST_SetSRID(geom,4269),4326); 
 
CREATE TABLE census_data AS
 SELECT 
   state,
   gid,
   county,
   tract,
   ST_X(ST_Centroid(geom)) as lon,
   ST_Y(ST_Centroid(geom)) as lat,
   ST_SetSRID(ST_MakePoint(ST_X(ST_Centroid(geom)),ST_Y(ST_Centroid(geom))),4326) as point
 FROM census_tract;
 
CREATE TABLE census_zones AS
 SELECT 
  c.state,
  c.county,
  c.tract,
  c.gid AS tract_gid, 
  n.gid AS zone_gid
 FROM census_data c, taxi_zones n
WHERE ST_Within(c.point, n.geom);
 