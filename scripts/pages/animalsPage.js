import { Router } from '../animals/router.js';

export class AnimalsPage {
   static initAnimalsPage() {
      const listEl = document.querySelector('.list');
      if (!listEl) return;

      const router = Router.createAnimalsRouter({ listEl });
      router.start();
   }

   static {
      document.addEventListener('DOMContentLoaded', () => {
         AnimalsPage.initAnimalsPage();
      });
   }
}
