class SharedStrings:
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
