import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
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
               ControllerUtils.getFieldValue(talkNameEl) && ControllerUtils.getFieldValue(locationEl)
            ),
            hasDate: Boolean(ControllerUtils.getFieldValue(dateEl)),
            autoSelectSingleTime: true,
         });
      }

      return OccurrenceFilterController.createOccurrenceFilterController({
         dateEl,
         populateTimes,
         getSelectionValues: () => ({
            talk: ControllerUtils.getFieldValue(talkNameEl),
            location: ControllerUtils.getFieldValue(locationEl),
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
