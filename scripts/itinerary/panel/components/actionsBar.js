import { ConfirmPopup } from './confirmPopup.js';
import { Dom } from '../dom.js';
import { Strings } from '../../../strings.js';

export class ActionsBar {
   static makeActionsBar({ onAfterClear } = {}) {
      const actionsWrap = Dom.el('div', 'itin-panel-actions-wrap');

      const editBtn = Dom.el(
         'button',
         'itin-panel-edit-btn',
         Strings.itinerary.actions.editItinerary
      );
      editBtn.type = 'button';
      editBtn.addEventListener('click', (e) => {
         e.stopPropagation();
         window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
      });

      const clearBtn = Dom.el('button', 'itin-panel-clear-btn', Strings.itinerary.actions.clear);
      clearBtn.type = 'button';
      clearBtn.addEventListener('click', (e) => {
         e.stopPropagation();

         ConfirmPopup.showItineraryConfirmPopup({
            title: Strings.itinerary.confirmation.clearTitle,
            message: Strings.itinerary.confirmation.clearMessage,
            confirmText: Strings.itinerary.actions.clear,
            cancelText: Strings.itinerary.actions.cancel,
            onConfirm: async () => {
               await onAfterClear?.();
            }
         });
      });

      actionsWrap.appendChild(editBtn);
      actionsWrap.appendChild(clearBtn);
      return actionsWrap;
   }
}
