import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AnimalDisplayStatusControllerFactory } from '../../forms/animalDisplayStatusControllerFactory.js';
import { Strings } from '../../../strings.js';

export class AnimalOffController {
   static createAnimalOffDisplayController(refs) {
      return AnimalOffController.createController(refs, {
         isOffDisplayForSeason: false,
         successMessage: result => Strings.status.animalOffDisplay(result),
      });
   }

   static createAnimalOffDisplayForSeasonController(refs) {
      return AnimalOffController.createController(refs, {
         isOffDisplayForSeason: true,
         successMessage: result => Strings.status.animalOffDisplayForSeason(result),
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
      startDateEl,
      endDateEl,
      messageEl,
      activatePanel,
   }, {
      isOffDisplayForSeason,
      successMessage,
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
            viewingScopes,
         }) => ConsoleOperationsClient.setAnimalOffDisplay({
            species,
            exhibit,
            viewingScopes,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            isOffDisplayForSeason,
         }),
         successMessage,
      });
   }
}
