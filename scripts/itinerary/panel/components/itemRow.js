import { createSpeciesLinkTitleElement } from '../../../animals/createSpeciesLinkTitle.js';
import {
   el,
   safeImg,
} from '../dom.js';

function appendItemName(text, { name, onNameClick }) {
   text.appendChild(createSpeciesLinkTitleElement({
      text: name,
      className: 'itin-panel-name',
      onClick: onNameClick,
   }));
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
   secondaryActionLabel = '',
   onSecondaryAction = null,
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

   const rowActions = [];

   if (actionLabel && typeof onAction === 'function') {
      rowActions.push({ label: actionLabel, onAction });
   }

   if (secondaryActionLabel && typeof onSecondaryAction === 'function') {
      rowActions.push({
         label: secondaryActionLabel,
         onAction: onSecondaryAction,
      });
   }

   if (rowActions.length) {
      const actions = el('div', 'itin-panel-item-actions');

      rowActions.forEach(({ label, onAction: handleAction }) => {
         const actionButton = document.createElement('button');

         actionButton.type = 'button';
         actionButton.className = 'itin-panel-item-action-btn';
         actionButton.textContent = label;
         actionButton.setAttribute('aria-label', label);
         actionButton.addEventListener('click', (event) => {
            event.stopPropagation();
            handleAction();
         });
         actions.appendChild(actionButton);
      });
      row.appendChild(actions);
   }

   return row;
}
