-- Move user itinerary session tables into itinerary.db (attached as itinerary).
INSERT OR IGNORE INTO itinerary.ItineraryStatusSuppression SELECT * FROM main.ItineraryStatusSuppression;
INSERT OR IGNORE INTO itinerary.ItineraryDate SELECT * FROM main.ItineraryDate;
INSERT OR IGNORE INTO itinerary.ItineraryExhibit SELECT * FROM main.ItineraryExhibit;
INSERT OR IGNORE INTO itinerary.ItineraryAnimal SELECT * FROM main.ItineraryAnimal;
INSERT OR IGNORE INTO itinerary.ItineraryAttraction (
   ATTRACTION, OLD_LIKELIHOOD, NEW_LIKELIHOOD, START_TIME, END_TIME
)
SELECT ATTRACTION, OLD_LIKELIHOOD, NEW_LIKELIHOOD, START_TIME, END_TIME
FROM main.ItineraryAttraction;
INSERT OR IGNORE INTO itinerary.ItineraryTransportation SELECT * FROM main.ItineraryTransportation;
INSERT OR IGNORE INTO itinerary.ItineraryTransportationLeg SELECT * FROM main.ItineraryTransportationLeg;
INSERT OR IGNORE INTO itinerary.ItineraryTransportationRouteMarker SELECT * FROM main.ItineraryTransportationRouteMarker;
INSERT OR IGNORE INTO itinerary.ItineraryGuardiansTalk SELECT * FROM main.ItineraryGuardiansTalk;
INSERT OR IGNORE INTO itinerary.ItineraryWildEncounter SELECT * FROM main.ItineraryWildEncounter;
INSERT OR IGNORE INTO itinerary.ItineraryEvent SELECT * FROM main.ItineraryEvent;
INSERT OR IGNORE INTO itinerary.ItineraryWalkRouteStop SELECT * FROM main.ItineraryWalkRouteStop;
INSERT OR IGNORE INTO itinerary.ItineraryWalkRoutePoint SELECT * FROM main.ItineraryWalkRoutePoint;
INSERT OR IGNORE INTO itinerary.ItineraryWalkRouteLeg SELECT * FROM main.ItineraryWalkRouteLeg;

DROP TABLE IF EXISTS main.ItineraryTransportationLeg;
DROP TABLE IF EXISTS main.ItineraryTransportationRouteMarker;
DROP TABLE IF EXISTS main.ItineraryWalkRouteLeg;
DROP TABLE IF EXISTS main.ItineraryWalkRoutePoint;
DROP TABLE IF EXISTS main.ItineraryWalkRouteStop;
DROP TABLE IF EXISTS main.ItineraryAnimal;
DROP TABLE IF EXISTS main.ItineraryAttraction;
DROP TABLE IF EXISTS main.ItineraryExhibit;
DROP TABLE IF EXISTS main.ItineraryGuardiansTalk;
DROP TABLE IF EXISTS main.ItineraryWildEncounter;
DROP TABLE IF EXISTS main.ItineraryEvent;
DROP TABLE IF EXISTS main.ItineraryTransportation;
DROP TABLE IF EXISTS main.ItineraryDate;
DROP TABLE IF EXISTS main.ItineraryStatusSuppression;
