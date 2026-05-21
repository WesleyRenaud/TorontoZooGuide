from .guardians_talk_cancellation_input import GuardiansTalkCancellationInput


def build_guardians_talk_cancellation( talk, location, date, time ):
   return GuardiansTalkCancellationInput(
      talk_name=talk,
      location=location,
      cancellation_date=date,
      talk_time=time )
