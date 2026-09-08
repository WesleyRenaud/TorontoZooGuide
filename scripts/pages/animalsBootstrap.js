import { AnimalsRouter } from '../animals/animalsRouter.js';

export class AnimalsBootstrap {
   static initAnimalsPage() {
      const listEl = document.querySelector('.list');
      if (!listEl) return;

      const router = AnimalsRouter.createAnimalsRouter({ listEl });
      router.start();
   }

   static {
      document.addEventListener('DOMContentLoaded', () => {
         AnimalsBootstrap.initAnimalsPage();
      });
   }
}
