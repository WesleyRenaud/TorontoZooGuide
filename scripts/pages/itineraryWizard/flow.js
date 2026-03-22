import { isItineraryEmpty, saveItinerary } from './itineraryApi.js';
import { loadArray } from '../../itinerary/panel/localStorage.js';
import { showItineraryPopup } from './popup.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from './keys.js';

function buildFinalItinerary({ date, animals, attractions, guardiansTalks, wildEncounters }) {
   return { date, animals, attractions, guardiansTalks, wildEncounters };
}

function closeItineraryFlow(mountEl) {
   if (!mountEl) return;
   mountEl.innerHTML = '';
}

export async function finalizeItinerary(
   { animals, attractions, guardiansTalks, wildEncounters } = {},
   mountEl,
   { onDone, allowEmpty = false } = {}
) {
   const date = localStorage.getItem(DATE_KEY) || '';

   const finalItin = buildFinalItinerary({
      date,
      animals: animals ?? loadArray(ANIMALS_KEY),
      attractions: attractions ?? loadArray(ATTRACTIONS_KEY),
      guardiansTalks: guardiansTalks ?? loadArray(GUARDIANS_KEY),
      wildEncounters: wildEncounters ?? loadArray(WILD_KEY),
   });

   if (!allowEmpty && isItineraryEmpty(finalItin)) {
      showItineraryPopup({
         mountEl,
         title: 'No Items Selected',
         message: 'Please add at least one Animal, Attraction, Meet the Guardians talk, or Wild Encounter before finishing.',
         buttonText: 'OK',
      });
      return;
   }

   await saveItinerary({
      date: finalItin.date,
      animals: finalItin.animals,
      attractions: finalItin.attractions,
      guardiansTalks: finalItin.guardiansTalks,
      wildEncounters: finalItin.wildEncounters,
      isActive: true,
   });

   closeItineraryFlow(mountEl);
   onDone?.();
}