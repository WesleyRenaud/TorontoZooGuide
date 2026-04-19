function normalizeExhibitKey(value) {
   return String(value || '')
      .trim()
      .toLowerCase()
      .replace(/'/g, '')
      .replace(/&/g, 'and')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
}

export function setClosedExhibitOverlaysVisible(closedExhibits) {
   const overlays = document.querySelectorAll('[id^="closed-exhibit-overlay-"]');

   overlays.forEach((overlay) => {
      overlay.style.display = 'none';
   });

   (closedExhibits || []).forEach((exhibit) => {
      const key = normalizeExhibitKey(exhibit);

      if (!key) {
         return;
      }

      const overlay = document.getElementById(`closed-exhibit-overlay-${key}`);

      if (overlay) {
         overlay.style.display = '';
      }
   });
}

export async function syncClosedExhibitOverlays(sources, ctx) {
   const src = sources.closedExhibit;

   if (!src?.fetch) {
      setClosedExhibitOverlaysVisible([]);
      return [];
   }

   try {
      const rows = await src.fetch(ctx);
      const closedExhibits = Array.isArray(rows) ? rows : [];

      setClosedExhibitOverlaysVisible(closedExhibits);
      return closedExhibits;
   } catch {
      setClosedExhibitOverlaysVisible([]);
      return [];
   }
}
