export class MarkersHelpers {
   static MARKER_SELECTOR = '.marker';

   static removeRenderedMarkers(mapInner) {
      mapInner.querySelectorAll(MarkersHelpers.MARKER_SELECTOR).forEach((markerEl) => {
         markerEl.remove();
      });
   }

   static shouldRenderMarkerGroup(group) {
      return group.items.length > 0;
   }
}
