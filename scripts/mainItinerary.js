import { ItineraryPage } from './pages/itineraryPage.js';

export class MainItinerary {
   static bind() {
      document.addEventListener('DOMContentLoaded', () => {
         const page = window.location.pathname.split('/').pop().replace('.html', '');
         if (page !== 'itinerary') return;
         ItineraryPage.initItineraryPage();
      });
   }
}

MainItinerary.bind();
