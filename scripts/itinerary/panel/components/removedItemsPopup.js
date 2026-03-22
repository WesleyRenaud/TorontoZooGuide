import { el } from '../dom.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';

function addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
   if (!rowNode) return null;

   rowNode.classList.add('itin-removed-row');

   const btn = el('button', 'itin-removed-alt-btn', 'View Alternatives');
   btn.type = 'button';

   btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      removePopupOnly();
      onViewAlternatives?.(stepKey);
   });

   rowNode.appendChild(btn);
   return rowNode;
}

function makeSection(title, rowNodes = []) {
   const validRows = rowNodes.filter(Boolean);
   if (!validRows.length) return null;

   const section = el('div', 'itin-removed-section');

   section.appendChild(
      el('div', 'itin-removed-section-title', title)
   );

   const list = el('div', 'itin-removed-list');

   validRows.forEach((node) => {
      list.appendChild(node);
   });

   section.appendChild(list);
   return section;
}

export function showRemovedItemsPopup({
   mountEl,
   removed = {},
   isEmptyItinerary = false,
   onAccept,
   onDismiss,
   onViewAlternatives,
} = {}) {
   if (!mountEl) return;

   const {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
   } = removed;

   const hasAnything =
      animals.length ||
      attractions.length ||
      guardiansTalks.length ||
      wildEncounters.length;

   if (!hasAnything) return;

   const root = el('div', 'tzg-popup');
   const overlay = el('div', 'itin-overlay');

   const card = el('section', 'itin-card itin-removed-popup-card');

   const topbar = el('div', 'itin-card-topbar itin-card-topbar-with-close');
   topbar.appendChild(
      el('div', 'itin-top-title', 'Itinerary Updated')
   );

   const closeBtn = el('button', 'itin-close', '×');
   closeBtn.type = 'button';
   topbar.appendChild(closeBtn);

   const body = el('div', 'itin-card-body tzg-popup-body itin-removed-popup-body');
   const content = el('div', 'itin-removed-popup-content');

   content.appendChild(
      el(
         'div',
         'itin-h1',
         isEmptyItinerary ? 'Your itinerary is now empty' : 'Some items were removed'
      )
   );

   content.appendChild(
      el(
         'div',
         'itin-subtitle',
         isEmptyItinerary
            ? 'None of your selected items are available on the new date. You can view alternatives below.'
            : 'These items are unavailable on your selected date.'
      )
   );

   let isCleanedUp = false;

   function removePopupOnly() {
      if (isCleanedUp) return;
      isCleanedUp = true;
      root.remove();
   }

   function acceptAndClose() {
      removePopupOnly();
      onAccept?.();
   }

   function dismissAndClose() {
      removePopupOnly();
      onDismiss?.();
   }

   const animalRows = buildAnimalRows(animals).map((row) =>
      addAlternativesButton(row, 'animals', onViewAlternatives, removePopupOnly)
   );

   const attractionRows = buildAttractionRows(attractions).map((row) =>
      addAlternativesButton(row, 'attractions', onViewAlternatives, removePopupOnly)
   );

   const guardiansRows = buildGuardiansRows(guardiansTalks).map((row) =>
      addAlternativesButton(row, 'guardiansTalks', onViewAlternatives, removePopupOnly)
   );

   const wildRows = buildWildRows(wildEncounters).map((row) =>
      addAlternativesButton(row, 'wildEncounters', onViewAlternatives, removePopupOnly)
   );

   const animalsSection = makeSection('Animals', animalRows);
   const attractionsSection = makeSection('Attractions', attractionRows);
   const guardiansSection = makeSection('Meet the Guardians', guardiansRows);
   const wildSection = makeSection('Wild Encounters', wildRows);

   [animalsSection, attractionsSection, guardiansSection, wildSection]
      .filter(Boolean)
      .forEach((section) => content.appendChild(section));

   body.appendChild(content);

   const actions = el('div', 'itin-card-actions');

   const okBtn = el('button', 'itin-finish', isEmptyItinerary ? 'Accept' : 'Okay');
   okBtn.type = 'button';
   actions.appendChild(okBtn);

   card.appendChild(topbar);
   card.appendChild(body);
   card.appendChild(actions);

   overlay.appendChild(card);
   root.appendChild(overlay);

   closeBtn.addEventListener('click', dismissAndClose);
   okBtn.addEventListener('click', acceptAndClose);

   overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
         dismissAndClose();
      }
   });

   mountEl.appendChild(root);
}