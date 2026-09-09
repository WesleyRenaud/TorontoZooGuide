import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapResolver } from '../../forms/openingScheduleOverlapResolver.js';
import { RecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { WildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkController {
   static createGuardiansTalkScheduleController({
      talkNameEl,
      locationEl,
      startDateEl,
      endDateEl,
      scheduleRowsEl,
      addScheduleRowEl,
      messageEl,
      talkLocationFilterController = null,
      ...controllerOptions
   } = {}) {
      const scheduleRowsController = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController({
         rowsEl: scheduleRowsEl,
         addRowButtonEl: addScheduleRowEl,
      });


      function resetTalkDropdown() {
         if (talkLocationFilterController?.clear) {
            talkLocationFilterController.clear();
            return;
         }

         if (talkNameEl?.tagName === 'SELECT') {
            ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, []);
         }
         else if (talkNameEl) {
            talkNameEl.value = '';
         }
      }

      function validateSelection({ talk, location }) {
         if (!location) {
            return Strings.validation.entityRequired(Strings.labels.location);
         }

         if (!talk) {
            return Strings.validation.entityRequired(Strings.labels.talkName);
         }

         return null;
      }

      async function submitSchedule({
         talk,
         location,
         startDate,
         endDate,
         message,
      }) {
         const scheduleRows = scheduleRowsController.getRows();
         const payload = {
            talk,
            location,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            scheduleRows,
         };

         const result = await ConsoleOperationsClient.setGuardiansTalkSchedule(payload);

         if (result.success || !OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result)) {
            return result;
         }

         return OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
            payload,
            replaceOverlaps: ConsoleOperationsClient.replaceGuardiansTalkScheduleOverlaps,
            trimOverlaps: ConsoleOperationsClient.trimGuardiansTalkScheduleOverlaps,
            dismissedResult: { success: false, dismissed: true },
         });
      }

      async function prepareForm() {
         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }
      }

      return RecurringScheduleFormController.createRecurringScheduleFormController({
         ...controllerOptions,
         startDateEl,
         endDateEl,
         messageEl,
         resetSelection: () => {
            ControllerHelper.resetFormFields([locationEl, startDateEl, endDateEl, messageEl]);
            resetTalkDropdown();
         },
         resetScheduleTimes: () => {
            scheduleRowsController.reset();
         },
         validateRecurringSchedule: () => scheduleRowsController.validate(),
         getSelectionValues: () => ({
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.locations,
         submitSchedule,
         successMessage: result => Strings.status.guardiansTalkScheduleSaved(result),
         shouldReportSubmitFailure: result => !result?.dismissed,
      });
   }
}
