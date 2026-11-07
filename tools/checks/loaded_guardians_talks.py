from __future__ import annotations

from dataclasses import dataclass

from api.guardians.cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.models import GuardiansTalk


@dataclass( frozen=True )
class LoadedGuardiansTalks:
   talks: list[ GuardiansTalk ]
   schedules: list[ GuardiansTalkScheduleRecord ]
   cancellations: list[ GuardiansTalkCancellationInput ]
