import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
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
            hasWildEncounter: Boolean(ControllerHelper.getFieldValue(wildEncounterEl)),
            hasDate: Boolean(ControllerHelper.getFieldValue(dateEl)),
            autoSelectSingleTime: true,
         });
      }

      return OccurrenceFilterController.createOccurrenceFilterController({
         dateEl,
         populateTimes,
         getSelectionValues: () => ({
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
         }),
         isSelectionReady: ({ wildEncounter }) => Boolean(wildEncounter),
         loadOccurrences: async ({ wildEncounter }) => {
            const result = await ConsoleOperationsClient.getWildEncounterOccurrences({
               wildEncounter,
            });

            return result?.occurrences ?? [];
         },
      });
   }
}
