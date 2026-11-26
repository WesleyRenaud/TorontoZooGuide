import { BannerSynchronizer } from './bannerSynchronizer.js';
import { CarouselView } from './carouselView.js';
import { GlobalListener } from './globalListener.js';
import { MarkerHelper } from '../markers/markerHelper.js';
import { PositionFragment } from './positionFragment.js';
import { ItemType } from '../shared/enums/itemType.js';
import { Strings } from '../strings.js';
import { TooltipFocusManager } from './tooltipFocusManager.js';
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
            focusManager.recoverFocus();
         },
         onClose: () => close(),
      });

      const globalListeners = GlobalListener.createTooltipGlobalListeners({
         tooltipEl,
         isOpen,
         close,
         step: (delta) => carousel.step(delta),
         getItemAtIndex: getOpenItem,
         onAnimalCardClick,
      });

      const focusManager = TooltipFocusManager.createTooltipFocusManager({
         tooltipEl,
         getOpener: getOpenMarker,
         isOpen,
         onFocusLeave: () => close(),
      });

      focusManager.install();

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

      function addMarkerClickHandler(markerEl, items, clickable, hover) {
         if (!clickable) {
            return;
         }

         markerEl.setAttribute('role', 'button');
         markerEl.setAttribute('tabindex', '0');
         markerEl.setAttribute('aria-label', getMarkerLabel(markerEl));
         markerEl.setAttribute('aria-expanded', 'false');

         if (tooltipEl?.id) {
            markerEl.setAttribute('aria-controls', tooltipEl.id);
         }

         markerEl.addEventListener('click', (event) => {
            event.stopPropagation();
            hover?.hide?.();
            toggle(markerEl, items, { moveFocus: true });
         });
         markerEl.addEventListener('keydown', (event) => {
            if (isForwardTab(event) && isOpenFor(markerEl)) {
               event.preventDefault();
               focusManager.focusInitial();
               return;
            }

            if (event.key !== 'Enter' && event.key !== ' ') {
               return;
            }

            event.preventDefault();
            event.stopPropagation();
            hover?.hide?.();
            toggle(markerEl, items, { moveFocus: true });
         });
      }

      function isForwardTab(event) {
         return event.key === 'Tab'
            && !event.shiftKey
            && !event.altKey
            && !event.ctrlKey
            && !event.metaKey;
      }

      function isOpenFor(markerEl) {
         return isTooltipVisible() && getOpenMarker() === markerEl;
      }

      function getMarkerLabel(markerEl) {
         return markerEl?.dataset?.hover || Strings.map.markerAria;
      }

      function setMarkerExpanded(markerEl, isExpanded) {
         if (markerEl?.getAttribute?.('aria-expanded') == null) {
            return;
         }

         markerEl.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
      }

      function addMarkerHoverHandlers(markerEl, hover) {
         markerEl.addEventListener('mouseenter', () => {
            hover.show(markerEl.dataset.hover || '', markerEl);
         });
         markerEl.addEventListener('mousemove', () => {
            hover.move();
         });
         markerEl.addEventListener('mouseleave', () => {
            hover.hide();
         });
      }

      function attachToMarker(markerEl, items, hover, opts = {}) {
         const clickable = opts.clickable !== false;

         addMarkerClickHandler(markerEl, items, clickable, hover);
         addMarkerHoverHandlers(markerEl, hover);
      }

      function toggle(markerEl, items, opts = {}) {
         if (isOpen() && getOpenMarker() === markerEl) {
            close();
            return;
         }

         open(markerEl, items, opts);
      }

      function open(markerEl, items, { moveFocus = false } = {}) {
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

         tooltipEl.setAttribute('aria-label', Strings.tooltips.detailsAria(getMarkerLabel(markerEl)));
         setTooltipVisibility(true);
         setMarkerExpanded(markerEl, true);
         globalListeners.install();
         carousel.showFirst();
         PositionFragment.positionTooltip(tooltipEl, markerEl);

         if (moveFocus) {
            focusManager.focusInitial();
         }
      }

      function close() {
         if (!tooltipEl) {
            resetOpenState();
            return;
         }

         const shouldRestoreFocus = focusManager.containsFocus();

         globalListeners.uninstall();
         banners.hideAll();
         setMarkerExpanded(getOpenMarker(), false);
         restoreOpenMarkerVisual();
         setTooltipVisibility(false);
         carousel.clear();

         if (shouldRestoreFocus) {
            focusManager.restoreFocusToOpener();
         }

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
