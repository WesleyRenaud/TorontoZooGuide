import { PanzoomLabelPresenter } from './panzoomLabelPresenter.js';

export class PanzoomAdapter {
   static PANZOOM_SCALE_RANGE = Object.freeze({
      minScale: 1,
      maxScale: 10,
   });

   static createPanzoom(mapInner, { contain, startX = 0, startY = 0 }) {
      const panzoom = globalThis.Panzoom(mapInner, {
         ...PanzoomAdapter.PANZOOM_SCALE_RANGE,
         contain,
         startX,
         startY,
      });

      mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);
      const updateSvgLabelVisibility = PanzoomLabelPresenter.createSvgLabelVisibilityHandler(
         mapInner,
         panzoom
      );

      mapInner.addEventListener('panzoomchange', updateSvgLabelVisibility);
      updateSvgLabelVisibility();

      return panzoom;
   }
}
