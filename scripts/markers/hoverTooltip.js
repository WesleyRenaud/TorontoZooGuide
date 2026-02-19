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
      if (!hoverTooltipEl || hoverTooltipEl.style.display === 'none') return;

      const pad = 14;
      const offsetX = 18;
      const offsetY = 22;

      const rect = hoverTooltipEl.getBoundingClientRect();

      let x = e.clientX + offsetX;
      let y = e.clientY - rect.height - offsetY;

      if (y < pad) y = e.clientY + offsetY;

      x = Math.max(pad, Math.min(window.innerWidth - rect.width - pad, x));
      y = Math.max(pad, Math.min(window.innerHeight - rect.height - pad, y));

      hoverTooltipEl.style.left = `${x}px`;
      hoverTooltipEl.style.top = `${y}px`;
   }

   return { show, hide, move };
}