import { MapBootstrap } from './pages/mapBootstrap.js';

export class MainMapBootstrap {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         const page = window.location.pathname.split('/').pop().replace('.html', '');
         if (page !== 'map') return;
         MapBootstrap.initMapPage();
      });
   }

   static {
      MainMapBootstrap.bind();
   }
}
