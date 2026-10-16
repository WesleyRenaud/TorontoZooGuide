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

   static apply(stage, mapInner) {
      const rect = MapStageController.coverRect(
         mapInner?.clientWidth,
         mapInner?.clientHeight,
         ZooMapConstants.ZOO_MAP_WIDTH_PX,
         ZooMapConstants.ZOO_MAP_HEIGHT_PX
      );

      if (!stage || !rect) {
         return;
      }

      stage.style.left = `${rect.left}px`;
      stage.style.top = `${rect.top}px`;
      stage.style.width = `${rect.width}px`;
      stage.style.height = `${rect.height}px`;
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

   static mount(mapInner) {
      if (!mapInner) {
         return null;
      }

      const existingStage = MapStageController.findStage(mapInner);

      if (existingStage) {
         MapStageController.apply(existingStage, mapInner);
         return existingStage;
      }

      const stage = MapStageController.createStage(mapInner);
      MapStageController.apply(stage, mapInner);
      MapStageController.observe(mapInner, () => {
         MapStageController.apply(stage, mapInner);
      });

      return stage;
   }
}
