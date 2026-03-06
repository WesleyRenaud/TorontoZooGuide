// scripts/itinerary/panel/components/buildOnly.js
import { el } from '../dom.js';

export function renderBuildOnly(body) {
   const wrap = el('div', 'itin-panel-actions-wrap');
   const buildBtn = el('button', 'itin-panel-build-btn', 'Build Itinerary');
   buildBtn.type = 'button';
   buildBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });
   wrap.appendChild(buildBtn);
   body.appendChild(wrap);
}