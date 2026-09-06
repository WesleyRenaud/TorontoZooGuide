import { Dom } from '../dom.js';
import { RemovedItemsPopupKeepButtonState } from './removedItemsPopupKeepButtonState.js';
import { RemovedItemsPopupSectionSpecs } from './removedItemsPopupSectionSpecs.js';
import { Strings } from '../../../strings.js';

function addAlternativesButton(rowNode, stepKey, onViewAlternatives, removePopupOnly) {
   if (!rowNode) {
      return null;
   }

   const btn = Dom.el(
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

function addKeepOverrideButton(
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

   const btn = Dom.el('button', 'itin-removed-alt-btn itin-removed-keep-btn');

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

function makeSection(title, subtitle, rowNodes = []) {
   const validRows = rowNodes.filter(Boolean);

   if (!validRows.length) {
      return null;
   }

   const section = Dom.el('div', 'itin-removed-section');

   section.appendChild(
      Dom.el('div', 'itin-removed-section-title', title)
   );

   if (subtitle) {
      section.appendChild(
         Dom.el('div', 'itin-removed-section-subtitle', subtitle)
      );
   }

   const list = Dom.el('div', 'itin-removed-list');

   validRows.forEach((node) => {
      list.appendChild(node);
   });

   section.appendChild(list);

   return section;
}

function buildSectionRows(
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

      const actions = Dom.el('div', 'itin-removed-row-actions');

      if (showViewAlternatives) {
         const alternativesButton = addAlternativesButton(
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
         const keepButton = addKeepOverrideButton(
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

export class RemovedItemsPopupContent {
   static buildRemovedItemsPopupSections({
      added,
      removed,
      unscheduled,
      reducedVisibility,
      improvedVisibility,
      adjustments,
      onViewAlternatives,
      removePopupOnly,
      onToggleKeepAnimal,
      isKeepAnimalSelected,
      onToggleKeepAttraction,
      isKeepAttractionSelected,
   } = {}) {
      const keepOverrideHandlers = {
         onToggleKeepAnimal,
         isKeepAnimalSelected,
         onToggleKeepAttraction,
         isKeepAttractionSelected,
      };

      return RemovedItemsPopupSectionSpecs.getRemovedItemsPopupSectionSpecs({
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
      })
         .map((section) => makeSection(
            section.title,
            section.subtitle,
            buildSectionRows(
               section.items,
               section.rowBuilder,
               section.stepKey,
               onViewAlternatives,
               removePopupOnly,
               section.showViewAlternatives ?? true,
               RemovedItemsPopupSectionSpecs.resolveKeepOverride(section, keepOverrideHandlers)
            )
         ))
         .filter(Boolean);
   }
}
