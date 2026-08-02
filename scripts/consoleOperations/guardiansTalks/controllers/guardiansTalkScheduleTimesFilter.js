import { getGuardiansTalkScheduleTimes } from '../../../api/consoleOperationsApi.js';
import {
   resolveScheduleTimesListEl,
   updateScheduleTimesCheckboxList,
} from '../../forms/scheduleTimesCheckboxField.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';

export function createGuardiansTalkScheduleTimesFilterController({
   talkNameEl,
   locationEl,
   timesEl,
   loadScheduleTimes = async ({ talk, location }) => {
      const result = await getGuardiansTalkScheduleTimes({
         talk,
         location,
      });

      return result?.times ?? [];
   },
} = {}) {

   function getTimesListEl() {
      return resolveScheduleTimesListEl(timesEl);
   }

   function hasSelection() {
      return Boolean(getFieldValue(talkNameEl) && getFieldValue(locationEl));
   }

   function renderTimesList(times = []) {
      updateScheduleTimesCheckboxList(getTimesListEl(), {
         times,
         hasWildEncounter: hasSelection(),
         hasDate: true,
         autoSelectSingleTime: true,
      });
   }

   function clear() {
      updateScheduleTimesCheckboxList(getTimesListEl(), {
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
