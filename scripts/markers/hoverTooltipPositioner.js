export class HoverTooltipPositioner {
   static HOVER_TOOLTIP_POSITION = Object.freeze({
      viewportPadding: 14,
      cursorOffsetX: 18,
      cursorOffsetY: 22,
   });

   static unitPx() {
      const probe = document.createElement('div');
      probe.style.position = 'absolute';
      probe.style.visibility = 'hidden';
      probe.style.pointerEvents = 'none';
      probe.style.width = 'var(--hover-tooltip-px)';
      document.documentElement.appendChild(probe);
      const { width } = probe.getBoundingClientRect();
      probe.remove();
      return width;
   }

   static length(px) {
      return HoverTooltipPositioner.unitPx() * px;
   }

   static isTooltipVisible(hoverTooltipEl) {
      return Boolean(
         hoverTooltipEl
         && hoverTooltipEl.style.display !== 'none'
      );
   }

   static clampToViewport(value, size, viewportSize) {
      const viewportPadding = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
      );

      return Math.max(
         viewportPadding,
         Math.min(viewportSize - size - viewportPadding, value)
      );
   }

   static calculateTooltipPosition(event, tooltipRect) {
      const cursorOffsetX = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.cursorOffsetX
      );
      const cursorOffsetY = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.cursorOffsetY
      );
      const viewportPadding = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
      );

      let x = event.clientX + cursorOffsetX;
      let y = event.clientY - tooltipRect.height - cursorOffsetY;

      if (y < viewportPadding) {
         y = event.clientY + cursorOffsetY;
      }

      return {
         x: HoverTooltipPositioner.clampToViewport(x, tooltipRect.width, window.innerWidth),
         y: HoverTooltipPositioner.clampToViewport(y, tooltipRect.height, window.innerHeight),
      };
   }

   static pageZoom(hoverTooltipEl) {
      if (typeof getComputedStyle !== 'function' || typeof hoverTooltipEl?.closest !== 'function') {
         return 1;
      }

      const zoomed = hoverTooltipEl.closest('.home-page, .console-operations-page');
      if (!zoomed) {
         return 1;
      }

      const zoom = Number.parseFloat(getComputedStyle(zoomed).zoom);
      return Number.isFinite(zoom) && zoom > 0 ? zoom : 1;
   }

   static applyTooltipPosition(hoverTooltipEl, { x, y }) {
      const zoom = HoverTooltipPositioner.pageZoom(hoverTooltipEl);
      hoverTooltipEl.style.left = `${x / zoom}px`;
      hoverTooltipEl.style.top = `${y / zoom}px`;
   }
}
