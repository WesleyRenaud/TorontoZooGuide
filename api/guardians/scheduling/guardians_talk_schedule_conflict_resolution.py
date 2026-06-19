from __future__ import annotations

from ..data_access.guardians_talk_schedule import delete_guardians_talk_schedule
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_conflicts
from ..data_access.guardians_talk_schedule import insert_copied_guardians_talk_schedule
from ..data_access.guardians_talk_schedule import insert_or_update_guardians_talk_schedule
from ..data_access.guardians_talk_schedule import update_guardians_talk_schedule_dates
from ...shared.build_opening_schedule_conflict_resolution import OpeningScheduleConflictResolution


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=fetch_guardians_talk_schedule_conflicts,
   delete_conflict=delete_guardians_talk_schedule,
   insert_or_update=insert_or_update_guardians_talk_schedule,
   update_dates=update_guardians_talk_schedule_dates,
   insert_copy=insert_copied_guardians_talk_schedule,
)

save_guardians_talk_schedule_replacing_overlaps = _resolution.save_replacing_overlaps
save_guardians_talk_schedule_trimming_overlaps = _resolution.save_trimming_overlaps
trim_guardians_talk_schedule_conflict = _resolution.trim_conflict


__all__ = [
   'save_guardians_talk_schedule_replacing_overlaps',
   'save_guardians_talk_schedule_trimming_overlaps',
   'trim_guardians_talk_schedule_conflict',
]
