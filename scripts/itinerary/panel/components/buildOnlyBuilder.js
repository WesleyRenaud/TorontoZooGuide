import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { Strings } from '../../../strings.js';

export class BuildOnlyBuilder {
   static renderBuildOnly(body) {
      const wrap = ItineraryPanelHelper.el('div', 'itin-panel-actions-wrap');
      const buildBtn = ItineraryPanelHelper.el(
         'button',
         'itin-panel-build-btn',
         Strings.itinerary.actions.build
      );
      buildBtn.type = 'button';
      buildBtn.addEventListener('click', (e) => {
         e.stopPropagation();
         window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
      });
      wrap.appendChild(buildBtn);
      body.appendChild(wrap);
   }
}
