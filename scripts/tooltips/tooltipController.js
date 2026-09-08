import { BannerSynchronizer } from './bannerSynchronizer.js';
import { CarouselView } from './carouselView.js';
import { GlobalListener } from './globalListener.js';
import { MarkerHelper } from '../markers/markerHelper.js';
import { PositionFragment } from './positionFragment.js';
import { ItemType } from '../shared/enums/itemType.js';
import { TooltipRenderer } from './tooltipRenderer.js';

export class TooltipController {
   static createTooltipController({
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

      const banners = BannerSynchronizer.createTooltipBannerSync({
         offDisplayBanner,
         restaurantClosedBanner,
         restroomMessageBanner,
         giftShopClosedBanner,
         attractionClosedBanner,
         drinkingFountainClosedBanner,
      });

      const carousel = CarouselView.createTooltipCarouselView({
         tooltipEl,
         getRendererForItem: TooltipRenderer.getRendererForItem,
         onIndexChange: (index) => {
            syncMarkerToIndex(index);
            banners.sync(getOpenItem(index));
         },
      });

      const globalListeners = GlobalListener.createTooltipGlobalListeners({
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
         tooltipEl.style.display = isVisible ? 'flex' : 'none';
         tooltipEl.style.pointerEvents = isVisible ? 'auto' : 'none';
      }

      function restoreOpenMarkerVisual() {
         const marker = getOpenMarker();

         if (!marker) {
            return;
         }

         MarkerHelper.applyMarkerVisual(marker, getOpenItems() || marker.__items || []);
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
         PositionFragment.positionTooltip(tooltipEl, markerEl);
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
         if (type !== ItemType.ANIMAL) {
            return;
         }

         MarkerHelper.setMarkerToAnimalIcon(marker, item);
      }

      function jumpTo(matchFn) {
         carousel.jumpTo(matchFn);
      }

      function reposition() {
         const marker = getOpenMarker();

         if (!tooltipEl || !isTooltipVisible() || !marker) {
            return;
         }

         PositionFragment.positionTooltip(tooltipEl, marker);
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
}
