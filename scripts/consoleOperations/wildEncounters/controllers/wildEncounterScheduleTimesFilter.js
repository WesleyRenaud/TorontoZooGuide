import { getWildEncounterScheduleTimes } from '../../../api/consoleOperationsApi.js';
import {
   resolveScheduleTimesListEl,
   updateScheduleTimesCheckboxList,
} from '../../forms/scheduleTimesCheckboxField.js';

export function createWildEncounterScheduleTimesFilterController({
   wildEncounterEl,
   timesEl,
   loadScheduleTimes = async ({ wildEncounter }) => {
      const result = await getWildEncounterScheduleTimes({
         wildEncounter,
      });

      return result?.times ?? [];
   },
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getTimesListEl() {
      return resolveScheduleTimesListEl(timesEl);
   }

   function renderTimesList(times = []) {
      const wildEncounter = getFieldValue(wildEncounterEl);

      updateScheduleTimesCheckboxList(getTimesListEl(), {
         times,
         hasWildEncounter: Boolean(wildEncounter),
         hasDate: true,
      });
   }

   function clear() {
      updateScheduleTimesCheckboxList(getTimesListEl(), {
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
