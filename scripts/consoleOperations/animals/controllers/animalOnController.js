import { AnimalsClient } from '../../../api/animalsClient.js';
import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AnimalDisplayStatusControllerFactory } from '../../forms/animalDisplayStatusControllerFactory.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AnimalOnController {
   static createAnimalOnDisplayController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      activatePanel,
   } = {}) {
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
         successMessage: result => Strings.status.animalOnDisplay(result),
         loadExhibits: ConsoleOptionsLoader.loadOffDisplayExhibits,
         loadExhibitsForSpecies: ConsoleOptionsLoader.loadOffDisplayExhibits,
         loadViewingScopes: ConsoleOptionsLoader.loadOffDisplayViewingScopes,
         loadAnimalViewingScopes: AnimalsClient.getAnimalViewingScopes,
      });
   }
}
