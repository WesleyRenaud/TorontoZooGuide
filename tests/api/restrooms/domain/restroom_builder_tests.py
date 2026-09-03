from __future__ import annotations

from datetime import date

from api.restrooms.data_access.restroom_record import RestroomRecord
from api.restrooms.domain.restroom_builder import RestroomBuilder
from api.restrooms.domain.restroom_context import RestroomContext


RESTROOM_NAME = 'Entrance Restroom'
CLOSED_MESSAGE = 'Closed for testing.'
ALERT_MESSAGE = "Women's restroom is temporarily unavailable."
VISIT_DATE = date( 2026, 6, 15 )
OUTSIDE_VISIT_DATE = date( 2026, 5, 31 )


def _restroom_record( **overrides: object ) -> RestroomRecord:
   values: dict[ str, object ] = {
      'title': RESTROOM_NAME,
      'x_coord': 1.0,
      'y_coord': 2.0,
      'is_closed': True,
      'closed_message': CLOSED_MESSAGE,
      'closed_start': '2026-06-01',
      'closed_end': '2026-06-30',
      'alert_message': None,
      'alert_start_date': None,
      'alert_end_date': None,
   }
   values.update( overrides )

   return RestroomRecord( **values )


def Test_IsStatusActive_TestVisitDateInRange_ExpectTrue() -> None:
   assert RestroomBuilder.is_status_active(
      _restroom_record(),
      VISIT_DATE ) is True


def Test_IsStatusActive_TestVisitDateOutsideRange_ExpectFalse() -> None:
   assert RestroomBuilder.is_status_active(
      _restroom_record(),
      OUTSIDE_VISIT_DATE ) is False


def Test_IsAlertActive_TestActiveAlert_ExpectTrue() -> None:
   assert RestroomBuilder.is_alert_active(
      _restroom_record(
         alert_message=ALERT_MESSAGE,
         alert_start_date='2026-06-01',
         alert_end_date='2026-06-30' ),
      VISIT_DATE ) is True


def Test_BuildRestroom_TestClosedStatus_ExpectClosedMessageOnlyWhenActive() -> None:
   restroom = RestroomBuilder.build_restroom(
      _restroom_record(),
      RestroomContext( target_date=VISIT_DATE ) )

   assert restroom.is_closed is True
   assert restroom.closed_message == CLOSED_MESSAGE
   assert restroom.has_alert is False
   assert restroom.alert_message is None


def Test_BuildRestrooms_TestClosedRestroom_ExpectExcludedUnlessRequested() -> None:
   context = RestroomContext( target_date=VISIT_DATE )
   records = [ _restroom_record() ]

   open_only = RestroomBuilder.build_restrooms(
      records,
      context,
      include_closed_restrooms=False )
   with_closed = RestroomBuilder.build_restrooms(
      records,
      context,
      include_closed_restrooms=True )

   assert open_only == []
   assert len( with_closed ) == 1
   assert with_closed[ 0 ].title == RESTROOM_NAME


def Test_IsStatusActive_TestNullIsClosed_ExpectFalse() -> None:
   record = _restroom_record( is_closed=None )

   assert RestroomBuilder.is_status_active( record, target_date=VISIT_DATE ) is False
