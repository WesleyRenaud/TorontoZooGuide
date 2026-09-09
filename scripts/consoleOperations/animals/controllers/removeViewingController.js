import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityRemovalFormController } from '../../forms/entityRemovalFormController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RemoveViewingController {
   static createRemoveViewingAlertController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      activatePanel,
   } = {}) {
      return EntityRemovalFormController.createEntityRemovalFormController({
         showButtonEl,
         panelEl,
         cancelButtonEl,
         submitButtonEl,
         statusEl,
         formFieldEls: [speciesEl, exhibitEl],
         activatePanel,
         loadOptions: ConsoleOptionsLoader.loadExhibits,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         targetEl: exhibitEl,
         loadErrorMessage: Strings.loadErrors.exhibits,
         getFormValues: () => ({
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
         }),
         validateForm: ({ species, exhibit }) => {
            if (!species) {
               return Strings.validation.entityRequired(Strings.labels.species);
            }

            if (!exhibit) {
               return Strings.validation.entityRequired(Strings.entityLabels.exhibit);
            }

            return null;
         },
         submitRemoval: ({ species, exhibit }) => ConsoleOperationsClient.removeAnimalViewingAlert({
            species,
            exhibit,
         }),
         successMessage: result => Strings.status.animalViewingAlertRemoved(result),
         bindResetValueOnChange: {
            sourceEl: exhibitEl,
            targetEl: speciesEl,
         },
      });
   }
}
