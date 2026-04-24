import { loadExhibits } from '../../options/loaders.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { setExhibitOpen } from '../../../api/consoleOperationsApi.js';
import { createEntityOpenFormController } from '../../forms/entityOpenFormController.js';

export function createExhibitOpenController({
   exhibitEl,
   ...controllerOptions
} = {}) {
   return createEntityOpenFormController({
      ...controllerOptions,
      entityEl: exhibitEl,
      loadOptions: loadExhibits,
      populateOptions: populateExhibitDropdown,
      submitOpenStatus: ({ entity, startDate, endDate }) => setExhibitOpen({
         exhibit: entity,
         startDate: startDate || null,
         endDate: endDate || null,
      }),
      entityLabel: 'Exhibit',
      optionsLabel: 'exhibits',
      successMessage: result => `${result.exhibit} was set as explicitly open.`,
   });
}
