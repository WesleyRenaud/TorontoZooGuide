import { ZooMapConstants } from '../shared/zooMapConstants.js';

export class MapStageController {
   static STAGE_ID = 'mapStage';

   static coverRect(containerWidth, containerHeight, contentWidth, contentHeight) {
      if (!(containerWidth > 0) || !(containerHeight > 0) || !(contentWidth > 0) || !(contentHeight > 0)) {
         return null;
      }

      const contentAspect = contentWidth / contentHeight;

      if ((containerWidth / containerHeight) > contentAspect) {
         const width = containerWidth;
         const height = width / contentAspect;

         return {
            left: 0,
            top: (containerHeight - height) / 2,
            width,
            height,
         };
      }

      const height = containerHeight;
      const width = height * contentAspect;

      return {
         left: (containerWidth - width) / 2,
         top: 0,
         width,
         height,
      };
   }

   static frameFor(mapInner) {
      return MapStageController.coverRect(
         mapInner?.clientWidth,
         mapInner?.clientHeight,
         ZooMapConstants.ZOO_MAP_WIDTH_PX,
         ZooMapConstants.ZOO_MAP_HEIGHT_PX
      );
   }

   static apply(stage, mapInner) {
      const rect = MapStageController.frameFor(mapInner);

      if (!stage || !rect) {
         return null;
      }

      stage.style.left = '0px';
      stage.style.top = '0px';
      stage.style.width = `${rect.width}px`;
      stage.style.height = `${rect.height}px`;
      return rect;
   }

   static syncPan(panzoom, rect) {
      if (panzoom.getScale() === 1) {
         panzoom.pan(rect.left, rect.top, { animate: false });
         return;
      }

      const pan = panzoom.getPan();
      panzoom.pan(pan.x, pan.y, { animate: false });
   }

   static findStage(mapInner) {
      return mapInner.querySelector?.(`#${MapStageController.STAGE_ID}`) ?? null;
   }

   static createStage(mapInner) {
      const stage = document.createElement('div');
      stage.id = MapStageController.STAGE_ID;
      const mount = mapInner.querySelector?.('#zooMapMount');

      if (mount) {
         stage.appendChild(mount);
      }

      if (typeof mapInner.prepend === 'function') {
         mapInner.prepend(stage);
      } else {
         mapInner.appendChild(stage);
      }

      return stage;
   }

   static observe(mapInner, onResize) {
      if (typeof ResizeObserver !== 'function') {
         return;
      }

      const observer = new ResizeObserver(() => {
         onResize();
      });
      observer.observe(mapInner);
   }

   static mount(mapInner, onFrame) {
      if (!mapInner) {
         return null;
      }

      const existingStage = MapStageController.findStage(mapInner);
      const stage = existingStage || MapStageController.createStage(mapInner);
      const publish = () => {
         const rect = MapStageController.apply(stage, mapInner);

         if (rect && onFrame) {
            onFrame(rect);
         }
      };

      MapStageController.apply(stage, mapInner);

      if (!existingStage) {
         MapStageController.observe(mapInner, publish);
      }

      return stage;
   }
}
