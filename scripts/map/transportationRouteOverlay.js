import { TransportationRouteArrowRenderer } from './transportationRouteArrowRenderer.js';
export class TransportationRouteOverlay {
   static hideTransportationRouteLayers() {
      const svgRoot = TransportationRouteArrowRenderer.getSvgRoot();

      TransportationRouteArrowRenderer.clearRouteMarkerFilters(svgRoot);
      TransportationRouteArrowRenderer.removeRouteArrowsLayer(svgRoot);
      TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, '#zoomobile-route-summer', false);
      TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, '#zoomobile-route-winter', false);
   }

   static showTransportationRouteLayer(route) {
      const svgRoot = TransportationRouteArrowRenderer.getSvgRoot();

      TransportationRouteOverlay.hideTransportationRouteLayers();

      if (!route) {
         return;
      }

      TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, `#zoomobile-route-${route}`, true);
   }

   static showTransportationRouteMarkers(route, markerSequences) {
      const svgRoot = TransportationRouteArrowRenderer.getSvgRoot();

      TransportationRouteOverlay.hideTransportationRouteLayers();

      const markerIds = markerSequences.flat();

      if (!route || markerIds.length === 0) {
         return;
      }

      const groupSelector = `#zoomobile-route-${route}`;
      const group = svgRoot?.querySelector(groupSelector);

      if (!group) {
         return;
      }

      const visibleMarkerIds = new Set(markerIds);

      TransportationRouteArrowRenderer.setLayerVisibility(svgRoot, groupSelector, true);
      group.querySelectorAll('circle[id]').forEach((circle) => {
         circle.style.setProperty(
            'display',
            visibleMarkerIds.has(circle.id) ? '' : 'none'
         );
      });
      TransportationRouteArrowRenderer.appendRouteArrows(svgRoot, group, markerSequences);
   }
}
