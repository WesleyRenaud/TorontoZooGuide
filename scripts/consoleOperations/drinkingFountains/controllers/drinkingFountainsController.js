import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { GlobalAmenityStatusFormController } from '../../forms/globalAmenityStatusFormController.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsController {
   static createDrinkingFountainsClosedController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      messageEl,
      activatePanel,
   } = {}) {
      return GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl,
         panelEl,
         submitButtonEl,
         statusEl,
         startDateEl,
         endDateEl,
         messageEl,
         activatePanel,
         submitStatus: ({ startDate, endDate, message }) => ConsoleOperationsClient.setDrinkingFountainsClosed({
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         successMessage: Strings.status.drinkingFountainsClosed,
      });
   }
}
