from __future__ import annotations

from datetime import date

from api.wild_encounters.data_access.wild_encounter_record import WildEncounterRecord
from api.wild_encounters.domain.wild_encounter_link import WildEncounterLink
from api.wild_encounters.domain.wild_encounter_schedule import WildEncounterSchedule
from .encounter_schedule_slots import EncounterScheduleSlots
from .encounter_website_images import EncounterWebsiteImages


class WildEncounterCheck:
   note: str
   records: list[ WildEncounterRecord ]
   encounters: list[ WildEncounterLink ]
   schedules: list[ WildEncounterSchedule ]
   website_slots: EncounterScheduleSlots
   images: EncounterWebsiteImages
   app_names: set[ str ]
   website_names: set[ str ]
   first: date


   def __init__(
         self,
         note: str,
         records: list[ WildEncounterRecord ],
         encounters: list[ WildEncounterLink ],
         schedules: list[ WildEncounterSchedule ],
         website_slots: EncounterScheduleSlots,
         images: EncounterWebsiteImages,
         app_names: set[ str ],
         website_names: set[ str ],
         first: date ) -> None:
      self.note = note
      self.records = records
      self.encounters = encounters
      self.schedules = schedules
      self.website_slots = website_slots
      self.images = images
      self.app_names = app_names
      self.website_names = website_names
      self.first = first
