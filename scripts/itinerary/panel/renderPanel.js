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
   clearItinerary,
   getItinerary,
   isItineraryEmpty,
} from '../itineraryService.js';

import { clearItineraryStorage } from './localStorage.js';

let latestRenderToken = 0;

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
            await clearItinerary();
            clearItineraryStorage();

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
