// scripts/itinerary/panel/components/actionsBar.js
import { el } from '../dom.js';
import { clearItineraryStorage } from '../storage.js';
import { showItineraryConfirmPopup } from './confirmPopup.js';

/**
 * Renders the top action row for the itinerary panel.
 * - Edit Itinerary (opens wizard)
 * - Clear (TZG-style confirm popup)
 */
export function makeActionsBar({ onAfterClear } = {}) {
   const actionsWrap = el('div', 'itin-panel-actions-wrap');

   const editBtn = el('button', 'itin-panel-edit-btn', 'Edit Itinerary');
   editBtn.type = 'button';
   editBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });

   const clearBtn = el('button', 'itin-panel-clear-btn', 'Clear');
   clearBtn.type = 'button';
   clearBtn.addEventListener('click', (e) => {
      e.stopPropagation();

      showItineraryConfirmPopup({
         title: 'Clear Itinerary?',
         message: 'This will remove all selected Animals, Attractions, Meet the Guardians talks, and Wild Encounters.',
         confirmText: 'Clear',
         cancelText: 'Cancel',
         onConfirm: () => {
            clearItineraryStorage();
            onAfterClear?.();
         }
      });
   });

   actionsWrap.appendChild(editBtn);
   actionsWrap.appendChild(clearBtn);
   return actionsWrap;
}