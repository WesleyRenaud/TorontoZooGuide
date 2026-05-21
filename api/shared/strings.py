from ..zoo_util import ZooUtil


class SharedStrings:
   class Animals:
      @staticmethod
      def temporarily_off_display( species ):
         return f'The { species } is temporarily off-display.'


      @staticmethod
      def viewing_alert( species ):
         return f'The { species } may be less visible than usual at this time.'


      @staticmethod
      def limited_viewing_schedule(
            species,
            daily_start_time,
            daily_end_time ):
         return (
            f'The { species } is viewable daily only from '
            f'{ daily_start_time } to { daily_end_time }.' )


      @staticmethod
      def limited_viewing_schedule_until(
            species,
            daily_start_time,
            daily_end_time,
            end_date ):
         return (
            f'The { species } is viewable daily only from '
            f'{ daily_start_time } to { daily_end_time }until '
            f'{ ZooUtil.format_display_date_value( end_date ) }.' )


   class Attractions:
      @staticmethod
      def weekends_and_holidays_only( attraction_name ):
         return f'The { attraction_name } is open on weekends and holidays only.'


      @staticmethod
      def not_scheduled_today( attraction_name ):
         return f'The { attraction_name } is not scheduled to be open today.'


      @staticmethod
      def likely_not_operating( attraction_name ):
         return f'The { attraction_name } is most likely not operating on this day.'


   class Locations:
      @staticmethod
      def temporarily_closed( name ):
         return f'The { name } is temporarily closed.'


      @staticmethod
      def not_scheduled_to_be_open_today( name ):
         return f'The { name } is not scheduled to be open today.'


   class DrinkingFountains:
      @staticmethod
      def closed_for_season():
         return 'The drinking fountains are closed for the season.'


   class WildEncounters:
      @staticmethod
      def not_scheduled_today( wild_encounter ):
         return f'The { wild_encounter } is not scheduled today.'


   class GuardiansTalks:
      @staticmethod
      def not_scheduled_today( talk_name, location ):
         return f'The { talk_name } at { location } is not scheduled today.'


   class VisitDaySchedule:
      """Guest-facing copy when a visit-day schedule row does not apply."""

      @staticmethod
      def not_scheduled_on_visit_day( name, target_date ):
         return (
            f'{ name } is not scheduled on { target_date.strftime( "%B" ) } '
            f'{ target_date.day }.' )


      @staticmethod
      def not_offered_this_weekday( name ):
         return f'{ name } is not offered on this day of the week.'


      @staticmethod
      def cancelled_for_this_date( name ):
         return f'{ name } has been cancelled for this date.'
