DELETE FROM ItineraryStatus
WHERE STATUS IN ( 'guardiansTalkLongWait', 'wildEncounterLongWait' );

INSERT INTO ItineraryStatus ( STATUS, IS_SUPPRESSABLE )
SELECT 'fixedTimeItemLongWait', 0
WHERE NOT EXISTS (
   SELECT 1
   FROM ItineraryStatus
   WHERE STATUS = 'fixedTimeItemLongWait'
)
AND EXISTS (
   SELECT 1
   FROM ItineraryStatus
);
