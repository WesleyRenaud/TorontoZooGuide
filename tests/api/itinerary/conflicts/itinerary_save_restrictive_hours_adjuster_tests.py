from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.conflicts.itinerary_save_restrictive_hours_adjuster import ItinerarySaveRestrictiveHoursAdjuster
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from api.shared.enums import ItineraryAdjustmentType
from api.shared.enums.position import Position
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ADJUSTER_SCHEMA = """
CREATE TABLE Itinerary (
   DATE                 TEXT        NOT NULL,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

CREATE TABLE ZooHours (
   OPERATING_DATE       TEXT        NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME            TEXT        NOT NULL,
   LAST_ADMISSION_TIME  TEXT        NOT NULL,
   CLOSE_TIME           TEXT        NOT NULL
);
"""

JUNE_20_DATE = date( 2026, 6, 20 )
JUNE_22_DATE = date( 2026, 6, 22 )
JUNE_20_HOURS = ZooHoursRecord(
   operating_date=JUNE_20_DATE.isoformat(),
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)
JUNE_22_HOURS = ZooHoursRecord(
   operating_date=JUNE_22_DATE.isoformat(),
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='17:00',
   close_time='18:00',
)


def _insert_zoo_hours(
      conn: sqlite3.Connection,
      hours: ZooHoursRecord ) -> None:
   conn.execute(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         hours.operating_date,
         hours.early_admission_time,
         hours.open_time,
         hours.last_admission_time,
         hours.close_time,
      ) )


def _stub_saved_itinerary(
      monkeypatch: pytest.MonkeyPatch,
      *,
      arrival_time: str,
      departure_time: str ) -> SavedItinerary:
   saved = SavedItinerary(
      date_value=JUNE_20_HOURS.operating_date,
      arrival_time=arrival_time,
      departure_time=departure_time,
   )
   monkeypatch.setattr(
      'api.itinerary.conflicts.itinerary_save_restrictive_hours_adjuster.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved )
   return saved


@pytest.fixture
def adjuster_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ADJUSTER_SCHEMA )
   conn.execute(
      """   INSERT INTO Itinerary (
               DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( JUNE_20_HOURS.operating_date, '09:00', '17:00' ) )
   _insert_zoo_hours( conn, JUNE_20_HOURS )
   _insert_zoo_hours( conn, JUNE_22_HOURS )
   conn.commit()
   yield conn
   conn.close()


def Test_Adjust_TestSameVisitDate_ExpectNoAdjustments(
      adjuster_conn: sqlite3.Connection ) -> None:
   save_input = ItinerarySaveInput(
      date=JUNE_20_DATE,
      arrival_time='9:00 AM',
      departure_time='17:00',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   assert updated_input is save_input
   assert adjustments == []


def Test_Adjust_TestChangedArrivalWithoutSavedMatch_ExpectNoArrivalAdjustment(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = '9:15 AM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time=arrival_time,
      departure_time='17:00',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   assert updated_input.arrival_time == arrival_time
   assert adjustments == []


def Test_Adjust_TestLateArrivalAfterLastAdmission_ExpectMovedToLastAdmission(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = '6:30 PM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time=arrival_time,
      departure_time='5:00 PM' )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time=arrival_time,
      departure_time='17:00',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   adjustment = adjustments[ Position.FIRST ]

   assert updated_input.arrival_time == JUNE_22_HOURS.last_admission_time
   assert len( adjustments ) == 1
   assert adjustment.type == ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED


def Test_Adjust_TestEarlyDepartureBeforeOpen_ExpectMovedToOpen(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   departure_time = '9:00 AM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time='9:30 AM',
      departure_time=departure_time )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time='9:30 AM',
      departure_time=departure_time,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   adjustment = adjustments[ Position.FIRST ]

   assert updated_input.departure_time == JUNE_22_HOURS.open_time
   assert len( adjustments ) == 1
   assert adjustment.type == ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED


def Test_Adjust_TestDateChangeFromEarlyAdmissionDay_ExpectArrivalMovedToOpen(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = '9:00 AM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time=arrival_time,
      departure_time='5:00 PM' )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time=arrival_time,
      departure_time='17:00',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   adjustment = adjustments[ Position.FIRST ]

   assert updated_input.arrival_time == ItineraryArrivalTimeValidator.earliest_arrival_time(
      JUNE_22_HOURS )
   assert len( adjustments ) == 1
   assert adjustment.type == ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED


def Test_Adjust_TestDateChangeWithLateDeparture_ExpectDepartureMovedToClose(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   departure_time = '8:00 PM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time='9:30 AM',
      departure_time=departure_time )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time='9:30 AM',
      departure_time=departure_time,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   adjustment = adjustments[ Position.FIRST ]

   assert updated_input.departure_time == JUNE_22_HOURS.close_time
   assert len( adjustments ) == 1
   assert adjustment.type == ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED


def Test_Adjust_TestEarlyAdmissionArrival_ExpectAdjustmentDict(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = '9:15 AM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time=arrival_time,
      departure_time='5:00 PM' )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time=arrival_time,
      departure_time='17:00',
   )
   expected_adjustment = ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=arrival_time,
      value=ItineraryArrivalTimeValidator.earliest_arrival_time( JUNE_22_HOURS ),
      reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   assert updated_input.arrival_time == expected_adjustment.value
   assert [ adjustment.to_dict() for adjustment in adjustments ] == [
      expected_adjustment.to_dict(),
   ]


def Test_Adjust_TestLateDepartureOnShorterDay_ExpectAdjustmentDict(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   departure_time = '6:30 PM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time='9:30 AM',
      departure_time=departure_time )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time='9:30 AM',
      departure_time=departure_time,
   )
   expected_adjustment = ItineraryAdjustment(
      type=ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED,
      field='departureTime',
      previous_value=departure_time,
      value=JUNE_22_HOURS.close_time,
      reason=ItineraryAdjustmentReason.DEPARTURE_OUTSIDE_OPERATING_HOURS,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   assert updated_input.departure_time == expected_adjustment.value
   assert [ adjustment.to_dict() for adjustment in adjustments ] == [
      expected_adjustment.to_dict(),
   ]


def Test_Adjust_TestChangedDepartureWithoutSavedMatch_ExpectNoDepartureAdjustment(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   departure_time = '19:00'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time='9:30 AM',
      departure_time='6:30 PM' )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time='9:30 AM',
      departure_time=departure_time,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   assert updated_input.departure_time == departure_time
   assert adjustments == []


def Test_Adjust_TestShortVisitDateChange_ExpectArrivalOnlyAdjusted(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   arrival_time = '9:15 AM'
   departure_time = '9:35 AM'
   _stub_saved_itinerary(
      monkeypatch,
      arrival_time=arrival_time,
      departure_time=departure_time )
   save_input = ItinerarySaveInput(
      date=JUNE_22_DATE,
      arrival_time=arrival_time,
      departure_time=departure_time,
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date=JUNE_20_DATE.isoformat(),
   )

   adjustment = adjustments[ Position.FIRST ]

   assert updated_input.arrival_time == ItineraryArrivalTimeValidator.earliest_arrival_time(
      JUNE_22_HOURS )
   assert updated_input.departure_time == departure_time
   assert len( adjustments ) == 1
   assert adjustment.type == ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED
