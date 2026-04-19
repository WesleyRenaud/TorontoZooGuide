function getSvgRoot() {
   return document.querySelector('#zooMapMount svg');
}

function setLayerVisibility(svgRoot, layerId, isVisible) {
   svgRoot?.querySelector(layerId)?.style.setProperty(
      'display',
      isVisible ? '' : 'none'
   );
}

export function hideZoomobileRouteLayers() {
   const svgRoot = getSvgRoot();

   setLayerVisibility(svgRoot, '#zoomobile-route-summer', false);
   setLayerVisibility(svgRoot, '#zoomobile-route-winter', false);
}

export function showZoomobileRouteLayer(route) {
   const svgRoot = getSvgRoot();
   const normalizedRoute = String(route || '').trim().toLowerCase();

   hideZoomobileRouteLayers();

   if (normalizedRoute === 'summer') {
      setLayerVisibility(svgRoot, '#zoomobile-route-summer', true);
   } else if (normalizedRoute === 'winter') {
      setLayerVisibility(svgRoot, '#zoomobile-route-winter', true);
   }
}
