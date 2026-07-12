import { getGuardiansTalkOccurrences } from '../../../api/consoleOperationsApi.js';
import {
   resolveScheduleTimesListEl,
   updateScheduleTimesCheckboxList,
} from '../../forms/scheduleTimesCheckboxField.js';
import { createOccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export function createGuardiansTalkOccurrenceFilterController({
   talkNameEl,
   locationEl,
   dateEl,
   timesEl,
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getTimesListEl() {
      return resolveScheduleTimesListEl(timesEl);
   }

   function populateTimes(times = []) {
      updateScheduleTimesCheckboxList(getTimesListEl(), {
         times,
         hasWildEncounter: Boolean(
            getFieldValue(talkNameEl) && getFieldValue(locationEl)
         ),
         hasDate: Boolean(getFieldValue(dateEl)),
         autoSelectSingleTime: true,
      });
   }

   return createOccurrenceFilterController({
      dateEl,
      populateTimes,
      getSelectionValues: () => ({
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
      }),
      isSelectionReady: ({ talk, location }) => Boolean(talk && location),
      loadOccurrences: async ({ talk, location }) => {
         const result = await getGuardiansTalkOccurrences({
            talk,
            location,
         });

         return result?.occurrences ?? [];
      },
   });
}
