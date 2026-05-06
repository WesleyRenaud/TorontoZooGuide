import { el } from '../dom.js';
import { APP_STRINGS } from '../../../strings.js';

export function renderBuildOnly(body) {
   const wrap = el('div', 'itin-panel-actions-wrap');
   const buildBtn = el(
      'button',
      'itin-panel-build-btn',
      APP_STRINGS.itinerary.actions.build
   );
   buildBtn.type = 'button';
   buildBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });
   wrap.appendChild(buildBtn);
   body.appendChild(wrap);
}
