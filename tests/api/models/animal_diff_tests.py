from __future__ import annotations

from api.models.animal_diff import AnimalDiff

def Test_ViewingSpotKey_TestEnclosureName_ExpectNormalizedTuple() -> None:
   diff = AnimalDiff(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=80,
      new_likelihood=60,
      enclosure_name='Indoor' )

   assert diff.viewing_spot_key() == ( 'amur tiger', 'eurasia wilds', 'Indoor' )

def Test_ToDict_TestFields_ExpectFrontendShape() -> None:
   diff = AnimalDiff(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=80,
      new_likelihood=60,
      enclosure_name='Indoor',
      is_added=True,
      covered_by_talk=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert diff.to_dict() == {
      'species': 'Amur Tiger',
      'exhibit': 'Eurasia Wilds',
      'enclosure_name': 'Indoor',
      'old_likelihood': 80,
      'new_likelihood': 60,
      'is_added': True,
      'covered_by_talk': False,
      'start_time': '10:00 AM',
      'end_time': '10:30 AM',
   }
