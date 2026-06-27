import { getGuardiansTalkOccurrences } from '../../../api/consoleOperationsApi.js';
import { createOccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export function createGuardiansTalkOccurrenceFilterController({
   talkNameEl,
   locationEl,
   dateEl,
   timeEl,
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   return createOccurrenceFilterController({
      dateEl,
      timeEl,
      autoSelectSingleTime: true,
      getSelectionValues: () => ({
         talk: getFieldValue(talkNameEl),
         location: getFieldValue(locationEl),
      }),
      isSelectionReady: ({ talk, location }) => Boolean(talk && location),
      loadOccurrences: async ({ talk, location }) => {
         const result = await getGuardiansTalkOccurrences({
            talk,
            location,
         });

         return result?.occurrences ?? [];
      },
   });
}
