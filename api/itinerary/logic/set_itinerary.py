from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary_persistence import clear_itinerary
from ..data_access.itinerary_persistence import save_validated_itinerary
from ..data_access.itinerary_save_input_mapper import map_itinerary_save_input
from .itinerary_validation import validate_itinerary_for_save


def set_itinerary(
      conn,
      date,
      animals,
      attractions,
      guardians_talks,
      wild_encounters,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller ):
   save_input = map_itinerary_save_input(
      date,
      animals,
      attractions,
      guardians_talks,
      wild_encounters )
   old_visit_date = fetch_itinerary_date( conn )

   validated_itinerary = validate_itinerary_for_save(
      conn,
      save_input,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      new_visit_date_temp=None,
      old_visit_date=old_visit_date )

   clear_itinerary( conn )
   save_validated_itinerary( conn, save_input.date, validated_itinerary )

   return True
