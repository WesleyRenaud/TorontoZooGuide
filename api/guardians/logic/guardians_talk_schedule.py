from ... import zoo
from ...shared.strings import SharedStrings
from .guardians_talk_name_filter import GuardiansTalkNameFilter


def find_guardians_talk_on_day_schedule( day_schedule, talk_name ):
   talk_filter = GuardiansTalkNameFilter( name=talk_name )

   if talk_filter.should_return_empty():
      return None

   for row in day_schedule:
      if talk_filter.allows_talk_name( row.name ):
         return row

   return None


def build_guardians_talk_schedule_for_target_date(
      records,
      target_date,
      occurrence_is_cancelled ):

   target_weekday = target_date.weekday()
   target_date_str = target_date.isoformat()

   guardians_talks = []

   for record in records:
      name = record.name
      location = record.location
      talk_time = record.talk_time

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

      is_cancelled = occurrence_is_cancelled(
         name,
         location,
            target_date_str,
            talk_time )

      is_available = date_range_ok and weekday_ok and not is_cancelled

      if not is_available:
         if not date_range_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_scheduled_on_visit_day(
               name,
               target_date )
         elif not weekday_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_offered_this_weekday( name )
         elif is_cancelled:
            unavailable_message = SharedStrings.VisitDaySchedule.cancelled_for_this_date( name )

      if is_available:
         guardians_talks.append(
            zoo.GuardiansTalk(
               name=name,
               location=location,
               x_coord=record.x_coord,
               y_coord=record.y_coord,
               start_time=talk_time,
               maximum_duration=record.maximum_duration,
               is_available=is_available,
               unavailable_message=unavailable_message ) )

   return guardians_talks
