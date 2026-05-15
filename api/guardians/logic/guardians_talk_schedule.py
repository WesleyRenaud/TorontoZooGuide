from ... import zoo
from ...shared.strings import SharedStrings


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

      start_ok = True
      end_ok = True
      unavailable_message = None

      if record.schedule_start_date != None:
         schedule_start_date = zoo.ZooUtil.parse_date_value(
            value=record.schedule_start_date )
         start_ok = target_date >= schedule_start_date

      if record.schedule_end_date != None:
         schedule_end_date = zoo.ZooUtil.parse_date_value(
            value=record.schedule_end_date )
         end_ok = target_date <= schedule_end_date

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

      is_available = start_ok and end_ok and weekday_ok and not is_cancelled

      if not is_available:
         if not start_ok or not end_ok:
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
