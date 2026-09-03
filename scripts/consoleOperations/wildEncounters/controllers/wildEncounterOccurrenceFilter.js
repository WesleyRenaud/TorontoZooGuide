import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import {
   resolveScheduleTimesListEl,
   updateScheduleTimesCheckboxList,
} from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';
import { createOccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export function createWildEncounterOccurrenceFilterController({
   wildEncounterEl,
   dateEl,
   timesEl,
} = {}) {

   function getTimesListEl() {
      return resolveScheduleTimesListEl(timesEl);
   }

   function populateTimes(times = []) {
      updateScheduleTimesCheckboxList(getTimesListEl(), {
         times,
         hasWildEncounter: Boolean(getFieldValue(wildEncounterEl)),
         hasDate: Boolean(getFieldValue(dateEl)),
         autoSelectSingleTime: true,
      });
   }

   return createOccurrenceFilterController({
      dateEl,
      populateTimes,
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      isSelectionReady: ({ wildEncounter }) => Boolean(wildEncounter),
      loadOccurrences: async ({ wildEncounter }) => {
         const result = await ConsoleOperationsApi.getWildEncounterOccurrences({
            wildEncounter,
         });

         return result?.occurrences ?? [];
      },
   });
}
