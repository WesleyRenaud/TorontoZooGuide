import { el } from '../dom.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRemovedItemsPopupLayout({ isEmptyItinerary = false } = {}) {
   const root = el('div', 'tzg-popup');
   const overlay = el('div', 'itin-overlay');

   const card = el('section', 'itin-card itin-removed-popup-card');

   const topbar = el('div', 'itin-card-topbar itin-card-topbar-with-close');
   topbar.appendChild(
      el('div', 'itin-top-title', APP_STRINGS.itinerary.removedItems.itineraryUpdated)
   );

   const closeBtn = el('button', 'itin-close', APP_STRINGS.common.closeSymbol);
   closeBtn.type = 'button';
   topbar.appendChild(closeBtn);

   const body = el('div', 'itin-card-body itin-removed-popup-body');
   const content = el(
      'div',
      isEmptyItinerary
         ? 'itin-removed-popup-content itin-removed-popup-content-empty'
         : 'itin-removed-popup-content'
   );

   content.appendChild(
      el(
         'div',
         'itin-h1',
         isEmptyItinerary
            ? APP_STRINGS.itinerary.removedItems.emptyItineraryTitle
            : APP_STRINGS.itinerary.removedItems.someDetailsChanged
      )
   );

   content.appendChild(
      el(
         'div',
         'itin-subtitle',
         isEmptyItinerary
            ? APP_STRINGS.itinerary.removedItems.emptyItinerarySubtitle
            : APP_STRINGS.itinerary.removedItems.changedSubtitle
      )
   );

   body.appendChild(content);

   const actions = el('div', 'itin-card-actions');

   const okBtn = el(
      'button',
      'itin-finish',
      APP_STRINGS.itinerary.actions.accept
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
