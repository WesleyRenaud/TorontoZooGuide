import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { GlobalAmenityStatusFormController } from '../../forms/globalAmenityStatusFormController.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpenController {
   static createDrinkingFountainsOpenController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      activatePanel,
   } = {}) {
      return GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl,
         panelEl,
         submitButtonEl,
         statusEl,
         startDateEl,
         endDateEl,
         activatePanel,
         submitStatus: ({ startDate, endDate }) => ConsoleOperationsClient.setDrinkingFountainsOpen({
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         successMessage: Strings.status.drinkingFountainsOpen,
      });
   }
}
