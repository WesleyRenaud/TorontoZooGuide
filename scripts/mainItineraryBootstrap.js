import { ItineraryBootstrap } from './pages/itineraryBootstrap.js';

export class MainItineraryBootstrap {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         const page = window.location.pathname.split('/').pop().replace('.html', '');
         if (page !== 'itinerary') return;
         ItineraryBootstrap.initItineraryPage();
      });
   }

   static {
      MainItineraryBootstrap.bind();
   }
}
