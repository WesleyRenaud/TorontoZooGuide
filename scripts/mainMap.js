import { MapPage } from './pages/mapPage.js';

document.addEventListener('DOMContentLoaded', () => {
   const page = window.location.pathname.split('/').pop().replace('.html', '');
   if (page !== 'map') return;
   MapPage.initMapPage();
});