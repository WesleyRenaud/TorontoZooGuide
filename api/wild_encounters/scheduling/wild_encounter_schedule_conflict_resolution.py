from __future__ import annotations

from ..data_access.wild_encounter_schedule import delete_wild_encounter_schedule
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_conflicts
from ..data_access.wild_encounter_schedule import insert_copied_wild_encounter_schedule
from ..data_access.wild_encounter_schedule import insert_or_update_wild_encounter_schedule
from ..data_access.wild_encounter_schedule import update_wild_encounter_schedule_dates
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=fetch_wild_encounter_schedule_conflicts,
   delete_conflict=delete_wild_encounter_schedule,
   insert_or_update=insert_or_update_wild_encounter_schedule,
   update_dates=update_wild_encounter_schedule_dates,
   insert_copy=insert_copied_wild_encounter_schedule,
)

save_wild_encounter_schedule_replacing_overlaps = _resolution.save_replacing_overlaps
save_wild_encounter_schedule_trimming_overlaps = _resolution.save_trimming_overlaps
trim_wild_encounter_schedule_conflict = _resolution.trim_conflict


__all__ = [
   'save_wild_encounter_schedule_replacing_overlaps',
   'save_wild_encounter_schedule_trimming_overlaps',
   'trim_wild_encounter_schedule_conflict',
]
