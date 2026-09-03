from __future__ import annotations

from api.models.attraction_diff import AttractionDiff

def Test_ToDict_TestFields_ExpectFrontendShape() -> None:
   diff = AttractionDiff(
      name='Conservation Carousel',
      old_likelihood=70,
      new_likelihood=50,
      start_time='11:00 AM',
      end_time='11:20 AM' )

   assert diff.to_dict() == {
      'name': 'Conservation Carousel',
      'old_likelihood': 70,
      'new_likelihood': 50,
      'start_time': '11:00 AM',
      'end_time': '11:20 AM',
   }
