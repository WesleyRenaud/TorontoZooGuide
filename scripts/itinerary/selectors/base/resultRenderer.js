const ADD_BUTTON_LABEL = '+';
const REMOVE_BUTTON_LABEL = '−';

function createSelectorInfoLink(infoLink) {
   if (!infoLink) {
      return null;
   }

   const linkEl = document.createElement('a');
   linkEl.className = 'tooltip-link';
   linkEl.href = infoLink;
   linkEl.target = '_blank';
   linkEl.rel = 'noopener noreferrer';
   linkEl.textContent = 'More Info';

   linkEl.addEventListener('click', (event) => {
      event.stopPropagation();
   });

   return linkEl;
}

export function createSelectorThumb({
   imageSrc = null,
   imageAlt = '',
} = {}) {
   const thumbWrap = document.createElement('div');
   thumbWrap.className = 'itin-animal-thumb';

   if (!imageSrc) {
      thumbWrap.classList.add('is-placeholder');
      return thumbWrap;
   }

   const img = document.createElement('img');
   img.className = 'itin-animal-thumb-img';
   img.loading = 'lazy';
   img.alt = imageAlt;
   img.src = imageSrc;

   img.addEventListener('error', () => {
      thumbWrap.classList.add('is-placeholder');
      img.remove();
   });

   thumbWrap.appendChild(img);

   return thumbWrap;
}

export function createSelectorTextColumn({
   title = 'Item',
   subtitle = '',
   infoLink = null,
   titleNode = null,
} = {}) {
   const left = document.createElement('div');
   left.className = 'animal-result-left';

   if (titleNode) {
      left.appendChild(titleNode);
   }
   else {
      const titleEl = document.createElement('div');
      titleEl.className = 'animal-result-species';
      titleEl.textContent = title;
      left.appendChild(titleEl);
   }

   if (subtitle) {
      const subtitleEl = document.createElement('div');
      subtitleEl.className = 'animal-result-exhibit';
      subtitleEl.textContent = subtitle;
      left.appendChild(subtitleEl);
   }

   const infoLinkEl = createSelectorInfoLink(infoLink);

   if (infoLinkEl) {
      left.appendChild(infoLinkEl);
   }

   return left;
}

export function createSelectorRowContent({
   imageSrc = null,
   imageAlt = '',
   textColumnEl,
} = {}) {
   const content = document.createElement('div');
   content.className = 'itin-animal-content';

   content.append(
      createSelectorThumb({
         imageSrc,
         imageAlt,
      }),
      textColumnEl
   );

   return content;
}

export function createDefaultSelectorRowLeftRenderer({
   getTitle,
   getSubtitle,
   getImageSrc,
   getInfoLink,
} = {}) {
   return function renderDefaultRowLeft(row) {
      const title = getTitle(row) || 'Item';
      const subtitle = getSubtitle(row);
      const imageSrc = getImageSrc(row);
      const infoLink = getInfoLink(row);

      return createSelectorRowContent({
         imageSrc,
         imageAlt: title ? `${title} image` : '',
         textColumnEl: createSelectorTextColumn({
            title,
            subtitle,
            infoLink,
         }),
      });
   };
}

function createEmptyState(emptyText) {
   const empty = document.createElement('div');
   empty.className = 'itin-empty';
   empty.textContent = emptyText;
   return empty;
}

function hasRows(rows) {
   return Array.isArray(rows) && rows.length > 0;
}

function createToggleButton({
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
      button.textContent = added ? REMOVE_BUTTON_LABEL : ADD_BUTTON_LABEL;
      button.classList.toggle('is-added', added);
      button.setAttribute('aria-pressed', String(added));
      button.setAttribute(
         'aria-label',
         added ? 'Remove from itinerary' : 'Add to itinerary'
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

function createResultRow({
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
      createToggleButton({
         id,
         row,
         isSelected,
         onToggle,
         onBeforeToggleAdd,
      })
   );

   return item;
}

function createResultRowsFragment({
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
         createResultRow({
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

export function renderSelectorResults({
   resultsEl,
   rows,
   emptyText,
   getId,
   isSelected,
   renderRowLeft,
   onToggle,
   onBeforeToggleAdd = null,
} = {}) {
   if (!resultsEl) {
      return;
   }

   if (!hasRows(rows)) {
      resultsEl.replaceChildren(createEmptyState(emptyText));
      return;
   }

   resultsEl.replaceChildren(
      createResultRowsFragment({
         rows,
         getId,
         isSelected,
         renderRowLeft,
         onToggle,
         onBeforeToggleAdd,
      })
   );
}
