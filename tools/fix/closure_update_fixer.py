from __future__ import annotations

from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.text_values import TextValues
from api.updates.coordinators.update_coordinator import UpdateCoordinator
from api.updates.domain.update_type import UpdateType
from tools.checks.check_report import CheckReport
from tools.checks.closure_update import ClosureUpdate
from tools.checks.closure_update_plan import ClosureUpdatePlan


class ClosureUpdateFixer():
   @classmethod
   def mentions( cls, addition: ClosureUpdate, names: list[ str ] ) -> bool:
      text = TextValues.beside( addition.title, addition.description ).casefold()
      return any( name.casefold() in text for name in names )


   @classmethod
   def successor(
         cls,
         ending: ClosureUpdate,
         additions: list[ ClosureUpdate ],
         animals: list[ ClosureLinkedOffDisplayAnimal ] ) -> ClosureUpdate | None:
      names = [
         animal.species
         for animal in animals
         if (
            animal.closure_update_title == ending.title
            and animal.closure_update_start == ending.start
         )
      ]
      matches = [
         addition
         for addition in additions
         if cls.mentions( addition, names )
      ]

      if len( matches ) == 1:
         return matches[ 0 ]

      return None


   @classmethod
   def add( cls, additions: list[ ClosureUpdate ] ) -> list[ ClosureUpdate ]:
      revised = []

      for addition in additions:
         created = UpdateCoordinator.create_update(
            title=addition.title,
            description=addition.description,
            update_type=UpdateType.CLOSURE.value,
            start_date=addition.start,
            end_date=addition.end,
         )

         if created:
            continue

         UpdateCoordinator.edit_update(
            title=addition.title,
            start_date=addition.start,
            description=addition.description,
            update_type=UpdateType.CLOSURE.value,
            end_date=addition.end,
         )
         revised.append( addition )

      return revised


   @classmethod
   def already_revised(
         cls,
         ending: ClosureUpdate,
         revised: list[ ClosureUpdate ] ) -> bool:
      for update in revised:
         if update.title == ending.title and update.start == ending.start:
            return True

      return False


   @classmethod
   def retire(
         cls,
         endings: list[ ClosureUpdate ],
         additions: list[ ClosureUpdate ],
         revised: list[ ClosureUpdate ],
         animals: list[ ClosureLinkedOffDisplayAnimal ] ) -> None:
      for ending in endings:
         if cls.already_revised( ending, revised ):
            continue

         successor = cls.successor( ending, additions, animals )

         if successor != None:
            AnimalCoordinator.move_closure_update(
               ending.title,
               ending.start,
               successor.title,
               successor.start,
            )

         UpdateCoordinator.end_update(
            title=ending.title,
            start_date=ending.start,
            end_date=ending.end,
         )


   @classmethod
   def extend( cls, extensions: list[ ClosureUpdate ] ) -> None:
      for extension in extensions:
         UpdateCoordinator.end_update(
            title=extension.title,
            start_date=extension.start,
            end_date=extension.end,
         )


   @classmethod
   def apply( cls, database: Path, plan: ClosureUpdatePlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         revised = cls.add( plan.added )
         animals = AnimalCoordinator.get_closure_linked_off_display_animals()
         cls.retire( plan.ended, plan.added, revised, animals )
         cls.extend( plan.extended )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( plan.count() )
