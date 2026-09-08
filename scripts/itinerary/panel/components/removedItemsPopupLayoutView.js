import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { Strings } from '../../../strings.js';

export class RemovedItemsPopupLayoutView {
   static createRemovedItemsPopupLayout({ isEmptyItinerary = false } = {}) {
      const root = ItineraryPanelHelper.el('div', 'tzg-popup');
      const overlay = ItineraryPanelHelper.el('div', 'itin-overlay');

      const card = ItineraryPanelHelper.el('section', 'itin-card itin-removed-popup-card');

      const topbar = ItineraryPanelHelper.el('div', 'itin-card-topbar itin-card-topbar-with-close');
      topbar.appendChild(
         ItineraryPanelHelper.el('div', 'itin-top-title', Strings.itinerary.removedItems.itineraryUpdated)
      );

      const closeBtn = ItineraryPanelHelper.el('button', 'itin-close', Strings.common.closeSymbol);
      closeBtn.type = 'button';
      topbar.appendChild(closeBtn);

      const body = ItineraryPanelHelper.el('div', 'itin-card-body itin-removed-popup-body');
      const content = ItineraryPanelHelper.el(
         'div',
         isEmptyItinerary
            ? 'itin-removed-popup-content itin-removed-popup-content-empty'
            : 'itin-removed-popup-content'
      );

      content.appendChild(
         ItineraryPanelHelper.el(
            'div',
            'itin-h1',
            isEmptyItinerary
               ? Strings.itinerary.removedItems.emptyItineraryTitle
               : Strings.itinerary.removedItems.someDetailsChanged
         )
      );

      content.appendChild(
         ItineraryPanelHelper.el(
            'div',
            'itin-subtitle',
            isEmptyItinerary
               ? Strings.itinerary.removedItems.emptyItinerarySubtitle
               : Strings.itinerary.removedItems.changedSubtitle
         )
      );

      body.appendChild(content);

      const actions = ItineraryPanelHelper.el('div', 'itin-card-actions');

      const okBtn = ItineraryPanelHelper.el(
         'button',
         'itin-finish',
         Strings.itinerary.actions.accept
      );
      okBtn.type = 'button';
      actions.appendChild(okBtn);

      card.appendChild(topbar);
      card.appendChild(body);
      card.appendChild(actions);

      overlay.appendChild(card);
      root.appendChild(overlay);

      return {
         root,
         overlay,
         content,
         closeBtn,
         okBtn,
      };
   }
}
