from datetime import timedelta

from ... import zoo
from .guardians_talk_weekday_time import guardians_talk_time_for_weekday


def build_guardians_talk_occurrences(
      schedule_record,
      cancellation_records,
      days_ahead ):
   if schedule_record == None:
      return []

   today = zoo.ZooUtil.parse_date_value( zoo.ZooUtil.today_date_key() )
   schedule_start_date = today
   schedule_end_date = today + timedelta( days=days_ahead )

   parsed_start_date = zoo.ZooUtil.parse_date_value(
      value=schedule_record.schedule_start_date )

   if parsed_start_date > schedule_start_date:
      schedule_start_date = parsed_start_date

   if schedule_record.schedule_end_date != None:
      parsed_end_date = zoo.ZooUtil.parse_date_value(
         value=schedule_record.schedule_end_date )

      if parsed_end_date < schedule_end_date:
         schedule_end_date = parsed_end_date

   if schedule_end_date < schedule_start_date:
      return []

   occurrences = []
   current_date = schedule_start_date

   while current_date <= schedule_end_date:
      current_date_key = current_date.isoformat()
      talk_time = guardians_talk_time_for_weekday(
         schedule_record,
         current_date.weekday() )

      if (
            talk_time != None
            and not guardians_talk_occurrence_is_cancelled(
               cancellation_records,
               current_date_key,
               talk_time ) ):
         occurrences.append(
            zoo.ScheduledOccurrence(
               date=current_date_key,
               time=talk_time ) )

      current_date += timedelta( days=1 )

   return occurrences


def guardians_talk_occurrence_is_cancelled(
      cancellation_records,
      occurrence_date,
      talk_time ):
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.talk_time == talk_time
      for cancellation in cancellation_records
   )
