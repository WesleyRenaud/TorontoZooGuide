from __future__ import annotations

from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from .guardians_talk_listing import GuardiansTalkListing
from .guardians_talk_occurrences import GuardiansTalkOccurrences


class GuardiansTalkCheck:
   note: str
   website: GuardiansTalkOccurrences
   app: GuardiansTalkOccurrences
   animals: list[ GuardiansTalkAnimalRecord ]
   catalog: set[ GuardiansTalkListing ]


   def __init__(
         self,
         note: str,
         website: GuardiansTalkOccurrences,
         app: GuardiansTalkOccurrences,
         animals: list[ GuardiansTalkAnimalRecord ],
         catalog: set[ GuardiansTalkListing ] ) -> None:
      self.note = note
      self.website = website
      self.app = app
      self.animals = animals
      self.catalog = catalog
