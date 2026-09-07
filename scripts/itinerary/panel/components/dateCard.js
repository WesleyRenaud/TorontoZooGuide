import { DraftStorage } from '../../draftStorage.js';
import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { Strings } from '../../../strings.js';

export class DateCard {
   static makeDateCard(itin = {}) {
      const date = itin.date || DraftStorage.getStoredItineraryDate();
      const prettyDate = ItineraryItemFormatter.formatISODateLong(date);

      if (!prettyDate) return null;

      const dateWrap = ItineraryPanelDom.el('div', 'itin-panel-date');

      const topRow = ItineraryPanelDom.el('div', 'itin-panel-date-top');
      const textWrap = ItineraryPanelDom.el('div', 'itin-panel-date-text');

      textWrap.appendChild(ItineraryPanelDom.el('div', 'itin-panel-date-label', Strings.itinerary.selectors.visitDate));
      textWrap.appendChild(ItineraryPanelDom.el('div', 'itin-panel-date-value', prettyDate));

      const actionsWrap = ItineraryPanelDom.el('div', 'itin-panel-header-actions');

      const editBtn = ItineraryPanelDom.el('button', 'itin-panel-section-edit-btn', Strings.itinerary.actions.edit);
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
