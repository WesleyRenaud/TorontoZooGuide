from ... import zoo
from .guardians_talk_filter import GuardiansTalkIncludeFilter


def meet_the_guardians_talk_record_to_model( record ):
   return zoo.GuardiansTalk(
      name=record.name,
      location=record.location,
      x_coord=record.x_coord,
      y_coord=record.y_coord,
      maximum_duration=record.maximum_duration )



def build_guardians_talk_details( talk_records, guardians_talks_to_include=None ):
   include_filter = GuardiansTalkIncludeFilter.from_optional_list(
      guardians_talks_to_include )

   if include_filter.should_return_empty():
      return []

   talks = []

   for record in talk_records:
      if not include_filter.allows_talk_name( record.name ):
         continue

      talks.append( meet_the_guardians_talk_record_to_model( record ) )

   talks.sort(
      key=lambda t: (
         ( t.name or '' ).lower(),
         ( t.location or '' ).lower()
      )
   )

   return talks
