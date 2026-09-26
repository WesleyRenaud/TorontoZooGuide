from __future__ import annotations

import math

from api.shared.duration_values import DurationValues


def Test_NormalizeMinutes_TestNone_ExpectNone() -> None:
   value = None

   minutes = DurationValues.normalize_minutes( value )

   assert minutes is None


def Test_NormalizeMinutes_TestZero_ExpectNone() -> None:
   value = 0

   minutes = DurationValues.normalize_minutes( value )

   assert minutes is None


def Test_NormalizeMinutes_TestFractional_ExpectCeiled() -> None:
   value = 7.2

   minutes = DurationValues.normalize_minutes( value )

   assert minutes == max( 1, math.ceil( value ) )


def Test_NormalizeMinutes_TestInteger_ExpectSame() -> None:
   value = 8

   minutes = DurationValues.normalize_minutes( value )

   assert minutes == value


def Test_NormalizeMinutes_TestLargerInteger_ExpectSame() -> None:
   value = 20

   minutes = DurationValues.normalize_minutes( value )

   assert minutes == value


def Test_NormalizeSeconds_TestNone_ExpectNone() -> None:
   value = None

   seconds = DurationValues.normalize_seconds( value )

   assert seconds is None


def Test_NormalizeSeconds_TestZero_ExpectNone() -> None:
   value = 0

   seconds = DurationValues.normalize_seconds( value )

   assert seconds is None


def Test_NormalizeSeconds_TestHalfMinute_ExpectCeiled() -> None:
   value = 0.5

   seconds = DurationValues.normalize_seconds( value )

   assert seconds == int(
      math.ceil( float( value ) * DurationValues.minutes_to_seconds( 1 ) ) )


def Test_NormalizeSeconds_TestFractional_ExpectCeiled() -> None:
   value = 7.2

   seconds = DurationValues.normalize_seconds( value )

   assert seconds == int(
      math.ceil( float( value ) * DurationValues.minutes_to_seconds( 1 ) ) )


def Test_NormalizeSeconds_TestInteger_ExpectMinutesToSeconds() -> None:
   value = 8

   seconds = DurationValues.normalize_seconds( value )

   assert seconds == DurationValues.minutes_to_seconds( value )


def Test_NormalizeSeconds_TestLargerInteger_ExpectMinutesToSeconds() -> None:
   value = 20

   seconds = DurationValues.normalize_seconds( value )

   assert seconds == DurationValues.minutes_to_seconds( value )
