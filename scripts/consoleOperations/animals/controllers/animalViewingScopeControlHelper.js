import { AnimalViewingModel } from '../../../shared/enums/animalViewingModel.js';

export class AnimalViewingScopeControlHelper {
   static animalHasIndoorAndOutdoorViewing(scopes = []) {
      return (
         scopes.includes(AnimalViewingModel.INDOOR) &&
         scopes.includes(AnimalViewingModel.OUTDOOR)
      );
   }

   static singleSpecificViewingScope(scopes = []) {
      const specificScopes = scopes.filter(scope => scope !== AnimalViewingModel.ALL);
      return specificScopes.length === 1
         ? specificScopes[0]
         : '';
   }
}
