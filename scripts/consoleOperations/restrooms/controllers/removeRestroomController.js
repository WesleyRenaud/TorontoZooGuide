import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityRemovalFormController } from '../../forms/entityRemovalFormController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RemoveRestroomController {
   static createRemoveRestroomAlertController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      restroomEl,
      activatePanel,
   } = {}) {
      return EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl,
         panelEl,
         cancelButtonEl,
         submitButtonEl,
         statusEl,
         formFieldEls: [restroomEl],
         activatePanel,
         loadOptions: ConsoleOptionsLoader.loadRestrooms,
         populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
         targetEl: restroomEl,
         loadErrorMessage: Strings.loadErrors.restrooms,
         getFormValues: () => ({
            restroom: ControllerHelper.getFieldValue(restroomEl),
         }),
         validateForm: ({ restroom }) => {
            if (!restroom) {
               return Strings.validation.entityRequired(Strings.entityLabels.restroom);
            }

            return null;
         },
         submitRemoval: ({ restroom }) => ConsoleOperationsClient.removeRestroomAlert({ restroom }),
         successMessage: result => Strings.status.restroomAlertRemoved(result),
      });
   }
}
