from ... import zoo
from ...shared.strings import SharedStrings
from .guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from .guardians_talk_schedule_input import GuardiansTalkScheduleInput


def build_guardians_talk_schedule(
      talk,
      location,
      start_date,
      end_date,
      talk_time,
      monday,
      tuesday,
      wednesday,
      thursday,
      friday,
      saturday,
      sunday,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.GuardiansTalks.not_scheduled_today(
         talk,
         location )

   return GuardiansTalkScheduleInput(
      talk_name=talk,
      location=location,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      talk_time=talk_time,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      message=message )


def build_guardians_talk_schedule_end( talk, location, schedule_end_date ):
   return GuardiansTalkScheduleEndInput(
      talk_name=talk,
      location=location,
      schedule_end_date=schedule_end_date )
