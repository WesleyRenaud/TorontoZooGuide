import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';

export class WildEncounterScheduleTimesFilter {
   static createWildEncounterScheduleTimesFilterController({
      wildEncounterEl,
      timesEl,
      loadScheduleTimes = async ({ wildEncounter }) => {
         const result = await ConsoleOperationsClient.getWildEncounterScheduleTimes({
            wildEncounter,
         });

         return result?.times ?? [];
      },
   } = {}) {

      function getTimesListEl() {
         return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(timesEl);
      }

      function renderTimesList(times = []) {
         const wildEncounter = ControllerHelper.getFieldValue(wildEncounterEl);

         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(getTimesListEl(), {
            times,
            hasWildEncounter: Boolean(wildEncounter),
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
         const wildEncounter = ControllerHelper.getFieldValue(wildEncounterEl);

         try {
            const scheduleTimes = wildEncounter
               ? await loadScheduleTimes?.({ wildEncounter }) ?? []
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
