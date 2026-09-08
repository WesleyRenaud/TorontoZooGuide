export class ItineraryPanelSectionBuilderHelper {
   static MAX_VISIBLE_ITEMS = 3;

   static updateSectionBodyHeight(body, bodyInner) {
      const items = Array.from(bodyInner.children);

      if (items.length === 0) {
         body.style.display = 'none';
         body.style.maxHeight = 'none';
         body.style.overflowY = 'hidden';
         body.style.overflowX = 'hidden';
         return;
      }

      body.style.display = '';

      if (items.length <= ItineraryPanelSectionBuilderHelper.MAX_VISIBLE_ITEMS) {
         body.style.maxHeight = 'none';
         body.style.overflowY = 'hidden';
         body.style.overflowX = 'hidden';
         return;
      }

      const innerStyles = window.getComputedStyle(bodyInner);
      const gap = parseFloat(innerStyles.rowGap || innerStyles.gap || '0') || 0;
      const paddingTop = parseFloat(innerStyles.paddingTop || '0') || 0;
      const paddingBottom = parseFloat(innerStyles.paddingBottom || '0') || 0;

      const visibleItems = items.slice(0, ItineraryPanelSectionBuilderHelper.MAX_VISIBLE_ITEMS);

      const itemsHeight = visibleItems.reduce((sum, item) => {
         return sum + item.getBoundingClientRect().height;
      }, 0);

      const totalGap = gap * Math.max(0, visibleItems.length - 1);
      const maxHeight = Math.ceil(itemsHeight + totalGap + paddingTop + paddingBottom);

      body.style.maxHeight = `${maxHeight}px`;
      body.style.overflowY = 'auto';
      body.style.overflowX = 'hidden';
   }
}
