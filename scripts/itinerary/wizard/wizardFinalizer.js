import { isItineraryEmpty, saveItinerary } from '../itineraryService.js';
import { normalizeItineraryDraft } from '../draftStorage.js';
import { showItineraryWizardPopup } from './wizardPopup.js';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: 'No Items Selected',
   message: 'Please add at least one Animal, Attraction, Meet the Guardians talk, or Wild Encounter before finishing.',
   buttonText: 'OK',
});

function clearWizardMount(mountEl) {
   mountEl?.replaceChildren();
}

function createFinalItineraryDraft(draft = {}) {
   return normalizeItineraryDraft(draft);
}

function shouldBlockEmptyFinish(finalItinerary, allowEmpty = false) {
   return !allowEmpty && isItineraryEmpty(finalItinerary);
}

function showEmptySelectionPopup(mountEl) {
   showItineraryWizardPopup({
      mountEl,
      ...EMPTY_SELECTION_POPUP_CONFIG,
   });
}

function saveFinalItinerary(finalItinerary) {
   return saveItinerary({
      ...finalItinerary,
      isActive: true,
   });
}

export async function finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false } = {}
) {
   const finalItinerary = createFinalItineraryDraft(draft);

   if (shouldBlockEmptyFinish(finalItinerary, allowEmpty)) {
      showEmptySelectionPopup(mountEl);
      return null;
   }

   const savedItinerary = await saveFinalItinerary(finalItinerary);

   clearWizardMount(mountEl);
   onDone?.();

   return savedItinerary;
}
