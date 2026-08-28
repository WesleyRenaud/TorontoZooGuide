from __future__ import annotations

from typing import TypeAlias

from ...animal_schedule_item_key import AnimalScheduleItemKey
from ...attraction_schedule_item_key import AttractionScheduleItemKey


class ListedScheduleItemKey():
   Key: TypeAlias = AnimalScheduleItemKey | AttractionScheduleItemKey
