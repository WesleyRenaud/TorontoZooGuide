import { Strings } from '../../strings.js';

const scheduleItemStrings = Strings.itinerary.scheduleItem;
const actionStrings = Strings.itinerary.actions;

function createEmptyState(emptyText) {
   const empty = document.createElement('div');
   empty.className = 'itin-empty';
   empty.textContent = emptyText;
   return empty;
}

function createSelectButton({
   isSelected,
   onSelect,
} = {}) {
   const button = document.createElement('button');
   button.type = 'button';
   button.className = 'itin-add-btn schedule-item-select-btn';

   function updateButtonState() {
      const selected = isSelected();
      button.textContent = selected ? '✓' : actionStrings.addSymbol;
      button.classList.toggle('is-added', selected);
      button.setAttribute('aria-pressed', String(selected));
      button.setAttribute(
         'aria-label',
         selected ? scheduleItemStrings.itemSelected : scheduleItemStrings.selectItem
      );
   }

   button.addEventListener('click', (event) => {
      event.stopPropagation();
      onSelect();
   });

   updateButtonState();

   return {
      button,
      updateButtonState,
   };
}

function createResultRow({
   row,
   getId,
   selectedRowId,
   renderRowLeft,
   onSelectRow,
} = {}) {
   const id = getId(row);
   const isSelected = () => id === selectedRowId;

   const item = document.createElement('div');
   item.className = 'animal-result schedule-item-result';
   item.classList.toggle('is-selected', isSelected());
   item.setAttribute('role', 'button');
   item.tabIndex = 0;
   item.setAttribute(
      'aria-pressed',
      String(isSelected())
   );

   const selectControl = createSelectButton({
      isSelected,
      onSelect: () => onSelectRow?.(row, id),
   });

   item.append(renderRowLeft(row), selectControl.button);

   function handleSelect() {
      onSelectRow?.(row, id);
   }

   item.addEventListener('click', handleSelect);
   item.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
         event.preventDefault();
         handleSelect();
      }
   });

   return item;
}

export class ScheduleItemResults {
   static renderScheduleItemSearchResults({
      resultsEl,
      rows = [],
      emptyText = '',
      getId,
      selectedRowId = '',
      renderRowLeft,
      onSelectRow,
   } = {}) {
      if (!resultsEl) {
         return;
      }

      if (!Array.isArray(rows) || rows.length === 0) {
         resultsEl.replaceChildren(createEmptyState(emptyText));
         return;
      }

      const fragment = document.createDocumentFragment();

      rows.forEach((row) => {
         fragment.appendChild(
            createResultRow({
               row,
               getId,
               selectedRowId,
               renderRowLeft,
               onSelectRow,
            })
         );
      });

      resultsEl.replaceChildren(fragment);
   }
}
