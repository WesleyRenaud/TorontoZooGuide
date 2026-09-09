import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityAlertFormController } from '../../forms/entityAlertFormController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestroomController {
   static createRestroomAlertController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      restroomEl,
      startDateEl,
      endDateEl,
      messageEl,
      activatePanel,
   } = {}) {
      return EntityAlertFormController.createEntityAlertFormController({
         showButtonEl,
         panelEl,
         cancelButtonEl,
         submitButtonEl,
         statusEl,
         formFieldEls: [restroomEl, startDateEl, endDateEl, messageEl],
         activatePanel,
         loadOptions: ConsoleOptionsLoader.loadRestrooms,
         populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
         targetEl: restroomEl,
         loadErrorMessage: Strings.loadErrors.restrooms,
         getFormValues: () => ({
            restroom: ControllerHelper.getFieldValue(restroomEl),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         }),
         validateForm: ({
            restroom,
            startDate,
            endDate,
            message,
         }) => {
            if (!restroom) {
               return Strings.validation.entityRequired(Strings.entityLabels.restroom);
            }

            if (!message) {
               return Strings.validation.entityRequired(Strings.labels.alertMessage);
            }

            return ControllerHelper.validateOptionalDateRange(startDate, endDate);
         },
         submitAlert: ({
            restroom,
            startDate,
            endDate,
            message,
         }) => ConsoleOperationsClient.setRestroomAlert({
            restroom,
            alertStartDate: startDate || null,
            alertEndDate: endDate || null,
            message,
         }),
         successMessage: result => Strings.status.restroomAlertSaved(result),
      });
   }
}
