from __future__ import annotations

from enum import Enum


class MapLocationKind( str, Enum ):
   WILD_ENCOUNTER_MEETING_SPOT = 'wild_encounter_meeting_spot'
   GUARDIANS_TALK = 'guardians_talk'
   ATTRACTION = 'attraction'
