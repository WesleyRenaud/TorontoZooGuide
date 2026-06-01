import {
   el,
   safeImg,
} from '../dom.js';

function appendItemName(text, { name, onNameClick }) {
   const nameEl = el('div', 'itin-panel-name', name);

   if (typeof onNameClick !== 'function') {
      text.appendChild(nameEl);
      return;
   }

   nameEl.classList.add('species-link');
   nameEl.setAttribute('role', 'button');
   nameEl.setAttribute('tabindex', '0');

   const activate = (event) => {
      event?.stopPropagation?.();
      onNameClick();
   };

   nameEl.addEventListener('click', activate);
   nameEl.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
         event.preventDefault();
         activate(event);
      }
   });

   text.appendChild(nameEl);
}

export function makeItemRow({
   name,
   imageSrc,
   metaLines = [],
   alertLine = '',
   alertTone = 'default',
   linkText,
   onLinkClick,
   onNameClick = null,
   actionLabel = '',
   onAction = null,
}) {
   const row = el('div', 'itin-panel-item');

   const left = el('div', 'itin-panel-item-left');

   const thumb = el('div', 'itin-panel-thumb');
   if (imageSrc) thumb.appendChild(safeImg(imageSrc));
   left.appendChild(thumb);

   const text = el('div', 'itin-panel-text');
   appendItemName(text, { name, onNameClick });

   metaLines.forEach(line => {
      if (!line) return;
      text.appendChild(el('div', 'itin-panel-meta', line));
   });

   if (alertLine) {
      const alertClass =
         alertTone === 'positive'
            ? 'itin-panel-alert-positive'
            : 'itin-panel-alert';

      text.appendChild(el('div', alertClass, alertLine));
   }

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

   if (actionLabel && typeof onAction === 'function') {
      const actionButton = document.createElement('button');

      actionButton.type = 'button';
      actionButton.className = 'itin-panel-item-action-btn';
      actionButton.textContent = actionLabel;
      actionButton.setAttribute('aria-label', actionLabel);
      actionButton.addEventListener('click', (event) => {
         event.stopPropagation();
         onAction();
      });
      row.appendChild(actionButton);
   }

   return row;
}
