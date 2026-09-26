from __future__ import annotations

from api.models.update import Update


UPDATE_TITLE = 'New baby giraffe'
UPDATE_DESCRIPTION = 'Come meet the new calf.'
UPDATE_TYPE = 'New Arrival'
UPDATE_START_DATE = '2026-06-01'
UPDATE_END_DATE = '2026-06-30'


def Test_ToDict_TestUpdateFields_ExpectFrontendShape() -> None:
   update = Update(
      title=UPDATE_TITLE,
      description=UPDATE_DESCRIPTION,
      update_type=UPDATE_TYPE,
      start_date=UPDATE_START_DATE,
      end_date=UPDATE_END_DATE )

   result = update.to_dict()

   assert result[ 'title' ] == update.title
   assert result[ 'description' ] == update.description
   assert result[ 'type' ] == update.update_type
   assert result[ 'start_date' ] == update.start_date
   assert result[ 'end_date' ] == update.end_date
