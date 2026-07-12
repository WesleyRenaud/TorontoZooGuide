import {
   replaceGuardiansTalkScheduleOverlaps,
   setGuardiansTalkSchedule,
   trimGuardiansTalkScheduleOverlaps,
} from '../../../api/consoleOperationsApi.js';
import {
   OPENING_SCHEDULE_OVERLAP_RESOLUTION,
   resultHasOpeningScheduleOverlap,
} from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { createRecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { createWildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { populateGuardiansTalkDropdown } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export function createGuardiansTalkScheduleController({
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
   const scheduleRowsController = createWildEncounterScheduleRowsController({
      rowsEl: scheduleRowsEl,
      addRowButtonEl: addScheduleRowEl,
   });

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetTalkDropdown() {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
         return;
      }

      if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }

   function validateSelection({ talk, location }) {
      if (!location) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
      }

      if (!talk) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
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

      const result = await setGuardiansTalkSchedule(payload);

      if (result.success || !resultHasOpeningScheduleOverlap(result)) {
         return result;
      }

      const resolution = await showOpeningScheduleOverlapDialog();

      if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
         return replaceGuardiansTalkScheduleOverlaps(payload);
      }

      if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
         return trimGuardiansTalkScheduleOverlaps(payload);
      }

      return { success: false, dismissed: true };
   }

   async function prepareForm() {
      if (talkLocationFilterController?.refreshLocations) {
         await talkLocationFilterController.refreshLocations();
      }
   }

   return createRecurringScheduleFormController({
      ...controllerOptions,
      startDateEl,
      endDateEl,
      messageEl,
      resetSelection: () => {
         resetFormFields([locationEl, startDateEl, endDateEl, messageEl]);
         resetTalkDropdown();
      },
      resetScheduleTimes: () => {
         scheduleRowsController.reset();
      },
      validateRecurringSchedule: () => scheduleRowsController.validate(),
      getSelectionValues: () => ({
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.locations,
      submitSchedule,
      successMessage: result => APP_STRINGS.status.guardiansTalkScheduleSaved(result),
      shouldReportSubmitFailure: result => !result?.dismissed,
   });
}
