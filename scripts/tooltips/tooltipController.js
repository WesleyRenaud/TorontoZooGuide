import { getRendererForItem } from './tooltipRenderers.js';
import { positionTooltip } from './positionTooltip.js';
import { setMarkerToAnimalIcon, applyMarkerVisual } from '../markers/markerVisuals.js';
import { createTooltipBannerSync } from './bannerSync.js';
import { createTooltipCarouselView } from './carouselView.js';
import { createTooltipGlobalListeners } from './globalListeners.js';

export function createTooltipController({
   tooltipEl,
   onAnimalCardClick,
   offDisplayBanner,
   restaurantClosedBanner,
   giftShopClosedBanner,
   attractionClosedBanner }) {

   let openMarker = null;
   let itemsForOpen = [];

   const banners = createTooltipBannerSync({
      offDisplayBanner,
      restaurantClosedBanner,
      giftShopClosedBanner,
      attractionClosedBanner,
   });

   const carousel = createTooltipCarouselView({
      tooltipEl,
      getRendererForItem,
      onIndexChange: (index) => {
         syncMarkerToIndex(index);
         banners.sync(itemsForOpen[index] || null);
      },
   });

   const globalListeners = createTooltipGlobalListeners({
      tooltipEl,
      isOpen,
      close,
      step: (delta) => carousel.step(delta),
      getItemAtIndex: (index) => itemsForOpen[index] || null,
      onAnimalCardClick,
   });

   function isOpen() {
      return tooltipEl && tooltipEl.style.display === 'flex';
   }

   function attachToMarker(markerEl, items, hover, opts = {}) {
      const clickable = opts.clickable !== false;

      if (clickable) {
         markerEl.addEventListener('click', (e) => {
            e.stopPropagation();
            toggle(markerEl, items);
         });
      }

      markerEl.addEventListener('mouseenter', (e) => hover.show(markerEl.dataset.hover || '', e));
      markerEl.addEventListener('mousemove', (e) => hover.move(e));
      markerEl.addEventListener('mouseleave', () => hover.hide());
   }

   function toggle(markerEl, items) {
      if (isOpen() && openMarker === markerEl) close();
      else open(markerEl, items);
   }

   function open(markerEl, items) {
      if (!tooltipEl) return;
      if (isOpen()) close();

      openMarker = markerEl;
      itemsForOpen = items || [];

      if (!carousel.render(itemsForOpen)) {
         openMarker = null;
         itemsForOpen = [];
         return;
      }

      tooltipEl.style.display = 'flex';
      tooltipEl.style.pointerEvents = 'auto';
      positionTooltip(tooltipEl, markerEl);

      globalListeners.install();
      carousel.showIndex(0);
   }

   function close() {
      if (!tooltipEl || !isOpen()) return;

      banners.hideAll();

      if (openMarker) {
         applyMarkerVisual(openMarker, itemsForOpen || openMarker.__items || []);
      }

      tooltipEl.style.display = 'none';
      tooltipEl.style.pointerEvents = 'none';
      carousel.clear();
      openMarker = null;
      itemsForOpen = [];
   }

   function syncMarkerToIndex(index) {
      if (!openMarker) return;

      const item = itemsForOpen[index] || null;
      if (!item) return;

      const type = String(item.type || '');
      if (type !== 'animal') return;

      setMarkerToAnimalIcon(openMarker, item);
   }

   function jumpTo(matchFn) {
      carousel.jumpTo(itemsForOpen, matchFn);
   }

   function getOpenItems() {
      return itemsForOpen;
   }

   function reposition() {
      if (!tooltipEl || !isOpen() || !openMarker) {
         return;
      }

      positionTooltip(tooltipEl, openMarker);
   }

   return {
      attachToMarker,
      open,
      close,
      toggle,
      jumpTo,
      getOpenItems,
      reposition,
   };
}
