from __future__ import annotations

from datetime import date

from ..app_strings import format_app_string
from .calendar_dates import DateValues


class SharedStrings:
   """Guest-facing copy resolved from scripts/strings/ (frontend source of truth)."""

   class Animals:
      @staticmethod
      def temporarily_off_display( species: str ) -> str:
         return format_app_string(
            'guestStatus.animals.temporarilyOffDisplay',
            species=species )


      @staticmethod
      def viewing_alert( species: str ) -> str:
         return format_app_string(
            'guestStatus.animals.viewingAlert',
            species=species )


      @staticmethod
      def single_habitat_alternate_enclosure_viewing_alert(
            species: str,
            chosen_location: str,
            alternate_habitat: str ) -> str:
         return format_app_string(
            'guestStatus.animals.singleHabitatAlternateEnclosureViewingAlert',
            species=species,
            chosenLocation=chosen_location,
            alternateHabitat=alternate_habitat )


      @staticmethod
      def limited_viewing_schedule(
            species: str,
            daily_start_time: str,
            daily_end_time: str ) -> str:
         return format_app_string(
            'guestStatus.animals.limitedViewingSchedule',
            species=species,
            dailyStartTime=daily_start_time,
            dailyEndTime=daily_end_time )


      @staticmethod
      def limited_viewing_schedule_until(
            species: str,
            daily_start_time: str,
            daily_end_time: str,
            end_date: str ) -> str:
         return format_app_string(
            'guestStatus.animals.limitedViewingScheduleUntil',
            species=species,
            dailyStartTime=daily_start_time,
            dailyEndTime=daily_end_time,
            endDate=DateValues.format_display_date_value( end_date ) )


   class Attractions:
      @staticmethod
      def weekends_and_holidays_only( attraction_name: str ) -> str:
         return format_app_string(
            'guestStatus.attractions.weekendsAndHolidaysOnly',
            attractionName=attraction_name )


      @staticmethod
      def not_scheduled_today( attraction_name: str ) -> str:
         return format_app_string(
            'guestStatus.attractions.notScheduledToday',
            attractionName=attraction_name )


      @staticmethod
      def likely_not_operating( attraction_name: str ) -> str:
         return format_app_string(
            'guestStatus.attractions.likelyNotOperating',
            attractionName=attraction_name )


   class Locations:
      @staticmethod
      def temporarily_closed( name: str ) -> str:
         return format_app_string(
            'guestStatus.locations.temporarilyClosed',
            name=name )


      @staticmethod
      def not_scheduled_to_be_open_today( name: str ) -> str:
         return format_app_string(
            'guestStatus.locations.notScheduledToBeOpenToday',
            name=name )


      @staticmethod
      def likely_not_open_on_day( name: str ) -> str:
         return format_app_string(
            'guestStatus.locations.likelyNotOpenOnDay',
            name=name )


   class DrinkingFountains:
      @staticmethod
      def closed_for_season() -> str:
         return format_app_string( 'guestStatus.drinkingFountains.closedForSeason' )


   class WildEncounters:
      @staticmethod
      def not_scheduled_today( wild_encounter: str ) -> str:
         return format_app_string(
            'guestStatus.wildEncounters.notScheduledToday',
            wildEncounter=wild_encounter )


   class GuardiansTalks:
      @staticmethod
      def not_scheduled_today( talk_name: str, location: str ) -> str:
         return format_app_string(
            'guestStatus.guardiansTalks.notScheduledToday',
            talkName=talk_name,
            location=location )


      @staticmethod
      def could_not_add_occurrence(
            talk: str,
            location: str,
            date: str ) -> str:
         return format_app_string(
            'guestStatus.guardiansTalks.couldNotAddOccurrence',
            talk=talk,
            location=location,
            date=date )


      @staticmethod
      def occurrence_already_exists(
            talk: str,
            location: str,
            date: str,
            talk_time: str ) -> str:
         return format_app_string(
            'guestStatus.guardiansTalks.occurrenceAlreadyExists',
            talk=talk,
            location=location,
            date=date,
            talkTime=talk_time )


   class Itinerary:
      @staticmethod
      def guardians_talk_fully_covered_by_blocker() -> str:
         return format_app_string(
            'guestStatus.itinerary.guardiansTalkFullyCoveredByBlocker' )


      @staticmethod
      def guardians_talk_unexpected_blocker_overlap() -> str:
         return format_app_string(
            'guestStatus.itinerary.guardiansTalkUnexpectedBlockerOverlap' )


      @staticmethod
      def guardians_talk_no_remaining_time_after_trimming() -> str:
         return format_app_string(
            'guestStatus.itinerary.guardiansTalkNoRemainingTimeAfterTrimming' )


      @staticmethod
      def wild_encounter_row_missing_start_time( wild_encounter: str ) -> str:
         return format_app_string(
            'guestStatus.itinerary.wildEncounterRowMissingStartTime',
            wildEncounter=repr( wild_encounter ) )


   class VisitDaySchedule:
      """Guest-facing copy when a visit-day schedule row does not apply."""

      @staticmethod
      def not_scheduled_on_visit_day( name: str, target_date: date ) -> str:
         return format_app_string(
            'guestStatus.visitDaySchedule.notScheduledOnVisitDay',
            name=name,
            month=target_date.strftime( '%B' ),
            day=target_date.day )


      @staticmethod
      def not_offered_this_weekday( name: str ) -> str:
         return format_app_string(
            'guestStatus.visitDaySchedule.notOfferedThisWeekday',
            name=name )


      @staticmethod
      def cancelled_for_this_date( name: str ) -> str:
         return format_app_string(
            'guestStatus.visitDaySchedule.cancelledForThisDate',
            name=name )
