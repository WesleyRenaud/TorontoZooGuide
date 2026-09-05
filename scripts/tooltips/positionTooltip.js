export class PositionTooltip {
   static positionTooltip(tooltipEl, markerEl) {
      const rect = markerEl.getBoundingClientRect();
      const tooltipRect = tooltipEl.getBoundingClientRect();
      const padding = 12;
      const gap = 12;

      const parent = tooltipEl.offsetParent || tooltipEl.parentElement;
      const parentRect = parent.getBoundingClientRect();

      let left = (rect.left + rect.width / 2) - parentRect.left - (tooltipRect.width / 2);
      let top = rect.top - parentRect.top - tooltipRect.height - gap;

      if (top < padding) {
         top = (rect.bottom - parentRect.top) + gap;
      }

      const maxLeft = parentRect.width - tooltipRect.width - padding;
      const maxTop = parentRect.height - tooltipRect.height - padding;

      left = Math.max(padding, Math.min(maxLeft, left));
      top = Math.max(padding, Math.min(maxTop, top));

      tooltipEl.style.left = `${left}px`;
      tooltipEl.style.top = `${top}px`;
   }
}
