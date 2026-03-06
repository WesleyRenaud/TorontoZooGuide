// scripts/itinerary/panel/components/itemRow.js
import { el, safeImg } from '../dom.js';

export function makeItemRow({ name, imageSrc, metaLines = [], linkText, onLinkClick }) {
   const row = el('div', 'itin-panel-item');

   const left = el('div', 'itin-panel-item-left');

   const thumb = el('div', 'itin-panel-thumb');
   if (imageSrc) thumb.appendChild(safeImg(imageSrc));
   left.appendChild(thumb);

   const text = el('div', 'itin-panel-text');
   text.appendChild(el('div', 'itin-panel-name', name));

   metaLines.forEach(line => {
      if (!line) return;
      text.appendChild(el('div', 'itin-panel-meta', line));
   });

   if (linkText) {
      const link = el('div', 'itin-panel-link', linkText);
      link.addEventListener('click', (e) => {
         e.stopPropagation();
         onLinkClick?.();
      });
      text.appendChild(link);
   }

   left.appendChild(text);
   row.appendChild(left);

   return row;
}