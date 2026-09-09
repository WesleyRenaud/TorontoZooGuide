import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AnimalDisplayStatusControllerFactory } from '../../forms/animalDisplayStatusControllerFactory.js';
import { Strings } from '../../../strings.js';

export class AnimalOffController {
   static createAnimalOffDisplayController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      startDateEl,
      endDateEl,
      messageEl,
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
         startDateEl,
         endDateEl,
         messageEl,
         activatePanel,
         submitDisplayStatus: ({
            species,
            exhibit,
            startDate,
            endDate,
            message,
            viewingScope,
         }) => ConsoleOperationsClient.setAnimalOffDisplay({
            species,
            exhibit,
            viewingScope,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         successMessage: result => Strings.status.animalOffDisplay(result),
      });
   }
}
