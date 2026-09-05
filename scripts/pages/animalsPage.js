import { Router } from '../animals/router.js';

export function initAnimalsPage() {
   const listEl = document.querySelector('.list');
   if (!listEl) return;

   const router = Router.createAnimalsRouter({ listEl });
   router.start();
}

document.addEventListener('DOMContentLoaded', () => {
   initAnimalsPage();
});