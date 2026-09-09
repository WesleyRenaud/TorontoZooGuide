import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { CancelOccurrenceControllerFactory } from '../../forms/cancelOccurrenceControllerFactory.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class CancelWildEncounterController {
   static createCancelWildEncounterOccurrenceController({
      wildEncounterEl,
      dateEl,
      timesEl,
      occurrenceFilterController = null,
      ...controllerOptions
   } = {}) {

      function resetOccurrenceFields() {
         occurrenceFilterController?.clear?.();
      }

      function validateSelection({ wildEncounter, date, times }) {
         if (!wildEncounter) {
            return Strings.validation.entityRequired(Strings.entityLabels.wildEncounter);
         }

         if (!date) {
            return Strings.validation.entityRequired(Strings.labels.date);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.encounterTimes);
         }

         return null;
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await ConsoleOptionsLoader.loadWildEncounters();
            ConsoleDropdownPopulator.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }
      }

      async function submitOccurrenceCancellation({ wildEncounter, date, times }) {
         return ConsoleOperationsClient.cancelWildEncounterOccurrence({
            wildEncounter,
            date,
            times,
         });
      }

      const controller = CancelOccurrenceControllerFactory.createCancelOccurrenceController({
         ...controllerOptions,
         dateEl,
         timesEl,
         occurrenceFilterController,
         resetSelection: () => {
            ControllerHelper.resetFormFields([wildEncounterEl]);
         },
         getSelectionValues: () => ({
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.wildEncounters,
         submitOccurrenceCancellation,
         successMessage: result => Strings.status.wildEncounterOccurrenceCancelled(result),
      });

      wildEncounterEl?.addEventListener('change', async () => {
         ControllerHelper.resetFormFields([dateEl]);
         resetOccurrenceFields();

         if (occurrenceFilterController?.refresh) {
            await occurrenceFilterController.refresh();
         }
      });

      return controller;
   }
}
