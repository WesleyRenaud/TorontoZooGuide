import { loadExhibits } from '../../options/loaders.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { setExhibitClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

export function createExhibitClosedController({
   exhibitEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: exhibitEl,
      loadOptions: loadExhibits,
      populateOptions: populateExhibitDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setExhibitClosed({
         exhibit: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: 'Exhibit',
      optionsLabel: 'exhibits',
      successMessage: result => `${result.exhibit} was set as closed.`,
   });
}
