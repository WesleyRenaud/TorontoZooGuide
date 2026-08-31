from __future__ import annotations

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator


def Test_MinutesFromLengthPx_TestLengths_ExpectFlooredMinutes() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE

   assert WalkTravelTimeCalculator.minutes_from_length_px( 0 ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( -10 ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( 0.5 * walk_px_per_minute ) == 0
   assert WalkTravelTimeCalculator.minutes_from_length_px( 1.0 * walk_px_per_minute ) == 1
   assert WalkTravelTimeCalculator.minutes_from_length_px( 1.5 * walk_px_per_minute ) == 1


def Test_SecondsFromLengthPx_TestLengths_ExpectFlooredMinuteSeconds() -> None:
   walk_px_per_minute = WalkTravelTimeCalculator.WALK_PX_PER_MINUTE

   assert WalkTravelTimeCalculator.seconds_from_length_px( 0.5 * walk_px_per_minute ) == 0
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.0 * walk_px_per_minute ) == 60
   assert WalkTravelTimeCalculator.seconds_from_length_px( 1.5 * walk_px_per_minute ) == 60
