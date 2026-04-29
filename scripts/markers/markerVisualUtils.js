import { likelihoodToColor } from '../likelihood/likelihoodColors.js';
import { clampLikelihood } from '../likelihood/likelihoodScale.js';

const DEFAULT_STACK_MARKER_COLOR = 'rgba(94,150,0,0.95)';

const MARKER_TYPE_CLASSES = [
   'marker-restaurant',
   'marker-restroom',
   'marker-gift-shop',
   'marker-attraction',
   'marker-zoomobile-station',
   'marker-zoomobile-route-marker',
   'marker-guardians-talk',
   'marker-wild-encounter',
   'marker-drinking-fountain',
   'marker-has-limited-viewing',
];

export function resetMarkerVisual(markerEl) {
   markerEl.textContent = '';
   markerEl.style.backgroundImage = 'none';
   markerEl.style.backgroundColor = 'transparent';
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.style.width = '';
   markerEl.style.height = '';

   markerEl.classList.remove(...MARKER_TYPE_CLASSES);
}

export function applyMarkerClass(markerEl, className) {
   if (className) {
      markerEl.classList.add(className);
   }
}

export function applyCountMarker(
   markerEl,
   count,
   backgroundColor = DEFAULT_STACK_MARKER_COLOR
) {
   markerEl.style.backgroundImage = 'none';
   markerEl.style.backgroundColor = backgroundColor;
   markerEl.textContent = String(count);
}

export function applyBackgroundImage(
   markerEl,
   iconUrl,
   backgroundColor = 'transparent'
) {
   markerEl.style.backgroundColor = backgroundColor;
   markerEl.style.backgroundImage = String(iconUrl || '').startsWith('url(')
      ? iconUrl
      : `url("${iconUrl}")`;
   markerEl.style.backgroundRepeat = 'no-repeat';
   markerEl.style.backgroundPosition = 'center';
   markerEl.style.backgroundSize = 'cover';
   markerEl.textContent = '';
}

export function applyGenericIcon(markerEl, iconUrl, count) {
   if (count > 1) {
      applyCountMarker(markerEl, count);
      return;
   }

   applyBackgroundImage(markerEl, iconUrl);
}

export { clampLikelihood };

export function getLikelihoodVisual(likelihood) {
   const clampedLikelihood = clampLikelihood(likelihood);
   const colour = likelihoodToColor(clampedLikelihood);
   const iconToken = clampedLikelihood >= 100
      ? 'open'
      : String(colour || '').replace('#', '');

   return {
      colour,
      iconToken,
      likelihood: clampedLikelihood,
   };
}
