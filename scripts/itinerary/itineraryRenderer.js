// scripts/itinerary/itineraryRenderer.js
import {
   ITIN_KEY,
   safeParseJSON,
} from './panel/storage.js';

import { makeActionsBar } from './panel/components/actionsBar.js';
import { makeSection } from './panel/components/section.js';
import { renderBuildOnly } from './panel/components/buildOnly.js';
import { makeDateCard } from './panel/components/dateCard.js';

import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from './panel/rows.js';

export function renderItineraryPanel() {
   const body = document.getElementById('itineraryPanelBody');
   if (!body) return;

   body.innerHTML = '';

   const raw = localStorage.getItem(ITIN_KEY);
   if (!raw) {
      renderBuildOnly(body);
      return;
   }

   const itin = safeParseJSON(raw, null);
   if (!itin) {
      renderBuildOnly(body);
      return;
   }

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [];
   const wildEncounters = Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [];

   // ✅ Action bar (Edit + Clear)
   body.appendChild(makeActionsBar({
      onAfterClear: () => renderItineraryPanel(),
   }));

   // ✅ Visit Date card
   const dateCard = makeDateCard(itin);
   if (dateCard) body.appendChild(dateCard);

   // ✅ Build rows (kept out of this file)
   const animalRows = buildAnimalRows(animals);
   const attractionRows = buildAttractionRows(attractions);
   const guardiansRows = buildGuardiansRows(guardiansTalks);
   const wildRows = buildWildRows(wildEncounters);

   // ✅ Always render all sections (even if empty)
   body.appendChild(makeSection({ title: 'Animals', count: animals.length, children: animalRows, stepKey: 'animals' }));
   body.appendChild(makeSection({ title: 'Attractions', count: attractions.length, children: attractionRows, stepKey: 'attractions' }));
   body.appendChild(makeSection({ title: 'Meet the Guardians', count: guardiansTalks.length, children: guardiansRows, stepKey: 'guardiansTalks' }));
   body.appendChild(makeSection({ title: 'Wild Encounters', count: wildEncounters.length, children: wildRows, stepKey: 'wildEncounters' }));
}