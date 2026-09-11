import { ItineraryServiceSaver } from '../itineraryServiceSaver.js';
import { ItineraryShape } from '../itineraryShape.js';
import { RegionStorageStore } from '../selectors/regionSelector/regionStorageStore.js';
import { StorageKeys } from '../storageKeys.js';

export class WizardFinalizerHelper {
   static clearWizardMount(mountEl) {
      mountEl?.replaceChildren();
   }

   static createFinalItineraryDraft(draft = {}, normalizeDraft = ItineraryShape.normalizeItineraryDraft) {
      return normalizeDraft(draft);
   }

   static saveFinalItinerary(
      finalItinerary,
      { overridingConflictingGuardiansTalks = false } = {},
      saveItineraryFn = ItineraryServiceSaver.saveItinerary,
   ) {
      return saveItineraryFn(finalItinerary, {
         overridingConflictingGuardiansTalks,
         selectedExhibits: RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      });
   }
}
