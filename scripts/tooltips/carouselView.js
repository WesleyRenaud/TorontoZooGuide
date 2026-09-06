import { Strings } from '../strings.js';

export class CarouselView {
   static createTooltipCarouselView({
   tooltipEl,
   getRendererForItem,
   onIndexChange,
}) {
      let carouselEl = null;
      let itemsForCarousel = [];
      let renderedItemIndices = [];

      function getCards() {
         return Array.from(carouselEl?.children ?? []);
      }

      function getCardCount() {
         return getCards().length;
      }

      function getCurrentPosition() {
         const position = Number(carouselEl?.dataset.position ?? 0);
         return Number.isFinite(position) ? position : 0;
      }

      function setCurrentPosition(position) {
         if (!carouselEl) {
            return;
         }

         carouselEl.dataset.position = String(position);
      }

      function clear() {
         tooltipEl.replaceChildren();
         tooltipEl.classList.add('no-arrows');
         carouselEl = null;
         itemsForCarousel = [];
         renderedItemIndices = [];
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

         const left = createArrow(Strings.common.previousSymbol, () => step(-1));
         left.classList.add('tooltip-prev', 'visible');

         const right = createArrow(Strings.common.nextSymbol, () => step(+1));
         right.classList.add('tooltip-next', 'visible');

         nav.appendChild(left);
         nav.appendChild(document.createElement('div'));
         nav.appendChild(right);
         return nav;
      }

      function createCardEntries(items) {
         return items.flatMap((item, index) => {
            const renderer = getRendererForItem(item);

            if (!renderer) {
               return [];
            }

            return [{
               itemIndex: index,
               card: renderer.createCard(item, index),
            }];
         });
      }

      function render(items) {
         clear();
         itemsForCarousel = Array.isArray(items) ? items : [];

         const content = document.createElement('div');
         content.className = 'tooltip-content';

         carouselEl = document.createElement('div');
         carouselEl.className = 'tooltip-carousel';
         setCurrentPosition(0);

         const entries = createCardEntries(itemsForCarousel);
         renderedItemIndices = entries.map(({ itemIndex }) => itemIndex);

         entries.forEach(({ card }) => {
            carouselEl.appendChild(card);
         });

         if (getCardCount() === 0) {
            clear();
            return false;
         }

         content.appendChild(carouselEl);
         tooltipEl.appendChild(content);

         if (getCardCount() > 1) {
            tooltipEl.classList.remove('no-arrows');
            tooltipEl.appendChild(createNav());
         } else {
            tooltipEl.classList.add('no-arrows');
         }

         return true;
      }

      function showIndex(position) {
         if (!carouselEl) {
            return;
         }

         const cards = getCards();

         if (cards.length === 0 || renderedItemIndices.length === 0) {
            return;
         }

         const safePosition = Math.max(0, Math.min(cards.length - 1, position));

         cards.forEach((card) => {
            card.style.display = 'none';
         });

         if (cards[safePosition]) {
            cards[safePosition].style.display = 'flex';
         }

         setCurrentPosition(safePosition);
         onIndexChange?.(renderedItemIndices[safePosition] ?? 0);
      }

      function showFirst() {
         showIndex(0);
      }

      function step(delta) {
         if (!carouselEl || renderedItemIndices.length === 0) {
            return;
         }

         const nextPosition = (
            getCurrentPosition() + delta + renderedItemIndices.length
         ) % renderedItemIndices.length;

         showIndex(nextPosition);
      }

      function jumpTo(matchFn) {
         if (!carouselEl) {
            return;
         }

         const itemIndex = itemsForCarousel.findIndex(matchFn);
         const position = renderedItemIndices.indexOf(itemIndex);
         showIndex(position >= 0 ? position : 0);
      }

      return {
         clear,
         render,
         showFirst,
         showIndex,
         step,
         jumpTo,
      };
   }
}
