import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';
import { OccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export class GuardiansTalkOccurrenceFilter {
   static createGuardiansTalkOccurrenceFilterController({
      talkNameEl,
      locationEl,
      dateEl,
      timesEl,
   } = {}) {

      function getTimesListEl() {
         return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(timesEl);
      }

      function populateTimes(times = []) {
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(getTimesListEl(), {
            times,
            hasWildEncounter: Boolean(
               getFieldValue(talkNameEl) && getFieldValue(locationEl)
            ),
            hasDate: Boolean(getFieldValue(dateEl)),
            autoSelectSingleTime: true,
         });
      }

      return OccurrenceFilterController.createOccurrenceFilterController({
         dateEl,
         populateTimes,
         getSelectionValues: () => ({
            talk: getFieldValue(talkNameEl),
            location: getFieldValue(locationEl),
         }),
         isSelectionReady: ({ talk, location }) => Boolean(talk && location),
         loadOccurrences: async ({ talk, location }) => {
            const result = await ConsoleOperationsApi.getGuardiansTalkOccurrences({
               talk,
               location,
            });

            return result?.occurrences ?? [];
         },
      });
   }
}
