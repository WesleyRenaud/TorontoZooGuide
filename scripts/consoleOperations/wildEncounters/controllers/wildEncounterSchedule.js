import {
   replaceWildEncounterScheduleOverlaps,
   setWildEncounterSchedule,
   trimWildEncounterScheduleOverlaps,
} from '../../../api/consoleOperationsApi.js';
import {
   OPENING_SCHEDULE_OVERLAP_RESOLUTION,
   resultHasOpeningScheduleOverlap,
} from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { createRecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { createWildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { loadWildEncounters } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createWildEncounterScheduleController({
   wildEncounterEl,
   startDateEl,
   endDateEl,
   scheduleRowsEl,
   addScheduleRowEl,
   messageEl,
   ...controllerOptions
} = {}) {
   const scheduleRowsController = createWildEncounterScheduleRowsController({
      rowsEl: scheduleRowsEl,
      addRowButtonEl: addScheduleRowEl,
   });

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function validateSelection({
      wildEncounter,
   }) {
      if (!wildEncounter) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
      }

      return null;
   }

   async function submitSchedule({
      wildEncounter,
      startDate,
      endDate,
      message,
   }) {
      const scheduleRows = scheduleRowsController.getRows();
      const payload = {
         wildEncounter,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
         scheduleRows,
      };

      const result = await setWildEncounterSchedule(payload);

      if (result.success || !resultHasOpeningScheduleOverlap(result)) {
         return result;
      }

      const resolution = await showOpeningScheduleOverlapDialog();

      if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
         return replaceWildEncounterScheduleOverlaps(payload);
      }

      if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
         return trimWildEncounterScheduleOverlaps(payload);
      }

      return { success: false, dismissed: true };
   }

   async function prepareForm() {
      if (wildEncounterEl?.tagName === 'SELECT') {
         const wildEncounters = await loadWildEncounters();
         populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
      }
   }

   return createRecurringScheduleFormController({
      ...controllerOptions,
      startDateEl,
      endDateEl,
      messageEl,
      resetSelection: () => {
         resetFormFields([wildEncounterEl, startDateEl, endDateEl, messageEl]);
      },
      resetScheduleTimes: () => {
         scheduleRowsController.reset();
      },
      validateRecurringSchedule: () => scheduleRowsController.validate(),
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.wildEncounters,
      submitSchedule,
      successMessage: result => APP_STRINGS.status.scheduleSaved(result.wildEncounter),
      shouldReportSubmitFailure: result => !result?.dismissed,
   });
}
