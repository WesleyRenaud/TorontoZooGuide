import { ItineraryPanelDom } from '../itineraryPanelDom.js';

export class ItineraryPanelPopupBuilder {
   static joinClassNames(...classNames) {
      return classNames.filter(Boolean).join(' ');
   }

   static createPopupButton({
      className,
      text,
   } = {}) {
      const button = ItineraryPanelDom.el('button', className, text);
      button.type = 'button';
      return button;
   }
}
