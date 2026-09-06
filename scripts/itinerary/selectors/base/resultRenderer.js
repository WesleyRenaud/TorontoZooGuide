import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';
import { Strings } from '../../../strings.js';

function createSelectorInfoLink(infoLink) {
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

export class ResultRenderer {
   static createSelectorThumb({
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

   static createSelectorTextColumn({
      title = Strings.entityLabels.item,
      titleSuffix = '',
      subtitle = '',
      infoLink = null,
      titleNode = null,
      titleParts = null,
      subtitleNode = null,
      onTitleClick = null,
   } = {}) {
      const left = document.createElement('div');
      left.className = 'animal-result-left';

      if (titleNode) {
         left.appendChild(titleNode);
      }
      else if (titleParts) {
         left.appendChild(CreateSpeciesLinkTitle.createAnimalTitleLinkElement({
            species: titleParts.species,
            enclosureName: titleParts.enclosureName,
            className: 'animal-result-species',
            onClick: onTitleClick,
         }));
      }
      else {
         left.appendChild(CreateSpeciesLinkTitle.createSpeciesLinkTitleElement({
            text: title,
            suffix: titleSuffix,
            className: 'animal-result-species',
            onClick: onTitleClick,
         }));
      }

      if (subtitleNode) {
         left.appendChild(subtitleNode);
      }
      else if (subtitle) {
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

   static createSelectorRowContent({
      imageSrc = null,
      imageAlt = '',
      textColumnEl,
   } = {}) {
      const content = document.createElement('div');
      content.className = 'itin-animal-content';

      content.append(
         ResultRenderer.createSelectorThumb({
            imageSrc,
            imageAlt,
         }),
         textColumnEl
      );

      return content;

   }

   static createDefaultSelectorRowLeftRenderer({
      getTitle,
      getTitleParts = null,
      getTitleSuffix = null,
      getSubtitle,
      getImageSrc,
      getInfoLink,
      onTitleClick = null,
      shouldEnableTitleClick = null,
   } = {}) {
      return function renderDefaultRowLeft(row) {
         const titleParts = typeof getTitleParts === 'function'
            ? getTitleParts(row)
            : null;
         const title = getTitle(row) || Strings.entityLabels.item;
         const titleSuffix = typeof getTitleSuffix === 'function'
            ? getTitleSuffix(row)
            : '';
         const subtitle = getSubtitle(row);
         const imageSrc = getImageSrc(row);
         const infoLink = getInfoLink(row);
         const titleClickEnabled = (
            typeof onTitleClick === 'function'
            && (
               typeof shouldEnableTitleClick !== 'function'
               || shouldEnableTitleClick(row)
            )
         );
         const titleForAlt = `${title}${titleSuffix}`;

         return ResultRenderer.createSelectorRowContent({
            imageSrc,
            imageAlt: titleForAlt ? Strings.itinerary.itemImage(titleForAlt) : '',
            textColumnEl: ResultRenderer.createSelectorTextColumn({
               title,
               titleSuffix,
               titleParts,
               subtitle,
               infoLink,
               onTitleClick: titleClickEnabled
                  ? () => onTitleClick(row)
                  : null,
            }),
         });
      };

   }

   static renderSelectorResults({
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
}
