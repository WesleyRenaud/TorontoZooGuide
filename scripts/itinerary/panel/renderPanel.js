import { makeActionsBar } from './components/actionsBar.js';
import { makeSection } from './components/section.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';

import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';

import {
   getItinerary,
   isItineraryEmpty,
} from '../../pages/itineraryWizard/itineraryApi.js';

import { clearItineraryStorage } from './localStorage.js';

let latestRenderToken = 0;

async function clearItineraryViaApi() {
   const res = await fetch('/clear-itinerary', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
      },
   });

   if (!res.ok) {
      throw new Error(`Failed to clear itinerary: ${res.status}`);
   }
}

export async function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) return;

   const renderToken = ++latestRenderToken;
   const itin = await getItinerary();

   if (renderToken !== latestRenderToken) return;

   bodyEl.innerHTML = '';

   if (!itin || isItineraryEmpty(itin)) {
      renderBuildOnly(bodyEl);
      return;
   }

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [];
   const wildEncounters = Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [];

   bodyEl.appendChild(makeActionsBar({
      onAfterClear: async () => {
         try {
            await clearItineraryViaApi();
            clearItineraryStorage();

            window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
            window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
               detail: {
                  itinerary: {
                     animals: [],
                     attractions: [],
                     guardiansTalks: [],
                     wildEncounters: [],
                  }
               }
            }));

            await renderItineraryPanelInto(bodyEl);
         } catch (err) {
            console.error('Failed to clear itinerary:', err);
         }
      },
   }));

   const dateCard = makeDateCard(itin);
   if (dateCard) bodyEl.appendChild(dateCard);

   const animalRows = buildAnimalRows(animals);
   const attractionRows = buildAttractionRows(attractions);
   const guardiansRows = buildGuardiansRows(guardiansTalks);
   const wildRows = buildWildRows(wildEncounters);

   bodyEl.appendChild(
      makeSection({
         title: 'Animals',
         count: animals.length,
         children: animalRows,
         stepKey: 'animals',
      })
   );

   bodyEl.appendChild(
      makeSection({
         title: 'Attractions',
         count: attractions.length,
         children: attractionRows,
         stepKey: 'attractions',
      })
   );

   bodyEl.appendChild(
      makeSection({
         title: 'Meet the Guardians',
         count: guardiansTalks.length,
         children: guardiansRows,
         stepKey: 'guardiansTalks',
      })
   );

   bodyEl.appendChild(
      makeSection({
         title: 'Wild Encounters',
         count: wildEncounters.length,
         children: wildRows,
         stepKey: 'wildEncounters',
      })
   );
}