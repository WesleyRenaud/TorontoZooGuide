// scripts/itinerary/panel/renderPanel.js
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

import { getItineraryData } from './getItineraryData.js';

export function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) return;

   bodyEl.innerHTML = '';

   const data = getItineraryData();
   if (!data) {
      renderBuildOnly(bodyEl);
      return;
   }

   const { itin, animals, attractions, guardiansTalks, wildEncounters } = data;

   // ✅ Action bar (Edit + Clear)
   bodyEl.appendChild(makeActionsBar({
      onAfterClear: () => renderItineraryPanelInto(bodyEl),
   }));

   // ✅ Visit Date card
   const dateCard = makeDateCard(itin);
   if (dateCard) bodyEl.appendChild(dateCard);

   // ✅ Rows
   const animalRows = buildAnimalRows(animals);
   const attractionRows = buildAttractionRows(attractions);
   const guardiansRows = buildGuardiansRows(guardiansTalks);
   const wildRows = buildWildRows(wildEncounters);

   // ✅ Always render sections
   bodyEl.appendChild(makeSection({ title: 'Animals', count: animals.length, children: animalRows, stepKey: 'animals' }));
   bodyEl.appendChild(makeSection({ title: 'Attractions', count: attractions.length, children: attractionRows, stepKey: 'attractions' }));
   bodyEl.appendChild(makeSection({ title: 'Meet the Guardians', count: guardiansTalks.length, children: guardiansRows, stepKey: 'guardiansTalks' }));
   bodyEl.appendChild(makeSection({ title: 'Wild Encounters', count: wildEncounters.length, children: wildRows, stepKey: 'wildEncounters' }));
}