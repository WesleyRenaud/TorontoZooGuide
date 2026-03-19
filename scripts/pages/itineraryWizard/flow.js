import { createMapStore } from '../../map/store.js';
import { createDataSources } from '../../map/sources.js';
import { parseItineraryIncludes, dateISOToMonthDay } from '../../itinerary/itineraryHelpers.js';

import { loadArray, isItineraryEmpty } from './storage.js';
import { showItineraryPopup } from './popup.js';
import {
   ITIN_KEY,
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   TALKS_KEY,
   WILD_KEY,
} from './keys.js';

function buildFinalItinerary({ dateISO, animals, attractions, guardiansTalks, wildEncounters }) {
   return { dateISO, animals, attractions, guardiansTalks, wildEncounters };
}

function saveFinalItinerary(itin) {
   localStorage.setItem(ITIN_KEY, JSON.stringify(itin));
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated'));
}

function closeItineraryFlow(mountEl) {
   if (!mountEl) return;
   mountEl.innerHTML = '';
}

export async function finalizeItinerary(
   { animals, attractions, guardiansTalks, wildEncounters } = {},
   mountEl,
   { onDone } = {}
) {
   const dateISO = localStorage.getItem(DATE_KEY) || '';

   const finalItin = buildFinalItinerary({
      dateISO,
      animals: animals ?? loadArray(ANIMALS_KEY),
      attractions: attractions ?? loadArray(ATTRACTIONS_KEY),
      guardiansTalks: guardiansTalks ?? loadArray(TALKS_KEY),
      wildEncounters: wildEncounters ?? loadArray(WILD_KEY),
   });

   if (isItineraryEmpty(finalItin)) {
      showItineraryPopup({
         mountEl,
         title: 'No Items Selected',
         message: 'Please add at least one Animal, Attraction, Meet the Guardians talk, or Wild Encounter before finishing.',
         buttonText: 'OK',
      });
      return;
   }

   const { month, day } = dateISOToMonthDay(dateISO);
   const inc = parseItineraryIncludes(finalItin);

   const payload = {
      month,
      day,
      temp: null,
      animals: inc.speciesToInclude,
      attractions: inc.attractionsToInclude,
      guardiansTalks: inc.guardiansTalksToInclude,
      wildEncounters: inc.wildEncountersToInclude,
   };

   try {
      const store = createMapStore();
      const sources = createDataSources(store);

      if (!sources?.buildItinerary?.fetch) {
         console.warn('sources.buildItinerary is missing (add it in scripts/map/sources.js)');
      } else {
         await sources.buildItinerary.fetch(payload);
      }
   } catch (err) {
      console.error('Error calling sources.buildItinerary:', err);
   }

   saveFinalItinerary(finalItin);
   closeItineraryFlow(mountEl);
   onDone?.();
}