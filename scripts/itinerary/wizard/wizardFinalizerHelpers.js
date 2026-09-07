import { ItineraryServiceSave } from '../itineraryServiceSave.js';
import { ItineraryShape } from '../itineraryShape.js';
import { RegionStorage } from '../selectors/regionSelector/regionStorage.js';
import { StorageKeys } from '../storageKeys.js';
import { Strings } from '../../strings.js';
import { WizardPopup } from './wizardPopup.js';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: Strings.itinerary.noItemsSelected.title,
   message: Strings.itinerary.noItemsSelected.message,
   buttonText: Strings.itinerary.noItemsSelected.button,
});

export class WizardFinalizerHelpers {
   static clearWizardMount(mountEl) {
      mountEl?.replaceChildren();
   }

   static createFinalItineraryDraft(draft = {}, normalizeDraft = ItineraryShape.normalizeItineraryDraft) {
      return normalizeDraft(draft);
   }

   static showEmptySelectionPopup(mountEl, showWizardPopup = WizardPopup.showItineraryWizardPopup) {
      showWizardPopup({
         mountEl,
         ...EMPTY_SELECTION_POPUP_CONFIG,
      });
   }

   static saveFinalItinerary(
      finalItinerary,
      { overridingConflictingGuardiansTalks = false } = {},
      saveItineraryFn = ItineraryServiceSave.saveItinerary,
   ) {
      return saveItineraryFn(finalItinerary, {
         overridingConflictingGuardiansTalks,
         selectedExhibits: RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
      });
   }
}
