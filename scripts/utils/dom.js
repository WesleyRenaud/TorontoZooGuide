export function getLikelihoodPhrase(likelihood) {
   const v = Number(likelihood) || 0;
   if (v >= 95) return 'Very high';
   if (v >= 80) return 'High';
   if (v >= 60) return 'Medium';
   if (v >= 40) return 'Moderate';
   if (v >= 20) return 'Low';
   return 'Very low';
}

export function positionTooltip(tooltipEl, markerEl) {
   const rect = markerEl.getBoundingClientRect();
   const tooltipRect = tooltipEl.getBoundingClientRect();
   const padding = 12;
   const gap = 12;

   const parent = tooltipEl.offsetParent || tooltipEl.parentElement;
   const parentRect = parent.getBoundingClientRect();

   let left = (rect.left + rect.width / 2) - parentRect.left - (tooltipRect.width / 2);
   let top  = rect.top - parentRect.top - tooltipRect.height - gap;

   if (top < padding) {
      top = (rect.bottom - parentRect.top) + gap;
   }

   const maxLeft = parentRect.width - tooltipRect.width - padding;
   const maxTop  = parentRect.height - tooltipRect.height - padding;

   left = Math.max(padding, Math.min(maxLeft, left));
   top  = Math.max(padding, Math.min(maxTop, top));

   tooltipEl.style.left = `${left}px`;
   tooltipEl.style.top = `${top}px`;
}