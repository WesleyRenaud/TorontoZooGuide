import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { Position } from '../../../shared/enums/position.js';

export class AnimalExhibitAutofillController {
   static createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits,
      loadExhibitsForSpecies,
      populateExhibits,
      onUniqueFill = null,
   } = {}) {
      if (!speciesEl || !exhibitEl) {
         return {
            applySpecies: async () => {},
         };
      }

      async function restoreExhibits() {
         const exhibits = await loadExhibits();
         populateExhibits?.(exhibitEl, exhibits);
         exhibitEl.value = '';
      }

      async function applySpecies() {
         const species = ControllerHelper.getFieldValue(speciesEl);

         if (!species) {
            try {
               await restoreExhibits();
            }
            catch (err) {
               exhibitEl.value = '';
            }

            return;
         }

         let uniqueFill = false;

         try {
            const exhibits = await loadExhibitsForSpecies(species);
            populateExhibits?.(exhibitEl, exhibits);

            if (exhibits.length === 1) {
               exhibitEl.value = exhibits[Position.FIRST];
               uniqueFill = true;
            }
            else {
               exhibitEl.value = '';
            }
         }
         catch (err) {
            exhibitEl.value = '';
            return;
         }

         if (uniqueFill) {
            await onUniqueFill?.();
         }
      }

      speciesEl.addEventListener('input', () => {
         if (!ControllerHelper.getFieldValue(speciesEl)) {
            applySpecies();
         }
      });
      speciesEl.addEventListener('change', () => applySpecies());

      return {
         applySpecies,
      };
   }
}
