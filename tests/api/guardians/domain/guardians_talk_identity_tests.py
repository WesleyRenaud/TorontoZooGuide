from __future__ import annotations

from api.guardians.domain.guardians_talk_identity import GuardiansTalkIdentity
from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator


def Test_EnclosureName_TestNamedEnclosure_ExpectStrippedName() -> None:
   enclosure_name = ' Giraffe House '

   result = GuardiansTalkIdentity.enclosure_name( enclosure_name )

   assert result == enclosure_name.strip()


def Test_ItemKey_TestNamedEnclosure_ExpectNameAndEnclosureJoined() -> None:
   name = 'Masai Giraffe'
   enclosure_name = 'Giraffe House'

   item_key = GuardiansTalkIdentity.item_key( name, enclosure_name )

   assert item_key == ScheduleItemKeySeparator.VALUE.join( [ name, enclosure_name ] )


def Test_ParseItemKey_TestNamedEnclosure_ExpectNameAndEnclosure() -> None:
   name = 'Masai Giraffe'
   enclosure_name = 'Giraffe House'
   item_key = GuardiansTalkIdentity.item_key( name, enclosure_name )

   parsed_name, parsed_enclosure_name = GuardiansTalkIdentity.parse_item_key( item_key )

   assert parsed_name == name
   assert parsed_enclosure_name == enclosure_name
