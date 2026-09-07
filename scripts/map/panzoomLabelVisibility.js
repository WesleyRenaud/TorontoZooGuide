export class PanzoomLabelVisibility {
   static LABEL_VISIBILITY_RULES = Object.freeze([
      {
         selector: '.map-label-primary-svg',
         hideAboveScale: 2,
      },
      {
         selector: '.map-label-secondary-svg',
         hideAboveScale: 2.5,
      },
   ]);

   static setLabelVisibility(labels, shouldHide) {
      labels.forEach((label) => {
         label.style.display = shouldHide ? 'none' : '';
      });
   }

   static syncSvgLabelVisibility(mapInner, scale) {
      PanzoomLabelVisibility.LABEL_VISIBILITY_RULES.forEach((rule) => {
         PanzoomLabelVisibility.setLabelVisibility(
            mapInner.querySelectorAll(rule.selector),
            scale > rule.hideAboveScale
         );
      });
   }

   static createSvgLabelVisibilityHandler(mapInner, panzoom) {
      return () => {
         PanzoomLabelVisibility.syncSvgLabelVisibility(mapInner, panzoom.getScale());
      };
   }
}
