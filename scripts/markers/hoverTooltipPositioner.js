export class HoverTooltipPositioner {
   static HOVER_TOOLTIP_POSITION = Object.freeze({
      viewportPadding: 14,
      arrowSize: 2.5,
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

   static clampToViewport(value, size, viewportSize, padding = null) {
      const viewportPadding = padding == null
         ? HoverTooltipPositioner.length(
            HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
         )
         : padding;

      return Math.max(
         viewportPadding,
         Math.min(viewportSize - size - viewportPadding, value)
      );
   }

   static calculateTooltipPosition(markerRect, tooltipRect, zoom = 1) {
      const scale = Number.isFinite(zoom) && zoom > 0 ? zoom : 1;
      const arrowSize = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.arrowSize
      ) * scale;
      const padding = HoverTooltipPositioner.length(
         HoverTooltipPositioner.HOVER_TOOLTIP_POSITION.viewportPadding
      ) * scale;
      const width = tooltipRect.width * scale;
      const height = tooltipRect.height * scale;
      const anchorX = (markerRect.left + markerRect.width / 2) * scale;
      const anchorTop = markerRect.top * scale;
      const anchorBottom = markerRect.bottom * scale;

      let x = anchorX - width / 2;
      let y = anchorTop - height - arrowSize;
      let below = false;

      if (y < padding) {
         below = true;
         y = anchorBottom + arrowSize;
      }

      x = HoverTooltipPositioner.clampToViewport(x, width, window.innerWidth, padding);
      y = HoverTooltipPositioner.clampToViewport(y, height, window.innerHeight, padding);

      return {
         x,
         y,
         below,
         arrowLeft: (anchorX - x) / scale - arrowSize / scale,
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

   static applyTooltipPosition(hoverTooltipEl, { x, y, below = false, arrowLeft }) {
      const zoom = HoverTooltipPositioner.pageZoom(hoverTooltipEl);
      hoverTooltipEl.style.left = `${x / zoom}px`;
      hoverTooltipEl.style.top = `${y / zoom}px`;
      hoverTooltipEl.classList?.toggle('hover-tooltip-below', below);

      if (Number.isFinite(arrowLeft)) {
         hoverTooltipEl.style.setProperty?.('--hover-tooltip-arrow-left', `${arrowLeft}px`);
      }
   }
}
