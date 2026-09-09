import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AnimalDisplayStatusControllerFactory } from '../../forms/animalDisplayStatusControllerFactory.js';
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
         submitDisplayStatus: ({ species, exhibit, viewingScope }) => (
            ConsoleOperationsClient.setAnimalOnDisplay({
               species,
               exhibit,
               viewingScope,
            })
         ),
         successMessage: result => Strings.status.animalOnDisplay(result),
      });
   }
}
