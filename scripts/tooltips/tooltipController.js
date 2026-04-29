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
   restroomMessageBanner,
   giftShopClosedBanner,
   attractionClosedBanner,
   drinkingFountainClosedBanner }) {

   let openState = createEmptyOpenState();

   function createEmptyOpenState() {
      return {
         marker: null,
         items: [],
      };
   }

   function getOpenMarker() {
      return openState.marker;
   }

   function getOpenItems() {
      return openState.items;
   }

   function getOpenItem(index) {
      return getOpenItems()[index] || null;
   }

   function setOpenState(marker, items) {
      openState = {
         marker,
         items: Array.isArray(items) ? items : [],
      };
   }

   function resetOpenState() {
      openState = createEmptyOpenState();
   }

   const banners = createTooltipBannerSync({
      offDisplayBanner,
      restaurantClosedBanner,
      restroomMessageBanner,
      giftShopClosedBanner,
      attractionClosedBanner,
      drinkingFountainClosedBanner,
   });

   const carousel = createTooltipCarouselView({
      tooltipEl,
      getRendererForItem,
      onIndexChange: (index) => {
         syncMarkerToIndex(index);
         banners.sync(getOpenItem(index));
      },
   });

   const globalListeners = createTooltipGlobalListeners({
      tooltipEl,
      isOpen,
      close,
      step: (delta) => carousel.step(delta),
      getItemAtIndex: getOpenItem,
      onAnimalCardClick,
   });

   function isOpen() {
      return Boolean(getOpenMarker()) || isTooltipVisible();
   }

   function isTooltipVisible() {
      return tooltipEl && tooltipEl.style.display === 'flex';
   }

   function setTooltipVisibility(isVisible) {
      if (!tooltipEl) {
         return;
      }

      tooltipEl.style.display = isVisible ? 'flex' : 'none';
      tooltipEl.style.pointerEvents = isVisible ? 'auto' : 'none';
   }

   function restoreOpenMarkerVisual() {
      const marker = getOpenMarker();

      if (!marker) {
         return;
      }

      applyMarkerVisual(marker, getOpenItems() || marker.__items || []);
   }

   function addMarkerClickHandler(markerEl, items, clickable) {
      if (!clickable) {
         return;
      }

      markerEl.addEventListener('click', (event) => {
         event.stopPropagation();
         toggle(markerEl, items);
      });
   }

   function addMarkerHoverHandlers(markerEl, hover) {
      markerEl.addEventListener('mouseenter', (event) => {
         hover.show(markerEl.dataset.hover || '', event);
      });
      markerEl.addEventListener('mousemove', (event) => {
         hover.move(event);
      });
      markerEl.addEventListener('mouseleave', () => {
         hover.hide();
      });
   }

   function attachToMarker(markerEl, items, hover, opts = {}) {
      const clickable = opts.clickable !== false;

      addMarkerClickHandler(markerEl, items, clickable);
      addMarkerHoverHandlers(markerEl, hover);
   }

   function toggle(markerEl, items) {
      if (isOpen() && getOpenMarker() === markerEl) {
         close();
         return;
      }

      open(markerEl, items);
   }

   function open(markerEl, items) {
      if (!tooltipEl || !markerEl) {
         return;
      }

      close();
      setOpenState(markerEl, items);

      if (!carousel.render(getOpenItems())) {
         banners.sync(getOpenItem(0));
         globalListeners.install();
         return;
      }

      setTooltipVisibility(true);
      globalListeners.install();
      carousel.showFirst();
      positionTooltip(tooltipEl, markerEl);
   }

   function close() {
      if (!tooltipEl) {
         resetOpenState();
         return;
      }

      globalListeners.uninstall();
      banners.hideAll();
      restoreOpenMarkerVisual();
      setTooltipVisibility(false);
      carousel.clear();
      resetOpenState();
   }

   function syncMarkerToIndex(index) {
      const marker = getOpenMarker();
      const item = getOpenItem(index);

      if (!marker || !item) {
         return;
      }

      const type = String(item.type || '');
      if (type !== 'animal') {
         return;
      }

      setMarkerToAnimalIcon(marker, item);
   }

   function jumpTo(matchFn) {
      carousel.jumpTo(matchFn);
   }

   function reposition() {
      const marker = getOpenMarker();

      if (!tooltipEl || !isTooltipVisible() || !marker) {
         return;
      }

      positionTooltip(tooltipEl, marker);
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
