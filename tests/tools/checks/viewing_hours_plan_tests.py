from __future__ import annotations

from datetime import date

from api.animals.domain.animal_visibility_schedule import AnimalVisibilitySchedule
from api.shared.calendar_dates import CalendarDates
from tools.checks.viewing_hours import ViewingHours
from tools.checks.viewing_hours_plan import ViewingHoursPlan


TODAY = date( 2026, 11, 12 )
HORIZON = CalendarDates.one_month_later( TODAY )
HIPPO = 'Pygmy Hippopotamus'
PAVILION = 'African Rainforest Pavilion'
OTTER = 'North American River Otter'
AMERICAS = 'Americas Pavilion'
CAMEL = 'Bactrian Camel'
EURASIA = 'Eurasia Wilds'
WOMBAT = 'Southern Hairy-Nosed Wombat'
AUSTRALASIA = 'Australasia Pavilion'
GIRAFFE = 'Masai Giraffe'
SAVANNA = 'Africa Savanna'


def _website(
      species: str,
      exhibit: str,
      opens: str,
      closes: str ) -> ViewingHours:
   return ViewingHours( species, exhibit, None, None, opens, closes )


def _stored(
      species: str,
      exhibit: str,
      start: str | None,
      end: str | None,
      opens: str,
      closes: str ) -> AnimalVisibilitySchedule:
   return AnimalVisibilitySchedule(
      species,
      exhibit,
      start,
      end,
      opens,
      closes,
      'Existing message.',
   )


def _labels( hours: list[ ViewingHours ] ) -> list[ tuple[ str, str, date | None, date | None, str, str ] ]:
   return sorted(
      (
         item.species,
         item.exhibit,
         item.start,
         item.end,
         item.opens,
         item.closes,
      )
      for item in hours
   )


def Test_Build_TestNewTrimExtendAndRemove_ExpectMonthWindow() -> None:
   website = [
      _website( OTTER, AMERICAS, '10:00 AM', '1:00 PM' ),
      _website( 'pygmy hippopotamus', 'african rainforest pavilion', '10:30 AM', '2:30 PM' ),
      _website( CAMEL, EURASIA, '10:00 AM', '2:00 PM' ),
      _website( WOMBAT, AUSTRALASIA, '9:00 AM', '11:00 AM' ),
   ]
   stored = [
      _stored( HIPPO, PAVILION, '2026-10-20', None, '10:30 AM', '2:30 PM' ),
      _stored( CAMEL, EURASIA, '2026-11-01', '2026-11-20', '10:00 AM', '2:00 PM' ),
      _stored( WOMBAT, AUSTRALASIA, None, '2027-01-01', '8:00 AM', '10:00 AM' ),
      _stored( GIRAFFE, SAVANNA, '2026-11-01', '2026-12-01', '11:00 AM', '1:00 PM' ),
   ]

   plan = ViewingHoursPlan.build( website, stored, TODAY )

   assert _labels( plan.added ) == [
      ( OTTER, AMERICAS, TODAY, HORIZON, '10:00 AM', '1:00 PM' ),
   ]
   assert _labels( plan.trimmed ) == [
      ( HIPPO, PAVILION, date( 2026, 10, 20 ), HORIZON, '10:30 AM', '2:30 PM' ),
      ( WOMBAT, AUSTRALASIA, TODAY, HORIZON, '9:00 AM', '11:00 AM' ),
   ]
   assert _labels( plan.extended ) == [
      ( CAMEL, EURASIA, date( 2026, 11, 1 ), HORIZON, '10:00 AM', '2:00 PM' ),
   ]
   assert _labels( plan.removed ) == [
      ( GIRAFFE, SAVANNA, date( 2026, 11, 1 ), date( 2026, 12, 1 ), '11:00 AM', '1:00 PM' ),
   ]
   assert plan.realigned == []


def Test_Build_TestAlignedClock_ExpectNoChanges() -> None:
   website = [ _website( HIPPO, PAVILION, '10:30am', '2:30pm' ) ]
   stored = [
      _stored( HIPPO, PAVILION, TODAY.isoformat(), HORIZON.isoformat(), '10:30 AM', '2:30 PM' ),
   ]

   plan = ViewingHoursPlan.build( website, stored, TODAY )

   assert plan.count() == 0


def Test_Build_TestDifferentClock_ExpectRealigned() -> None:
   website = [ _website( HIPPO, PAVILION, '11:00 AM', '1:00 PM' ) ]
   stored = [
      _stored( HIPPO, PAVILION, '2026-10-20', HORIZON.isoformat(), '10:30 AM', '2:30 PM' ),
   ]

   plan = ViewingHoursPlan.build( website, stored, TODAY )

   assert _labels( plan.realigned ) == [
      ( HIPPO, PAVILION, date( 2026, 10, 20 ), HORIZON, '11:00 AM', '1:00 PM' ),
   ]
   assert plan.added == []
   assert plan.removed == []
   assert plan.extended == []
   assert plan.trimmed == []
