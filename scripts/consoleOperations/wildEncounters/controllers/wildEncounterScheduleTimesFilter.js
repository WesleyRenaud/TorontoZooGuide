import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';

export function createWildEncounterScheduleTimesFilterController({
   wildEncounterEl,
   timesEl,
   loadScheduleTimes = async ({ wildEncounter }) => {
      const result = await ConsoleOperationsApi.getWildEncounterScheduleTimes({
         wildEncounter,
      });

      return result?.times ?? [];
   },
} = {}) {

   function getTimesListEl() {
      return ScheduleTimesCheckboxField.resolveScheduleTimesListEl(timesEl);
   }

   function renderTimesList(times = []) {
      const wildEncounter = getFieldValue(wildEncounterEl);

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
      const wildEncounter = getFieldValue(wildEncounterEl);

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
