def save_itinerary_date( cur, visit_date ):
   cur.execute(
      """   INSERT INTO ItineraryDate ( ITINERARY_DATE )
            VALUES ( ? );
      """,
      ( visit_date, ) )


def save_itinerary_animals( cur, animals ):
   if not animals:
      return

   for animal in animals:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryAnimal (
                  SPECIES,
                  EXHIBIT,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD
               )
               VALUES ( ?, ?, ?, ? );
         """,
         (
            animal.species,
            animal.exhibit,
            animal.old_likelihood,
            animal.new_likelihood,
         ) )


def save_itinerary_attractions( cur, attractions ):
   if not attractions:
      return

   for attraction in attractions:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryAttraction (
                  ATTRACTION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD
               )
               VALUES ( ?, ?, ? );
         """,
         (
            attraction.name,
            attraction.old_likelihood,
            attraction.new_likelihood,
         ) )


def save_itinerary_guardians_talks( cur, guardians_talks ):
   if not guardians_talks:
      return

   for talk in guardians_talks:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryGuardiansTalk (
                  TALK_NAME,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               )
               VALUES ( ?, ?, ?, ? );
         """,
         (
            talk.name,
            talk.start_time,
            talk.end_time,
            1 if talk.is_deleted else 0,
         ) )


def save_itinerary_wild_encounters( cur, wild_encounters ):
   if not wild_encounters:
      return

   for encounter in wild_encounters:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryWildEncounter (
                  WILD_ENCOUNTER,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               )
               VALUES ( ?, ?, ?, ? );
         """,
         (
            encounter.name,
            encounter.start_time,
            encounter.end_time,
            1 if encounter.is_deleted else 0,
         ) )


def save_validated_itinerary( conn, visit_date, validated_itinerary ):
   cur = conn.cursor()

   try:
      save_itinerary_date( cur, visit_date )
      save_itinerary_animals( cur, validated_itinerary.animals )
      save_itinerary_attractions( cur, validated_itinerary.attractions )
      save_itinerary_guardians_talks( cur, validated_itinerary.guardians_talks )
      save_itinerary_wild_encounters( cur, validated_itinerary.wild_encounters )

      conn.commit()

   finally:
      cur.close()

   return True
