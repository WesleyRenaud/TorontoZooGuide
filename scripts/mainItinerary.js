import { ItineraryPage } from './pages/itineraryPage.js';

document.addEventListener('DOMContentLoaded', () => {
   const page = window.location.pathname.split('/').pop().replace('.html', '');
   if (page !== 'itinerary') return;
   ItineraryPage.initItineraryPage();
});
