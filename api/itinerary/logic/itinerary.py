from ... import zoo


def empty_itinerary():
   return zoo.Itinerary(
      date='',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[] )


def build_itinerary(
      date,
      animals,
      attractions,
      guardians_talks,
      wild_encounters ):

   return zoo.Itinerary(
      date=date,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )


def build_current_itinerary(
      saved_itinerary,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller ):

   if saved_itinerary.is_empty():
      return empty_itinerary()

   day = saved_itinerary.day()
   month = saved_itinerary.month()
   year = saved_itinerary.year()

   animals = animal_controller.get_animals_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_animals=saved_itinerary.animal_rows )

   attractions = attraction_controller.get_attractions_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_attractions=saved_itinerary.attraction_rows )

   guardians_talks = guardians_controller.get_guardians_talks_for_saved_itinerary(
      saved_itinerary.guardians_talk_rows )

   wild_encounters = wild_encounter_controller.get_wild_encounters_for_saved_itinerary(
      saved_itinerary.wild_encounter_rows )

   return build_itinerary(
      date=saved_itinerary.date_value,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )
