from __future__ import annotations

from datetime import date

from tools.checks.station_closure_reader import StationClosureReader


TODAY = date( 2026, 11, 14 )


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def found( boxes: list[ str ], today: date = TODAY ) -> list[ tuple[ str, date | None, date | None ] ]:
   return [
      ( notice.station, notice.start, notice.end )
      for notice in StationClosureReader.read( page( boxes ), today )
   ]


def Test_Read_TestEurasiaClosure_ExpectOpenEnded() -> None:
   notices = found( [
      (
         '<p><strong>Eurasia pathway</strong> '
         'The Eurasia Zoomobile stop is closed at this time.</p>'
      ),
   ] )

   assert notices == [ ( 'Eurasia Zoomobile Station', None, None ) ]


def Test_Read_TestMainStationRelocation_ExpectNothing() -> None:
   notices = found( [
      (
         '<p><strong>Temporary Front Entrance &amp; Zoomobile Station Relocation</strong> '
         'The Zoomobile main station has been temporarily relocated to Indo-Malaya.</p>'
      ),
   ] )

   assert notices == []


def Test_Read_TestTundraPrivateEvent_ExpectHeadingRange() -> None:
   notices = found( [
      (
         '<p><strong>Monday, April 20 - Wednesday, April 22</strong> '
         'The Scarborough Rapid Transit (SRT) car at the Tundra Zoomobile Station '
         'will be closed for a private event.</p>'
      ),
   ], date( 2026, 4, 21 ) )

   assert notices == [
      ( 'Tundra Zoomobile Station', date( 2026, 4, 20 ), date( 2026, 4, 22 ) ),
   ]


def Test_Read_TestSingleDay_ExpectThatDay() -> None:
   notices = found( [
      (
         '<p><strong>Thursday, May 14</strong> '
         'The Scarborough Rapid Transit (SRT) car at the Tundra Zoomobile Station '
         'will be closed for a private event.</p>'
      ),
   ] )

   assert notices == [
      ( 'Tundra Zoomobile Station', date( 2026, 5, 14 ), date( 2026, 5, 14 ) ),
   ]


def Test_Read_TestRemainOpen_ExpectNothing() -> None:
   notices = found( [
      (
         '<p><strong>Africa</strong> '
         'The African Zoomobile stop will remain open.</p>'
      ),
   ] )

   assert notices == []


def Test_Read_TestWholeRide_ExpectNothing() -> None:
   notices = found( [
      (
         '<p><strong>Construction</strong> '
         'Zoomobile will be closed due to construction occurring on the pathway.</p>'
      ),
   ] )

   assert notices == []


def Test_Read_TestWheelchairLift_ExpectNothing() -> None:
   notices = found( [
      (
         '<p><strong>Tundra</strong> '
         'The wheelchair lift at the Tundra Zoomobile Station is closed.</p>'
      ),
   ] )

   assert notices == []


def Test_Read_TestNowOpen_ExpectNothing() -> None:
   notices = found( [
      (
         '<p><strong>Eurasia</strong> '
         'The Eurasia Zoomobile stop is now open.</p>'
      ),
   ] )

   assert notices == []


def Test_Read_TestDateAfterOtherSentence_ExpectOpenEnded() -> None:
   notices = found( [
      (
         '<p><strong>Monday, April 20 - Wednesday, April 22</strong> '
         'Please use the other pathway. '
         'The Eurasia Zoomobile stop is closed at this time.</p>'
      ),
   ], date( 2026, 4, 21 ) )

   assert notices == [ ( 'Eurasia Zoomobile Station', None, None ) ]


def Test_Read_TestSentenceDate_ExpectSentenceRange() -> None:
   notices = found( [
      (
         '<p><strong>Thursday, May 14</strong> '
         'The Tundra Zoomobile Station is closed from April 20 through April 22.</p>'
      ),
   ] )

   assert notices == [
      ( 'Tundra Zoomobile Station', date( 2026, 4, 20 ), date( 2026, 4, 22 ) ),
   ]


def Test_Read_TestYearWrap_ExpectFollowingYear() -> None:
   notices = found( [
      (
         '<p><strong>Winter</strong> '
         'The Indo-Malaya Zoomobile Station is closed December 28 through January 4.</p>'
      ),
   ] )

   assert notices == [
      ( 'Indo-Malaya Zoomobile Station', date( 2026, 12, 28 ), date( 2027, 1, 4 ) ),
   ]


def Test_Read_TestPastMonth_ExpectCheckYear() -> None:
   notices = found( [
      (
         '<p><strong>Paving</strong> '
         'The Africa Zoomobile Station is closed April 28 \u2013 April 30.</p>'
      ),
   ] )

   assert notices == [
      ( 'Africa Zoomobile Station', date( 2026, 4, 28 ), date( 2026, 4, 30 ) ),
   ]
