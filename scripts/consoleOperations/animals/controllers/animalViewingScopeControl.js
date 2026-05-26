import { getAnimalViewingScopes } from '../../../api/animalsApi.js';
import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';

function getFieldValue(fieldEl) {
   return fieldEl?.value.trim() ?? '';
}

function animalHasIndoorAndOutdoorViewing(scopes = []) {
   return (
      scopes.includes(AnimalViewingScope.INDOOR) &&
      scopes.includes(AnimalViewingScope.OUTDOOR)
   );
}

function singleSpecificViewingScope(scopes = []) {
   const specificScopes = scopes.filter(scope => scope !== AnimalViewingScope.ALL);
   return specificScopes.length === 1
      ? specificScopes[0]
      : '';
}

export function createAnimalViewingScopeControl({
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
      const species = getFieldValue(speciesEl);
      const exhibit = getFieldValue(exhibitEl);

      if (!species || !exhibit || !viewingScopeEl) {
         reset();
         return;
      }

      viewingScopeEl.disabled = true;

      try {
         const scopes = await getAnimalViewingScopes({
            species,
            exhibit,
         });

         const canChooseSpecificScope = animalHasIndoorAndOutdoorViewing(scopes);
         viewingScopeEl.disabled = !canChooseSpecificScope;

         if (canChooseSpecificScope) {
            viewingScopeEl.value = AnimalViewingScope.ALL;
            return;
         }

         const availableScope = singleSpecificViewingScope(scopes);

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
