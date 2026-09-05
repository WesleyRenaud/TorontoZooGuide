import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';

export class GuardiansTalkScheduleTimesFilter {
   static createGuardiansTalkScheduleTimesFilterController({
      talkNameEl,
      locationEl,
      timesEl,
      loadScheduleTimes = async ({ talk, location }) => {
         const result = await ConsoleOperationsApi.getGuardiansTalkScheduleTimes({
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
         return Boolean(getFieldValue(talkNameEl) && getFieldValue(locationEl));
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
                  talk: getFieldValue(talkNameEl),
                  location: getFieldValue(locationEl),
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
