import { getRendererForItem } from './tooltipRenderers.js';
import { positionTooltip } from '../utils/dom.js';

export function createTooltipController({ tooltipEl, onAnimalCardClick }) {
   let openMarker = null;
   let itemsForOpen = [];
   let carouselEl = null;
   let listenersInstalled = false;

   function isOpen() {
      return tooltipEl && tooltipEl.style.display === 'flex';
   }

   function attachToMarker(markerEl, items, hover) {
      markerEl.addEventListener('click', (e) => {
         e.stopPropagation();
         toggle(markerEl, items);
      });

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
      carouselEl = null;

      render(itemsForOpen);

      tooltipEl.style.display = 'flex';
      tooltipEl.style.pointerEvents = 'auto';
      positionTooltip(tooltipEl, markerEl);

      installGlobalListeners();
   }

   function close() {
      if (!tooltipEl || !isOpen()) return;
      tooltipEl.style.display = 'none';
      tooltipEl.style.pointerEvents = 'none';
      tooltipEl.innerHTML = '';
      openMarker = null;
      itemsForOpen = [];
      carouselEl = null;
   }

   function render(items) {
      tooltipEl.innerHTML = '';

      const content = document.createElement('div');
      content.className = 'tooltip-content';

      carouselEl = document.createElement('div');
      carouselEl.className = 'tooltip-carousel';
      carouselEl.dataset.index = 0;

      items.forEach((item, i) => {
         const renderer = getRendererForItem(item);
         carouselEl.appendChild(renderer.createCard(item, i));
      });

      content.appendChild(carouselEl);
      tooltipEl.appendChild(content);

      if (items.length > 1) tooltipEl.appendChild(createNav());
      else tooltipEl.classList.add('no-arrows');
   }

   function createNav() {
      const nav = document.createElement('div');
      nav.className = 'tooltip-nav';

      const left = createArrow('<', () => step(-1));
      left.classList.add('tooltip-prev', 'visible');

      const right = createArrow('>', () => step(+1));
      right.classList.add('tooltip-next', 'visible');

      nav.appendChild(left);
      nav.appendChild(document.createElement('div'));
      nav.appendChild(right);
      return nav;
   }

   function createArrow(symbol, onClick) {
      const el = document.createElement('div');
      el.className = 'tooltip-arrow';
      el.textContent = symbol;
      el.addEventListener('click', (e) => {
         e.stopPropagation();
         onClick();
      });
      return el;
   }

   function step(delta) {
      if (!carouselEl) return;
      const cards = Array.from(carouselEl.children);
      if (cards.length === 0) return;

      let index = Number(carouselEl.dataset.index || 0);
      cards[index].style.display = 'none';

      index = (index + delta + cards.length) % cards.length;
      cards[index].style.display = 'flex';
      carouselEl.dataset.index = index;
   }

   function installGlobalListeners() {
      if (listenersInstalled) return;
      listenersInstalled = true;

      document.addEventListener('click', (e) => {
         const speciesLink = e.target.closest('.species-link');
         if (speciesLink) {
         e.stopPropagation();
         const idx = Number(speciesLink.dataset.index);
         const item = itemsForOpen[idx];
         if (onAnimalCardClick) onAnimalCardClick(item);
         return;
         }

         if (!isOpen()) return;
         const clickedMarker = e.target.closest('.marker');
         const clickedTooltip = tooltipEl.contains(e.target);
         if (!clickedMarker && !clickedTooltip) close();
      });

      document.addEventListener('keydown', (e) => {
         if (!isOpen()) return;
         if (e.key === 'Escape') close();
         if (e.key === 'ArrowRight') step(+1);
         if (e.key === 'ArrowLeft') step(-1);
      });
   }

   function jumpTo(matchFn) {
      if (!carouselEl) return;

      const items = itemsForOpen;
      const idx = items.findIndex(matchFn);
      const newIndex = idx >= 0 ? idx : 0;

      const cards = Array.from(carouselEl.children);
      cards.forEach((c) => (c.style.display = 'none'));
      if (cards[newIndex]) cards[newIndex].style.display = 'flex';
      carouselEl.dataset.index = newIndex;
   }

   function getOpenItems() {
      return itemsForOpen;
   }

   return { attachToMarker, open, close, toggle, jumpTo, getOpenItems };
}