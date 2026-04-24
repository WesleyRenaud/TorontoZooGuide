const HOVER_TOOLTIP_POSITION = Object.freeze({
   viewportPadding: 14,
   cursorOffsetX: 18,
   cursorOffsetY: 22,
});

function isTooltipVisible(hoverTooltipEl) {
   return Boolean(
      hoverTooltipEl
      && hoverTooltipEl.style.display !== 'none'
   );
}

function clampToViewport(value, size, viewportSize) {
   const { viewportPadding } = HOVER_TOOLTIP_POSITION;

   return Math.max(
      viewportPadding,
      Math.min(viewportSize - size - viewportPadding, value)
   );
}

function calculateTooltipPosition(event, tooltipRect) {
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
      x: clampToViewport(x, tooltipRect.width, window.innerWidth),
      y: clampToViewport(y, tooltipRect.height, window.innerHeight),
   };
}

function applyTooltipPosition(hoverTooltipEl, { x, y }) {
   hoverTooltipEl.style.left = `${x}px`;
   hoverTooltipEl.style.top = `${y}px`;
}

export function createHoverTooltip(hoverTooltipEl) {
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
      if (!isTooltipVisible(hoverTooltipEl)) return;

      const position = calculateTooltipPosition(
         e,
         hoverTooltipEl.getBoundingClientRect()
      );

      applyTooltipPosition(hoverTooltipEl, position);
   }

   return { show, hide, move };
}
