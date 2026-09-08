import { ItemRowHelper } from './itemRowHelper.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';

export class ItemView {
   static makeItemRow({
      name,
      nameSuffix = '',
      species,
      enclosureName,
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
      const row = ItineraryPanelHelper.el('div', 'itin-panel-item');

      const left = ItineraryPanelHelper.el('div', 'itin-panel-item-left');

      if (imageSrc) {
         const thumb = ItineraryPanelHelper.el('div', 'itin-panel-thumb');
         thumb.appendChild(ItineraryPanelHelper.safeImg(imageSrc));
         left.appendChild(thumb);
      }

      const text = ItineraryPanelHelper.el('div', 'itin-panel-text');
      text.appendChild(ItemRowHelper.createItemNameElement({
         name,
         nameSuffix,
         species,
         enclosureName,
         onNameClick,
      }));

      metaLines.forEach(line => {
         if (!line) return;
         text.appendChild(ItineraryPanelHelper.el('div', 'itin-panel-meta', line));
      });

      if (alertLine) {
         const alertClass =
            alertTone === 'positive'
               ? 'itin-panel-alert-positive'
               : 'itin-panel-alert';

         text.appendChild(ItineraryPanelHelper.el('div', alertClass, alertLine));
      }

      if (linkText) {
         const link = ItineraryPanelHelper.el('div', 'itin-panel-link', linkText);
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
         const actions = ItineraryPanelHelper.el('div', 'itin-panel-item-actions');

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
}
