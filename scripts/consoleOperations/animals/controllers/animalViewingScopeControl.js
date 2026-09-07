import { AnimalViewingScopeControlHelpers } from './animalViewingScopeControlHelpers.js';
import { AnimalsApi } from '../../../api/animalsApi.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';

export class AnimalViewingScopeControl {
   static createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   } = {}) {
      function reset() {
         if (!viewingScopeEl) {
            return;
         }

         viewingScopeEl.value = '';
         viewingScopeEl.disabled = true;
      }

      async function refresh() {
         const species = ControllerUtils.getFieldValue(speciesEl);
         const exhibit = ControllerUtils.getFieldValue(exhibitEl);

         if (!species || !exhibit || !viewingScopeEl) {
            reset();
            return;
         }

         viewingScopeEl.disabled = true;

         try {
            const scopes = await AnimalsApi.getAnimalViewingScopes({
               species,
               exhibit,
            });

            const canChooseSpecificScope = AnimalViewingScopeControlHelpers.animalHasIndoorAndOutdoorViewing(scopes);
            viewingScopeEl.disabled = !canChooseSpecificScope;

            if (canChooseSpecificScope) {
               viewingScopeEl.value = AnimalViewingScope.ALL;
               return;
            }

            const availableScope = AnimalViewingScopeControlHelpers.singleSpecificViewingScope(scopes);

            if (availableScope) {
               viewingScopeEl.value = availableScope;
            }
            else {
               reset();
            }
         }
         catch(err) {
            reset();
         }
      }

      speciesEl?.addEventListener('input', reset);
      speciesEl?.addEventListener('change', refresh);
      exhibitEl?.addEventListener('change', reset);

      reset();

      return {
         reset,
         refresh,
      };
   }
}
