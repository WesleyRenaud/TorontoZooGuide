from .wild_encounter_cancellation_input import WildEncounterCancellationInput


def build_wild_encounter_cancellation( wild_encounter, date, time ):
   return WildEncounterCancellationInput(
      wild_encounter=wild_encounter,
      cancellation_date=date,
      encounter_time=time )
