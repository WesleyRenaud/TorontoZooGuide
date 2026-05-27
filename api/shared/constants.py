OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20


def itinerary_config_to_dict() -> dict[ str, int ]:
   return {
      'animal_visibility_change_threshold': ANIMAL_VISIBILITY_CHANGE_THRESHOLD,
   }
