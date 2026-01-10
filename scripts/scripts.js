const apiKey = '657afbbbe68b892616c765dce8e68d6b';
const lat = 43.8177;   // Toronto Zoo latitude
const lon = -79.1859;

// Ensure the DOM is loaded before running
document.addEventListener('DOMContentLoaded', () => {
   const mapInner = document.getElementById('mapInner');

   if (mapInner != null) {
      const panzoom = Panzoom(mapInner, {
      maxScale: 3,
      minScale: 1,
      contain: 'outside'
      });

      mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);
   }

   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');

   // Initialize Flatpickr
   const fp = flatpickr(mapDateInput, {
      defaultDate: new Date(),
      dateFormat: 'Y-m-d',
      allowInput: true,
      clickOpens: true,
      minDate: 'today',
      monthSelectorType: "static",
      onChange: function (_, dateStr) {
         if (mapPreset.value === 'specific-day') {
            updateMap('specific-day', dateStr);
         }
      }
   });

   // Handle preset changes
   mapPreset.addEventListener('change', () => {
      const preset = mapPreset.value;

      // No selection (placeholder)
      if (!preset) {
         mapDateInput.style.display = 'none';
         return;
      }

      if (preset === 'specific-day') {
         mapDateInput.style.display = 'inline-block';
         updateMap('specific-day', mapDateInput.value || fp.input.value);
      } else {
         mapDateInput.style.display = 'none';
         updateMap(preset, null);
      }
   });

   // Initialize visibility on page load
   mapPreset.dispatchEvent(new Event('change'));
});

