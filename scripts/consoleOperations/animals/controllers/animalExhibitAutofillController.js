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

      async function applySpecies() {
         const species = ControllerHelper.getFieldValue(speciesEl);
         const selectedExhibit = ControllerHelper.getFieldValue(exhibitEl);
         let exhibits;

         try {
            exhibits = species
               ? await loadExhibitsForSpecies(species)
               : await loadExhibits();
         }
         catch (err) {
            return;
         }

         populateExhibits?.(exhibitEl, exhibits);
         exhibitEl.value = selectedExhibit;

         if (!selectedExhibit && species && exhibits.length === 1) {
            exhibitEl.value = exhibits[Position.FIRST];
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
