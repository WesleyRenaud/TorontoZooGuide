import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityAlertFormController } from '../../forms/entityAlertFormController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AnimalViewingController {
   static createAnimalViewingAlertController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
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
         formFieldEls: [speciesEl, exhibitEl, startDateEl, endDateEl, messageEl],
         activatePanel,
         loadOptions: ConsoleOptionsLoader.loadExhibits,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         targetEl: exhibitEl,
         loadErrorMessage: Strings.loadErrors.exhibits,
         getFormValues: () => ({
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         }),
         validateForm: ({
            species,
            exhibit,
            startDate,
            endDate,
            message,
         }) => {
            if (!species) {
               return Strings.validation.entityRequired(Strings.labels.species);
            }

            if (!exhibit) {
               return Strings.validation.entityRequired(Strings.entityLabels.exhibit);
            }

            if (!message) {
               return Strings.validation.entityRequired(Strings.labels.alertMessage);
            }

            return ControllerHelper.validateOptionalDateRange(startDate, endDate);
         },
         submitAlert: ({
            species,
            exhibit,
            startDate,
            endDate,
            message,
         }) => ConsoleOperationsClient.setAnimalViewingAlert({
            species,
            exhibit,
            alertStartDate: startDate || null,
            alertEndDate: endDate || null,
            message,
         }),
         successMessage: result => Strings.status.animalViewingAlertSaved(result),
         bindResetValueOnChange: {
            sourceEl: exhibitEl,
            targetEl: speciesEl,
         },
      });
   }
}
