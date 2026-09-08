import { ItineraryServiceSaver } from '../itineraryServiceSaver.js';
import { ItineraryShape } from '../itineraryShape.js';
import { RegionStorageStore } from '../selectors/regionSelector/regionStorageStore.js';
import { StorageKeys } from '../storageKeys.js';
import { Strings } from '../../strings.js';
import { WizardFragment } from './wizardFragment.js';

export class WizardFinalizerHelper {
   static EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
      title: Strings.itinerary.noItemsSelected.title,
      message: Strings.itinerary.noItemsSelected.message,
      buttonText: Strings.itinerary.noItemsSelected.button,
   });

   static clearWizardMount(mountEl) {
      mountEl?.replaceChildren();
   }

   static createFinalItineraryDraft(draft = {}, normalizeDraft = ItineraryShape.normalizeItineraryDraft) {
      return normalizeDraft(draft);
   }

   static showEmptySelectionPopup(mountEl, showWizardPopup = WizardFragment.showItineraryWizardPopup) {
      showWizardPopup({
         mountEl,
         ...WizardFinalizerHelper.EMPTY_SELECTION_POPUP_CONFIG,
      });
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
