import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';
import { OccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export class WildEncounterOccurrenceFilter {
   static createWildEncounterOccurrenceFilterController({
      wildEncounterEl,
      dateEl,
      timesEl,
   } = {}) {

      function getTimesListEl() {
         return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(timesEl);
      }

      function populateTimes(times = []) {
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(getTimesListEl(), {
            times,
            hasWildEncounter: Boolean(getFieldValue(wildEncounterEl)),
            hasDate: Boolean(getFieldValue(dateEl)),
            autoSelectSingleTime: true,
         });
      }

      return OccurrenceFilterController.createOccurrenceFilterController({
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
}
