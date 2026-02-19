export function createPanzoom(mapInner, { contain }) {
   const panzoom = Panzoom(mapInner, {
      maxScale: 10,
      minScale: 1,
      contain,
   });

   mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

   // hide labels at zoom
   const regionLabels = document.querySelectorAll('.region-label');
   const exhibitLabels = document.querySelectorAll('.exhibit-label');

   const regionHideZoomScale = 1.5;
   const exhibitHideZoomScale = 2;

   mapInner.addEventListener('panzoomchange', () => {
      const currentScale = panzoom.getScale();

      regionLabels.forEach(label => {
         label.style.display = currentScale > regionHideZoomScale ? 'none' : 'block';
      });

      exhibitLabels.forEach(label => {
         label.style.display = currentScale > exhibitHideZoomScale ? 'none' : 'block';
      });
   });

   return panzoom;
}