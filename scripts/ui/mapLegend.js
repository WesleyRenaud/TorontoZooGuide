const STORAGE_KEY = 'tzg.legendCollapsed';

export function createMapLegendController({ rootEl }) {
   let el = rootEl || null;
   let toggleBtn = null;

   function ensure() {
      if (el) return el;

      el = document.getElementById('mapLegend');
      if (!el) return null;

      toggleBtn = el.querySelector('.map-legend-toggle');

      // Restore saved state
      const collapsed = localStorage.getItem(STORAGE_KEY) === '1';
      setCollapsed(collapsed, { persist: false });

      if (toggleBtn) {
         toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggle();
         });
      }

      return el;
   }

   function isCollapsed() {
      return !!el?.classList.contains('is-collapsed');
   }

   function setCollapsed(collapsed, { persist = true } = {}) {
      if (!el) return;

      el.classList.toggle('is-collapsed', !!collapsed);

      if (toggleBtn) {
         toggleBtn.setAttribute('aria-expanded', String(!collapsed));
         toggleBtn.setAttribute('aria-label', collapsed ? 'Show legend' : 'Hide legend');
      }

      if (persist) {
         localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0');
      }
   }

   function toggle() {
      if (!el) return;
      setCollapsed(!isCollapsed());
   }

   return {
      ensure,
      toggle,
      setCollapsed,
      isCollapsed,
   };
}

// Convenience init (matches your “initX” style)
export function initMapLegend(rootEl = null) {
   const ctrl = createMapLegendController({ rootEl });
   ctrl.ensure();
   return ctrl;
}