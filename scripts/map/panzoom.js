export function createPanzoom(mapInner, { contain }) {
   const panzoom = Panzoom(mapInner, {
      maxScale: 10,
      minScale: 1,
      contain,
   });

   mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

   // hide labels at zoom
   const primaryLabels = document.querySelectorAll('.map-label-primary');
   const secondaryLabels = document.querySelectorAll('.map-label-secondary');

   const primaryLabelHideZoomScale = 1.5;
   const secondaryLabelHideZoomScale = 2;

   mapInner.addEventListener('panzoomchange', () => {
      const currentScale = panzoom.getScale();

      primaryLabels.forEach(label => {
         label.style.display = currentScale > primaryLabelHideZoomScale ? 'none' : 'block';
      });

      secondaryLabels.forEach(label => {
         label.style.display = currentScale > secondaryLabelHideZoomScale ? 'none' : 'block';
      });
   });

   return panzoom;
}