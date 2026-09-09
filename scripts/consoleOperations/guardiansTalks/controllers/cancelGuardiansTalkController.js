import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { CancelOccurrenceControllerFactory } from '../../forms/cancelOccurrenceControllerFactory.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { GuardiansTalkDropdownResetHelper } from '../helpers/guardiansTalkDropdownResetHelper.js';
import { Strings } from '../../../strings.js';

export class CancelGuardiansTalkController {
   static createCancelGuardiansTalkOccurrenceController({
      talkNameEl,
      locationEl,
      dateEl,
      timesEl,
      talkLocationFilterController = null,
      occurrenceFilterController = null,
      ...controllerOptions
   } = {}) {

      function resetOccurrenceFields() {
         occurrenceFilterController?.clear?.();
      }

      function validateSelection({ talk, location, date, times }) {
         if (!location) {
            return Strings.validation.entityRequired(Strings.labels.location);
         }

         if (!talk) {
            return Strings.validation.entityRequired(Strings.labels.talkName);
         }

         if (!date) {
            return Strings.validation.entityRequired(Strings.labels.date);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.talkTimes);
         }

         return null;
      }

      async function prepareForm() {
         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }
      }

      async function submitOccurrenceCancellation({ talk, location, date, times }) {
         return ConsoleOperationsClient.cancelGuardiansTalkOccurrence({
            talk,
            location,
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
            ControllerHelper.resetFormFields([locationEl]);
            GuardiansTalkDropdownResetHelper.resetTalkDropdown({
               talkNameEl,
               talkLocationFilterController,
            });
         },
         getSelectionValues: () => ({
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.locations,
         submitOccurrenceCancellation,
         successMessage: result => Strings.status.guardiansTalkOccurrenceCancelled(result),
      });

      locationEl?.addEventListener('change', () => {
         resetOccurrenceFields();
      });

      talkNameEl?.addEventListener('change', async () => {
         if (occurrenceFilterController?.refresh) {
            await occurrenceFilterController.refresh();
         }
         else {
            resetOccurrenceFields();
         }
      });

      return controller;
   }
}
