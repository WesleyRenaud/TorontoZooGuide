export function createTooltipCarouselView({
   tooltipEl,
   getRendererForItem,
   onIndexChange,
}) {
   let carouselEl = null;

   function clear() {
      tooltipEl.innerHTML = '';
      carouselEl = null;
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

   function render(items) {
      clear();

      const first = items?.[0] || null;
      const firstRenderer = first ? getRendererForItem(first) : null;

      if (!firstRenderer) {
         return false;
      }

      const content = document.createElement('div');
      content.className = 'tooltip-content';

      carouselEl = document.createElement('div');
      carouselEl.className = 'tooltip-carousel';
      carouselEl.dataset.index = '0';

      items.forEach((item, index) => {
         const renderer = getRendererForItem(item);

         if (!renderer) {
            return;
         }

         carouselEl.appendChild(renderer.createCard(item, index));
      });

      content.appendChild(carouselEl);
      tooltipEl.appendChild(content);

      if (items.length > 1) {
         tooltipEl.classList.remove('no-arrows');
         tooltipEl.appendChild(createNav());
      } else {
         tooltipEl.classList.add('no-arrows');
      }

      return carouselEl.children.length > 0;
   }

   function showIndex(newIndex) {
      if (!carouselEl) {
         return;
      }

      const cards = Array.from(carouselEl.children);

      if (cards.length === 0) {
         return;
      }

      const safeIndex = Math.max(0, Math.min(cards.length - 1, newIndex));

      cards.forEach((card) => {
         card.style.display = 'none';
      });

      if (cards[safeIndex]) {
         cards[safeIndex].style.display = 'flex';
      }

      carouselEl.dataset.index = String(safeIndex);
      onIndexChange?.(safeIndex);
   }

   function step(delta) {
      if (!carouselEl) {
         return;
      }

      const cards = Array.from(carouselEl.children);

      if (cards.length === 0) {
         return;
      }

      let index = Number(carouselEl.dataset.index || 0);

      if (!Number.isFinite(index)) {
         index = 0;
      }

      index = (index + delta + cards.length) % cards.length;
      showIndex(index);
   }

   function jumpTo(items, matchFn) {
      if (!carouselEl) {
         return;
      }

      const index = items.findIndex(matchFn);
      showIndex(index >= 0 ? index : 0);
   }

   return {
      clear,
      render,
      showIndex,
      step,
      jumpTo,
   };
}
