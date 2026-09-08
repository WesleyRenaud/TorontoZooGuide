import { AnimalViewingScopeControlHelper } from './animalViewingScopeControlHelper.js';
import { AnimalsClient } from '../../../api/animalsClient.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';

export class AnimalViewingScopeController {
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
         const species = ControllerHelper.getFieldValue(speciesEl);
         const exhibit = ControllerHelper.getFieldValue(exhibitEl);

         if (!species || !exhibit || !viewingScopeEl) {
            reset();
            return;
         }

         viewingScopeEl.disabled = true;

         try {
            const scopes = await AnimalsClient.getAnimalViewingScopes({
               species,
               exhibit,
            });

            const canChooseSpecificScope = AnimalViewingScopeControlHelper.animalHasIndoorAndOutdoorViewing(scopes);
            viewingScopeEl.disabled = !canChooseSpecificScope;

            if (canChooseSpecificScope) {
               viewingScopeEl.value = AnimalViewingScope.ALL;
               return;
            }

            const availableScope = AnimalViewingScopeControlHelper.singleSpecificViewingScope(scopes);

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
