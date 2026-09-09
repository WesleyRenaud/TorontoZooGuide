import animalViewingScopeValues from '../../../shared/enums/animalViewingScope.json' with { type: 'json' };

export class AnimalViewingScope {
   static {
      Object.assign(AnimalViewingScope, animalViewingScopeValues);
   }

   static wireValues() {
      return Object.values(animalViewingScopeValues);
   }
}
