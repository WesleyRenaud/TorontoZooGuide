def clear_itinerary_date( cur ):
   cur.execute( 'DELETE FROM ItineraryDate;' )


def clear_itinerary_animals( cur ):
   cur.execute( 'DELETE FROM ItineraryAnimal;' )


def clear_itinerary_attractions( cur ):
   cur.execute( 'DELETE FROM ItineraryAttraction;' )


def clear_itinerary_guardians_talks( cur ):
   cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )


def clear_itinerary_wild_encounters( cur ):
   cur.execute( 'DELETE FROM ItineraryWildEncounter;' )


def clear_itinerary( conn ):
   cur = conn.cursor()

   try:
      clear_itinerary_date( cur )
      clear_itinerary_animals( cur )
      clear_itinerary_attractions( cur )
      clear_itinerary_guardians_talks( cur )
      clear_itinerary_wild_encounters( cur )

      conn.commit()

   finally:
      cur.close()

   return True
