import { getWildEncounterOccurrences } from '../../../api/consoleOperationsApi.js';
import { createOccurrenceFilterController } from '../../helpers/occurrenceFilterController.js';

export function createWildEncounterOccurrenceFilterController({
   wildEncounterEl,
   dateEl,
   timeEl,
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   return createOccurrenceFilterController({
      dateEl,
      timeEl,
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      isSelectionReady: ({ wildEncounter }) => Boolean(wildEncounter),
      loadOccurrences: async ({ wildEncounter }) => {
         const result = await getWildEncounterOccurrences({
            wildEncounter,
         });

         return result?.occurrences ?? [];
      },
   });
}
