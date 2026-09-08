import { DraftStore } from '../../draftStore.js';
import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { Strings } from '../../../strings.js';

export class DateView {
   static makeDateCard(itin = {}) {
      const date = itin.date || DraftStore.getStoredItineraryDate();
      const prettyDate = ItineraryItemFormatter.formatISODateLong(date);

      if (!prettyDate) return null;

      const dateWrap = ItineraryPanelHelper.el('div', 'itin-panel-date');

      const topRow = ItineraryPanelHelper.el('div', 'itin-panel-date-top');
      const textWrap = ItineraryPanelHelper.el('div', 'itin-panel-date-text');

      textWrap.appendChild(ItineraryPanelHelper.el('div', 'itin-panel-date-label', Strings.itinerary.selectors.visitDate));
      textWrap.appendChild(ItineraryPanelHelper.el('div', 'itin-panel-date-value', prettyDate));

      const actionsWrap = ItineraryPanelHelper.el('div', 'itin-panel-header-actions');

      const editBtn = ItineraryPanelHelper.el('button', 'itin-panel-section-edit-btn', Strings.itinerary.actions.edit);
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
