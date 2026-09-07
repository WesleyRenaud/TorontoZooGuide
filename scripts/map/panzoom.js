import { PanzoomLabelVisibility } from './panzoomLabelVisibility.js';

const PANZOOM_SCALE_RANGE = Object.freeze({
   minScale: 1,
   maxScale: 10,
});

export class Panzoom {
   static createPanzoom(mapInner, { contain }) {
      const panzoom = globalThis.Panzoom(mapInner, {
         ...PANZOOM_SCALE_RANGE,
         contain,
      });

      mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);
      const updateSvgLabelVisibility = PanzoomLabelVisibility.createSvgLabelVisibilityHandler(
         mapInner,
         panzoom
      );

      mapInner.addEventListener('panzoomchange', updateSvgLabelVisibility);
      updateSvgLabelVisibility();

      return panzoom;
   }
}
