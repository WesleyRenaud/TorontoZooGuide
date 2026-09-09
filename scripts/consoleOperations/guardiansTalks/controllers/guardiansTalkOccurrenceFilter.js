import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
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
            hasSelectedEntity: Boolean(
               ControllerHelper.getFieldValue(talkNameEl) && ControllerHelper.getFieldValue(locationEl)
            ),
            hasDate: Boolean(ControllerHelper.getFieldValue(dateEl)),
            autoSelectSingleTime: true,
         });
      }

      return OccurrenceFilterController.createOccurrenceFilterController({
         dateEl,
         populateTimes,
         getSelectionValues: () => ({
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
         }),
         isSelectionReady: ({ talk, location }) => Boolean(talk && location),
         loadOccurrences: async ({ talk, location }) => {
            const result = await ConsoleOperationsClient.getGuardiansTalkOccurrences({
               talk,
               location,
            });

            return result?.occurrences ?? [];
         },
      });
   }
}
