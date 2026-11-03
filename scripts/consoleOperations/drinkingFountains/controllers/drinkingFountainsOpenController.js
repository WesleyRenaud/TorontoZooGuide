import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { GlobalAmenityStatusFormController } from '../../forms/globalAmenityStatusFormController.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpenController {
   static createDrinkingFountainsOpenController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      activatePanel,
   } = {}) {
      return GlobalAmenityStatusFormController.createGlobalAmenityStatusFormController({
         showButtonEl,
         panelEl,
         submitButtonEl,
         statusEl,
         includeDateRange: false,
         activatePanel,
         submitStatus: () => ConsoleOperationsClient.setDrinkingFountainsOpen({}),
         successMessage: Strings.status.drinkingFountainsOpen,
      });
   }
}
