import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';

export class AnimalViewingScopeControlHelper {
   static animalHasIndoorAndOutdoorViewing(scopes = []) {
      return (
         scopes.includes(AnimalViewingScope.INDOOR) &&
         scopes.includes(AnimalViewingScope.OUTDOOR)
      );
   }

   static singleSpecificViewingScope(scopes = []) {
      const specificScopes = scopes.filter(scope => scope !== AnimalViewingScope.ALL);
      return specificScopes.length === 1
         ? specificScopes[0]
         : '';
   }
}
