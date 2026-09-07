import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { RemovedItemsPopupKeepButtonState } from './removedItemsPopupKeepButtonState.js';
import { Strings } from '../../../strings.js';

export class RemovedItemsPopupContentBuilder {
   static addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
      if (!rowNode) {
         return null;
      }

      const btn = ItineraryPanelDom.el(
         'button',
         'itin-removed-alt-btn',
         Strings.itinerary.removedItems.viewAlternatives
      );

      btn.type = 'button';

      btn.addEventListener('click', (e) => {
         e.preventDefault();
         e.stopPropagation();

         removePopupOnly();
         onViewAlternatives?.(stepKey);
      });

      return btn;
   }

   static addKeepOverrideButton(
      item,
      buildKey,
      onToggleKeep,
      isKeepSelected
   ) {
      if (!item) {
         return null;
      }

      const key = buildKey(item);

      if (!key) {
         return null;
      }

      const btn = ItineraryPanelDom.el('button', 'itin-removed-alt-btn itin-removed-keep-btn');

      btn.type = 'button';

      function sync() {
         RemovedItemsPopupKeepButtonState.applyKeepOverrideButtonState(
            btn,
            RemovedItemsPopupKeepButtonState.getKeepOverrideButtonState(isKeepSelected?.(key))
         );
      }

      btn.addEventListener('click', (e) => {
         e.preventDefault();
         e.stopPropagation();
         onToggleKeep?.(item);
         sync();
      });

      sync();

      return btn;
   }

   static makeSection(title, subtitle, rowNodes = []) {
      const validRows = rowNodes.filter(Boolean);

      if (!validRows.length) {
         return null;
      }

      const section = ItineraryPanelDom.el('div', 'itin-removed-section');

      section.appendChild(
         ItineraryPanelDom.el('div', 'itin-removed-section-title', title)
      );

      if (subtitle) {
         section.appendChild(
            ItineraryPanelDom.el('div', 'itin-removed-section-subtitle', subtitle)
         );
      }

      const list = ItineraryPanelDom.el('div', 'itin-removed-list');

      validRows.forEach((node) => {
         list.appendChild(node);
      });

      section.appendChild(list);

      return section;
   }

   static buildSectionRows(
      items,
      rowBuilder,
      stepKey,
      onViewAlternatives,
      removePopupOnly,
      showViewAlternatives = true,
      keepOverride = null
   ) {
      return rowBuilder(items).map((row, index) => {
         const item = items?.[index];

         if (!showViewAlternatives && !keepOverride) {
            return row;
         }

         row.classList.add('itin-removed-row');

         const actions = ItineraryPanelDom.el('div', 'itin-removed-row-actions');

         if (showViewAlternatives) {
            const alternativesButton = RemovedItemsPopupContentBuilder.addAlternativesButton(
               row,
               stepKey,
               onViewAlternatives,
               removePopupOnly
            );

            if (alternativesButton) {
               actions.appendChild(alternativesButton);
            }
         }

         if (keepOverride) {
            const keepButton = RemovedItemsPopupContentBuilder.addKeepOverrideButton(
               item,
               keepOverride.buildKey,
               keepOverride.onToggle,
               keepOverride.isSelected
            );

            if (keepButton) {
               actions.appendChild(keepButton);
            }
         }

         if (actions.children.length > 0) {
            row.appendChild(actions);
         }

         return row;
      });
   }
}
