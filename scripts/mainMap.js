import { MapPage } from './pages/mapPage.js';

export class MainMap {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         const page = window.location.pathname.split('/').pop().replace('.html', '');
         if (page !== 'map') return;
         MapPage.initMapPage();
      });
   }
}

MainMap.bind();
