// scripts/pages/itineraryWizard/builder.js
import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';

import { safeParseJSON } from './storage.js';
import { ITIN_KEY } from './keys.js';
import { finalizeItinerary } from './flow.js';

export function openItineraryBuilder({ mountEl, startAt = 'date', onDone } = {}) {
   if (!mountEl) return;

   const existing = safeParseJSON(localStorage.getItem(ITIN_KEY) || '', null) || {};
   let selectedAnimals = Array.isArray(existing.animals) ? existing.animals : [];
   let selectedAttractions = Array.isArray(existing.attractions) ? existing.attractions : [];
   let selectedGuardiansTalks = Array.isArray(existing.guardiansTalks) ? existing.guardiansTalks : [];
   let selectedWildEncounters = Array.isArray(existing.wildEncounters) ? existing.wildEncounters : [];

   const finish = (override = {}) =>
      finalizeItinerary(
         {
            animals: override.animals ?? selectedAnimals,
            attractions: override.attractions ?? selectedAttractions,
            guardiansTalks: override.guardiansTalks ?? selectedGuardiansTalks,
            wildEncounters: override.wildEncounters ?? selectedWildEncounters,
         },
         mountEl,
         { onDone }
      );

   const wildEncounterSelector = createItineraryWildEncounterSelectorController({
      mountEl,
      onPrev: () => guardiansTalkSelector.show(),
      onFinish: (wildEncounters) => {
         selectedWildEncounters = Array.isArray(wildEncounters) ? wildEncounters : [];
         finish({ wildEncounters: selectedWildEncounters });
      },
   });

   const guardiansTalkSelector = createItineraryGuardiansTalkSelectorController({
      mountEl,
      onPrev: () => attractionSelector.show(),
      onNext: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         wildEncounterSelector.show();
      },
      onFinish: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         finish({ guardiansTalks: selectedGuardiansTalks });
      },
   });

   const attractionSelector = createItineraryAttractionSelectorController({
      mountEl,
      onPrev: () => animalSelector.show(),
      onNext: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         guardiansTalkSelector.show();
      },
      onFinish: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         finish({ attractions: selectedAttractions });
      },
   });

   const animalSelector = createItineraryAnimalSelectorController({
      mountEl,
      onPrev: () => dateSelector.show(),
      onNext: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         attractionSelector.show();
      },
      onFinish: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         finish({ animals: selectedAnimals });
      },
   });

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onSave: () => animalSelector.show(),
      onFinish: () => finish(),
   });

   switch (startAt) {
      case 'animals': return animalSelector.show();
      case 'attractions': return attractionSelector.show();
      case 'guardiansTalks': return guardiansTalkSelector.show();
      case 'wildEncounters': return wildEncounterSelector.show();
      case 'date':
      default: return dateSelector.show();
   }
}