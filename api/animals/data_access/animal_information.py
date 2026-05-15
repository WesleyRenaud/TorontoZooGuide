from ... import zoo


def fetch_animal_information( conn, species ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  a.LATIN_NAME,
                  a.GENERAL_VIEWING_TIPS,
                  a.SEASONAL_VIEWING_TIPS,
                  a.IDENTIFICATION,
                  a.HABITAT_AND_RANGE,
                  a.DIET_AND_FEEDING,
                  a.BEHAVIOUR_AND_SOCIAL_LIFE,
                  a.ADAPTATIONS,
                  a.REPRODUCTION_AND_LIFE_CYCLE,
                  a.ANIMALS_AT_THE_ZOO,
                  e.EXHIBIT,
                  e.SEASONAL_VIEWING_SUMMARY,
                  e.SEASONAL_VIEWING_INFORMATION
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE a.SPECIES = ?;
         """,
         ( species, ) )

      row = data.fetchone()

      if row == None:
         return None

      return zoo.Animal(
         species=species,
         latin_name=row[ 'LATIN_NAME' ],
         general_viewing_tips=row[ 'GENERAL_VIEWING_TIPS' ],
         seasonal_viewing_tips=row[ 'SEASONAL_VIEWING_TIPS' ],
         identification=row[ 'IDENTIFICATION' ],
         habitat_and_range=row[ 'HABITAT_AND_RANGE' ],
         diet_and_feeding=row[ 'DIET_AND_FEEDING' ],
         behaviour_and_life_cycle=row[ 'BEHAVIOUR_AND_SOCIAL_LIFE' ],
         adaptations=row[ 'ADAPTATIONS' ],
         reproduction_and_life_cycle=row[ 'REPRODUCTION_AND_LIFE_CYCLE' ],
         animals_at_the_zoo=row[ 'ANIMALS_AT_THE_ZOO' ],
         exhibit=row[ 'EXHIBIT' ],
         seasonal_viewing_summary=row[ 'SEASONAL_VIEWING_SUMMARY' ],
         seasonal_viewing_information=row[ 'SEASONAL_VIEWING_INFORMATION' ] )

   finally:
      cur.close()
