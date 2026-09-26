from __future__ import annotations

from api.models.attraction_diff import AttractionDiff


def Test_ToDict_TestFields_ExpectFrontendShape() -> None:
   diff = AttractionDiff(
      name='Conservation Carousel',
      old_likelihood=70,
      new_likelihood=50,
      start_time='11:00 AM',
      end_time='11:20 AM' )

   result = diff.to_dict()

   assert result[ 'name' ] == diff.name
   assert result[ 'old_likelihood' ] == diff.old_likelihood
   assert result[ 'new_likelihood' ] == diff.new_likelihood
   assert result[ 'start_time' ] == diff.start_time
   assert result[ 'end_time' ] == diff.end_time
