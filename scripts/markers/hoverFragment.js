import { HoverTooltipPositioner } from './hoverTooltipPositioner.js';

export class HoverFragment {
   static createHoverTooltip(hoverTooltipEl) {
      function show(text, e) {
         if (!hoverTooltipEl) return;

         hoverTooltipEl.textContent = text || '';
         hoverTooltipEl.style.display = text ? 'block' : 'none';

         if (e) move(e);
      }

      function hide() {
         if (!hoverTooltipEl) return;
         hoverTooltipEl.style.display = 'none';
      }

      function move(e) {
         if (!HoverTooltipPositioner.isTooltipVisible(hoverTooltipEl)) return;

         const position = HoverTooltipPositioner.calculateTooltipPosition(
            e,
            hoverTooltipEl.getBoundingClientRect()
         );

         HoverTooltipPositioner.applyTooltipPosition(hoverTooltipEl, position);
      }

      return { show, hide, move };
   }
}
