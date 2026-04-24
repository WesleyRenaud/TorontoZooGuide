const PANZOOM_SCALE_RANGE = Object.freeze({
   minScale: 1,
   maxScale: 10,
});

const LABEL_VISIBILITY_RULES = Object.freeze([
   {
      selector: '.map-label-primary-svg',
      hideAboveScale: 2,
   },
   {
      selector: '.map-label-secondary-svg',
      hideAboveScale: 2.5,
   },
]);

function setLabelVisibility(labels, shouldHide) {
   labels.forEach((label) => {
      label.style.display = shouldHide ? 'none' : '';
   });
}

function syncSvgLabelVisibility(mapInner, scale) {
   LABEL_VISIBILITY_RULES.forEach((rule) => {
      setLabelVisibility(
         mapInner.querySelectorAll(rule.selector),
         scale > rule.hideAboveScale
      );
   });
}

function createSvgLabelVisibilityHandler(mapInner, panzoom) {
   return () => {
      syncSvgLabelVisibility(mapInner, panzoom.getScale());
   };
}

export function createPanzoom(mapInner, { contain }) {
   const panzoom = Panzoom(mapInner, {
      ...PANZOOM_SCALE_RANGE,
      contain,
   });

   mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);
   const updateSvgLabelVisibility = createSvgLabelVisibilityHandler(
      mapInner,
      panzoom
   );

   mapInner.addEventListener('panzoomchange', updateSvgLabelVisibility);
   updateSvgLabelVisibility();

   return panzoom;
}
