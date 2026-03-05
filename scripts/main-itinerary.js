// scripts/main-itinerary.js
import { initItineraryWizardPage } from './pages/itineraryWizardPage.js';

document.addEventListener('DOMContentLoaded', () => {
   const page = window.location.pathname.split('/').pop().replace('.html', '');
   if (page !== 'itinerary') return;
   initItineraryWizardPage();
});