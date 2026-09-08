import { LikelihoodColors } from '../likelihood/likelihoodColors.js';
import { LikelihoodScale } from '../likelihood/likelihoodScale.js';

export class MarkerVisualHelper {
   static DEFAULT_STACK_MARKER_COLOR = '#5e9600f2';

   static MARKER_TYPE_CLASSES = [
      'marker-restaurant',
      'marker-restroom',
      'marker-gift-shop',
      'marker-attraction',
      'marker-zoomobile-station',
      'marker-zoomobile-route-marker',
      'marker-guardians-talk',
      'marker-wild-encounter',
      'marker-drinking-fountain',
      'marker-defibrillator',
      'marker-emergency-intercom',
      'marker-guest-service',
      'marker-guest-service-first-aid',
      'marker-picnic-site',
      'marker-event-site',
      'marker-has-limited-viewing',
   ];

   static resetMarkerVisual(markerEl) {
      markerEl.textContent = '';
      markerEl.style.backgroundImage = 'none';
      markerEl.style.backgroundColor = 'transparent';
      markerEl.style.backgroundRepeat = 'no-repeat';
      markerEl.style.backgroundPosition = 'center';
      markerEl.style.backgroundSize = 'cover';
      markerEl.style.width = '';
      markerEl.style.height = '';

      markerEl.classList.remove(...MarkerVisualHelper.MARKER_TYPE_CLASSES);
   }

   static applyMarkerClass(markerEl, className) {
      if (className) {
         markerEl.classList.add(className);
      }
   }

   static applyCountMarker(
      markerEl,
      count,
      backgroundColor = MarkerVisualHelper.DEFAULT_STACK_MARKER_COLOR
   ) {
      markerEl.style.backgroundImage = 'none';
      markerEl.style.backgroundColor = backgroundColor;
      markerEl.textContent = String(count);
   }

   static applyBackgroundImage(
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

   static applyGenericIcon(markerEl, iconUrl, count) {
      if (count > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, count);
         return;
      }

      MarkerVisualHelper.applyBackgroundImage(markerEl, iconUrl);
   }

   static clampLikelihood = LikelihoodScale.clampLikelihood;

   static getLikelihoodVisual(likelihood) {
      const clampedLikelihood = LikelihoodScale.clampLikelihood(likelihood);
      const colour = LikelihoodColors.likelihoodToColor(clampedLikelihood);
      const iconToken = clampedLikelihood >= 100
         ? 'open'
         : String(colour || '').replace('#', '');

      return {
         colour,
         iconToken,
         likelihood: clampedLikelihood,
      };
   }
}
