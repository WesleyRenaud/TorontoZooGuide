export function createPanzoom(mapInner, { contain }) {
   const panzoom = Panzoom(mapInner, {
      maxScale: 10,
      minScale: 1,
      contain,
   });

   mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

   const primaryLabelHideZoomScale = 2;
   const secondaryLabelHideZoomScale = 2.5;

   function updateSvgLabelVisibility() {
      const currentScale = panzoom.getScale();

      const primaryLabels = mapInner.querySelectorAll('.map-label-primary-svg');
      const secondaryLabels = mapInner.querySelectorAll('.map-label-secondary-svg');

      primaryLabels.forEach((label) => {
         label.style.display = currentScale > primaryLabelHideZoomScale ? 'none' : '';
      });

      secondaryLabels.forEach((label) => {
         label.style.display = currentScale > secondaryLabelHideZoomScale ? 'none' : '';
      });
   }

   mapInner.addEventListener('panzoomchange', updateSvgLabelVisibility);

   updateSvgLabelVisibility();

   return panzoom;
}