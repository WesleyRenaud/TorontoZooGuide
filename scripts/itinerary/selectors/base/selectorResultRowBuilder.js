import { Strings } from '../../../strings.js';

export class SelectorResultRowBuilder {
   static createSelectorInfoLink(infoLink) {
      if (!infoLink) {
         return null;
      }

      const linkEl = document.createElement('a');
      linkEl.className = 'tooltip-link';
      linkEl.href = infoLink;
      linkEl.target = '_blank';
      linkEl.rel = 'noopener noreferrer';
      linkEl.textContent = Strings.common.moreInfo;

      linkEl.addEventListener('click', (event) => {
         event.stopPropagation();
      });

      return linkEl;
   }

   static createEmptyState(emptyText) {
      const empty = document.createElement('div');
      empty.className = 'itin-empty';
      empty.textContent = emptyText;
      return empty;
   }

   static hasRows(rows) {
      return Array.isArray(rows) && rows.length > 0;
   }

   static createToggleButton({
      id,
      row,
      isSelected,
      onToggle,
      onBeforeToggleAdd,
   } = {}) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'itin-add-btn';

      function isRowSelected() {
         return Boolean(id) && isSelected(id);
      }

      function updateButtonState() {
         const added = isRowSelected();
         button.textContent = added
            ? Strings.itinerary.actions.remove
            : Strings.itinerary.actions.addSymbol;
         button.classList.toggle('is-added', added);
         button.setAttribute('aria-pressed', String(added));
         button.setAttribute(
            'aria-label',
            added
               ? Strings.itinerary.aria.removeFromItinerary
               : Strings.itinerary.aria.addToItinerary
         );
      }

      function toggleSelection() {
         onToggle(row);
         updateButtonState();
      }

      button.addEventListener('click', (event) => {
         event.stopPropagation();

         const added = isRowSelected();

         if (typeof onBeforeToggleAdd === 'function') {
            onBeforeToggleAdd({
               row,
               id,
               isSelected: added,
               proceed: toggleSelection,
            });
            return;
         }

         toggleSelection();
      });

      updateButtonState();

      return button;
   }

   static createResultRow({
      row,
      getId,
      isSelected,
      renderRowLeft,
      onToggle,
      onBeforeToggleAdd,
   } = {}) {
      const id = getId(row);

      const item = document.createElement('div');
      item.className = 'animal-result';

      item.append(
         renderRowLeft(row),
         SelectorResultRowBuilder.createToggleButton({
            id,
            row,
            isSelected,
            onToggle,
            onBeforeToggleAdd,
         })
      );

      return item;
   }

   static createResultRowsFragment({
      rows,
      getId,
      isSelected,
      renderRowLeft,
      onToggle,
      onBeforeToggleAdd,
   } = {}) {
      const fragment = document.createDocumentFragment();

      rows.forEach((row) => {
         fragment.appendChild(
            SelectorResultRowBuilder.createResultRow({
               row,
               getId,
               isSelected,
               renderRowLeft,
               onToggle,
               onBeforeToggleAdd,
            })
         );
      });

      return fragment;
   }
}
