import { CreateSpeciesLinkTitle } from '../../../animals/createSpeciesLinkTitle.js';
import { SelectorResultRowBuilder } from './selectorResultRowBuilder.js';
import { Strings } from '../../../strings.js';

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

      const infoLinkEl = SelectorResultRowBuilder.createSelectorInfoLink(infoLink);

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

      if (!SelectorResultRowBuilder.hasRows(rows)) {
         resultsEl.replaceChildren(SelectorResultRowBuilder.createEmptyState(emptyText));
         return;
      }

      resultsEl.replaceChildren(
         SelectorResultRowBuilder.createResultRowsFragment({
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
