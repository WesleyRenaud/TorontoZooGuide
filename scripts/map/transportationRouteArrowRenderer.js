export class TransportationRouteArrowRenderer {
   static SVG_NS = 'http://www.w3.org/2000/svg';

   static ROUTE_ARROWS_LAYER_ID = 'transportation-route-arrows';

   static ARROWS_CLASS = 'transportation-route-arrows';

   static ARROW_CLASS = 'transportation-route-arrow';

   static ARROW_HEAD_POINTS = '0,-4.5 20,0 0,4.5';

   static getSvgRoot() {
      return document.querySelector('#zooMapMount svg');
   }

   static setLayerVisibility(svgRoot, layerId, isVisible) {
      svgRoot?.querySelector(layerId)?.style.setProperty(
         'display',
         isVisible ? '' : 'none'
      );
   }

   static clearRouteMarkerFilters(svgRoot) {
      svgRoot?.querySelectorAll(
         '#zoomobile-route-summer circle[id], #zoomobile-route-winter circle[id]'
      ).forEach((circle) => {
         circle.style.removeProperty('display');
      });
   }

   static removeRouteArrowsLayer(svgRoot) {
      svgRoot?.querySelector(`#${TransportationRouteArrowRenderer.ROUTE_ARROWS_LAYER_ID}`)?.remove();
   }

   static createArrowMarker({ x, y, angleDeg }) {
      const markerGroup = document.createElementNS(TransportationRouteArrowRenderer.SVG_NS, 'g');
      markerGroup.classList.add(TransportationRouteArrowRenderer.ARROW_CLASS);
      markerGroup.setAttribute(
         'transform',
         `translate(${x} ${y}) rotate(${angleDeg})`
      );

      const head = document.createElementNS(TransportationRouteArrowRenderer.SVG_NS, 'polygon');
      head.setAttribute('points', TransportationRouteArrowRenderer.ARROW_HEAD_POINTS);
      markerGroup.appendChild(head);

      return markerGroup;
   }

   static circlePoint(circle) {
      const x = Number(circle?.getAttribute?.('cx'));
      const y = Number(circle?.getAttribute?.('cy'));

      if (!Number.isFinite(x) || !Number.isFinite(y)) {
         return null;
      }

      return { x, y };
   }

   static buildMarkerArrowPlacements(points) {
      const placements = [];

      for (let index = 0; index < points.length - 1; index += 2) {
         const start = points[index];
         const end = points[index + 1];
         const deltaX = end.x - start.x;
         const deltaY = end.y - start.y;

         if (deltaX === 0 && deltaY === 0) {
            continue;
         }

         placements.push({
            x: start.x,
            y: start.y,
            angleDeg: Math.atan2(deltaY, deltaX) * (180 / Math.PI),
         });
      }

      return placements;
   }

   static appendRouteArrows(svgRoot, routeGroup, markerSequences) {
      TransportationRouteArrowRenderer.removeRouteArrowsLayer(svgRoot);

      if (!svgRoot || !routeGroup) {
         return;
      }

      const arrowsLayer = document.createElementNS(TransportationRouteArrowRenderer.SVG_NS, 'g');
      arrowsLayer.setAttribute('id', TransportationRouteArrowRenderer.ROUTE_ARROWS_LAYER_ID);
      arrowsLayer.setAttribute('aria-hidden', 'true');
      arrowsLayer.classList.add(TransportationRouteArrowRenderer.ARROWS_CLASS);

      const circlesById = new Map(
         Array.from(routeGroup.querySelectorAll('circle[id]')).map((circle) => [
            circle.id,
            circle,
         ])
      );

      for (const markerIds of markerSequences) {
         const points = markerIds
            .map((markerId) => TransportationRouteArrowRenderer.circlePoint(circlesById.get(markerId)))
            .filter(Boolean);

         for (const placement of TransportationRouteArrowRenderer.buildMarkerArrowPlacements(points)) {
            arrowsLayer.appendChild(TransportationRouteArrowRenderer.createArrowMarker(placement));
         }
      }

      if (arrowsLayer.childNodes.length > 0) {
         svgRoot.appendChild(arrowsLayer);
      }
   }
}
