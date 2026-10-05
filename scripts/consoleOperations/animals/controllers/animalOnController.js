import { AnimalsClient } from '../../../api/animalsClient.js';
import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AnimalDisplayStatusControllerFactory } from '../../forms/animalDisplayStatusControllerFactory.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AnimalOnController {
   static createAnimalOnDisplayController(refs) {
      return AnimalOnController.createController(refs, {
         successMessage: result => Strings.status.animalOnDisplay(result),
         loadExhibits: ConsoleOptionsLoader.loadOffDisplayExhibits,
         loadViewingScopes: ConsoleOptionsLoader.loadOffDisplayViewingScopes,
      });
   }

   static createAnimalOnDisplayForSeasonController(refs) {
      return AnimalOnController.createController(refs, {
         successMessage: result => Strings.status.animalOnDisplayForSeason(result),
         loadExhibits: ConsoleOptionsLoader.loadOffDisplayForSeasonExhibits,
         loadViewingScopes: ConsoleOptionsLoader.loadOffDisplayForSeasonViewingScopes,
      });
   }

   static createController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      activatePanel,
   }, {
      successMessage,
      loadExhibits,
      loadViewingScopes,
   }) {
      return AnimalDisplayStatusControllerFactory.createAnimalDisplayStatusController({
         showButtonEl,
         panelEl,
         cancelButtonEl,
         submitButtonEl,
         statusEl,
         speciesEl,
         exhibitEl,
         viewingScopeEl,
         activatePanel,
         submitDisplayStatus: ({ species, exhibit, viewingScopes }) => (
            ConsoleOperationsClient.setAnimalOnDisplay({
               species,
               exhibit,
               viewingScopes,
            })
         ),
         successMessage,
         loadExhibits,
         loadExhibitsForSpecies: loadExhibits,
         loadViewingScopes,
         loadAnimalViewingScopes: AnimalsClient.getAnimalViewingScopes,
      });
   }
}