function updateMap(preset, date) {
   if (preset === 'summer') {
      $.ajax({
         type: 'POST',
         url: '/get-summer-animals',
         contentType: 'application/json',
         success: function (response) {
            addMarkers(response.animals);
         }
      });
   }
   else if (preset === 'winter') {
      $.ajax({
         type: 'POST',
         url: '/get-winter-animals',
         contentType: 'application/json',
         success: function (response) {
            addMarkers(response.animals);
         }
      });
   }
   // Specific day preset
   else {
      if (isWithinNextNDays(date, 7)) {
         fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`)
            .then(res => res.json())
            .then(data => {
               // Filter forecasts for the selected day
               const targetDateStr = date; // 'YYYY-MM-DD'
               const dailyForecasts = data.list.filter(forecast =>
                  forecast.dt_txt.startsWith(targetDateStr)
               );

               var temp = null;
               if (dailyForecasts.length > 0) {
                  temp = Math.max(...dailyForecasts.map(f => f.main.temp_max));
               }

               $.ajax({
                  type: 'POST',
                  url: '/get-animals-viewable-in-day',
                  contentType: 'application/json',
                  data: JSON.stringify({
                     month: getMonth(date),
                     day: getDay(date),
                     temp: temp
                  }),
                  success: function (response) {
                     addMarkers(response.animals);
                  }
               });
            });
      }
      else {
         $.ajax({
            type: 'POST',
            url: '/get-animals-viewable-in-month',
            contentType: 'application/json',
            data: JSON.stringify({
               month: getMonth(date)
            }),
            success: function (response) {
               addMarkers(response.animals);
            }
         });
      }      
   }
}

function isWithinNextNDays(dateStr, n) {
   const today = new Date();
   today.setHours(0, 0, 0, 0);

   const target = parseLocalDate(dateStr);
   target.setHours(0, 0, 0, 0);

   const diffDays = (target - today) / 86400000;

   return diffDays >= 0 && diffDays <= n;
}

function parseLocalDate(dateStr) {
   const [year, month, day] = dateStr.split('-').map(Number);
   return new Date(year, month - 1, day); // LOCAL time
}

function getMonth(dateStr) {
   const date = parseLocalDate(dateStr);
   return date
      .toLocaleString('en-US', { month: 'short' })
      .toUpperCase();
}

function getDay(dateStr) {
   const date = new Date(dateStr);
   return date.getDate();
}

/* ============================================================
   MARKERS & TOOLTIP SYSTEM (Click-to-Open)
============================================================ */

const tooltip = document.getElementById('tooltip');
let currentCarousel = null;

// Clear all markers from the map
function clearMarkers() {
   const mapInner = document.getElementById('mapInner');
   mapInner.querySelectorAll('.marker').forEach(marker => marker.remove());
}

// Add markers to the map based on animal data
function addMarkers(animals) {
   clearMarkers();

   const mapInner = document.getElementById('mapInner');

   animalExhibitMarkers.forEach(markerData => {
      const speciesList = Array.isArray(markerData.species)
         ? markerData.species
         : [markerData.species];

      const location = markerData.location;
      const exhibitType = markerData.exhibitType;

      // Filter the actual animal objects that are on exhibit
      const animalsOnExhibit = speciesList.map(species => {
         return animals.find(a =>
            a.species === species &&
            a.location === location &&
            a.exhibit_type === exhibitType
         );
      }).filter(a => a !== undefined);

      if (animalsOnExhibit.length === 0) return;

      const el = document.createElement('div');
      el.className = 'marker';
      el.style.left = `${markerData.x}%`;
      el.style.top = `${markerData.y}%`;
      el.title = ''; // remove default browser tooltip

      // Optionally add a class based on likelihood of highest animal
      const maxLikelihood = Math.max(...animalsOnExhibit.map(a => a.likelihood || 0));
      el.classList.add(getLikelihoodClass(maxLikelihood));

      mapInner.appendChild(el);

      // Attach click-to-open tooltip
      attachTooltip(el, animalsOnExhibit);
   });
}

// Determine class for marker color based on likelihood
function getLikelihoodClass(likelihood) {
   if (likelihood >= 5) {
      return 'likelihood-very-high';
   }
   else if (likelihood >= 4) {
      return 'likelihood-high';
   }
   else if (likelihood >= 3) {
      return 'likelihood-medium';
   }
   else if (likelihood >= 2) {
      return 'likelihood-moderate';
   }
   else if (likelihood >= 1) {
      return 'likelihood-low';
   }
   else if (likelihood > 0) {
      return 'likelihood-very-low';
   }
   return 'likelihood-none';
}

/* ============================================================
   TOOLTIP FUNCTIONS
============================================================ */

// Attach click behavior to show/hide tooltip
function attachTooltip(marker, animals) {
   marker.addEventListener('click', (e) => {
      e.stopPropagation(); // prevent map click events

      const isVisible = tooltip.style.display === 'flex';
      if (isVisible) {
         hideTooltip();
      } else {
         showTooltipForMarker(marker, animals);
      }
   });
}

function showTooltipForMarker(marker, animals) {
   clearTooltip();
   tooltip.style.display = 'flex';
   tooltip.style.pointerEvents = 'auto';

   const content = document.createElement('div');
   content.className = 'tooltip-content';

   const carousel = createCarousel(animals);
   currentCarousel = carousel;

   // Enable arrow key navigation
   enableTooltipKeyboard(carousel);

   content.appendChild(carousel);
   tooltip.appendChild(content);

   // Only create arrow nav if multiple cards
   if (animals.length > 1) {
      const nav = document.createElement('div');
      nav.className = 'tooltip-nav';

      const leftArrow = createArrow('<', () => carouselPrev(carousel));
      leftArrow.classList.add('tooltip-prev', 'visible');

      const rightArrow = createArrow('>', () => carouselNext(carousel));
      rightArrow.classList.add('tooltip-next', 'visible');

      nav.appendChild(leftArrow);
      nav.appendChild(document.createElement('div')); // spacer
      nav.appendChild(rightArrow);

      tooltip.appendChild(nav);
      tooltip.classList.remove('no-arrows');
   } else {
      // Single species - remove arrow spacing
      tooltip.classList.add('no-arrows');
   }

   positionTooltip(marker);
}

// Hide tooltip completely
function hideTooltip() {
   tooltip.style.display = 'none';
}

// Clear the tooltip content
function clearTooltip() {
   tooltip.innerHTML = '';
   currentCarousel = null;
}

/* ============================================================
   CAROUSEL FUNCTIONS
============================================================ */

function createCarousel(animals) {
   const carousel = document.createElement('div');
   carousel.className = 'tooltip-carousel';
   animals.forEach((a, i) => {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = i;

      card.innerHTML = `
         <strong>${a.species}</strong>
         <span>Location: ${a.location}</span>
         <span>Exhibit: ${a.exhibit_type}</span>
         <span>Likelihood: ${getLikelihoodPhrase(a.likelihood)}</span>
      `;
      card.style.display = i === 0 ? 'flex' : 'none';
      carousel.appendChild(card);
   });
   carousel.dataset.index = 0;
   return carousel;
}

function getLikelihoodPhrase(likelihood) {
   if (likelihood >= 5) {
      return 'Very high';
   }
   else if (likelihood >= 4) {
      return 'High';
   }
   else if (likelihood >= 3) {
      return 'Medium';
   }
   else if (likelihood >= 2) {
      return 'Moderate';
   }
   else if (likelihood >= 1) {
      return 'Low';
   }
   else if (likelihood > 0) {
      return 'Very low';
   }
   return 'None';
}

function carouselNext(carousel) {
   const cards = Array.from(carousel.children);
   let index = Number(carousel.dataset.index);
   cards[index].style.display = 'none';
   index = (index + 1) % cards.length;
   cards[index].style.display = 'flex';
   carousel.dataset.index = index;
}

function carouselPrev(carousel) {
   const cards = Array.from(carousel.children);
   let index = Number(carousel.dataset.index);
   cards[index].style.display = 'none';
   index = (index - 1 + cards.length) % cards.length;
   cards[index].style.display = 'flex';
   carousel.dataset.index = index;
}

// Add keyboard navigation for carousel
function enableTooltipKeyboard(carousel) {
   function handleKey(e) {
      if (e.key === "ArrowRight") {
         carouselNext(carousel);
      } else if (e.key === "ArrowLeft") {
         carouselPrev(carousel);
      }
   }

   document.addEventListener('keydown', handleKey);

   // Remove listener when tooltip is hidden
   tooltip.addEventListener('mouseleave', () => {
      document.removeEventListener('keydown', handleKey);
   }, { once: true });
}

/* ============================================================
   ARROWS
============================================================ */

function createArrow(symbol, onClick) {
   const arrow = document.createElement('div');
   arrow.className = 'tooltip-arrow';
   arrow.textContent = symbol;
   arrow.addEventListener('click', e => {
      e.stopPropagation();
      onClick();
   });
   return arrow;
}

function updateArrowVisibility(count, left, right) {
   if (count > 1) {
      left.classList.add('visible');
      right.classList.add('visible');
   } else {
      left.classList.remove('visible');
      right.classList.remove('visible');
   }
}

/* ============================================================
   POSITIONING
============================================================ */

function positionTooltip(marker) {
   const rect = marker.getBoundingClientRect();
   const tooltipRect = tooltip.getBoundingClientRect();
   tooltip.style.left = `${rect.left + rect.width/2 - tooltipRect.width/2}px`;
   tooltip.style.top = `${rect.top - tooltipRect.height - 12}px`;
}

/* ============================================================
   CLOSE TOOLTIP ON OUTSIDE CLICK
============================================================ */

document.addEventListener('click', (e) => {
   if (!tooltip.contains(e.target)) {
      hideTooltip();
   }
});

const animalExhibitMarkers =
[
   // Australasia Pavilion
   {
      species:
      [
         'Brownbanded bamboo shark', 'Central bearded dragon', 'Clown triggerfish', 'Crimson rosella', 'Eastern rosella',
         'Emerald tree boa', 'Fly River turtle', 'Green tree python', 'Green-winged dove', 'Komodo dragon', 'Kookaburra',
         'Lau banded iguana', 'Lionfish', 'Live coral reefs', 'Longnose butterflyfish', 'MacLeay\'s spectres', 'Moon jellyfish',
         'Nicobar pigeon', 'Pennant coral fish', 'Pot-bellied seahorse', 'Red claw yabby', 'Red-tailed black cockatoo',
         'Short-beaked echidna', 'Solomon Island leaf frog', 'Southern hairy-nosed wombat', 'Thorny devil stick insect',
         'Victoria crowned pigeon', 'White\'s tree frog'
      ],
      location: 'Australasia Pavilion',
      exhibitType: 'Indoor',
      x: 65,
      y: 41
   },
   {
      species: ['Demoiselle crane', 'Kookaburra'],
      location: 'Australasia Pavilion',
      exhibitType: 'Outdoor',
      x: 63,
      y: 39.75
   },
   {
      species: ['Southern hairy-nosed wombat'],
      location: 'Australasia Pavilion',
      exhibitType: 'Outdoor',
      x: 66.75,
      y: 40.25
   },

   // Australasia Outdoor
   {
      species: ['Western grey kangaroo'],
      location: 'Australasia Outdoor',
      exhibitType: 'Outdoor',
      x: 68,
      y: 42.5
   },

   // Eurasia Wilds
   {
      species: ['Amur tiger'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 71.5,
      y: 39
   },
   {
      species: ['Asian wild horse'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 85,
      y: 22
   },
   {
      species: ['Asian wild horse'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 67.5,
      y: 25.75
   },
   {
      species: ['Bactrian camel'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 78.25,
      y: 34.25
   },
   {
      species: ['Bactrian camel'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 80.5,
      y: 28.5
   },
   {
      species: ['Domestic yak'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 86,
      y: 27.5
   },
   {
      species: ['Highland cattle'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 87.75,
      y: 41.25
   },
   {
      species: ['Mouflon'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 68.75,
      y: 32.25
   },
   {
      species: ['Red panda'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 77.625,
      y: 38.125
   },
   {
      species: ['Snow leopard'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 75.125,
      y: 25.25
   },
   {
      species: ['Steller\'s sea eagle'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 77.125,
      y: 24.875
   },
   {
      species: ['West caucasian tur'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 72.5,
      y: 25.5
   },
   {
      species: ['West caucasian tur'],
      location: 'Eurasia Wilds',
      exhibitType: 'Outdoor',
      x: 85.75,
      y: 31
   },

   // Tundra Trek
   {
      species: ['Arctic wolf'],
      location: 'Tundra Trek',
      exhibitType: 'Outdoor',
      x: 56,
      y: 33.25
   },
   {
      species: ['Caribou'],
      location: 'Tundra Trek',
      exhibitType: 'Outdoor',
      x: 50.25,
      y: 28.75
   },
   {
      species: ['Lesser snow goose'],
      location: 'Tundra Trek',
      exhibitType: 'Outdoor',
      x: 53.75,
      y: 37
   },
   {
      species: ['Northern bald eagle'],
      location: 'Tundra Trek',
      exhibitType: 'Outdoor',
      x: 51.25,
      y: 33.5
   },
   {
      species: ['Polar bear'],
      location: 'Tundra Trek',
      exhibitType: 'Outdoor',
      x: 55.5,
      y: 29.375
   },

   // Americas Outdoor Mayan Temple Ruins
   {
      species: ['American flamingo'],
      location: 'Americas Outdoor Mayan Temple Ruins',
      exhibitType: 'Outdoor',
      x: 46,
      y: 25.875
   },
   {
      species: ['Black-handed spider monkey'],
      location: 'Americas Outdoor Mayan Temple Ruins',
      exhibitType: 'Outdoor',
      x: 44.125,
      y: 26.5
   },
   {
      species: ['Capybara'],
      location: 'Americas Outdoor Mayan Temple Ruins',
      exhibitType: 'Outdoor',
      x: 46.5,
      y: 29.75
   },

   // Americas Pavilion
   {
      species:
      [
         'American alligator', 'American eel', 'American lobster', 'Axolotl', 'Black-footed ferret', 'Black-widow spider',
         'Blanding\'s turtle', 'Blue and yellow macaw', 'Blue poison dart frog', 'Boa constrictor', 'Brazilian giant cockroach',
         'Brazilian salmon pink bird-eating tarantula', 'Butterfly goodied', 'Crested tinamou', 'Desert grassland whiptail',
         'Dyeing poison dart frog', 'Eastern loggerhead shrike', 'Eastern lubber grasshopper', 'Eyelash viper', 'Ferocious water bug',
         'Golden lion tamarin', 'Green and black poison dart frog', 'Green surf anemone', 'Green-winged macaw', 'Jamaican boa',
         'Leather sea star', 'Lemur leaf frog', 'Longnose dace', 'Massasauga rattlesnake', 'Painted anemone', 'Panamanian golden frog',
         'Plumose anemone', 'Plush-crested jay', 'Puerto Rican crested toad', 'Pumpkinseed sunfish', 'Red Island bird-eating tarantula',
         'Red-crested finch', 'Reticulated gila monster', 'Round goby', 'Rufous-collared sparrow', 'San-Esteban Island chuckwalla',
         'Snapping turtle', 'Spot prawn', 'Spotted river stingray', 'Spotted turtle', 'Timber rattlesnake', 'Turquoise tanager',
         'Two-toed sloth', 'Western blacknose dace', 'White-faced saki', 'Yellow-banded poison dart frog', 'Zebra finch'
      ],
      location: 'Americas Pavilion',
      exhibitType: 'Indoor',
      x: 51.375,
      y: 41.75
   },
   {
      species: ['Golden lion tamarin', 'Two-toed sloth', 'White-faced saki'],
      location: 'Americas Pavilion',
      exhibitType: 'Outdoor',
      x: 53,
      y: 42.5
   },
   {
      species: ['Great-horned owl'],
      location: 'Americas Pavilion',
      exhibitType: 'Outdoor',
      x: 50.375,
      y: 40.75
   },
   {
      species: ['North American river otter'],
      location: 'Americas Pavilion',
      exhibitType: 'Outdoor',
      x: 49,
      y: 40.625
   },

   // Canadian Domain
   {
      species: ['Cougar'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 9.25,
      y: 60.75
   },
   {
      species: ['Grizzly bear'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 6.125,
      y: 65
   },
   {
      species: ['Northern bald eagle'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 7.5,
      y: 71
   },
   {
      species: ['Raccoon'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 15,
      y: 65.5
   },
   {
      species: ['Wood bison'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 11,
      y: 58.75
   },
   {
      species: ['Wood bison'],
      location: 'Canadian Domain',
      exhibitType: 'Outdoor',
      x: 8.5,
      y: 76.125
   },

   // Africa Savanna
   {
      species: ['African lion'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 39,
      y: 62
   },
   {
      species: ['African penguin'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 45.5,
      y: 66
   },
   {
      species: ['African penguin'],
      location: 'Africa Savanna',
      exhibitType: 'Indoor',
      x: 46.25,
      y: 63.75
   },
   {
      species: ['Cheetah'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 36.125,
      y: 75.5
   },
   {
      species: ['Common eland'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 41.375,
      y: 65.5
   },
   {
      species: ['Greater kudu', 'Marabou stork', 'Southern ground hornbill', 'White-headed vulture'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 45.5,
      y: 80
   },
   {
      species: ['Greater kudu', 'Marabou stork', 'Southern ground hornbill', 'White-headed vulture'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 47.375,
      y: 81.75
   },
   {
      species: ['Greater kudu', 'Marabou stork', 'Southern ground hornbill', 'White-headed vulture'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 51.25,
      y: 77.875
   },
   {
      species: ['Grevy\'s zebra'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 38.5,
      y: 70.25
   },
   {
      species: ['Marabou stork'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 38.375,
      y: 73.875
   },
   {
      species: ['Masai giraffe'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 55,
      y: 86.25
   },
   {
      species: ['Masai giraffe'],
      location: 'Africa Savanna',
      exhibitType: 'Indoor',
      x: 55.875,
      y: 82.5
   },
   {
      species: ['Olive baboon'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 36,
      y: 68
   },
   {
      species: ['Ostrich'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 36.25,
      y: 65.5
   },
   {
      species: ['Ostrich'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 32,
      y: 63
   },
   {
      species: ['River hippopotamus'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 52.5,
      y: 87.375
   },
   {
      species: ['Southern ground hornbill'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 40.5,
      y: 61.75
   },
   {
      species: ['Southern white rhinoceros'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 43.25,
      y: 78.375
   },
   {
      species: ['Spotted hyena'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 41.125,
      y: 60
   },
   {
      species: ['Warthog'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 51.75,
      y: 82.5
   },
   {
      species: ['Watusi cattle'],
      location: 'Africa Savanna',
      exhibitType: 'Outdoor',
      x: 44.75,
      y: 58.5
   },

   // African Rainforest Pavilion
   {
      species:
      [
         'African clawed frog', 'Blake Crake', 'Blue-bellied roller', 'Hamerkop', 'Lake Malawi cichlids', 'Lau banded iguana',
         'Naked mole rat', 'Ngege', 'Speckled mousebird', 'Veiled chameleon', 'West African dwarf crocodile'
      ],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Indoor',
      x: 53,
      y: 76
   },
   {
      species: ['Aldabra tortoise', 'Grey-necked crowned crane', 'Ring-tailed lemur', 'Royal python'],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Indoor',
      x: 54,
      y: 80.5
   },
   {
      species: ['Aldabra tortoise'],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Outdoor',
      x: 55,
      y: 74
   },
   {
      species:
      [
         'African spoonbill', 'Nile soft-shelled turtle', 'Pygmy hippopotamus', 'Red-footed tortoise', 'Sacred ibis',
         'South African shelduck', 'Straw coloured fruit bat'
      ],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Indoor',
      x: 53.75,
      y: 78.625
   },
   {
      species: ['Red river hog'],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Outdoor',
      x: 55.5,
      y: 78.375
   },
   {
      species: ['Western lowland gorilla'],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Indoor',
      x: 52.25,
      y: 73.25
   },
   {
      species: ['Western lowland gorilla'],
      location: 'African Rainforest Pavilion',
      exhibitType: 'Outdoor',
      x: 51.75,
      y: 70.125
   },

   // Indo-Malaya Pavilion
   {
      species:
      [
         'Asian brown tortoise', 'Bighead carp', 'Black carp', 'Black-breasted leaf turtle', 'Black-throated laughing thrush',
         'Burmese star tortoise', 'Concave casqued hornbill', 'Crested wood partridge', 'Crocodile lizard', 'Crocodile newt',
         'Grass carp', 'Green crested basilisk', 'Luzon bleeding-heart dove', 'Malayan bonytongue', 'Malayan crested fireback pheasant',
         'Malaysian painted turtle', 'Mekong barb', 'Monocled cobra', 'Nicobar pigeon', 'Reticulated python', 'Siamese catfish',
         'Spiny turtle', 'Sumatran orangutan', 'Tentacled snake', 'Tinfoli barb', 'Tomistoma', 'Tri-coloured shark',
         'White-handed gibbon'
      ],
      location: 'Indo-Malaya Pavilion',
      exhibitType: 'Indoor',
      x: 60.75,
      y: 78.75
   },
   {
      species: ['Sumatran orangutan'],
      location: 'Indo-Malaya Pavilion',
      exhibitType: 'Outdoor',
      x: 61.75,
      y: 85
   },

   // Indo-Malaya Outdoor
   {
      species: ['Babirusa'],
      location: 'Indo-Malaya Outdoor',
      exhibitType: 'Outdoor',
      x: 68.75,
      y: 69.5
   },
   {
      species: ['Babirusa', 'Greater one-horned rhinoceros'],
      location: 'Indo-Malaya Outdoor',
      exhibitType: 'Indoor',
      x: 68.625,
      y: 71.375
   },
   {
      species: ['Indian peafowl'],
      location: 'Indo-Malaya Outdoor',
      exhibitType: 'Outdoor',
      x: 65.125,
      y: 71
   },
   {
      species: ['Sumatran tiger'],
      location: 'Indo-Malaya Outdoor',
      exhibitType: 'Outdoor',
      x: 61.25,
      y: 73.25
   },
   {
      species: ['Sumatran tiger'],
      location: 'Indo-Malaya Outdoor',
      exhibitType: 'Outdoor',
      x: 59.75,
      y: 74
   },

   // Malayan Woods Pavilion
   {
      species:
      [
         'Asian giant millipede', 'Clouded leopard', 'Giant gourami', 'Gooty sapphire ornamental tarantula',
         'Malaysian stick insect jungle wood nymph', 'Red-tailed green ratsnake', 'Wrinkled hornbill'
      ],
      location: 'Malayan Woods Pavilion',
      exhibitType: 'Indoor',
      x: 66.25,
      y: 74.5
   }
];