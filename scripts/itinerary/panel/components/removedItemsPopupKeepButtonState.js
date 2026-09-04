import { APP_STRINGS } from '../../../strings.js';

export class RemovedItemsPopupKeepButtonState {
   static getKeepOverrideButtonState(
      isSelected,
      strings = APP_STRINGS
   ) {
      const selected = Boolean(isSelected);
      const removedItemsStrings = strings.itinerary.removedItems;

      return {
         selected,
         textContent: selected
            ? strings.itinerary.dayPlanner.remove
            : removedItemsStrings.keepInItinerary,
         title: selected ? removedItemsStrings.removeFromItineraryHint : '',
         ariaPressed: selected ? 'true' : 'false',
      };
   }

   static applyKeepOverrideButtonState(button, state) {
      button.classList.toggle('is-selected', state.selected);
      button.setAttribute('aria-pressed', state.ariaPressed);
      button.textContent = state.textContent;
      button.title = state.title;
   }
}
