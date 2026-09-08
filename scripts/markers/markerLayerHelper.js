export class MarkerLayerHelper {
   static MARKER_SELECTOR = '.marker';

   static removeRenderedMarkers(mapInner) {
      mapInner.querySelectorAll(MarkerLayerHelper.MARKER_SELECTOR).forEach((markerEl) => {
         markerEl.remove();
      });
   }

   static shouldRenderMarkerGroup(group) {
      return group.items.length > 0;
   }
}
