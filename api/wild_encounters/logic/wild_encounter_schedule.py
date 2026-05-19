from ... import zoo
from ...shared.strings import SharedStrings
from .wild_encounter_name_filter import WildEncounterNameFilter


def find_wild_encounter_on_day_schedule( day_schedule, encounter_name ):
   encounter_filter = WildEncounterNameFilter( name=encounter_name )

   if encounter_filter.should_return_empty():
      return None

   for row in day_schedule:
      if encounter_filter.allows_wild_encounter_name( row.name ):
         return row

   return None


def filter_available_wild_encounters( wild_encounters ):
   return [
      wild_encounter
      for wild_encounter in wild_encounters
      if getattr( wild_encounter, 'is_available', True )
   ]


def build_wild_encounter_schedule_for_target_date(
      records,
      target_date ):

   target_weekday = target_date.weekday()

   wild_encounters = []

   for record in records:
      name = record.name
      encounter_time = record.encounter_time

      date_range_ok = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=record.schedule_start_date,
         end_date_value=record.schedule_end_date )
      unavailable_message = None

      weekday_ok = zoo.ZooUtil.schedule_includes_weekday(
         target_weekday,
         (
            record.monday,
            record.tuesday,
            record.wednesday,
            record.thursday,
            record.friday,
            record.saturday,
            record.sunday,
         ) )

      is_available = date_range_ok and weekday_ok and not record.is_cancelled

      if not is_available:
         if not date_range_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_scheduled_on_visit_day(
               name,
               target_date )
         elif not weekday_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_offered_this_weekday( name )
         elif record.is_cancelled:
            unavailable_message = SharedStrings.VisitDaySchedule.cancelled_for_this_date( name )

      wild_encounters.append(
         zoo.WildEncounter(
            name=name,
            meeting_spot=record.meeting_spot,
            link=record.link,
            start_time=encounter_time,
            maximum_duration=record.maximum_duration,
            x_coord=record.x_coord,
            y_coord=record.y_coord,
            is_available=is_available,
            unavailable_message=unavailable_message ) )

   return wild_encounters
