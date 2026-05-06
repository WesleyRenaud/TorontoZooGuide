import { el } from '../dom.js';
import { APP_STRINGS } from '../../../strings.js';
import { showItineraryConfirmPopup } from './confirmPopup.js';

export function makeActionsBar({ onAfterClear } = {}) {
   const actionsWrap = el('div', 'itin-panel-actions-wrap');

   const editBtn = el(
      'button',
      'itin-panel-edit-btn',
      APP_STRINGS.itinerary.actions.editItinerary
   );
   editBtn.type = 'button';
   editBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });

   const clearBtn = el('button', 'itin-panel-clear-btn', APP_STRINGS.itinerary.actions.clear);
   clearBtn.type = 'button';
   clearBtn.addEventListener('click', (e) => {
      e.stopPropagation();

      showItineraryConfirmPopup({
         title: APP_STRINGS.itinerary.confirmation.clearTitle,
         message: APP_STRINGS.itinerary.confirmation.clearMessage,
         confirmText: APP_STRINGS.itinerary.actions.clear,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         onConfirm: async () => {
            await onAfterClear?.();
         }
      });
   });

   actionsWrap.appendChild(editBtn);
   actionsWrap.appendChild(clearBtn);
   return actionsWrap;
}
