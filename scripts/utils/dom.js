export function getLikelihoodPhrase(likelihood) {
   const v = Number(likelihood) || 0;
   if (v >= 95) return 'Very high';
   if (v >= 80) return 'High';
   if (v >= 60) return 'Medium';
   if (v >= 40) return 'Moderate';
   if (v >= 20) return 'Low';
   return 'Very low';
}

// Tooltip positioning helper (used by tooltipController if you want to share)
export function positionTooltip(tooltipEl, markerEl) {
   const rect = markerEl.getBoundingClientRect();
   const tooltipRect = tooltipEl.getBoundingClientRect();
   const padding = 12;

   let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
   let top = rect.top - tooltipRect.height - 12;

   if (top < padding) top = rect.bottom + 12;

   left = Math.max(padding, Math.min(window.innerWidth - tooltipRect.width - padding, left));
   top = Math.max(padding, Math.min(window.innerHeight - tooltipRect.height - padding, top));

   tooltipEl.style.left = `${left}px`;
   tooltipEl.style.top = `${top}px`;
}