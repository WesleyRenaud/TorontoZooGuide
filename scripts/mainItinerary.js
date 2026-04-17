import { initItineraryPage } from './pages/itineraryPage.js';

document.addEventListener('DOMContentLoaded', () => {
   const page = window.location.pathname.split('/').pop().replace('.html', '');
   if (page !== 'itinerary') return;
   initItineraryPage();
});
