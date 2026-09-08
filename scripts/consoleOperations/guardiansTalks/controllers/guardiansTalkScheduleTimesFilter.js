import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';

export class GuardiansTalkScheduleTimesFilter {
   static createGuardiansTalkScheduleTimesFilterController({
      talkNameEl,
      locationEl,
      timesEl,
      loadScheduleTimes = async ({ talk, location }) => {
         const result = await ConsoleOperationsClient.getGuardiansTalkScheduleTimes({
            talk,
            location,
         });

         return result?.times ?? [];
      },
   } = {}) {

      function getTimesListEl() {
         return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(timesEl);
      }

      function hasSelection() {
         return Boolean(ControllerHelper.getFieldValue(talkNameEl) && ControllerHelper.getFieldValue(locationEl));
      }

      function renderTimesList(times = []) {
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(getTimesListEl(), {
            times,
            hasWildEncounter: hasSelection(),
            hasDate: true,
            autoSelectSingleTime: true,
         });
      }

      function clear() {
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(getTimesListEl(), {
            times: [],
            hasWildEncounter: false,
         });
      }

      async function refresh() {
         try {
            const scheduleTimes = hasSelection()
               ? await loadScheduleTimes?.({
                  talk: ControllerHelper.getFieldValue(talkNameEl),
                  location: ControllerHelper.getFieldValue(locationEl),
               }) ?? []
               : [];

            renderTimesList(scheduleTimes);
         }
         catch (err) {
            renderTimesList([]);
         }
      }

      return {
         refresh,
         clear,
      };
   }
}
