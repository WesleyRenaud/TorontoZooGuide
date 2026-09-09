import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { RecurringScheduleSetControllerFactory } from '../../forms/recurringScheduleSetControllerFactory.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class WildEncounterController {
   static createWildEncounterScheduleController({
      wildEncounterEl,
      startDateEl,
      endDateEl,
      scheduleRowsEl,
      addScheduleRowEl,
      messageEl,
      ...controllerOptions
   } = {}) {
      return RecurringScheduleSetControllerFactory.createRecurringScheduleSetController({
         ...controllerOptions,
         scheduleRowsEl,
         addScheduleRowEl,
         startDateEl,
         endDateEl,
         messageEl,
         getSelectionValues: () => ({
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
         }),
         validateSelection: ({ wildEncounter }) => {
            if (!wildEncounter) {
               return Strings.validation.entityRequired(Strings.entityLabels.wildEncounter);
            }

            return null;
         },
         resetSelection: () => {
            ControllerHelper.resetFormFields([wildEncounterEl, startDateEl, endDateEl, messageEl]);
         },
         prepareForm: async () => {
            if (wildEncounterEl?.tagName === 'SELECT') {
               const wildEncounters = await ConsoleOptionsLoader.loadWildEncounters();
               ConsoleDropdownPopulator.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
            }
         },
         loadErrorMessage: Strings.loadErrors.wildEncounters,
         successMessage: result => Strings.status.scheduleSaved(result.wildEncounter),
         setSchedule: payload => ConsoleOperationsClient.setWildEncounterSchedule(payload),
         replaceOverlaps: payload => ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps(payload),
         trimOverlaps: payload => ConsoleOperationsClient.trimWildEncounterScheduleOverlaps(payload),
      });
   }
}
