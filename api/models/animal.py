from __future__ import annotations

from ..zoo_util import ZooUtil


class Animal:
   def __init__(
         self,
         species: str,
         latin_name: str | None = None,
         general_viewing_tips: str | None = None,
         seasonal_viewing_tips: str | None = None,
         identification: str | None = None,
         habitat_and_range: str | None = None,
         diet_and_feeding: str | None = None,
         behaviour_and_life_cycle: str | None = None,
         adaptations: str | None = None,
         reproduction_and_life_cycle: str | None = None,
         animals_at_the_zoo: str | None = None,
         exhibit: str | None = None,
         seasonal_viewing_summary: str | None = None,
         seasonal_viewing_information: str | None = None,
         off_display_message: str | None = None,
         enclosure_type: str | None = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         likelihood: int | None = None,
         has_limited_viewing_schedule: bool | None = None,
         limited_viewing_message: str | None = None,
         has_viewing_alert: bool | None = None,
         viewing_alert_message: str | None = None,
         is_deleted: bool = False,
         old_likelihood: int | None = None ) -> None:
      self.species = species
      self.latin_name = latin_name
      self.general_viewing_tips = general_viewing_tips
      self.seasonal_viewing_tips = seasonal_viewing_tips
      self.identification = identification
      self.habitat_and_range = habitat_and_range
      self.diet_and_feeding = diet_and_feeding
      self.behaviour_and_life_cycle = behaviour_and_life_cycle
      self.adaptations = adaptations
      self.reproduction_and_life_cycle = reproduction_and_life_cycle
      self.animals_at_the_zoo = animals_at_the_zoo
      self.exhibit = exhibit
      self.seasonal_viewing_summary = seasonal_viewing_summary
      self.seasonal_viewing_information = seasonal_viewing_information
      self.off_display_message = off_display_message
      self.enclosure_type = enclosure_type
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.likelihood = likelihood
      self.has_limited_viewing_schedule = has_limited_viewing_schedule
      self.limited_viewing_message = limited_viewing_message
      self.has_viewing_alert = has_viewing_alert
      self.viewing_alert_message = viewing_alert_message
      self.is_deleted = is_deleted
      self.old_likelihood = old_likelihood


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'species': self.species,
         'latin_name': self.latin_name,
         'general_viewing_tips': self.general_viewing_tips,
         'seasonal_viewing_tips': self.seasonal_viewing_tips,
         'identification': self.identification,
         'habitat_and_range': self.habitat_and_range,
         'diet_and_feeding': self.diet_and_feeding,
         'behaviour_and_life_cycle': self.behaviour_and_life_cycle,
         'adaptations': self.adaptations,
         'reproduction_and_life_cycle': self.reproduction_and_life_cycle,
         'animals_at_the_zoo': self.animals_at_the_zoo,
         'exhibit': self.exhibit,
         'seasonal_viewing_summary': self.seasonal_viewing_summary,
         'seasonal_viewing_information': self.seasonal_viewing_information,
         'off_display_message': self.off_display_message,
         'enclosure_type': self.enclosure_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'likelihood': self.likelihood,
         'has_limited_viewing_schedule': ZooUtil.as_boolean( self.has_limited_viewing_schedule ),
         'limited_viewing_message': self.limited_viewing_message,
         'has_viewing_alert': ZooUtil.as_boolean( self.has_viewing_alert ),
         'viewing_alert_message': self.viewing_alert_message,
         'is_deleted': ZooUtil.as_boolean( self.is_deleted ),
         'old_likelihood': self.old_likelihood
      }
