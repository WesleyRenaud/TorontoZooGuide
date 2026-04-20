export function createDefaultSelectorRowLeftRenderer({
   getTitle,
   getSubtitle,
   getImageSrc,
   getInfoLink,
} = {}) {
   return function renderDefaultRowLeft(row) {
      const title = getTitle(row);
      const subtitle = getSubtitle(row);
      const imageSrc = getImageSrc(row);
      const infoLink = getInfoLink(row);

      const content = document.createElement('div');
      content.className = 'itin-animal-content';

      const thumbWrap = document.createElement('div');
      thumbWrap.className = 'itin-animal-thumb';

      if (imageSrc) {
         const img = document.createElement('img');
         img.className = 'itin-animal-thumb-img';
         img.loading = 'lazy';
         img.alt = title ? `${title} image` : '';
         img.src = imageSrc;

         img.addEventListener('error', () => {
            thumbWrap.classList.add('is-placeholder');
            img.remove();
         });

         thumbWrap.appendChild(img);
      } else {
         thumbWrap.classList.add('is-placeholder');
      }

      const left = document.createElement('div');
      left.className = 'animal-result-left';

      const titleEl = document.createElement('div');
      titleEl.className = 'animal-result-species';
      titleEl.textContent = title || 'Item';
      left.appendChild(titleEl);

      if (subtitle) {
         const subtitleEl = document.createElement('div');
         subtitleEl.className = 'animal-result-exhibit';
         subtitleEl.textContent = subtitle;
         left.appendChild(subtitleEl);
      }

      if (infoLink) {
         const linkEl = document.createElement('a');
         linkEl.className = 'tooltip-link';
         linkEl.href = infoLink;
         linkEl.target = '_blank';
         linkEl.rel = 'noopener noreferrer';
         linkEl.textContent = 'More Info';

         linkEl.addEventListener('click', (e) => {
            e.stopPropagation();
         });

         left.appendChild(linkEl);
      }

      content.appendChild(thumbWrap);
      content.appendChild(left);

      return content;
   };
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
   resultsEl.innerHTML = '';

   if (!Array.isArray(rows) || rows.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'itin-empty';
      empty.textContent = emptyText;
      resultsEl.appendChild(empty);
      return;
   }

   rows.forEach((row) => {
      const id = getId(row);

      const item = document.createElement('div');
      item.className = 'animal-result';

      const leftNode = renderRowLeft(row);

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'itin-add-btn';

      const updateBtn = () => {
         const added = Boolean(id) && isSelected(id);
         btn.textContent = added ? '−' : '+';
         btn.classList.toggle('is-added', added);
      };

      const proceed = () => {
         onToggle(row);
         updateBtn();
      };

      updateBtn();

      btn.addEventListener('click', (e) => {
         e.stopPropagation();

         const added = Boolean(id) && isSelected(id);

         if (typeof onBeforeToggleAdd === 'function') {
            onBeforeToggleAdd({
               row,
               id,
               isSelected: added,
               proceed,
            });
            return;
         }

         proceed();
      });

      item.appendChild(leftNode);
      item.appendChild(btn);

      resultsEl.appendChild(item);
   });
}
