const HOVER_TOOLTIP_POSITION = Object.freeze({
   viewportPadding: 14,
   cursorOffsetX: 18,
   cursorOffsetY: 22,
});

export class HoverTooltipPositioner {
   static isTooltipVisible(hoverTooltipEl) {
      return Boolean(
         hoverTooltipEl
         && hoverTooltipEl.style.display !== 'none'
      );
   }

   static clampToViewport(value, size, viewportSize) {
      const { viewportPadding } = HOVER_TOOLTIP_POSITION;

      return Math.max(
         viewportPadding,
         Math.min(viewportSize - size - viewportPadding, value)
      );
   }

   static calculateTooltipPosition(event, tooltipRect) {
      const {
         cursorOffsetX,
         cursorOffsetY,
         viewportPadding,
      } = HOVER_TOOLTIP_POSITION;

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

   static applyTooltipPosition(hoverTooltipEl, { x, y }) {
      hoverTooltipEl.style.left = `${x}px`;
      hoverTooltipEl.style.top = `${y}px`;
   }
}
