import { Dom } from '../dom.js';
import { DraftStorage } from '../../draftStorage.js';
import { Format } from '../format.js';
import { Strings } from '../../../strings.js';

const { actions, selectors } = Strings.itinerary;

export class DateCard {
   static makeDateCard(itin = {}) {
      const date = itin.date || DraftStorage.getStoredItineraryDate();
      const prettyDate = Format.formatISODateLong(date);

      if (!prettyDate) return null;

      const dateWrap = Dom.el('div', 'itin-panel-date');

      const topRow = Dom.el('div', 'itin-panel-date-top');
      const textWrap = Dom.el('div', 'itin-panel-date-text');

      textWrap.appendChild(Dom.el('div', 'itin-panel-date-label', selectors.visitDate));
      textWrap.appendChild(Dom.el('div', 'itin-panel-date-value', prettyDate));

      const actionsWrap = Dom.el('div', 'itin-panel-header-actions');

      const editBtn = Dom.el('button', 'itin-panel-section-edit-btn', actions.edit);
      editBtn.type = 'button';

      editBtn.addEventListener('click', (e) => {
         e.preventDefault();
         e.stopPropagation();

         window.dispatchEvent(new CustomEvent('tzg:editItinerarySection', {
            detail: { step: 'date' }
         }));
      });

      actionsWrap.appendChild(editBtn);

      topRow.appendChild(textWrap);
      topRow.appendChild(actionsWrap);

      dateWrap.appendChild(topRow);

      return dateWrap;
   }
}
