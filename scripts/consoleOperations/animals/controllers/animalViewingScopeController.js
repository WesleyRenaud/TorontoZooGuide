import { AnimalViewingScopeControlHelper } from './animalViewingScopeControlHelper.js';
import { AnimalsClient } from '../../../api/animalsClient.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';

export class AnimalViewingScopeController {
   static createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      loadViewingScopes = AnimalsClient.getAnimalViewingScopes,
      loadAnimalViewingScopes = loadViewingScopes,
   } = {}) {
      function reset() {
         AnimalViewingScopeControlHelper.clearOptions(viewingScopeEl);
      }

      async function refresh() {
         const species = ControllerHelper.getFieldValue(speciesEl);
         const exhibit = ControllerHelper.getFieldValue(exhibitEl);

         if (!species || !exhibit || !viewingScopeEl) {
            reset();
            return;
         }

         const payload = {
            species,
            exhibit,
         };

         try {
            const scopesPromise = loadViewingScopes(payload);
            const [scopes, animalScopes] = await Promise.all([
               scopesPromise,
               loadAnimalViewingScopes === loadViewingScopes
                  ? scopesPromise
                  : loadAnimalViewingScopes(payload),
            ]);

            AnimalViewingScopeControlHelper.populateOptions(
               viewingScopeEl,
               scopes,
               {
                  optionIdPrefix: viewingScopeEl.id,
                  isFieldVisible: animalScopes.length > 1,
               }
            );
         }
         catch (err) {
            reset();
         }
      }

      function selectedEnclosureNames() {
         return AnimalViewingScopeControlHelper.selectedEnclosureNames(viewingScopeEl);
      }

      speciesEl?.addEventListener('input', reset);
      speciesEl?.addEventListener('change', refresh);
      exhibitEl?.addEventListener('change', refresh);

      reset();

      return {
         reset,
         refresh,
         selectedEnclosureNames,
      };
   }
}
