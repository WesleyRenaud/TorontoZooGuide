import { ItineraryCardModal } from '../itineraryCardModal.js';
import { ItineraryServiceSaver } from '../itineraryServiceSaver.js';
import { ItineraryShape } from '../itineraryShape.js';
import { RegionStorageStore } from '../selectors/regionSelector/regionStorageStore.js';
import { StorageKeys } from '../storageKeys.js';

export class WizardFinalizerHelper {
   static clearWizardMount(mountEl) {
      // Release the modal first, or the page behind the card stays inert.
      ItineraryCardModal.release();
      mountEl?.replaceChildren();
   }

   static createFinalItineraryDraft(draft = {}, normalizeDraft = ItineraryShape.normalizeItineraryDraft) {
      return normalizeDraft(draft);
   }

   static saveFinalItinerary(
      finalItinerary,
      {
         overridingConflictingGuardiansTalks = false,
         confirmingShortVisit = false,
         confirmingEarlyAdmission = false,
      } = {},
      saveItineraryFn = ItineraryServiceSaver.saveItinerary,
   ) {
      return saveItineraryFn(finalItinerary, {
         overridingConflictingGuardiansTalks,
         confirmingShortVisit,
         confirmingEarlyAdmission,
         selectedExhibits: RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      });
   }
}
