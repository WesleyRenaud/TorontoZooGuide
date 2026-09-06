import { Dom } from '../dom.js';
import { Strings } from '../../../strings.js';

export class RemovedItemsPopupLayout {
   static createRemovedItemsPopupLayout({ isEmptyItinerary = false } = {}) {
      const root = Dom.el('div', 'tzg-popup');
      const overlay = Dom.el('div', 'itin-overlay');

      const card = Dom.el('section', 'itin-card itin-removed-popup-card');

      const topbar = Dom.el('div', 'itin-card-topbar itin-card-topbar-with-close');
      topbar.appendChild(
         Dom.el('div', 'itin-top-title', Strings.itinerary.removedItems.itineraryUpdated)
      );

      const closeBtn = Dom.el('button', 'itin-close', Strings.common.closeSymbol);
      closeBtn.type = 'button';
      topbar.appendChild(closeBtn);

      const body = Dom.el('div', 'itin-card-body itin-removed-popup-body');
      const content = Dom.el(
         'div',
         isEmptyItinerary
            ? 'itin-removed-popup-content itin-removed-popup-content-empty'
            : 'itin-removed-popup-content'
      );

      content.appendChild(
         Dom.el(
            'div',
            'itin-h1',
            isEmptyItinerary
               ? Strings.itinerary.removedItems.emptyItineraryTitle
               : Strings.itinerary.removedItems.someDetailsChanged
         )
      );

      content.appendChild(
         Dom.el(
            'div',
            'itin-subtitle',
            isEmptyItinerary
               ? Strings.itinerary.removedItems.emptyItinerarySubtitle
               : Strings.itinerary.removedItems.changedSubtitle
         )
      );

      body.appendChild(content);

      const actions = Dom.el('div', 'itin-card-actions');

      const okBtn = Dom.el(
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
