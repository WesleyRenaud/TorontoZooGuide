import { HoverTooltipPositioner } from './hoverTooltipPositioner.js';

export class HoverFragment {
   static createHoverTooltip(hoverTooltipEl) {
      let anchorEl = null;

      function place() {
         if (!hoverTooltipEl || !anchorEl?.getBoundingClientRect) return;
         if (!HoverTooltipPositioner.isTooltipVisible(hoverTooltipEl)) return;

         const position = HoverTooltipPositioner.calculateTooltipPosition(
            anchorEl.getBoundingClientRect(),
            hoverTooltipEl.getBoundingClientRect(),
            HoverTooltipPositioner.pageZoom(hoverTooltipEl)
         );

         HoverTooltipPositioner.applyTooltipPosition(hoverTooltipEl, position);
      }

      function show(text, markerEl) {
         if (!hoverTooltipEl) return;

         hoverTooltipEl.textContent = text || '';
         hoverTooltipEl.style.display = text ? 'block' : 'none';
         anchorEl = markerEl?.getBoundingClientRect ? markerEl : null;

         if (anchorEl) place();
      }

      function hide() {
         if (!hoverTooltipEl) return;
         hoverTooltipEl.style.display = 'none';
         anchorEl = null;
      }

      function move() {}

      function reposition() {
         place();
      }

      return { show, hide, move, reposition };
   }
}
