def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Animal;' )
   cursor.execute( ''' CREATE TABLE Animal
                     (  SPECIES                       VARCHAR(64) NOT NULL,
                        LATIN_NAME                    VARCHAR(64),
                        MIN_TEMPERATURE               INTEGER,
                        GENERAL_VIEWING_TIPS          TEXT,
                        SEASONAL_VIEWING_TIPS         TEXT,
                        IDENTIFICATION                TEXT,
                        HABITAT_AND_RANGE             TEXT,
                        DIET_AND_FEEDING              TEXT,
                        BEHAVIOUR_AND_SOCIAL_LIFE     TEXT,
                        ADAPTATIONS                   TEXT,
                        REPRODUCTION_AND_LIFE_CYCLE   TEXT,
                        ANIMALS_AT_THE_ZOO            TEXT,
                        PRIMARY KEY (SPECIES) ); ''' )

animals = [
   # Australasia Pavilion
   (
      'Black Tree Monitor',
      'Varanus Beccarii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black tree monitor at the zoo shares an enclosure with the red-bellied short-necked turtles. Once you exit the aviary,
         this will be the enclosure directly to the left. The monitor tends to hide towards the back of the enclosure, often on top
         of one of the tree branches.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The black tree monitor is a slender, medium-sized monitor lizard distinguished by its glossy jet-black colouration. It has
         a long neck, narrow head, and an exceptionally long tail used for balance while climbing. Unlike many other monitor
         species, it lacks visible patterning, giving it a sleek, uniform appearance. As a member of the monitor lizard family
         (Varanidae), it is closely related to other tree-dwelling monitors of New Guinea.'''.replace( '\n', ' ' ),
      '''Black tree monitors are native to the tropical rainforests of New Guinea and nearby islands. They are highly arboreal,
         spending most of their lives in the forest canopy where dense vegetation provides cover and access to prey. These lizards
         prefer warm, humid environments with abundant trees and minimal temperature fluctuation.'''.replace( '\n', ' ' ),
      '''In the wild, black tree monitors are opportunistic carnivores that feed primarily on insects, spiders, small birds, bird
         eggs, and small mammals. They are active hunters, using their keen eyesight and agility to locate prey among branches and
         foliage. At the zoo, their diet typically includes insects, small vertebrates, and nutritionally balanced prey items
         appropriate for monitor lizards.'''.replace( '\n', ' ' ),
      '''Black tree monitors are solitary and territorial animals. They are most active during the day and spend much of their time
         climbing, exploring, and basking in elevated areas. While generally shy and secretive, they are intelligent and curious
         reptiles that may become more visible once accustomed to their environment.'''.replace( '\n', ' ' ),
      '''This species is exceptionally well adapted for life in the trees. Its long claws and powerful limbs allow it to climb
         vertical surfaces with ease, while its long tail provides balance during rapid movement through branches. The dark
         colouration may help with camouflage in shaded forest canopies and also aids in absorbing heat during basking.'''
         .replace( '\n', ' ' ),
      '''Female black tree monitors lay clutches of eggs, typically depositing them in protected locations such as hollow logs or
         burrows. After an incubation period, hatchlings emerge fully independent and capable climbers. Like many reptiles, growth
         is gradual, and individuals may live for several decades under human care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Blue-Girdled Angelfish',
      'Pomacanthus Navarchus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The blue-girdled angelfish is part of the main tank habitat in the Great Barrier Reef exhibit in the Australasia pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The blue-girdled angelfish is a striking marine fish with a deep, laterally compressed body, long flowing dorsal and anal
         fins, and a rounded tail. Adults are known for their vibrant yellow body covered in fine blue spotting, contrasted by a dark
         blue to black face and chest. A vivid blue band or “girdle” curves behind the head, giving the species its common name.'''
         .replace('\n', ' '),
      '''This species is native to the tropical Indo-Pacific, particularly around coral reefs in Southeast Asia, Indonesia, the
         Philippines, and nearby regions. It inhabits outer reef slopes, lagoons, and coral-rich areas where caves, ledges, and reef
         walls provide shelter. Blue-girdled angelfish are usually found in warm, clear saltwater environments with abundant coral
         growth.'''.replace('\n', ' '),
      '''Blue-girdled angelfish feed mainly on marine sponges, tunicates, algae, and small benthic invertebrates. In aquariums, they
         are given a varied diet that may include marine angelfish preparations, algae sheets, sponge-based foods, and finely chopped
         seafood. Their diet must be nutrient-rich to maintain their vivid coloration and health.'''.replace('\n', ' '),
      '''This angelfish is generally calm but can be territorial, especially around favored hiding spaces or feeding areas. It spends
         much of its time gliding gracefully around reef structures, often alone or in pairs. Individuals are curious and active,
         frequently exploring rock crevices and coral formations throughout the day.'''.replace('\n', ' '),
      '''Its laterally compressed body allows it to move easily through narrow reef passages and coral gaps. The extended dorsal and
         anal fins provide excellent maneuverability and stability in reef currents. Its bold coloration may help with species
         recognition and territorial displays, while the spotted yellow body blends surprisingly well with reef lighting and coral
         textures.'''.replace('\n', ' '),
      '''Blue-girdled angelfish are egg-layers that spawn in open water, usually at dusk. Pairs rise into the water column where eggs
         and sperm are released simultaneously. The fertilized eggs drift with ocean currents until hatching into tiny larvae, which
         later settle onto reefs and develop their juvenile coloration before maturing into adults.'''.replace('\n', ' '),
      None                                                           # Animals at the zoo
   ),
   (
      'Brush-Tailed Bettong',
      'Bettongia Penicillata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The brush-tailed bettong lives in the small aviary the kookaburras call home in the winter, just past the cockatoos and to
         the left. The brush-tailed bettong spends most of its time underground, but occasionally comes up, so be sure to check
         around the floor of the enclosure, specifically around any potential burrows. Brush-tailed bettongs are most active at
         evening, and during the night, so your best chance to see them is to visit the Australasia pavilion at the end of you day,'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The brush-tailed bettong, also known as the woylie, is a small marsupial with soft grey-brown fur, a pointed snout, and
         large, upright ears. Its most distinctive feature is its long, bushy tail with a dark tip, which it uses for balance and to
         carry nesting material. It belongs to the kangaroo and wallaby family (Macropodidae).''' .replace( '\n', ' ' ),
      '''Brush-tailed bettongs are native to southwestern Australia, where they once occupied a wide range of habitats including
         woodlands, shrublands, and open forests. Today, due to habitat loss and introduced predators, their range is much more
         limited, and they survive mainly in protected areas and fenced reserves.'''.replace( '\n', ' ' ),
      '''This species feeds primarily on underground fungi, tubers, roots, seeds, and other plant material. Brush-tailed bettongs
         play an important ecological role by digging for food, which helps aerate the soil and disperse fungal spores. At the zoo,
         they receive a diet that mimics their natural feeding habits, including vegetables, fruits, and specially prepared
         supplements.''' .replace( '\n', ' ' ),
      '''Brush-tailed bettongs are nocturnal and spend the daytime resting in shallow nests made from grass and leaf litter. They
         are generally solitary but may share overlapping home ranges. At night, they emerge to forage, using their keen sense of
         smell to locate food beneath the soil.'''.replace( '\n', ' ' ),
      '''Strong hind legs allow brush-tailed bettongs to move quickly using hopping motions, while their flexible tails help with
         balance and carrying materials. Their digging behaviour not only aids feeding but also benefits the ecosystem by improving
         soil health and promoting plant growth.'''.replace( '\n', ' ' ),
      '''Like other marsupials, brush-tailed bettongs give birth to very underdeveloped young. The tiny joey continues to grow in
         the mother’s pouch for several months before emerging. Females can reproduce year-round under suitable conditions, which
         helps populations recover when threats are controlled.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a male brush-tailed bettong, Tucker.'''
   ),
   (
      'Clown Triggerfish',
      'Balistoides Capriscus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The clown triggerfish is part of the main tank habitat in the Great Barrier Reef exhibit in the Australasia pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The clown triggerfish is a striking marine fish known for its bold black body covered in large white spots, a yellow mouth,
         and vivid yellow accents on the fins and tail. It has a chunky, oval-shaped body and a strong, beak-like mouth used for
         crushing hard prey. The species belongs to the triggerfish family (Balistidae), named for the locking dorsal spine that can
         be “triggered” into place as a defense mechanism.'''.replace( '\n', ' ' ),
      '''lown triggerfish are found in tropical and subtropical waters of the Indo-Pacific region, including coral reefs around
         Southeast Asia, northern Australia, and the western Pacific islands. They typically inhabit reef slopes and lagoons, often
         sheltering in crevices during the night.'''.replace( '\n', ' ' ),
      '''In the wild, clown triggerfish feed on hard-shelled invertebrates such as sea urchins, crustaceans, mollusks, and
         occasionally small fish. Their powerful jaws and specialized teeth allow them to crush shells that many other fish cannot.
         At the zoo or aquarium, they are offered a varied diet of seafood items designed to promote natural feeding behaviours and
         dental health.'''.replace( '\n', ' ' ),
      '''Clown triggerfish are generally solitary and highly territorial, especially as adults. They are intelligent and curious
         fish, often recognizing keepers and actively investigating their surroundings. While visually appealing, they can be
         aggressive toward tank mates and are usually housed alone or with carefully selected species.'''.replace( '\n', ' ' ),
      '''One of the clown triggerfish’s most notable adaptations is its locking dorsal spine, which can be raised to wedge the fish
         securely into reef crevices, making it difficult for predators to remove. Its thick skin and strong jaws provide further
         protection, while excellent eyesight helps it locate prey among coral structures.'''.replace( '\n', ' ' ),
      '''Clown triggerfish reproduce by laying eggs on sandy or rocky substrates near reefs. The eggs are guarded aggressively,
         often by the female, until they hatch. The larvae drift in open water before settling onto reefs as they mature, gradually
         developing their distinctive colouration.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crested Pigeon',
      'Ocyphaps Lophotes',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crested pigeon is part of the main aviary in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The crested pigeon is a medium-sized pigeon distinguished by the tall, slender crest of feathers on the top of its head.
         Its plumage is soft grey with pinkish tones on the chest, darker wings, and a distinctive black wing stripe bordered by
         iridescent green or purple patches. When startled into flight, the wings produce a sharp whistling sound caused by modified
         feathers. The species belongs to the pigeon and dove family (Columbidae).'''.replace( '\n', ' ' ),
      '''Crested pigeons are native to Australia and are found across a wide range of environments, including open woodlands,
         grasslands, farmland, parks, and urban areas. They are highly adaptable and often thrive near human settlements, as long as
         food and water are available.'''.replace( '\n', ' ' ),
      '''These pigeons primarily feed on seeds and grains gathered from the ground. Their diet includes grasses, herbs, and
         agricultural crops. At the zoo, crested pigeons are provided with a balanced mix of seeds and grains that reflects their
         natural feeding habits, often scattered to encourage natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Crested pigeons are social birds that are commonly seen in pairs or small flocks. They are generally calm and tolerant of
         other species. The distinctive whistling sound produced during takeoff acts as a warning signal to other pigeons when
         danger is nearby. They spend much of their time walking on the ground and fly only when necessary.'''.replace( '\n', ' ' ),
      '''The whistling wing feathers are a key adaptation that provides an early warning system for nearby birds, increasing group
         survival. Their strong legs and feet are well suited for ground feeding, while their ability to live in dry environments is
         supported by efficient water use and flexible feeding habits.'''.replace( '\n', ' ' ),
      '''Crested pigeons form monogamous pairs and build simple stick nests in trees or shrubs. The female typically lays two eggs,
         which are incubated by both parents. Chicks grow quickly and are fed “pigeon milk,” a nutrient-rich secretion produced by
         the parents, before transitioning to solid food.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crimson Rosella',
      'Platycercus Elegans',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crimson rosella is part of the main aviary in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The crimson rosella is a brightly coloured parrot known for its vivid red plumage, deep blue wings and tail, and black
         scalloped patterning across the back. Adults have a pale beak and dark eyes, while juveniles are mostly green and gradually
         develop their red colouring as they mature. The species belongs to the parrot family (Psittaculidae) and is easily
         recognized by both its colouration and strong, curved beak.'''.replace( '\n', ' ' ),
      '''Crimson rosellas are native to eastern and southeastern Australia, including forested regions, woodlands, and coastal
         bushland. They are also commonly found in parks and gardens near urban areas, where suitable trees and food sources are
         available.'''.replace( '\n', ' ' ),
      '''Their diet consists mainly of seeds, fruits, berries, nuts, blossoms, and insects. Crimson rosellas forage both in trees
         and on the ground. At the zoo, they are offered a varied diet that includes seeds, fresh fruits, vegetables, and formulated
         pellets to ensure balanced nutrition.'''.replace( '\n', ' ' ),
      '''Crimson rosellas are usually seen alone, in pairs, or in small family groups. They are active and agile birds, often moving
         quietly through trees. During the breeding season, pairs become more territorial. Their calls are clear and ringing, often
         heard before the bird is seen.'''.replace( '\n', ' ' ),
      '''Strong beaks allow crimson rosellas to crack seeds and nuts efficiently, while their zygodactyl feet (two toes facing
         forward nd two backward) provide excellent grip for climbing and handling food. Their bright plumage plays a role in
         communication and mate selection within forested environments.'''.replace( '\n', ' ' ),
      '''Breeding usually occurs in spring and summer. Crimson rosellas nest in tree hollows, where the female lays between four and
         eight eggs. The female incubates the eggs while the male provides food. Chicks remain in the nest for several weeks before
         fledging and may stay with their parents for a time after leaving the nest.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Demoiselle Crane',
      'Grus Virgo',
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The demoiselle cranes can be found in the outdoor aviary at the entrance to the Australasia Pavilion. The demoiselle cranes
         are generally more active earlier in the day, when they can often be seen wandering around their habitat, foraging for
         food. The cranes have no indoor public viewing.'''.replace( '\n', ' ' ),
      '''Demoiselle cranes are most reliably seen from the spring through the fall. They are fairly hardy birds, but will generally
         retreat to shelter in the coldest months. '''.replace( '\n', ' ' ),
      '''The demoiselle crane is a medium-sized crane distinguished by its slender body, long legs, and striking gray plumage.
         Adults have a white face stripe running from the eye down the neck, a black neck, and long, delicate white feathers
         trailing from the back of the head, giving it a “veil-like” appearance. The species belongs to the crane family (Gruidae)
         and is named for its elegant, graceful appearance reminiscent of a young lady.'''.replace( '\n', ' ' ),
      '''Demoiselle cranes are native to central Eurasia, ranging from the Black Sea region through Central Asia to Mongolia. They
         inhabit grasslands, steppes, and semi-arid plains, often near water sources. During migration, they travel thousands of
         kilometers, spending winters in India and northeastern Africa.'''.replace( '\n', ' ' ),
      '''They are omnivorous, feeding primarily on seeds, grains, insects, small vertebrates, and plant material. Demoiselle cranes
         forage by walking slowly through grasslands, pecking at the ground, and probing for insects or other small prey. In
         captivity, their diet is supplemented with grains, vegetables, and formulated pellets to mimic their natural intake.'''
         .replace( '\n', ' ' ),
      '''Demoiselle cranes are highly social and often form pairs or small family groups outside of migration. They are known for
         their elaborate courtship dances, which include bowing, jumping, and wing-flapping displays. These cranes are generally
         quiet when foraging but produce loud trumpeting calls during flight and when communicating with conspecifics.'''
         .replace( '\n', ' ' ),
      '''Long legs and toes allow efficient movement across grasslands and shallow water, while strong wings support long migratory
         flights. Their elongated neck and sharp beak assist in foraging and social displays. The trailing white feathers on the
         head are thought to enhance visual signals during mating rituals.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring and summer. Pairs nest on the ground in shallow scrapes lined with grass. Typically, two eggs
         are laid and both parents share incubation duties. Chicks are precocial, leaving the nest shortly after hatching and
         following their parents to learn foraging and survival behaviours.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one male and one female demoiselle crane.'''.replace( '\n', ' ' )
   ),
   (
      'Eastern Rosella',
      'Platycercus Eximius',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Eastern rosella is part of the main aviary in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Eastern Rosella is a medium-sized parrot with vibrant plumage. Its head is bright red, the back and wings are green and
         yellow, and the belly is white with scalloped black markings. The species has a short, strong beak and a long, tapered
         tail. Belonging to the parrot family (Psittaculidae), it is easily recognized by its striking mix of colours and lively
         presence.'''.replace( '\n', ' ' ),
      '''Eastern Rosellas are native to southeastern Australia, Tasmania, and nearby islands. They inhabit open forests, woodlands,
         farmlands, and urban parks. They adapt well to areas with scattered trees and open grassy ground, often near water sources.'''
         .replace( '\n', ' ' ),
      '''These birds are primarily granivorous, feeding on seeds, fruits, berries, flowers, and occasionally insects. They forage
         both on the ground and in low vegetation. At the zoo, their diet includes a mix of seeds, fresh fruits, vegetables, and
         nutritionally balanced pellets, often scattered to encourage natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Eastern Rosellas are social but less gregarious than some other parrots, often seen in pairs or small groups. They are
         active and curious, frequently moving between perches and feeding areas. They are generally non-aggressive and interact
         calmly with other compatible species in mixed aviaries.'''.replace( '\n', ' ' ),
      '''Strong, curved beaks allow them to efficiently crack seeds and manipulate objects. Their bright plumage aids in
         communication and mate selection, while agile feet help them perch, climb, and forage in trees and shrubs. They are well
         adapted to open forest and grassland habitats with moderate temperature variation.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in spring. Eastern Rosellas nest in tree hollows, where the female lays 4–8 eggs. Both parents
         participate in incubation and feeding the young. Juveniles are initially green with muted colours, developing adult plumage
         over several months.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Emerald Tree Boa',
      'Corallus Caninus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The emerald tree boa can be found in a habitat down the hallway past the aviary and to the left.''',
      None,                                                          # Seasonal viewing tips
      '''The emerald tree boa is a striking, non-venomous snake known for its bright green dorsal colouring and white zigzag
         markings along its back. Adults typically reach 1.2–2 metres in length. Its triangular head and heat-sensing pits along the
         upper lip help detect prey. The species belongs to the boa family (Boidae) and is famous for its arboreal lifestyle and
         coiled resting posture on branches.'''.replace( '\n', ' ' ),
      '''Emerald tree boas are native to the tropical rainforests of northern South America, including Brazil, Colombia, and
         Venezuela. They spend most of their lives in the forest canopy, preferring humid, shaded environments near rivers and
         streams.'''.replace( '\n', ' ' ),
      '''In the wild, emerald tree boas feed on small mammals, birds, and occasionally reptiles. They are ambush predators, waiting
         coiled on branches until prey comes within striking distance. At the zoo, their diet consists of appropriately sized
         rodents and birds, offered to mimic natural hunting behaviour.'''.replace( '\n', ' ' ),
      '''Emerald tree boas are largely solitary and highly territorial. They are mostly nocturnal, becoming active at night to
         hunt. During the day, they remain coiled on branches, using their cryptic colouring to blend in with the foliage. They are
         generally non-aggressive unless provoked.'''.replace( '\n', ' ' ),
      '''These snakes are perfectly adapted for life in the trees. Prehensile tails allow them to maintain a secure grip on
         branches, while their muscular bodies enable them to coil tightly and strike accurately. Heat-sensing pits help locate
         warm-blooded prey even in low-light conditions, and their green colouration provides camouflage among leaves.'''
         .replace( '\n', ' ' ),
      '''Emerald tree boas are ovoviviparous, meaning females give birth to live young rather than laying eggs. Litters typically
         contain 10–30 neonates. Juveniles are yellow or orange at birth, gradually developing the bright green adult colouration
         over several months.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Flame Angelfish',
      'Centropyge Loriculus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The flame angelfish is part of the main tank habitat in the Great Barrier Reef exhibit in the Australasia pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The flame angelfish is a small, vividly coloured marine fish with a bright orange-red body crossed by several vertical black
         bars. Its dorsal and anal fins are edged with electric blue, making it one of the most recognizable angelfish species in reef
         aquariums. The species belongs to the pygmy angelfish group, which are smaller and more compact than the larger marine
         angelfishes.'''.replace('\n', ' '),
      '''Flame angelfish are native to the tropical Pacific Ocean, particularly around coral reefs in regions such as Hawaii, the
         Marshall Islands, and other central Pacific island systems. They inhabit coral-rich reef slopes and lagoons where rockwork,
         caves, and branching corals provide shelter and grazing surfaces.'''.replace('\n', ' '),
      '''In the wild, flame angelfish feed on algae, detritus, and small benthic invertebrates found on reef surfaces. In aquariums,
         they are typically offered a varied diet that can include marine algae, sponge-based angelfish preparations, and finely
         chopped seafood. Frequent grazing opportunities help support their natural behaviour and coloration.'''.replace('\n', ' '),
      '''Flame angelfish are active, alert reef fish that spend much of the day weaving through rockwork and coral structures. They can
         be territorial toward similar fish, especially in confined spaces, but are generally curious and constantly on the move. Their
         quick, darting movements make them visually striking additions to large reef displays.'''.replace('\n', ' '),
      '''Their compact body and precise fin control allow them to move efficiently through narrow reef crevices while foraging. Bright
         colouration may help with species recognition and territorial signalling on busy coral reefs. Like many reef fish, they are
         well adapted to complex three-dimensional habitats where agility is more important than sustained speed.'''.replace('\n', ' '),
      '''Flame angelfish reproduce by spawning in open water, typically near dusk. Eggs and sperm are released into the water column
         where fertilization occurs externally. The larvae drift as plankton before settling onto reefs and gradually developing into
         their adult coloration and form.'''.replace('\n', ' '),
      None                                                           # Animals at the zoo
   ),
   (
      'Fly River Turtle',
      'Carettochelys Insculpta',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Fly River turtles live in the pond in the main aviary. You can spot them by taking a right once you pass the aviary,
         and looking into the underwater viewing area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Fly River turtle, also known as the pig-nosed turtle, is a freshwater turtle notable for its soft, leathery shell and
         distinctive pig-like snout. Adults typically have a grey-green carapace and large, flipper-like limbs adapted for swimming.
         The species belongs to the family Carettochelyidae and is the only freshwater turtle with fully webbed flippers, giving it
         a unique appearance among turtles.'''.replace( '\n', ' ' ),
      '''Fly River turtles are native to northern Australia and southern New Guinea, primarily inhabiting slow-moving rivers,
         billabongs, and lagoons. They prefer freshwater habitats with soft substrates and submerged vegetation, which provide cover
         and feeding opportunities.'''.replace( '\n', ' ' ),
      '''In the wild, Fly River turtles are omnivorous, feeding on aquatic plants, fruits, and invertebrates. They use their
         flexible, flippered limbs to forage along the bottom of rivers and creeks. At the zoo, their diet includes a mix of leafy
         greens, aquatic vegetation, and small protein sources such as insects or fish to replicate natural foraging behaviour.'''
         .replace( '\n', ' ' ),
      '''Fly River turtles are largely solitary and spend most of their time submerged. They are strong swimmers and are capable of
         moving quickly through the water. During nesting season, females come ashore to lay eggs in sand or soil banks. They are
         generally calm and non-aggressive but may retreat quickly when disturbed.'''.replace( '\n', ' ' ),
      '''This species is highly adapted for aquatic life. The flipper-like limbs allow powerful swimming, while the pig-shaped snout
         helps with breathing at the water’s surface without raising the body. Their soft shell provides flexibility, and their
         cryptic colouration aids in camouflage among river vegetation.'''.replace( '\n', ' ' ),
      '''Females lay eggs on sandy riverbanks, often travelling significant distances from water to nest. The eggs incubate in warm
         sand, with temperature influencing the sex of the hatchlings. Young turtles are fully aquatic from birth and rely on their
         strong swimming abilities and cryptic colouring to avoid predators.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Galah',
      'Eolophus Roseicapilla',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The galah is part of the main aviary in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Galah, also known as the rose-breasted cockatoo, is a medium-sized parrot distinguished by its pink face and chest,
         grey back, wings, and tail, and a short, curved beak. Both males and females look similar, though subtle differences in eye
         colour can indicate sex. Galahs belong to the cockatoo family (Cacatuidae) and are easily recognised by their soft
         pink-and-grey plumage and crest.'''.replace( '\n', ' ' ),
      '''Galahs are native to most of mainland Australia, inhabiting open woodlands, grasslands, farmland, and urban areas. They are
         highly adaptable and are commonly found near water and food sources, often in large flocks.'''.replace( '\n', ' ' ),
      '''Their diet consists mainly of seeds, fruits, nuts, and vegetation. Galahs forage on the ground or in low trees and shrubs.
         In captivity, they are provided with a mix of seeds, fruits, vegetables, and formulated pellets to ensure balanced
         nutrition and encourage natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Galahs are social and highly gregarious, often forming flocks of dozens or hundreds. They are intelligent and playful,
         frequently engaging in acrobatic behaviours such as hanging upside down or swinging from branches. Vocal and interactive,
         they communicate with a range of calls and whistles, and pairs often form lifelong bonds.'''.replace( '\n', ' ' ),
      '''Strong, curved beaks allow Galahs to crack seeds and nuts, while zygodactyl feet (two toes forward, two backward) aid in
         climbing and handling food. Their vibrant pink-and-grey plumage helps with mate attraction and species recognition. Their
         social behaviour provides protection, as group vigilance reduces predation risk.'''.replace( '\n', ' ' ),
      '''Breeding usually occurs in spring and summer. Pairs nest in tree hollows, where the female lays 2–5 eggs. Both parents take
         part in incubation and feeding of the chicks. Juveniles fledge after several weeks but may remain with the parents for a
         short period before joining larger flocks.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a female galah, Rosie.'''
   ),
   (
      'Green Tree Python',
      'Morelia Viridis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green tree python can be found in a habitat down the hallway past the aviary and to the left.''',
      None,                                                          # Seasonal viewing tips
      '''The green tree python is a slender, arboreal snake known for its brilliant green colouration, sometimes with blue or yellow
         accents depending on the individual and age. Juveniles are often yellow, red, or orange before changing to the vivid green
         of adults. The species has a triangular head, prehensile tail, and large eyes adapted for low-light hunting. It belongs to
         the python family (Pythonidae).'''.replace( '\n', ' ' ),
      '''Green tree pythons are native to the rainforests of New Guinea, parts of Indonesia, and northern Australia. They inhabit
         humid tropical forests, often resting coiled on branches high above the forest floor. Dense foliage provides camouflage
         and protection from predators.'''.replace( '\n', ' ' ),
      '''In the wild, green tree pythons feed primarily on small mammals, birds, and occasionally reptiles. They are ambush
         predators, remaining coiled on branches and striking quickly when prey passes nearby. At the zoo, their diet consists of
         appropriately sized rodents or birds, offered in a way that encourages natural hunting behaviour.'''.replace( '\n', ' ' ),
      '''Green tree pythons are solitary and highly territorial. They are mostly nocturnal hunters and spend much of the day resting
         coiled around branches. Their arboreal lifestyle makes them slow to move but extremely effective in ambushing prey. They
         are generally non-aggressive unless handled or provoked.'''.replace( '\n', ' ' ),
      '''Their prehensile tails allow them to maintain balance and grip on branches while hunting. Heat-sensing pits along their
         upper lips detect warm-blooded prey even in low-light conditions. Cryptic green colouring provides excellent camouflage in
         dense foliage, while their muscular bodies enable powerful, precise strikes.'''.replace( '\n', ' ' ),
      '''Green tree pythons are oviparous, laying clutches of 6–30 eggs in concealed locations. Females coil around the eggs to
         provide protection and regulate temperature until hatching. Juveniles are independent from birth and undergo dramatic
         colour changes as they mature.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Green-Winged Dove',
      'Chalcophaps Indica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green-winged dove is part of the main aviary in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Green-winged Dove is a small, plump pigeon with a soft grey-brown body, a slightly iridescent green sheen on its wings,
         and a pale pinkish chest. It has a short, slender beak and red eyes with a subtle ring around them. The species belongs to
         the pigeon and dove family (Columbidae) and is easily recognised by its delicate colouring and gentle posture.'''
         .replace( '\n', ' ' ),
      '''Green-winged Doves are native to South and Southeast Asia, inhabiting forests, plantations, gardens, and open wooded areas.
         They adapt well to human-modified landscapes and are often seen near water sources or feeding areas.'''.replace( '\n', ' ' ),
      '''These doves feed primarily on seeds, grains, fruits, and occasionally small insects. They forage on the ground or in low
         vegetation. In captivity, their diet includes a mix of seeds, grains, and small fruits, designed to reflect natural
         feeding behaviour.'''.replace( '\n', ' ' ),
      '''Green-winged Doves are social birds, often seen in pairs or small groups. They are generally calm and non-aggressive,
         moving quietly and foraging steadily. During courtship, males perform gentle displays and soft cooing calls to attract
         mates.'''.replace( '\n', ' ' ),
      '''Their compact bodies and strong wings allow efficient short-distance flight and manoeuvring through dense foliage. Subtle
         green iridescence helps with camouflage in leafy habitats, while their keen eyesight aids in detecting food and predators.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs year-round in favourable conditions. Nests are small platforms of twigs and leaves, often built in shrubs
         or low trees. Typically, the female lays 1–2 eggs, incubated by both parents. Chicks are altricial, dependent on parental
         care until fledging.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Komodo Dragon',
      'Varanus Komodoensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Komodo dragons can we found in the center habitat in the main area of the pavilion past the aviary. The Komodo dragons
         at the zoo are young, and still getting used to their habitat. Most of the time you can find them high in the tree in the
         center of the enclosure. Look closely for a claw, or a dangling tail.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Komodo dragon is the largest living lizard in the world, growing up to 3 metres in length and weighing up to 70
         kilograms. It has a robust body covered in rough, scaly skin ranging from grey to reddish-brown, a broad head with powerful
         jaws, and a long, muscular tail. Its forked tongue and keen sense of smell aid in detecting prey over long distances. This
         species belongs to the monitor lizard family (Varanidae) and is instantly recognisable for its size and imposing presence.'''
         .replace( '\n', ' ' ),
      '''Komodo dragons are native to a few Indonesian islands, including Komodo, Rinca, Flores, and Gili Motang. They inhabit
         tropical savannahs, dry forests, and scrublands, often seeking shelter in burrows or under shade during the heat of the
         day.'''.replace( '\n', ' ' ),
      '''Komodo dragons are apex predators and opportunistic scavengers. Their diet includes deer, pigs, smaller reptiles, birds,
         eggs, and carrion. They use their sharp teeth, powerful bite, and bacteria-laden saliva to subdue prey. In captivity, their
         diet is carefully managed and includes a mix of meat, whole prey items, and enrichment to encourage natural hunting
         behaviours.'''.replace( '\n', ' ' ),
      '''These lizards are mostly solitary, coming together only to feed or breed. They are diurnal hunters, patrolling their
         territories during the day. Dominance hierarchies are established through physical displays and occasional combat. Komodo
         dragons are excellent swimmers and climbers in juvenile stages, though adults remain primarily terrestrial.'''
         .replace( '\n', ' ' ),
      '''Komodo dragons have evolved powerful limbs, strong jaws, and serrated teeth to take down large prey. Their forked tongues
         allow them to “smell” airborne chemicals, detecting carcasses up to 10 km away. Thick, armored skin provides protection
         from injury during fights and hunts. Their slow metabolism enables them to survive on infrequent, large meals.'''
         .replace( '\n', ' ' ),
      '''Komodo dragons reproduce sexually, and females can also reproduce via facultative parthenogenesis. Clutch sizes range from
         15–30 eggs, incubated for approximately 8 months in burrows or under vegetation. Hatchlings are highly vulnerable and
         spend their early years in trees to avoid predation. Adults reach sexual maturity around 8–9 years of age. In captivity,
         Komodo dragons live up to 30 years, while in the wild, typical lifespans are 25–30 years.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has two ~4-year-old Komodo dragons which were acquired in November of 2025. They were named by the
         community--the female being named Raya, and the male, Komo. They are still getting used to their new space and thus may be
         difficult to spot. They are also only a fraction of their full-grown size.'''.replace( '\n', ' ' )
   ),
   (
      'Kookaburra',
      'Dacelo Novaeguineae',
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The kookaburras can either be found in the outdoor aviary with the demoiselle cranes, or inside in the small aviary just
         past and to the right of the cockatoos, depending on the time of year.'''.replace( '\n', ' ' ),
      '''Kookaburras are warm weather birds, and thus are only comfortable outside during the warmer months of the year, roughly
         from May to September.'''.replace( '\n', ' ' ),
      '''The kookaburra is a medium-sized kingfisher known for its robust body, large head, and strong, hooked bill. Its plumage is
         mostly brown and cream, with blue wing patches and dark eye stripes. The species belongs to the kingfisher family
         (Alcedinidae) and is instantly recognised by its unmistakable “laughing” call.'''.replace( '\n', ' ' ),
      '''Kookaburras are native to eastern Australia and New Guinea, inhabiting open forests, woodlands, and urban areas. They
         prefer environments with scattered trees and perches that allow them to hunt and call over their territory.'''
         .replace( '\n', ' ' ),
      '''They are carnivorous, feeding on insects, small mammals, reptiles, and amphibians. Kookaburras hunt by perching silently
         and swooping down on prey. At the zoo, they are provided with a diet that mirrors their natural hunting behaviour,
         including insects, small rodents, and other appropriate protein sources.'''.replace( '\n', ' ' ),
      '''Kookaburras are social birds, often seen in family groups. They are territorial and use their distinctive call to
         communicate with others and mark boundaries. They are generally diurnal and spend much of the day perched and observing
         their surroundings.'''.replace( '\n', ' ' ),
      '''Strong, sturdy beaks allow them to capture and kill prey efficiently. Their plumage provides camouflage among trees, and
         their keen eyesight enables precise strikes. Loud, recognizable calls help maintain social cohesion and deter intruders.'''
         .replace( '\n', ' ' ),
      '''Kookaburras nest in tree hollows or termite mounds. Females lay 2–4 eggs, with both parents participating in incubation
         and feeding of the chicks. Juveniles fledge after several weeks. In the wild, kookaburras typically live up to 15–20 years,
         while in captivity they may live longer with proper care.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of kookaburras.'''
   ),
   ( # Also in African Rainforest Pavilion
      'Lau Banded Iguana',
      'Brachylophus Fasciatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Lau banded iguana can be found in Australasia Pavilion in the hallway past the aviary and to the left. The igunas live
         in the habitat right at the end of the hallway, beside the wombats. In this habitat, the iguanas like to lay on top of the
         branches near the top and sides of the enclosure. In the African Rainforest Pavilion, the iguanas can be found about
         halfway through the pavilion near the chameleons and naked mole rats, in between the cichlids and the pygmy hippos.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Lau Banded Iguana is a small, vibrant lizard notable for its bright green body with distinctive pale blue or white
         transverse bands across the back. Males are generally brighter than females, especially during the breeding season. It has
         a slender body, long tail, and sharp claws adapted for climbing. This species belongs to the iguana family (Iguanidae) and
         is easily recognised by its striking colour pattern.'''.replace( '\n', ' ' ),
      '''Native to the islands of Lau in Fiji, this iguana inhabits tropical forests and coastal vegetation, often living in trees
         or shrubs. It prefers warm, humid environments with plenty of foliage for cover and sunning.'''.replace( '\n', ' ' ),
      '''The Lau Banded Iguana is primarily herbivorous, feeding on leaves, flowers, fruits, and shoots. Occasionally, it may
         consume insects or small invertebrates. At the zoo, their diet includes a variety of leafy greens, vegetables, and fruits,
         carefully balanced to reflect natural feeding habits and maintain vibrant colouring.'''.replace( '\n', ' ' ),
      '''These iguanas are generally solitary and territorial, especially males. They are diurnal, spending much of the day basking
         in sunlight to regulate body temperature. Males may display head-bobbing and dewlap extension to assert dominance or during
         courtship. They are calm but alert, often retreating to higher branches when disturbed.'''.replace( '\n', ' ' ),
      '''The iguana’s sharp claws and strong limbs make it an excellent climber, while its long tail aids in balance and defensive
         displays. Bright colouration is used for both camouflage among foliage and social signalling during mating season. Their
         digestive system is adapted to process fibrous plant material efficiently.'''.replace( '\n', ' ' ),
      '''Mating occurs in the warmer months, with females laying clutches of 2–7 eggs in shallow nests on the ground or in leaf
         litter. Hatchlings emerge fully independent. In the wild, these iguanas can live up to 15 years, while captive individuals
         may live longer with proper care.'''.replace( '\n', ' ' ),
      '''The Toronto zoo is home to a pair of Lau banded iguanas which live in the Australasia Pavilion, and another pair which
         lives in the African Rainforest Pavilion.'''.replace( '\n', ' ' ),
   ),
   (
      'Lionfish',
      'Pterois Volitans',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The lionfish can be found in the main tank in the Great Barrier Reef exhibit in the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The lionfish is a venomous marine fish known for its dramatic appearance, with long, flowing pectoral fins and spiky,
         striped dorsal fins. Its body is reddish-brown with white vertical stripes, giving it a “lion-like” mane effect. Belonging
         to the scorpionfish family (Scorpaenidae), it is instantly recognisable by its ornate fins and bold patterning.'''
         .replace( '\n', ' ' ),
      '''Lionfish are native to the Indo-Pacific region, inhabiting coral reefs, lagoons, and rocky crevices. They are typically
         found at depths of 2–60 metres, favouring complex reef structures that provide shelter and hunting opportunities.'''
         .replace( '\n', ' ' ),
      '''Lionfish are carnivorous ambush predators, feeding on small fish, crustaceans, and invertebrates. They use their wide
         pectoral fins to corner prey before striking rapidly. In aquariums, they are fed a diet of small fish and crustaceans,
         often delivered  encourage natural hunting behaviours.'''.replace( '\n', ' ' ),
      '''Lionfish are generally solitary, occupying defined territories. They are slow-moving and deliberate, relying on camouflage
         and their striking fins to intimidate or confuse potential threats. While venomous, they are generally passive unless
         provoked.'''.replace( '\n', ' ' ),
      '''Venomous dorsal, pelvic, and anal spines provide defence against predators. Their patterned colouring and fins aid in
         camouflage among reef structures, while their lateral line system and large eyes enable precise detection of nearby prey.'''
         .replace( '\n', ' ' ),
      '''Lionfish reproduce by laying gelatinous egg masses, which float in the water column until hatching. They reach sexual
         maturity within one year. In the wild, lionfish can live up to 10–15 years, and they exhibit high reproductive rates,
         contributing to their success as both native and invasive species.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Live Coral Reefs',
      None,                                                          # Latin name
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # General viewing tips
      None,                                                          # Seasonal viewing tips
      '''Live coral reefs are complex underwater ecosystems formed by colonies of tiny animals called coral polyps. These polyps
         secrete calcium carbonate skeletons that build the reef structure over time. The reefs are home to a vast array of
         organisms, including fish, invertebrates, algae, and microorganisms. Colourful corals display hues of red, orange, pink,
         purple, and green, contributing to the visual richness of the habitat.'''.replace( '\n', ' ' ),
      '''Coral reefs are found in warm, shallow, tropical oceans around the world, particularly in the Indo-Pacific region, the
         Caribbean, and parts of the Indian Ocean. They thrive in clear, sunlit waters where temperature, salinity, and water
         quality are stable. Reefs provide shelter, breeding grounds, and feeding areas for countless marine species.'''
         .replace( '\n', ' ' ),
      '''Coral polyps feed primarily on microscopic plankton and photosynthetic algae called zooxanthellae, which live inside their
         tissues. The algae provide nutrients via photosynthesis, while the corals offer protection. Reefs as a whole support a
         diverse food web, from small invertebrates and fish to large predators.'''.replace( '\n', ' ' ),
      '''While corals themselves are sessile, the reef ecosystem is highly dynamic. Fish and invertebrates interact continuously —
         schooling, foraging, cleaning, and defending territories. Coral polyps reproduce both sexually and asexually, contributing
         to reef growth and recovery.'''.replace( '\n', ' ' ),
      '''Corals have evolved symbiosis with algae to survive in nutrient-poor waters. Their calcium carbonate skeletons protect
         polyps and provide habitat for other species. Many reef inhabitants have camouflage, bright warning colours, or specialized
         feeding adaptations to thrive within the complex reef structure.'''.replace( '\n', ' ' ),
      '''Corals reproduce via broadcast spawning, releasing eggs and sperm into the water simultaneously, or through budding
         (asexual reproduction). Reef ecosystems develop slowly over decades or centuries. Individual coral colonies can live for
         decades, while the reef as a whole can persist for thousands of years under favourable conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Longnose Butterflyfish',
      'Forcipiger Longirostris',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The longnose butterflyfish is found in the main tank in the Great Barrier Reef exhibit in the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Longnose Butterflyfish is a small, colourful reef fish recognised by its elongated, pointed snout and bright yellow
         body. Its face and dorsal area are marked with black stripes, and the fins are mostly yellow with translucent edges. It
         belongs to the butterflyfish family (Chaetodontidae) and is easily recognised by its distinctive snout, which helps it
         reach food in narrow crevices.'''.replace( '\n', ' ' ),
      '''This species is native to the Indo-Pacific region, including coral reefs around Hawaii, Australia, and Southeast Asia. It
         prefers shallow reef slopes and lagoons with abundant coral cover, which provides both food and shelter.'''
         .replace( '\n', ' ' ),
      '''Longnose Butterflyfish feed primarily on small invertebrates, coral polyps, and crustaceans. Their long, pointed snout
         allows them to extract prey from crevices in coral. In aquariums, they are provided with a diet that replicates their
         natural feeding behaviour, including small invertebrates and specialized reef fish pellets.'''.replace( '\n', ' ' ),
      '''These fish are usually seen in pairs or small groups. They are diurnal and highly active during the day, patrolling reef
         areas for food. Longnose Butterflyfish are territorial, particularly around feeding zones, and use body displays and fin
         movements to signal dominance or courtship.'''.replace( '\n', ' ' ),
      '''The elongated snout is a specialised adaptation for extracting prey from tight coral spaces. Their bright colouration acts
         as both camouflage among corals and a signal to conspecifics during social interactions. Laterally compressed bodies allow
         agile movement through complex reef structures.'''.replace( '\n', ' ' ),
      '''Longnose Butterflyfish reproduce through external fertilization, with females releasing eggs into the water column where
         males fertilise them. The eggs hatch into free-swimming larvae, which eventually settle on coral reefs as juveniles. In the
         wild, they can live up to 7–10 years, while in captivity they may live slightly longer under proper care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'MacLeay\'s Spectres',
      'Extatosoma Tiaratum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The MacLeay's spectres can be found past the aviary and in the room to the right.''',
      None,                                                          # Seasonal viewing tips
      '''MacLeay’s Spectre, commonly known as the Giant Spiny Stick Insect, is a large, camouflaged insect with a long, slender body
         and spiny projections along its legs and thorax. Adults can reach up to 25–30 cm in length. Its mottled brown colouring and
         twig-like appearance provide excellent camouflage among branches and leaves. This species belongs to the phasmid family
         (Phasmatidae).'''.replace( '\n', ' ' ),
      '''Native to eastern Australia, MacLeay’s Spectres inhabit rainforests, woodlands, and scrub areas. They spend most of their
         lives on shrubs and trees, blending into twigs and foliage to avoid predators.'''.replace( '\n', ' ' ),
      '''These insects are herbivorous, feeding primarily on leaves, especially eucalyptus. They are slow-moving and rely on
         camouflage rather than speed to avoid being eaten. In captivity, they are provided with a diet of suitable leaves and
         occasionally soft plant material to maintain health.'''.replace( '\n', ' ' ),
      '''MacLeay’s Spectres are largely solitary and nocturnal, becoming more active at night. When disturbed, they remain
         motionless or sway gently to mimic surrounding vegetation. Their stick-like appearance and slow movements are their primary
         defence against predators.'''.replace( '\n', ' ' ),
      '''Exceptional camouflage allows them to evade visual predators. Spiny projections deter predators from handling them. They
         can also shed limbs if caught, which may later regenerate. Their slow metabolism allows survival on a leaf-only diet.'''
         .replace( '\n', ' ' ),
      '''Females can reproduce sexually or via parthenogenesis (asexual reproduction). Eggs resemble seeds and are dropped to the
         ground, where they may remain dormant until suitable conditions arise. Nymphs hatch resembling miniature adults and undergo
         several moults before reaching maturity. Lifespan is typically 1–2 years in captivity, depending on conditions.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Malagasy Rainbowfish',
      'Bedotia Madagascariensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Malagasy rainbowfish can be found in room past the aviary and to the right, in one of the tank enclosures.''',
      None,                                                          # Seasonal viewing tips
      '''The Malagasy Rainbowfish is a small, colourful freshwater fish native to Madagascar. Males are more brightly coloured than
         females, displaying iridescent shades of red, orange, and green along the body, while females are generally paler. It has a
         slender, streamlined body with a forked tail, characteristic of the Bedotiidae family.'''.replace( '\n', ' ' ),
      '''This species inhabits small rivers, streams, and freshwater wetlands in eastern Madagascar. It prefers clear, slow-moving
         waters with plenty of aquatic vegetation and submerged structures for shelter.'''.replace( '\n', ' ' ),
      '''Malagasy Rainbowfish are omnivorous, feeding on insects, crustaceans, algae, and small plant matter. In aquariums, they are
         offered a mix of flake food, live or frozen insects, and plant-based foods to mimic their natural diet and encourage
         foraging behaviour.'''.replace( '\n', ' ' ),
      '''These fish are active and schooling, often seen moving in small groups. Males display bright colours to attract mates and
         establish dominance hierarchies, while females tend to remain more cryptic. They are peaceful and interact well with other
         compatible species in shared exhibits.'''.replace( '\n', ' ' ),
      '''Their streamlined bodies and strong tails allow agile swimming through vegetation and currents. Colouration plays a key
         role in mating displays and social signalling within schools. Their omnivorous diet and flexibility help them survive in
         variable freshwater environments.'''.replace( '\n', ' ' ),
      '''Malagasy Rainbowfish reproduce by laying small eggs on submerged vegetation or surfaces. Eggs hatch in about 7–10 days,
         with juveniles growing rapidly under optimal conditions. Lifespan is typically 3–5 years in captivity, with good water
         quality and diet contributing to longevity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Mimic Surgeonfish',
      'Acanthurus Pyroferus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The mimic surgeonfish is part of the main tank habitat in the Great Barrier Reef exhibit in the Australasia pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The mimic surgeonfish has a sleek, oval-shaped body with a pointed snout, continuous dorsal and anal fins, and a crescent-
         shaped tail. Adults are typically warm brown to golden-orange in colour with darker edging on the fins and a bold dark
         stripe running through the eye and across the face. Juveniles often resemble dwarf angelfish species, giving this fish its
         “mimic” name.'''.replace('\n', ' '),
      '''This species is found throughout the tropical Indo-Pacific, especially around coral reefs, lagoons, and reef slopes near
         Indonesia, the Philippines, the Great Barrier Reef, and surrounding regions. It prefers shallow reef environments with plenty
         of algae growth and coral structures that provide shelter from predators.'''.replace('\n', ' '),
      '''Mimic surgeonfish primarily graze on algae growing on rocks and coral surfaces. They use their small mouths to nip
         filamentous algae and organic material from reef surfaces throughout the day. In aquariums, they are fed algae sheets,
         herbivore pellets, and vegetable-based marine diets to support healthy digestion and colouration.'''.replace('\n', ' '),
      '''This fish is active and constantly on the move, spending much of the day grazing and exploring reef surfaces. It is generally
         peaceful but may become territorial toward similar-shaped fish, especially other surgeonfish. Juveniles often remain close to
         coral shelter, while adults roam more openly through the reef habitat.'''.replace('\n', ' '),
      '''Its mimicry of dwarf angelfish species as a juvenile likely helps deter predators by resembling less vulnerable reef fish.
         Like other surgeonfish, it possesses a sharp retractable spine near the base of the tail, used for defense against threats.
         Its streamlined body and strong fins make it highly efficient at maneuvering through reef currents and narrow coral
         passages.'''.replace('\n', ' '),
      '''Mimic surgeonfish reproduce by broadcast spawning, where males and females release eggs and sperm into open water, usually at
         dusk. Fertilized eggs drift with currents before hatching into planktonic larvae. As they grow, juveniles develop their
         distinctive angelfish-like mimic coloration before gradually transitioning into the adult form.'''.replace('\n', ' '),
      None                                                           # Animals at the zoo
   ),
   (
      'Moon Jellyfish',
      'Aurelia Aurita',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The moon jellyfish can be found in the Great Barrier Reef exhibit, in the last tank before you exhibit the pavilion, on the
         right-hand side.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The moon jellyfish is a translucent, delicate-looking cnidarian with a smooth, bell-shaped body typically 25–40 cm in
         diameter. It has four distinct horseshoe-shaped gonads visible through the bell and trailing tentacles used for capturing
         prey. Belonging to the class Scyphozoa, it is instantly recognised by its ethereal, floating appearance.'''
         .replace( '\n', ' ' ),
      '''Moon jellyfish are found in coastal waters worldwide, often in bays, harbours, and estuaries. They prefer temperate to
         tropical waters and can tolerate varying salinity, making them adaptable to different marine environments.'''
         .replace( '\n', ' ' ),
      '''Moon jellyfish are carnivorous, feeding primarily on plankton, small crustaceans, fish eggs, and larvae. They capture prey
         using stinging cells (cnidocytes) on their tentacles, which paralyse and guide food to the mouth. In aquaria, they are fed
         a diet of live or frozen planktonic foods.'''.replace( '\n', ' ' ),
      '''Moon jellyfish drift with ocean currents and display pulsing movements to propel themselves slowly through water. They are
         generally solitary but may appear in large aggregations when currents concentrate them. Their stings are mild and primarily
         used for feeding rather than defence.'''.replace( '\n', ' ' ),
      '''Moon jellyfish are perfectly adapted to a drifting lifestyle. Their gelatinous, low-density body allows them to float
         effortlessly, and their stinging tentacles efficiently capture small prey. The simple nerve net allows basic responses to
         touch and environmental stimuli without a central brain.'''.replace( '\n', ' ' ),
      '''Moon jellyfish have a complex life cycle that includes both sexual and asexual stages. Adults (medusae) release eggs and
         sperm into the water; fertilised eggs develop into polyps, which can clone themselves before eventually transforming into
         juvenile medusae. Lifespan varies by stage: medusae typically live 6–12 months, though polyps can persist for several years
         under suitable conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   ( # Also in Indo-Malaya Pavilion
      'Nicobar Pigeon',
      'Caloenas Nicobarica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''Nicobar pigeons can be spotted in the main aviaries in the Australasia and Indo-Malaya Pavilions. In the Indo-Malaya
         Pavilion you can spot them most reliably when going down the staircase from the elevated Sumatran orangutan viewing, or
         along the part of the path between the Asian tortoises and the reticulated python, or across where you access the outdoor
         orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Nicobar Pigeon is a medium-sized, strikingly coloured bird with metallic green, blue, and copper plumage, a white tail,
         and a short, stout beak. Its neck feathers are long and glossy, forming a shaggy ruff. It belongs to the pigeon and dove
         family (Columbidae) and is easily recognised by its iridescent colours and distinctive body shape.'''.replace( '\n', ' ' ),
      '''Native to small islands in the Nicobar Islands, Southeast Asia, and the western Pacific, Nicobar Pigeons inhabit coastal
         forests, mangroves, and wooded areas near beaches. They are often found on remote islands, where they roost and forage
         safely from predators.'''.replace( '\n', ' ' ),
      '''Nicobar Pigeons are omnivorous, feeding primarily on seeds, fruits, berries, and small invertebrates. They forage on the
         ground, using their beaks to pick and manipulate food. At the zoo, they are provided with a varied diet that mimics natural
         feeding, including seeds, fruits, and occasional protein supplements.'''.replace( '\n', ' ' ),
      '''These pigeons are social birds, often seen in small flocks. They are strong fliers but spend considerable time foraging on
         the ground. They communicate with soft coos and calls and maintain hierarchical relationships within their group.'''
         .replace( '\n', ' ' ),
      '''Their strong legs and feet allow efficient ground foraging, while their iridescent feathers play a role in courtship and
         species recognition. Their flight is fast and direct, allowing them to escape predators and travel between islands.'''
         .replace( '\n', ' ' ),
      '''Nicobar Pigeons form monogamous pairs during the breeding season. They nest in trees or shrubs, laying a single egg, which
         is incubated by both parents. Chicks fledge after a few weeks but remain under parental care for some time. In captivity,
         they can live up to 15–20 years, while wild lifespans are generally slightly shorter.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Pennant Coral Fish',
      'Heniochus Acuminatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The pennant coral fish can be found in the main tank in the Great Barrier Reef exhibit in the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Pennant Coralfish, also known as the Longfin Bannerfish, is a striking marine fish recognised by its tall, triangular
         dorsal fin that resembles a pennant. Its body is mostly white with bold black vertical stripes and bright yellow fins. It
         belongs to the butterflyfish family (Chaetodontidae) and is easily recognised by its contrasting colour pattern and
         elongated dorsal fin.'''.replace( '\n', ' ' ),
      '''This species is native to the Indo-Pacific region, including coral reefs around the Philippines, Indonesia, and northern
         Australia. They inhabit shallow reef slopes and lagoons, preferring areas with plenty of coral structures for shelter and
         feeding.'''.replace( '\n', ' ' ),
      '''Pennant Coralfish are omnivorous, feeding on small invertebrates, plankton, and occasionally algae. They use their small,
         protrusible mouths to pick food from crevices in the coral. In aquariums, they are fed a mix of frozen or live
         invertebrates, supplemented with plant-based foods to mimic natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''These fish are often observed in pairs or small groups. They are diurnal and relatively peaceful, actively swimming through
         reef areas while maintaining territory around sheltering coral. Social interactions include coordinated swimming and
         occasional display behaviours during mating or courtship.'''.replace( '\n', ' ' ),
      '''The tall dorsal fin and contrasting colour pattern may help with species recognition and predator confusion. Their
         laterally compressed bodies allow agile movement through complex coral structures, and their small mouths are adapted for
         precision feeding on small prey items.'''.replace( '\n', ' ' ),
      '''Pennant Coralfish reproduce via external fertilisation, releasing eggs into the water column where they hatch into
         free-swimming larvae. Juveniles gradually settle onto reefs and develop adult colouration as they mature. In the wild, they
         typically live 5–8 years, while in aquariums, with optimal care, they may live longer.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Pied Imperial Pigeon',
      'Ducula Bicolor',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The pied imperial pigeons can be found in the main aviary in the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Pied Imperial Pigeon is a large, stocky pigeon with predominantly white plumage, contrasting with dark flight feathers
         on the wings and tail. It has a short, stout beak and a pale yellow or orange eye. Belonging to the pigeon and dove family
         (Columbidae), it is easily recognised by its striking white body and dark wing tips.'''.replace( '\n', ' ' ),
      '''Native to coastal forests, mangroves, and islands across Southeast Asia, northern Australia, and the Pacific islands, Pied
         Imperial Pigeons prefer areas with abundant fruiting trees. They are strong fliers, often moving between islands or coastal
         habitats in search of food.'''.replace( '\n', ' ' ),
      '''These pigeons are frugivorous, feeding primarily on fruits, berries, and figs. They forage in trees and occasionally
         descend to feed on fallen fruit. In zoos, their diet includes a variety of fruits and supplements that mimic their natural
         intake, ensuring proper nutrition.'''.replace( '\n', ' ' ),
      '''Pied Imperial Pigeons are social and often seen in flocks. They are strong, direct fliers and communicate with soft cooing
         calls. During feeding and breeding seasons, they may form larger congregations, and pairs often maintain close bonds.'''
         .replace( '\n', ' ' ),
      '''Their strong wings and lightweight bodies are adapted for long flights between islands and across open habitats.
         Frugivorous diets are supported by a digestive system capable of processing fibrous fruits efficiently. Their contrasting
         plumage aids in social signalling and species recognition during flight and display.'''.replace( '\n', ' ' ),
      '''These pigeons nest in trees, often on high branches or in mangroves, laying a single egg per breeding attempt. Both parents
         participate in incubation and feeding of the chick. Juveniles fledge after a few weeks. Lifespan in the wild is typically
         10–15 years, while captive individuals can live longer with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Pot-Bellied Seahorse',
      'Hippocampus Abdominalis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The pot-bellied seahorses can be found in a smaller tank in the Great Barrier Reef exhibit across from the main tank.''',
      None,                                                          # Seasonal viewing tips
      '''The Pot-bellied Seahorse is a small marine fish with a curved body, prehensile tail, and a distinctive swollen belly, which
         gives it its common name. Its body is covered in bony plates, and it can range in colour from pale yellow to deep brown,
         sometimes with spots or banding. Belonging to the seahorse family (Syngnathidae), it is recognised for its upright posture
         and horse-like head.'''.replace( '\n', ' ' ),
      '''Pot-bellied Seahorses are native to southern Australia and Tasmania, inhabiting seagrass beds, kelp forests, and sheltered
         coastal waters. They prefer areas with plenty of holdfasts, such as seagrass, coral, or man-made structures, to anchor
         their tails.'''.replace( '\n', ' ' ),
      '''These seahorses are carnivorous, feeding primarily on small crustaceans, plankton, and tiny fish larvae. They use their
         elongated snouts to suck in prey. In aquariums, they are offered live or frozen foods such as mysid shrimp, tailored to
         encourage natural hunting and feeding behaviour.'''.replace( '\n', ' ' ),
      '''Pot-bellied Seahorses are generally solitary but form monogamous pairs during the breeding season. They are slow-moving and
         rely on camouflage to avoid predators. Males and females perform elaborate courtship dances that strengthen pair bonds
         before mating.'''.replace( '\n', ' ' ),
      '''The prehensile tail allows seahorses to anchor to vegetation and resist currents, while their vertical posture helps them
         blend into seagrass or kelp. Camouflaged colouring and small size reduce predation risk. Their unique body shape allows
         them to feed efficiently on tiny planktonic organisms.'''.replace( '\n', ' ' ),
      '''Pot-bellied Seahorses exhibit male pregnancy. Females deposit eggs into the male’s brood pouch, where he fertilises and
         carries them until they hatch. Juveniles are fully formed and independent at birth. In the wild, they typically live 2–5
         years, while captive individuals can live longer with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red Claw Yabby',
      'Cherax Quadricarinatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red claw yabbies can be seen in a tank enclosure in the room in the Australasia Pavilion past the aviary and to the
         right.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Red Claw Yabby is a freshwater crayfish distinguished by its robust body, dark green to bluish-grey carapace, and
         bright red tips on the larger claws. Adults can reach up to 20 cm in length. This species belongs to the crayfish family
         (Parastacidae) and is easily recognised by its red claws and segmented, armored body.'''.replace( '\n', ' ' ),
      '''Native to northern Australia and parts of Papua New Guinea, Red Claw Yabbies inhabit rivers, billabongs, and freshwater
         lakes. They prefer environments with soft substrates and plenty of cover such as rocks, vegetation, or burrows to hide from
         predators.'''.replace( '\n', ' ' ),
      '''Red Claw Yabbies are omnivorous, feeding on algae, plant matter, detritus, small invertebrates, and carrion. In captivity,
         they are provided with a balanced diet of fresh vegetables, protein-rich feeds, and sinking pellets to encourage natural
         foraging and scavenging behaviours.'''.replace( '\n', ' ' ),
      '''These yabbies are primarily nocturnal and spend much of the day hidden in burrows or under cover. They are territorial,
         especially larger individuals, and may engage in displays or mild combat to defend space. They are solitary but can coexist
         in groups with sufficient shelter and hiding places.'''.replace( '\n', ' ' ),
      '''Strong claws allow Red Claw Yabbies to capture food, defend themselves, and dig burrows. Their exoskeleton provides
         protection, and the bright red claw tips may signal maturity or dominance to other yabbies. Burrowing behaviour helps them
         survive during dry periods or when predators are near.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in warmer months, with females carrying eggs under their tail until they hatch. Juveniles go
         through several moults before reaching adult size. In the wild, Red Claw Yabbies can live up to 5–6 years, while captive
         individuals may live longer under optimal conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red-Bellied Short-Necked Turtle',
      'Emydura Subglobosa',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red-bellied short-necked turtles can be found in the habitat just pas the aviary and on the left. They share the
         enclosure with the Asian tree monitor.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Red-bellied Short-necked Turtle is a medium-sized freshwater turtle with a smooth, oval carapace that ranges from olive
         to brown, and a distinctive red or orange plastron (belly). Its head is broad with a short neck, and the skin is generally
         greyish-green. This species belongs to the family Chelidae and is easily recognised by its vibrant belly and short,
         retractable neck.'''.replace( '\n', ' ' ),
      '''Native to northern Australia and southern New Guinea, these turtles inhabit slow-moving rivers, swamps, and freshwater
         lagoons with abundant aquatic vegetation. They prefer shallow water with soft substrates and access to basking areas.'''
         .replace( '\n', ' ' ),
      '''Red-bellied Short-necked Turtles are omnivorous, feeding on aquatic plants, algae, small fish, invertebrates, and carrion.
         In captivity, their diet includes leafy greens, vegetables, commercial turtle pellets, and protein supplements to ensure
         balanced nutrition and encourage natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''These turtles are mostly solitary but may share basking spots with others. They are active during the day, spending time
         swimming, feeding, and basking. When threatened, they retract their short necks partially and retreat into water.'''
         .replace( '\n', ' ' ),
      '''Their streamlined shell and webbed feet make them strong swimmers, while the short neck allows quick retraction for
         protection. Brightly coloured plastrons may help with species recognition during social interactions. They can tolerate a
         range of freshwater conditions, aiding survival in variable habitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs during warmer months, with females laying clutches of 10–20 eggs in sandy or soft soil near water.
         Hatchlings emerge fully independent and begin foraging immediately. Lifespan is typically 20–30 years in the wild, and
         turtles in captivity can live longer with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red-Tailed Black Cockatoo',
      'Calyptorhynchus Banksii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red-tailed black cockatoos live in the first enclosure you encounter when you enter the pavilion. They share their
         habitat with the short-beaked echidna.''',
      None,                                                          # Seasonal viewing tips
      '''The Red-tailed Black Cockatoo is a large, striking parrot with glossy black plumage and bright red panels on the tail
         feathers in males, while females have more subdued brownish-red tail markings and spotted plumage on the body. It has a
         strong, curved beak and a prominent crest that can be raised or lowered. This species belongs to the cockatoo family
         (Cacatuidae) and is instantly recognisable by its size and dramatic colouring.'''.replace( '\n', ' ' ),
      '''Red-tailed Black Cockatoos are native to Australia, inhabiting woodlands, forests, and savannah regions, often near water
         sources. They prefer areas with tall eucalyptus or other native trees that provide food and nesting hollows.'''
         .replace( '\n', ' ' ),
      '''These cockatoos feed primarily on seeds, nuts, fruits, and native vegetation. Their strong beaks allow them to crack open
         hard seeds and access otherwise protected food sources. In zoos, they are provided with a varied diet of seeds, fruits,
         nuts, and formulated pellets to reflect natural feeding behaviour.'''.replace( '\n', ' ' ),
      '''Red-tailed Black Cockatoos are social and often seen in pairs or small flocks. They are vocal, producing distinctive calls
         and whistles to communicate. Males may display to attract mates, raising their crest and fanning their tail feathers. They
         are diurnal and spend much of the day foraging or perching in trees.'''.replace( '\n', ' ' ),
      '''Strong, curved beaks allow them to access tough seeds and nuts, while zygodactyl feet (two toes forward, two back) help
         them grip branches and manipulate food. Their black plumage provides camouflage in dense forest canopies, and their social
         behaviour enhances survival by maintaining group vigilance against predators.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in spring and summer. Females nest in large tree hollows, laying 1–2 eggs per clutch. Both
         parents participate in feeding and caring for the chicks. Juveniles fledge after several weeks but may remain with parents
         for extended learning. In the wild, Red-tailed Black Cockatoos can live up to 50 years, while captive individuals often
         live longer with proper care.'''.replace( '\n', ' ' ),
      '''The Toronto zoo is home to a pair of female red-tailed black cockatoos.'''
   ),
   (
      'Short-Beaked Echidna',
      'Tachyglossus Aculeatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The short-beaked echidna shares a habitat with the red-tailed black cockatoos. This habitat is the first one you see after
         you enter the Australasia Pavilion. The short-beaked echidna is perhaps the most difficult animal to spot at the zoo. This
         is because the species is nocturnal, and rarely exits its burrow during the day. Your best chance of spotting the echidna
         is to visit the Australasia pavilion right at the end of the day, and looking around the bottom of its enclosure.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Short-beaked Echidna is a small, spiny monotreme with a distinctive coat of coarse hair and sharp spines covering its
         back. It has a long, slender snout used for probing, a sticky tongue for capturing prey, and strong, clawed limbs for
         digging. Belonging to the monotreme family (Tachyglossidae), it is one of only a few egg-laying mammals in the world.'''
         .replace( '\n', ' ' ),
      '''Native to Australia and Tasmania, Short-beaked Echidnas inhabit a variety of environments, including forests, grasslands,
         and deserts. They prefer areas with loose soil for burrowing and ample invertebrate prey.'''.replace( '\n', ' ' ),
      '''Echidnas are insectivorous, feeding mainly on ants and termites. They use their strong claws to dig into nests and their
         long, sticky tongue to capture prey. In captivity, their diet includes specially formulated insect-based foods and live
         invertebrates to simulate natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Short-beaked Echidnas are solitary and primarily nocturnal or crepuscular. They spend much of the day resting in burrows or
         under cover. When threatened, they curl into a ball, presenting their spines to predators. They communicate minimally,
         using grunts or snuffles during social encounters or mating.'''.replace( '\n', ' ' ),
      '''The spines provide protection from predators, while strong limbs and claws allow efficient digging. The long, sensitive
         snout helps detect prey underground. Their low metabolic rate and ability to enter torpor allow them to survive in a wide
         range of temperatures and food availability.'''.replace( '\n', ' ' ),
      '''Echidnas are egg-laying mammals. Females lay a single leathery egg into a pouch where it incubates for about 10 days. The
         young, called a puggle, remains in the pouch for several weeks before gradually exploring the environment. Short-beaked
         Echidnas can live up to 14–16 years in the wild, with much longer lifespans in captivity under good care.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo has one short-beaked echidna, a female named Annie, who is about 45 years old!'''.replace( '\n', ' ' )
   ),
   (
      'Solomon Island Leaf Frog',
      'Ceratobatrachus Guentheri',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Solomon Island leaf frogs live in one of the first enclosures you see once you enter the Great Barrier Reef exhibit in
         the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Solomon Island Leaf Frog is a small, terrestrial frog with a flattened, leaf-like body and cryptic brown, green, or
         mottled colouration that provides camouflage among forest leaf litter. It has large eyes and slender limbs adapted for
         jumping. Belonging to the family Ceratobatrachidae, it is recognised for its remarkable camouflage and distinctive
         leaf-like appearance.'''.replace( '\n', ' ' ),
      '''Native to the Solomon Islands, this frog inhabits tropical lowland forests and dense leaf litter. It prefers humid, shaded
         environments where moisture and cover are abundant, often staying close to decomposing vegetation.'''.replace( '\n', ' ' ),
      '''Solomon Island Leaf Frogs are insectivorous, feeding primarily on ants, termites, small insects, and other invertebrates.
         In captivity, they are offered a diet of small insects such as crickets and fruit flies, replicating natural foraging
         behaviour.'''.replace( '\n', ' ' ),
      '''These frogs are largely solitary and nocturnal, remaining hidden during the day and emerging at night to forage. They rely
         on camouflage for protection and remain motionless when threatened. Males communicate with soft calls during the breeding
         season to attract mates.'''.replace( '\n', ' ' ),
      '''Their flattened, leaf-like body and cryptic colouration provide excellent camouflage in leaf litter. Long, slender limbs
         allow quick, efficient hopping, and their sticky fingers aid in navigating the forest floor. Being nocturnal helps reduce
         predation risk and avoid heat stress.'''.replace( '\n', ' ' ),
      '''Solomon Island Leaf Frogs reproduce via direct development, meaning eggs hatch directly into miniature froglets rather than
         free-swimming tadpoles. Females lay eggs in moist leaf litter, which are guarded by the parent until hatching. Lifespan is
         typically 5–7 years in captivity with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Solomon Island Monkey-Tailed Skink',
      'Corucia Zebrata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Solomon Island monkey-tailed skink lives in the first habitat you see once you enter the Great Barrier Reef exhibit.''',
      None,                                                          # Seasonal viewing tips
      '''The Solomon Island Monkey-tailed Skink is a large, arboreal lizard with a long, prehensile tail, robust body, and a
         darkgreen to olive-brown colouration. Adults can reach up to 60–70 cm in length. It belongs to the skink family (Scincidae)
         and is easily recognised by its elongated, grasping tail and strong limbs adapted for climbing.'''.replace( '\n', ' ' ),
      '''Native to the Solomon Islands, this skink inhabits tropical forests, living predominantly in trees and dense vegetation. It
         prefers humid, shaded environments with plenty of branches for climbing and basking.'''.replace( '\n', ' ' ),
      '''The Solomon Island Monkey-tailed Skink is primarily herbivorous, feeding on leaves, fruits, flowers, and shoots. In
         captivity,their diet includes a variety of leafy greens, vegetables, and fruits, providing essential nutrients and
         encouraging natural foraging behaviours'''.replace( '\n', ' ' ),
      '''These skinks are generally social, often seen in small family groups. They are mostly diurnal, spending daylight hours
         basking or moving slowly among branches. Their prehensile tails allow them to maintain balance while climbing and
         navigating the canopy. When threatened, they may use tail-whipping as a defensive behaviour.'''.replace( '\n', ' ' ),
      '''The prehensile tail acts like a fifth limb for grasping branches, while sharp claws aid in climbing. Their cryptic
         greenish-brown colouring provides camouflage among leaves. Slow, deliberate movements help them avoid detection by
         predators and conserve energy.'''.replace( '\n', ' ' ),
      '''Solomon Island Monkey-tailed Skinks give birth to live young (viviparous reproduction), usually 2–8 per litter. Juveniles
         are fully independent at birth. Lifespan in the wild can reach 15–20 years, with captive individuals sometimes living
         longer under optimal care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Lasiorhinus Latifrons',
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The wombats can be viewed both inside and outside. To see their indoor habitat, head inside the Australasia Pavilion, and
         go to the left once you exist the aviary area. To spot them in their outdoor habitat, you may walk through the pavilion,
         and their enclosure will be on the left when you exit, or take a walk around the outside of the pavilion, towards the exit.
         The wombats are most active closer to dusk or dawn. They spend much of the daytime sleeping, and during these lazy hours
         they are likely to be viewable in their indoor habitat.'''.replace( '\n', ' ' ),
      '''Wombats are warm weather animals, and tend to only venture outside in the warmer months of the year. They are also
         generally less active in the winter, spending more time sleeping in their burrows. Even in the warmer months, the wombats
         are often found in their indoor habitat in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      '''The Southern Hairy-nosed Wombat is a robust, burrowing marsupial with a compact, muscular body covered in coarse grey-brown
         fur. It has a distinctive flattened nose with fine hair, small ears, and powerful forelimbs with sharp claws for digging.
         Adults typically weigh 25–35 kg and measure around 1 metre in length. This species belongs to the wombat family
         (Vombatidae) and is easily recognised by its stocky build and characteristic nose shape.'''.replace( '\n', ' ' ),
      '''Native to semi-arid and arid regions of southern Australia, Southern Hairy-nosed Wombats inhabit grasslands, scrublands,
         and sandy plains. They rely on soft soils for extensive burrow systems, which provide shelter from heat, cold, and
         predators. These wombats are highly adapted to dry environments and can survive in areas with sparse vegetation.'''
         .replace( '\n', ' ' ),
      '''Southern Hairy-nosed Wombats are herbivorous, feeding primarily on native grasses, roots, and tubers. They have strong,
         ever-growing incisors and molars suited for grinding tough, fibrous plants. At the zoo, their diet includes fresh grasses,
         hay, leafy greens, and fibre-rich vegetables, supplemented to mimic their natural nutrient intake. They are mostly
         nocturnal feeders, emerging at night to graze.'''.replace( '\n', ' ' ),
      '''These wombats are generally solitary, defending individual burrow systems but may tolerate neighbours at boundaries. They
         are nocturnal, spending the day hidden in burrows to avoid extreme temperatures. Burrow systems are complex, with multiple
         entrances and chambers, and are central to their territorial behaviour. They mark territory with scent and dung placed at
         the burrow entrances. Though generally slow-moving, wombats are capable of surprising bursts of speed when threatened.'''
         .replace( '\n', ' ' ),
      '''Southern Hairy-nosed Wombats are highly adapted to survive in arid and semi-arid environments. Their powerful limbs and
         sharp claws allow them to dig extensive burrow systems, which provide protection from extreme temperatures and predators.
         They have highly efficient kidneys and extract most of their water from the vegetation they eat, enabling them to thrive
         where free water is scarce. Their continuously growing incisors are perfectly suited for grinding tough, fibrous grasses
         and roots. Being primarily nocturnal helps them avoid daytime heat and predation, while their stocky, low-slung bodies
         conserve energy and aid in digging and moving through burrows.'''.replace( '\n', ' ' ),
      '''Breeding occurs from late spring to summer, with females producing a single young per year. The joey develops in the pouch
         for about 6–7 months before emerging and continues to nurse while gradually exploring the burrow. Sexual maturity is
         reached at around 2–3 years. Lifespan in the wild is typically 10–15 years, while wombats in captivity may live up to 20
         years or more.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has a breeding pair of wombats, male Arthur, and female Matilba.'''.replace( '\n', ' ' )
   ),
   (
      'Stimson\'s Python',
      'Antaresia Stimsoni',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Stimson's python is found in a habitat in the hallway you access once you exit the aviary area and turn left.''',
      None,                                                          # Seasonal viewing tips
      '''Stimson’s Python is a small to medium-sized, non-venomous snake, typically reaching 1–2 metres in length. It has a slender,
         cylindrical body with smooth scales, and its colouration ranges from reddish-brown to tan with pale markings along the
         back. Belonging to the python family (Pythonidae), it is recognised for its gentle temperament and manageable size, making
         it popular in captivity.'''.replace( '\n', ' ' ),
      '''Native to northern and central Australia, Stimson’s Pythons inhabit savannahs, shrublands, and rocky areas. They prefer dry
         to semi-arid environments and often shelter under rocks, in hollow logs, or in burrows made by other animals.'''
         .replace( '\n', ' ' ),
      '''These pythons are constrictors, feeding primarily on small mammals, birds, and reptiles. They strike quickly, coil around
         their prey, and constrict until it suffocates. In zoos, they are offered appropriately sized rodents or birds, with feeding
         routines designed to replicate natural hunting behaviour.'''.replace( '\n', ' ' ),
      '''Stimson’s Pythons are generally solitary and nocturnal, active mainly at night when they hunt. They are non-aggressive
         toward humans but will defend themselves if threatened. In captivity, they are known for their calm, docile nature and
         often tolerate careful handling.'''.replace( '\n', ' ' ),
      '''Stimson’s Pythons are well adapted to life in arid and semi-arid regions. Their slender, muscular bodies allow them to move
         efficiently through narrow spaces and under cover. Constriction is a highly effective method for subduing prey, and their
         cryptic colouring provides camouflage against the rocky and sandy landscapes they inhabit. Nocturnal habits reduce heat
         stress and exposure to predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the cooler months, with females laying 6–12 eggs per clutch. Eggs are incubated in warm, hidden
         locations, and hatchlings are independent from birth. In the wild, Stimson’s Pythons typically live 10–15 years, while
         captive individuals can exceed this with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Tawny Frogmouth',
      'Podargus Strigoides',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tawny frogmouth is found in the main aviary in the Australasia Pavilion. The tawny frogmouth is a difficult species to
         spot as it usually hangs out towards the back of the habitat, often against the wall towards the rest of the pavilion, or
         around the pond. Check high up in all the trees to spot him.''',
      None,                                                          # Seasonal viewing tips
      '''The Tawny Frogmouth is a medium-sized nocturnal bird with mottled grey, brown, and black plumage that closely resembles
         tree bark. It has a broad, flattened head, large eyes adapted for low light, and a wide, frog-like beak surrounded by stiff
         bristles. Although often mistaken for an owl, it belongs to a separate group of birds and differs in behaviour and anatomy.'''
         .replace( '\n', ' ' ),
      '''Tawny Frogmouths are widespread across Australia, Tasmania, and parts of southern New Guinea. They inhabit a wide range of
         environments, including woodlands, forests, savannas, and urban parks and gardens. They rely on trees for roosting and
         nesting, particularly those with horizontal branches.'''.replace( '\n', ' ' ),
      '''These birds are primarily insectivorous, feeding on insects such as beetles, moths, spiders, and worms. They also
         occasionally take small vertebrates, including lizards and mice. Rather than hunting in flight, Tawny Frogmouths typically
         perch quietly and swoop down to capture prey from the ground or tree trunks.'''.replace( '\n', ' ' ),
      '''Tawny Frogmouths are nocturnal and usually seen alone or in pairs. During the day, they remain motionless on branches,
         relying on camouflage to avoid detection. When threatened, they adopt a distinctive posture by stretching their necks
         upward and closing their eyes to resemble a broken branch. They are territorial and communicate using a range of low,
         booming calls at night.'''.replace( '\n', ' ' ),
      '''The Tawny Frogmouth’s bark-like plumage provides exceptional camouflage, allowing it to blend seamlessly into tree branches
         during daylight hours. Its wide mouth and surrounding bristles help funnel insects into the beak, while large eyes enhance
         night vision. Remaining still for long periods conserves energy and reduces the risk of predation.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs from spring to early summer. Pairs build a flimsy nest of sticks on a horizontal branch, where
         the female lays 1–3 eggs. Both parents share incubation and chick-rearing duties. Chicks fledge after about a month. Tawny
         Frogmouths can live 10–14 years in the wild, with longer much lifespans possible in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has one male tawny frogmouth named Erkle.'''
   ),
   (
      'Thorny Devil Stick Insect',
      'Eurycantha Calcarata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The thorny devil stick insect can be found in the room past the aviary and to the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Thorny Devil Stick Insect is a large, leaf-mimicking insect with an irregular, spiny body covered in lobes and
         thorn-like projections. Colouration varies from brown to grey and green, closely resembling dried leaves or bark. Females
         are significantly larger and heavier than males, while males are slimmer and capable of flight. This species belongs to the
         stick insect family (Phasmatidae) and is renowned for its exceptional camouflage.'''.replace( '\n', ' ' ),
      '''Native to eastern Australia, Thorny Devil Stick Insects inhabit forests and woodlands where leaf litter and dense
         vegetation provide cover. They are most commonly found among eucalyptus trees, where their appearance blends seamlessly
         with surrounding foliage.'''.replace( '\n', ' ' ),
      '''These insects are herbivorous, feeding primarily on eucalyptus leaves, as well as other suitable native plants. In zoos,
         they are provided with fresh leafy branches, which also serve as climbing and resting structures. Feeding occurs mostly at
         night.'''.replace( '\n', ' ' ),
      '''Thorny Devil Stick Insects are solitary and nocturnal. During the day, they remain motionless to avoid detection, relying
         entirely on camouflage. When disturbed, they may sway gently to imitate leaves moving in the breeze or curl their bodies
         defensively. Males are more active and mobile, particularly during the breeding season.'''.replace( '\n', ' ' ),
      '''This species’ extreme leaf-like shape, spines, and uneven texture provide outstanding camouflage among foliage and leaf
         litter. Their slow movements and tendency to remain still reduce the chance of being noticed by predators. Some individuals
         can also release a mild defensive scent when threatened, adding another layer of protection'''.replace( '\n', ' ' ),
      '''Females lay eggs by dropping them to the forest floor, where they resemble seeds. Eggs hatch after several months,
         producing tiny nymphs that closely resemble ants, helping deter predators. As they grow, they shed their exoskeleton
         multiple times before reaching adulthood. Lifespan is typically 6–12 months, depending on environmental conditions.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Threadfin Butterflyfish',
      'Chaetodon Auriga',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The threadfin butterflyfish can be found in the main tank of the Great Barrier Reef exhibit in the Australasia Pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Threadfin Butterflyfish is a striking reef fish with a bright white body marked by diagonal yellow bands and a
         distinctive black eyespot near the rear of the dorsal fin. A long, trailing filament extends from the dorsal fin in adults,
         giving the species its name. It has a pointed snout adapted for picking food from crevices. Adults typically reach 20–23 cm
         in length.'''.replace( '\n', ' ' ),
      '''This species is widely distributed across the Indo-Pacific region, including coral reefs, lagoons, and rocky coastal areas.
         It is commonly found at shallow to moderate depths, where coral cover and reef structure provide feeding opportunities and
         shelter.'''.replace( '\n', ' ' ),
      '''Threadfin Butterflyfish are omnivorous, feeding on coral polyps, small invertebrates, algae, and plankton. Their narrow
         snouts allow them to reach food hidden within reef crevices. In zoos and aquariums, they are offered a varied diet of
         prepared marine foods, small invertebrates, and algae-based supplements.'''.replace( '\n', ' ' ),
      '''These fish are usually seen alone or in pairs and are often territorial. The false eyespot near the tail may confuse
         predators by drawing attention away from the head. They are active swimmers during the day and frequently patrol reef
         surfaces in search of food.'''.replace( '\n', ' ' ),
      '''The Threadfin Butterflyfish’s elongated snout is perfectly adapted for extracting food from narrow spaces within coral
         reefs. Its bold colour patterns help with species recognition, while the false eyespot may misdirect predators during
         attacks. The dorsal filament may play a role in communication or display.'''.replace( '\n', ' ' ),
      '''Spawning occurs in open water, where eggs are released and fertilized externally. The eggs develop into planktonic larvae
         before settling onto reefs as juveniles. In the wild, Threadfin Butterflyfish can live 5–7 years, with similar lifespans
         observed in captivity under optimal conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Victoria Crowned Pigeon',
      'Goura Victoria',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Victoria crowned pigeons can be found foraging around the ground floor of the main aviary in the pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Victoria Crowned Pigeon is the largest species of pigeon in the world, notable for its striking blue-grey plumage and
         elaborate fan-shaped crest of lacy feathers tipped with white. It has deep red eyes, a maroon chest, and strong reddish
         legs. Adults can reach over 70 cm in length and weigh up to 2.5 kg. Despite its size, it retains the classic pigeon body
         shape, making it both impressive and distinctive.'''.replace( '\n', ' ' ),
      '''This species is native to the lowland rainforests and swamp forests of northern New Guinea and surrounding islands. It
         spends much of its time on the forest floor but relies on trees for roosting and nesting. Dense vegetation and undisturbed
         forest habitats are essential for its survival.'''.replace( '\n', ' ' ),
      '''Victoria Crowned Pigeons are primarily frugivorous, feeding on fallen fruits, seeds, and berries found on the forest floor.
         They also consume insects and small invertebrates on occasion. In zoos, they are offered a carefully balanced diet of
         fruits, grains, seeds, and formulated feeds that support their nutritional needs.'''.replace( '\n', ' ' ),
      '''These pigeons are generally calm and social, often seen in pairs or small groups. They are diurnal and spend much of the
         day walking slowly along the ground in search of food. When alarmed, they can take flight with loud wing claps, although
         they prefer to avoid flying when possible. They communicate using deep, resonant calls that can carry through dense forest.'''
         .replace( '\n', ' ' ),
      '''The Victoria Crowned Pigeon’s large size and strong legs allow it to forage efficiently on the forest floor, while its
         powerful wings enable short flights to escape danger or reach roosting sites. Its ornate crest may play a role in display
         and communication, especially during courtship. The bird’s muted but elegant colouring provides some camouflage in shaded
         forest environments.'''.replace( '\n', ' ' ),
      '''Breeding pairs build simple platform nests in trees, where the female lays a single egg. Both parents share incubation and
         chick-rearing duties. The chick is fed crop milk and fledges after several weeks. Victoria Crowned Pigeons can live 15–25
         years, with individuals in captivity often reaching the upper end of this range.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'White\'s Tree Frog',
      'Litoria Caerulea',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The White's tree frog is found in a habitat down the hallway past and to the left of the aviary.''',
      None,                                                          # Seasonal viewing tips
      '''White’s Tree Frog is a large, robust tree frog with smooth, waxy skin that ranges from bright green to bluish-green, often
         with pale white or cream markings along the sides. It has large toe pads adapted for climbing and prominent golden eyes
         with horizontal pupils. Adults typically grow 7–11 cm in length. This species is also commonly known as the Australian
         Green Tree Frog.'''.replace( '\n', ' ' ),
      '''Native to northern and eastern Australia and parts of New Guinea, White’s Tree Frogs inhabit a wide variety of
         environments, including forests, wetlands, grasslands, and urban areas. They are often found near water sources but are
         highly adaptable and can tolerate drier conditions better than many other amphibians.'''.replace( '\n', ' ' ),
      '''These frogs are opportunistic carnivores, feeding on insects such as crickets, moths, beetles, and cockroaches, as well as
         occasional small vertebrates. At the zoo, they are fed a varied diet of appropriately sized insects, ensuring proper
         nutrition and enrichment through active feeding behaviours.'''.replace( '\n', ' ' ),
      '''White’s Tree Frogs are primarily nocturnal and are often seen resting during the day in sheltered locations such as tree
         hollows or behind foliage. They are relatively tolerant of one another and may be observed sharing resting sites. During
         the breeding season, males produce loud, deep calls near water to attract females.'''.replace( '\n', ' ' ),
      '''This species has several adaptations that allow it to thrive in a wide range of conditions. Its large toe pads provide
         excellent grip for climbing smooth surfaces, while its waxy skin helps reduce moisture loss, allowing it to survive in
         drier habitats. White’s Tree Frogs can also store water in their bodies and adjust their activity patterns to avoid extreme
         heat.'''.replace( '\n', ' ' ),
      '''Breeding occurs during warmer months, often following heavy rainfall. Females lay large clusters of eggs in water, which
         hatch into tadpoles within days. Tadpoles develop into froglets over several weeks. White’s Tree Frogs can live 15–20 years
         in captivity, making them one of the longer-lived frog species commonly found in zoos.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Australasia Outdoor
   (
      'Western Grey Kangaroo',
      'Macropus Fuliginosus',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The Western kangaroo enclosure can be found by heading just past the Australasia Pavilion, sticking to the right. The
         kangaroos at the Toronto Zoo have a rather large habitat, meaning that sometimes the animals will be fairly far from the
         guest viewing. The kangaroos are the most active, and the most likely to be closer to the guest viewing early in the
         morning. In the warmer months (approximately Jun-Oct) any guest of the zoo may enter the kangaroo habitat via the kangaroo
         walkthrough from 11:00 am to 3:00 pm, to get an up-close view of these remarkable creatures.'''.replace( '\n', ' ' ),
      '''The Western grey kangaroo is a fairly hardy species. As long as the temperature is above 0°C and there isn't much snow on
         the ground, they should be viewable outside.'''.replace( '\n', ' ' ),
      '''The Western Grey Kangaroo is a large marsupial with thick grey-brown fur, a pale underside, and a robust, muscular build.
         It has powerful hind legs, large feet adapted for hopping, and a long, muscular tail used for balance and support. Males
         are significantly larger than females and may show darker facial markings and heavier musculature. Adults can reach over
         1.3 metres in body length, with tails adding nearly another metre.'''.replace( '\n', ' ' ),
      '''This species is native to southern and western Australia, where it inhabits open woodlands, grasslands, scrublands, and
         forest edges. Western Grey Kangaroos prefer areas with a mix of open grazing space and nearby cover for shade and shelter.
         They are highly adaptable and can tolerate a wide range of climates, including cooler regions.'''.replace( '\n', ' ' ),
      '''Western Grey Kangaroos are herbivorous grazers, feeding primarily on grasses and other low-growing vegetation. They are
         adapted to digest tough, fibrous plant material through a complex, multi-chambered stomach similar to that of ruminants.
         At the zoo, they are fed a diet of grasses, hay, and specially formulated herbivore pellets, supplemented with fresh
         browse.'''.replace( '\n', ' ' ),
      '''These kangaroos are social animals, commonly forming loose groups known as mobs. Group size can vary depending on food
         availability and environmental conditions. They are most active during early morning and late afternoon, resting in shaded
         areas during the heat of the day. Social interactions include grooming, vocalizations, and, among males, ritualized boxing
         displays to establish dominance.'''.replace( '\n', ' ' ),
      '''Western Grey Kangaroos possess a suite of adaptations for efficient movement and survival in open landscapes. Their 
         powerful hind legs and elastic tendons allow them to travel long distances while conserving energy through hopping. The
         thick tail acts as a counterbalance and a powerful support limb when moving slowly or standing upright. Their digestive
         system enables them to extract nutrients from low-quality forage, and their ability to regulate activity patterns helps
         them cope with heat and limited water availability.'''.replace( '\n', ' ' ),
      '''Breeding can occur year-round, with females capable of delayed implantation, allowing them to pause embryonic development
         until conditions are favourable. After a short gestation of about one month, a tiny, underdeveloped joey crawls into the
         mother’s pouch, where it continues to develop for several months. Joeys gradually begin exploring outside the pouch before
         weaning. Western Grey Kangaroos can live 15–20 years, particularly in protected environments such as zoos.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a group of Western grey kangaroos, called a mob, with several active breeding members.'''
         .replace( '\n', ' ' )
   ),

   # Eurasia Wilds
   (
      'Amur Tiger',
      'Panthera Tigris Altaica',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Amur tiger habitat is located near the entrance to the Eurasia Wilds exhibit, towards the right near the kangaroo
         habitat. The Amur tigers at the zoo have several spaces which they can be in during any given day. From closest the
         kangaroos to furthur away, there is the main habitat with the pool and den, two indoor spaces, and the secondary outdoor
         habitat. For a year-round, comfortable experience, the tigers at the zoo always have access to indoor and outdoor spaces.
         Specifically when it is warmer, the tiger may be in one of her indoor habitats, past the main habitat and on the left. Amur
         tigers are most active early and late in the day.'''.replace( '\n', ' ' ),
      '''While the Amur tigers at the zoo can be viewed year-round, these cats are actually most comfortable when it is cooler, so
         your best chance of seeing them active is in the winter.'''.replace( '\n', ' ' ),
      '''The Amur tiger, also known as the Siberian tiger, is the largest living cat species. It has a thick, pale orange coat with
         widely spaced black stripes and a white underside, adaptations that help it blend into snowy forest environments. Compared
         to other tiger subspecies, it has longer fur, a thicker layer of body fat, and a broader head. Adult males can exceed 300
         kg, making them among the most powerful terrestrial predators on Earth.''' .replace( '\n', ' ' ),
      '''Amur tigers are native to the temperate forests of the Russian Far East, with small populations historically extending into
         northeastern China and the Korean Peninsula. They inhabit boreal forests, mixed woodlands, and mountainous regions, often
         in areas with harsh winters, deep snow, and rugged terrain. Large, undisturbed territories are essential for their
         survival.'''.replace( '\n', ' ' ),
      '''These tigers are apex predators that primarily hunt large ungulates such as deer and wild boar. They rely on stealth,
         strength, and ambush tactics rather than long chases. At the zoo, Amur tigers are fed a carefully managed diet of raw meat,
         bones, and occasional whole prey items, designed to meet nutritional needs while encouraging natural feeding behaviours.'''
         .replace( '\n', ' ' ),
      '''Amur tigers are solitary and highly territorial. Each individual maintains a vast home range, marked with scent markings
         and  marks on trees. They are mostly crepuscular, being most active at dawn and dusk. Despite their solitary nature, they
         communicate through vocalizations, scent marking, and visual signals.'''.replace( '\n', ' ' ),
      '''Amur tigers are exceptionally well adapted to cold climates. Their thick fur and dense fat layer provide insulation against
         extreme winter temperatures, while their large paws act like snowshoes, distributing weight and allowing easier movement
         across snow. Their striped coat offers camouflage in forested environments, breaking up their outline among trees and
         shadows. Powerful forelimbs and retractable claws enable them to subdue large prey efficiently.'''.replace( '\n', ' ' ),
      '''Breeding can occur year-round. After a gestation period of about 3.5 months, females give birth to litters of 2–4 cubs.
         Cubs remain with their mother for up to two years, learning essential hunting and survival skills. In the wild, Amur tigers
         typically live 10–15 years, while individuals in captivity may live 20 years or more with proper care.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female Amur tiger, Mazy. Mazy is in her golden years, and will spend much of her time
         resting, but you can still see her being active, specifically in the cooler months and earlier in the day, or whenever she
         is being given enrichment. Mazy is past her breeding days, and will remain alone, as she likes it, for the rest of her days
         at the zoo.'''.replace( '\n', ' ' )
   ),
   (
      'Asian Wild Horse',
      'Equus Ferus Przewalskii',
      -25,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Asian wild horses can be spotted at two spots in the Eurasia Wilds region of the zoo. A pair of the zoo's older horses
         can be spotted in a habitat across from the West Caucasian turs across the river. The rest of the herd can be spotted
         up-close in the Eurasia Wilds drive-thru exhibit aboard the zoomobile. To go through the drive-through you must hop on
         zoomobile before the Eurasia stop and stay on after the Tundra Trek stop.'''.replace( '\n', ' ' ),
      '''Asian wild horses are suited to handle the extreme cold, and can be seen outside year-round.'''.replace( '\n', ' ' ),
      '''The Asian Wild Horse, also known as Przewalski’s horse, is a stocky, muscular horse with a large head, short neck, and
         upright, bristly mane that lacks a forelock. Its coat is typically sandy brown with a pale belly and darker legs, often
         marked with faint striping. Unlike domestic horses, it has a heavier build, shorter legs, and a more robust skull,
         reflecting its wild ancestry.'''.replace( '\n', ' ' ),
      '''Historically, Asian Wild Horses ranged across the steppes and semi-deserts of Central Asia. By the mid-20th century, they
         were extinct in the wild, surviving only in zoos. Thanks to international conservation efforts, they have been reintroduced
         to protected areas in Mongolia and parts of China. They inhabit open grasslands, desert steppe, and arid plains with
         extreme seasonal temperatures.'''.replace( '\n', ' ' ),
      '''Asian Wild Horses are grazing herbivores, feeding primarily on grasses, sedges, and other hardy steppe vegetation. They are
         adapted to forage on coarse, low-nutrient plants and can dig through snow to reach buried grasses in winter. At the zoo,
         they are fed hay, grasses, and specialized equine diets that reflect their natural feeding behaviour.'''.replace( '\n', ' ' ),
      '''These horses live in small social groups typically consisting of a dominant stallion, several mares, and their offspring.
         Bachelor males form separate groups or live alone. Social structure is maintained through body language, vocalizations, and
         occasional displays of dominance. They are diurnal and spend much of their day grazing, resting, and moving between feeding
         areas.'''.replace( '\n', ' ' ),
      '''Asian Wild Horses are well adapted to harsh, continental climates. Their thick winter coats provide insulation against
         extreme cold, while seasonal shedding helps them cope with summer heat. Strong hooves and sturdy legs allow them to travel
         long distances across rocky and uneven terrain. Their efficient digestive system enables them to extract nutrients from
         tough, sparse vegetation.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in late spring or early summer. After a gestation period of about 11–12 months, a single foal is
         born and can stand and walk shortly after birth. Foals remain with their mothers within the herd and mature over several
         years. Asian Wild Horses can live 20–25 years, with similar lifespans observed in managed care.'''.replace( '\n', ' ' ),
      None,                                                          # Animals at the zoo
   ),
   (
      'Bactrian Camel',
      'Camelus Bactrianus',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Bactrian camels can be spotted in two habitats in the Eurasia Wilds section of the zoo. Both habitats can be spotted by
         taking the Eurasia loop. You will find them in between the snow leopards and the red pandas.'''.replace( '\n', ' ' ),
      '''Bactrian camels are adapted to thrive in a wide range of habitats, and can be seen being active in their habitats all
         year-round.'''.replace( '\n', ' ' ),
      '''The Bactrian camel is a large camel species distinguished by its two prominent humps. It has long legs, a broad body, and a
         thick, shaggy coat that becomes especially dense in winter and is shed seasonally. Colouration ranges from sandy beige to
         dark brown. Compared to the one-humped dromedary camel, Bactrian camels are heavier, stockier, and better adapted to cold
         climates.'''.replace( '\n', ' ' ),
      '''Bactrian camels are native to the cold deserts and steppes of Central Asia, including parts of Mongolia and northwestern
         China. They inhabit arid regions with extreme temperature fluctuations, from scorching summers to bitterly cold winters.
         Wild Bactrian camels are critically endangered, while domesticated populations are widespread.'''.replace( '\n', ' ' ),
      '''These camels are hardy herbivores capable of feeding on coarse, thorny, and salty vegetation that few other animals can
         tolerate. Their diet includes grasses, shrubs, and desert plants. At the zoo, they are fed hay, browse, and specially
         formulated herbivore diets that meet their nutritional needs while encouraging natural foraging behaviour.'''
         .replace( '\n', ' ' ),
      '''Bactrian camels are generally calm and social, often living in small groups. In the wild, they may form loose herds,
         especially around feeding and watering areas. They are diurnal and spend much of their time grazing, resting, and
         ruminating. During the breeding season, males may become more territorial and assertive.'''.replace( '\n', ' ' ),
      '''Bactrian camels are exceptionally adapted to extreme environments. Their humps store fat, not water, providing energy
         during times of food scarcity. Long eyelashes, closable nostrils, and thick lips protect them from blowing sand and dust.
         Their thick winter coat insulates them against severe cold, while wide, padded feet help prevent sinking into sand or snow.'''
         .replace( '\n', ' ' ),
      '''Breeding typically occurs in winter or early spring. After a gestation period of about 13 months, a single calf is born and
         is able to stand within hours. Calves remain with their mothers for extended periods and mature slowly. Bactrian camels can
         live 30–40 years, particularly in managed care.'''.replace( '\n', ' ' ),
      '''Female camel, Suria, recently gave birth to a calf, fathered by male camel, Zip. The mother and calf are currently spending
         time with another female camel, Jozy, and they may be viewable periodically throughout the day.'''.replace( '\n', ' ' ),
   ),
   (
      'Domestic Yak',
      'Bos Grunniens',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The domestic yak can only be seen aboard the zoomobile, in the Eurasia drive-thru section. To go through the drive-through
         you must hop on zoomobile before the Eurasia stop and stay on after the Tundra Trek stop.'''.replace( '\n', ' ' ),
      '''Yaks are very well suited to the extreme cold, and can be seen outside year-round in the drive-thru.''',
      '''The Domestic Yak is a large, long-haired bovine with a heavy build, sturdy legs, and broad hooves adapted to rough,
         mountainous terrain. It has a dense coat of long, shaggy hair that provides insulation against extreme cold. Colouration
         ranges from black or brown to lighter shades, with some individuals displaying white markings. Both males and females have
         horns, though males typically have thicker, more curved ones.'''.replace( '\n', ' ' ),
      '''Domestic Yaks are native to the high-altitude regions of the Himalayas, Tibetan Plateau, and Central Asia. They inhabit
         cold, mountainous grasslands and alpine meadows, thriving at elevations above 3,000 metres. Domesticated yaks are found
         throughout these regions, providing transport, milk, meat, and fibre for local communities.'''.replace( '\n', ' ' ),
      '''Yaks are herbivorous grazers, feeding on grasses, herbs, and shrubs. Their robust digestive system allows them to extract
         nutrients from coarse, fibrous vegetation that grows at high altitudes. In captivity, they are provided with hay, grasses,
         and supplemental feeds that mimic their natural diet and maintain optimal health.'''.replace( '\n', ' ' ),
      '''Domestic Yaks are social animals, often forming small herds for grazing and protection. They are generally calm but may
         become assertive during mating season. Herds provide safety from predators and facilitate communal feeding, resting, and
         thermoregulation in cold climates.'''.replace( '\n', ' ' ),
      '''Yaks are exceptionally adapted to high-altitude life. Their thick, insulating coats and long underfur protect against
         sub-zero temperatures, while large lungs and a strong cardiovascular system allow efficient oxygen use in low-oxygen
         environments. Wide hooves prevent sinking in snow or soft soil, and their rugged teeth and digestive efficiency allow them
         to consume coarse vegetation that other grazers cannot.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs during the summer months. After a gestation period of approximately 9 months, females give birth
         to a single calf. Calves are able to stand and walk within hours, following the herd for protection. Domestic Yaks can live
         15–20 years, with proper care extending their lifespan in managed environments.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Highland Cattle',
      'Bos Taurus',
      -25,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The highland cattle can be seen by taking the Eurasia Wilds loop, and taking the offshoot path away from the red pandas.''',
      '''The highland cattle can be seen outside all year.''',
      '''Highland Cattle are a robust, long-haired breed of domestic bovine, easily recognised by their shaggy coat and long, curved
         horns. Their dense hair, ranging from ginger to black, grey, or dun, protects them against harsh weather. They have a broad
         body, strong legs, and a calm, hardy appearance, adapted for rugged terrain.'''.replace( '\n', ' ' ),
      '''Originally from the Scottish Highlands, Highland Cattle are well suited to cold, wet, and windy environments. They thrive
         in mountainous pastures, moorlands, and open grasslands. At the zoo, they are provided with large outdoor enclosures that
         replicate open, grassy habitats.'''.replace( '\n', ' ' ),
      '''Highland Cattle are herbivorous grazers, feeding primarily on grasses, shrubs, and coarse vegetation. Their strong
         digestive systems allow them to extract nutrients from fibrous plant material. In managed care, they are fed hay, grasses,
         and supplemental feed to maintain health and encourage natural grazing behaviours'''.replace( '\n', ' ' ),
      '''These cattle are social and form hierarchical herds with clear dominance structures. They spend much of the day grazing or
         resting and are generally calm and docile. Males can become more assertive during the breeding season. Herd interactions
         include grooming, nuzzling, and occasional play among younger animals'''.replace( '\n', ' ' ),
      '''Highland Cattle are adapted to cold, wet climates. Their long, double-layered coat provides insulation against rain, wind,
         and snow, while their large, muscular build helps conserve heat. Broad hooves allow them to traverse soft or uneven
         terrain, and their efficient digestion enables them to thrive on coarse forage.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in managed populations, with a gestation period of approximately 9 months. Calves are born
         relatively well-developed and can stand and follow the herd shortly after birth. Lifespan typically ranges 15–20 years,
         with careful management in zoos often extending longevity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two young highland cattle, Blue and Jay, who are named after the Toronto Blue Jays baseball
         team. They are still growing, and love interacting with guests during wild encounters.'''.replace( '\n', ' ' )
   ),
   (
      'Mouflon',
      'Ovis Orientalis',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The mouflon can be spotted at the mouth of the Eurasia Wilds loop, just past the sign with the bactrian camel and wild
         horse at the base.'''.replace( '\n', ' ' ),
      '''The mouflon can be seen in their habitat year-round.''',
      '''The Mouflon is a medium-sized wild sheep with a sturdy build and short, reddish-brown coat, often with a light saddle patch
         across the back. Males are distinguished by large, curved horns that spiral outward, while females have shorter, thinner
         horns or none at all. They belong to the family Bovidae and are considered one of the ancestors of modern domestic sheep.'''
         .replace( '\n', ' ' ),
      '''Mouflon are native to the mountainous regions of Europe and western Asia, including Corsica, Sardinia, and parts of the
         Middle East. They inhabit rocky hills, open woodlands, and steep slopes, preferring areas with both grazing vegetation and
         rugged terrain for protection from predators.'''.replace( '\n', ' ' ),
      '''Mouflon are primarily grazers, feeding on grasses, herbs, and shrubs. Their digestive system allows them to extract
         nutrients efficiently from tough, fibrous vegetation. At the zoo, they are provided with a mix of grasses, hay, and browse
         to encourage natural grazing and foraging behaviours.'''.replace( '\n', ' ' ),
      '''Mouflon are social animals, forming herds structured by age and sex. Males may compete for dominance during the breeding
         season through horn clashes and displays of strength. Herds provide safety in numbers, and group living facilitates
         learning and protection against predators.'''.replace( '\n', ' ' ),
      '''Mouflon are highly adapted to steep, rocky environments. Their strong legs and hooves provide balance and traction on
         uneven terrain, while their agility allows them to escape predators. Horns serve both as weapons during mating competitions
         and as a visual signal of maturity and dominance. Their thick coats protect against cold mountain temperatures, and their
         alert senses help detect danger quickly.'''.replace( '\n', ' ' ),
      '''Breeding occurs in the autumn, with dominant males competing for access to females. After a gestation period of about 5
         months, females give birth to a single lamb, which is able to walk and follow the herd within hours. Mouflon typically live
         10–12 years in the wild, with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red Panda',
      'Ailurus Fulgens',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      # '''You can get to the red panda habitat by taking the Eurasia Wilds loop from the side with the Amur tigers. The red panda
      #    enclosure will be the first one you encounter after the tigers. The red pandas will be in the second habitat, the one with
      #    the glass viewing. Red pandas are most active early and late in the day, so your best chance of seeing them active is to
      #    visit their enclosure first thing in the morning. Through much of the day they spend their time sleeping way up in the
      #    trees. To spot them in their exhibit, look all the way up to the top branches of the tallest trees in their habitat, and
      #    look for a couple of red-black furry balls.'''.replace( '\n', ' ' ),
      '''The red pandas' normal habitat in Eurasia is currently under construction and inaccessible. In the meantime, the red pandas
         have moved into a temporary habitat in the Africa savanna in between the lions and hyenas. It is across from the main
         open-air lion viewing.'''.replace( '\n', ' ' ),
      '''Red pandas are most comfortable in the cooler weather, so visiting them from the fall through the spring will give you the
         best chance to see them active. During the summer months they spend much of their time sleeping high up in the trees. On
         the warmest summer days they may opt to spend their time inside, away from guests.'''.replace( '\n', ' ' ),
      '''The Red Panda is a small, arboreal mammal with reddish-brown fur, a bushy ringed tail, and a round face marked with white
         patches around the eyes and snout. Adults weigh 3–6 kg and measure about 50–64 cm in body length, with the tail adding
         another 28–59 cm. Despite its name, it is not closely related to the giant panda but belongs to its own family, Ailuridae.'''
         .replace( '\n', ' ' ),
      '''Red Pandas are native to the temperate forests of the Himalayas, including Bhutan, Nepal, India, and parts of China. They
         inhabit mountainous regions with dense bamboo understories, often at elevations of 2,200–4,800 metres. They rely on forest
         cover for shelter, nesting, and protection from predators.'''.replace( '\n', ' ' ),
      '''Red Pandas are primarily herbivorous, feeding mainly on bamboo leaves and shoots, though they also eat fruits, berries,
         insects, and small mammals occasionally. In zoos, their diet includes bamboo, fruits, specially formulated herbivore
         biscuits, and enrichment items that encourage natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Red Pandas are mostly solitary and territorial. They are crepuscular and nocturnal, being most active at dawn and dusk.
         They are skilled climbers and spend much of their time in trees, using their bushy tails for balance and warmth.
         Communication occurs through vocalisations, scent markings, and body language.'''.replace( '\n', ' ' ),
      '''Red Pandas are adapted to life in temperate, mountainous forests. Their semi-retractable claws, flexible ankles, and strong
         limbs enable agile climbing. Dense fur insulates against cold, and the long, bushy tail provides both balance and warmth
         while resting. Their false thumb, an extension of the wrist bone, helps grip bamboo and other vegetation efficiently.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in late winter to early spring. Females give birth to 1–4 cubs in nests lined with leaves and moss, often
         in tree hollows. Cubs are dependent on their mother for several months, gradually learning to climb and forage. Red Pandas
         can live 8–10 years in the wild, with some individuals reaching 14 years in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two red pandas, a young female, Poppy, born in 2024, and an older male, Kalden, who came from
         the Edmonton Zoo. Poppy is young and energetic, and can often be spotted zooming around her habitat in the cool mornings.
         Kalden moves at a slower pace, and spends most of his time high up in the trees.'''.replace( '\n', ' ' )
   ),
   (
      'Snow Leopard',
      'Panthera Uncia',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The snow leopard habitat can be accessed by taking the Eurasia Wilds loop on the side to the left of the mouflon. You can
         find them across from the West Caucasian turs. The snow leopards are most active early in the day, especially during the
         summer months, so your best chance of seeing them active is to head to their exhibit first thing in your visit. The snow
         leopard habitat is designed to mimic the mountainous habitats they originate from. They can often be spotted towards the
         back of the exhibit on top of their rock wall. During the warm months of the year, you may walk up the mountain to get a
         good vantage point of the habitat. They may also lie down in front of the glass viewing inside the cave. A couple of other
         good spots to check are the set of trees across from the West Caucasian tur habitat, and in the dip beside the rocks by the
         viewing nearest to the Steller's sea eagle. Look closely and you should be able to spot them.'''.replace( '\n', ' ' ),
      '''Snow leopards are built for the extreme cold of the Himalayas, and thus are the most active in the winter. During the
         warmer months, they may be active earlier in the day, but they will spend a lot of the day sleeping in the shade, and
         perhaps away from the view of zoo visitors.'''.replace( '\n', ' ' ),
      '''The Snow Leopard is a large, elusive big cat with a thick, smoky-grey coat marked with black rosettes and spots. Its long,
         bushy tail is nearly as long as its body, providing balance and warmth. Adults weigh between 35–55 kg, with males typically
         larger than females. Adapted to mountainous terrain, it has short forelimbs, long hind limbs, and wide, fur-covered paws
         that act as natural snowshoes.'''.replace( '\n', ' ' ),
      '''Snow Leopards are native to the high mountains of Central and South Asia, including the Himalayas, Tibetan Plateau, and
         ranges across Mongolia, China, Afghanistan, and Russia. They inhabit rugged, rocky terrain at elevations from 3,000 to
         5,500 metres, where steep cliffs, ridges, and snowfields provide camouflage and hunting advantage.'''.replace( '\n', ' ' ),
      '''Snow Leopards are carnivorous apex predators, primarily hunting wild ungulates such as bharal (blue sheep), ibex, and
         argali. They also take smaller mammals, birds, and occasionally livestock. In captivity, their diet is managed with a
         variety of raw meat and enrichment feeding that encourages stalking, pouncing, and natural predatory behaviours.'''
         .replace( '\n', ' ' ),
      '''Snow Leopards are solitary and territorial, with overlapping home ranges monitored through scent marking, scrapes, and
         vocalisations. They are mostly crepuscular, hunting at dawn and dusk. Despite their solitary nature, they communicate with
         soft vocalisations, scent markings, and visual cues to maintain territory boundaries. They are strong, agile climbers
         capable of jumping up to 6 metres between rocky outcrops.'''.replace( '\n', ' ' ),
      '''Snow Leopards are exceptionally adapted to cold, high-altitude environments. Their thick, dense fur provides insulation
         against sub-zero temperatures, while the long tail wraps around the body for additional warmth. Fur-covered paws help
         traverse snow without sinking, and strong, muscular limbs allow them to scale steep cliffs and rocky terrain efficiently.
         Their cryptic coat provides camouflage against rocky and snowy backgrounds, aiding stealth in hunting and predator
         avoidance.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late winter to early spring. Females give birth to 2–3 cubs in rocky dens or crevices, which provide
         protection from predators and harsh weather. Cubs are dependent on the mother for 18–22 months, learning to hunt and
         navigate mountainous terrain. Snow Leopards can live 10–12 years in the wild, with captive individuals sometimes exceeding
         20 years under optimal care.'''.replace( '\n', ' ' ),
      '''The zoo is home to four snow leopards: an adult male, Pemba who goes in exhibit by himself on Mondays, Wednesdays, and
         Fridays, and a mother, Jita, and her two female cubs, Minu and Zoya, who are all on exhibit together on Tuesdays,
         Thursdays, Saturdays,and Sundays. The mother and cubs are nearing the end of their time together on exhibit. Once the cubs
         become too old for their mother, they will be moved to other zoos. Snow leopards are solitary animals, except for during
         breeding season, and a mother and her cubs, hence why Pemba goes on exhibit by himself. The snow leopard cubs are quite
         active, and can often be seen chasing each other, or their mother, around the habitat.'''.replace( '\n', ' ' )
   ),
   (
      'Steller\'s Sea Eagle',
      'Haliaeetus Pelagicus',
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Steller's sea eagles can be spotted by taking the Eurasia Wilds loop to the left of the mouflon. The eagles can be
         spotted just past the snow leopards, and across from the first camel habitat.'''.replace( '\n', ' ' ),
      '''The Steller's sea eagles are very well adapted to the cold, and can be seen outside year-round.''',
      '''The Steller’s Sea Eagle is one of the largest eagles in the world, notable for its massive yellow beak, striking
         black-and-white plumage, and powerful build. Adults typically weigh 5–9 kg and have a wingspan of 2–2.5 metres. Their
         strong talons and hooked beak are perfectly adapted for hunting and consuming fish, their primary prey.'''
         .replace( '\n', ' ' ),
      '''Native to coastal regions of northeastern Asia, particularly Russia’s Kamchatka Peninsula, the Sea of Okhotsk, and Japan,
         Steller’s Sea Eagles inhabit river valleys, coastal cliffs, and large water bodies. They rely on areas with abundant fish
         populations and often perch near ice edges or open water during winter.'''.replace( '\n', ' ' ),
      '''These eagles are primarily piscivorous, feeding on salmon, trout, and other fish species, though they also hunt waterfowl
         and small mammals when available. At the zoo, they are fed a diet of fish, supplemented with meat and enrichment items to
         encourage hunting and foraging behaviours.'''.replace( '\n', ' ' ),
      '''Steller’s Sea Eagles are generally solitary or found in pairs, though large congregations can form in wintering areas with
         abundant fish. They are territorial, especially during the breeding season, and use vocalisations, posturing, and wing
         displays to communicate dominance and defend nesting sites. Flight is powerful and deliberate, allowing them to patrol
         large territories.'''.replace( '\n', ' ' ),
      '''These eagles are well adapted to cold, coastal environments. Their dense feathers provide insulation against frigid
         temperatures, and their strong talons and beak enable them to catch and handle large, slippery fish. Their large wingspan
         allows efficient soaring over long distances, while keen eyesight enables precise hunting in open water and along ice
         edges.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late winter or early spring. Pairs build massive stick nests on cliffs or tall trees, sometimes reusing
         them for several years. Females typically lay 1–3 eggs, which are incubated for about 40–45 days. Chicks fledge after 10–12
         weeks but remain dependent on their parents for several more months. Lifespan in the wild is 20–25 years, with captive
         individuals often living longer.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has a young breeding pair of Steller's Sea Eagles.'''.replace( '\n', ' ' )
   ),
   (
      'West Caucasian Tur',
      'Capra Caucasica',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The West Caucasian turs can be spotted in two different habitats in the Eurasia Wilds section of the zoo. The female tur
         can be spotted in a habitat in the main Eurasia Wilds loop, which can be accessed by taking the loop to the left of the
         mouflon. The tur habitat will be the first one you see. The male turs can be found in the Eurasia Wilds drive-thru. To go
         through the drive-through you must hop on zoomobile before the Eurasia stop and stay on after the Tundra Trek stop.'''
         .replace( '\n', ' ' ),
      '''The tur can be seen on-foot and in the drive-through year-round.''',
      '''The West Caucasian Tur is a robust mountain goat with a muscular body, short legs, and large, curved horns that spiral
         backwards. Adults have a dense, dark brown coat in winter, which lightens slightly in summer, providing insulation against
         cold. Males are larger and have thicker, more prominently curved horns than females. This species belongs to the family
         Bovidae and is recognised for its agility and climbing ability.'''.replace( '\n', ' ' ),
      '''Native to the high mountains of the western Caucasus region (Russia and Georgia), West Caucasian Turs inhabit steep, rocky
         slopes and alpine meadows at elevations of 1,000–4,000 metres. They prefer rugged terrain that offers protection from
         predators and extreme weather conditions.'''.replace( '\n', ' ' ),
      '''These turs are herbivores, grazing on grasses, herbs, shrubs, and lichens. Their digestive system efficiently extracts
         nutrients from sparse mountain vegetation. At the zoo, they are provided with hay, browse, and grasses that encourage
         natural grazing and foraging behaviours.'''.replace( '\n', ' ' ),
      '''West Caucasian Turs are social, forming small herds usually segregated by sex outside the breeding season. Males join
         females only during the rut. They are agile climbers, moving effortlessly over rocky cliffs to escape predators and access
         food. Herd members communicate through body language, vocalisations, and horn displays.'''.replace( '\n', ' ' ),
      '''West Caucasian Turs are well adapted to mountainous environments. Their strong legs, muscular build, and split hooves allow
         them to navigate sheer cliffs with stability and precision. Dense winter coats provide insulation, while their horns serve
         for dominance displays, defence, and competition during mating season. Their keen eyesight and alert senses help detect
         predators from a distance.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late autumn, with males competing for access to females through horn clashes and displays. Females give
         birth to a single kid in spring after a gestation of around 160 days. Kids are able to climb within hours of birth.
         Lifespan in the wild is typically 12–15 years, with longer lifespans in captivity under proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Tundra Trek
   (
      'Arctic Wolf',
      'Canis Lupus Arctos',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Arctic wolf enclosure is located in the center of the Tundra Trek exhibit. The arctic wolf enclosure at the is very
         large, and has many viewing points. To get the best view of the wolves, you can move 360° around the habitat, and  the
         Tundra Trek exhibit, and you should get a semi-close view. The wolves will generally be more active in the morning, and
         closer to dusk.'''.replace( '\n', ' ' ),
      '''Arctic wolves are adapted to the extreme cold, and will be the most active in the cooler months, although you are likely to
         see them moving around on any day that is not too hot.'''.replace( '\n', ' ' ),
      '''The Arctic Wolf is a subspecies of gray wolf adapted to the extreme conditions of the Arctic. It has a thick, white to
         creamy coat that provides camouflage in snowy landscapes, small rounded ears to minimize heat loss, and a stocky build with
         short muzzle and legs relative to other wolf subspecies. Adults typically weigh 36–50 kg, with males slightly larger than
         females.'''.replace( '\n', ' ' ),
      '''Native to the Arctic regions of Canada, Greenland, and northern Alaska, Arctic Wolves inhabit tundra, ice fields, and
         boreal forest edges. They are highly adapted to cold, open environments with sparse vegetation and long winters. Denning
         areas are usually sheltered, rocky crevices or snowbanks.'''.replace( '\n', ' ' ),
      '''Arctic Wolves are carnivorous apex predators. Their diet primarily consists of muskoxen, Arctic hares, caribou, and
         occasionally small rodents or birds. In captivity, their diet is managed with meat, bones, and enrichment to simulate
         hunting and feeding behaviours, ensuring physical and mental stimulation.'''.replace( '\n', ' ' ),
      '''These wolves are social, living in packs of 5–20 individuals with a strict dominance hierarchy. Packs cooperate in hunting,
         territory defense, and raising pups. They communicate through howls, growls, body posture, and scent marking. Arctic Wolves
         are generally more tolerant of cold weather than other wolf subspecies and are highly territorial.'''.replace( '\n', ' ' ),
      '''Arctic Wolves are superbly adapted to extreme cold and scarce prey. Their dense undercoat and long guard hairs provide
         insulation, while their short ears and compact body reduce heat loss. Large, padded paws act as snowshoes, distributing
         weight across snow and ice. White camouflage allows them to approach prey stealthily, and their cooperative hunting
         strategies help tackle animals much larger than themselves.'''.replace( '\n', ' ' ),
      '''Breeding occurs once a year in late winter. Females give birth to 4–7 pups in dens sheltered from the elements. Both
         parents, along with pack members, help feed and protect the young. Pups grow quickly, joining the pack in hunting by
         autumn. Lifespan in the wild is typically 7–10 years, with captive individuals often living 12–14 years.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo has a pack of seven arctic wolves. Typically speaking, they move through their exhibit together.'''
         .replace( '\n', ' ' )
   ),
   (
      'Caribou',
      'Rangifer Tarandus',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The caribou habitat can be accessed by taking the Tundra Trek path from either side, and stopping when you get to the
         entrance to the Americas Outdoor Mayan Temple Ruins exhibit. There is one viewing of the habitat here, and another if you
         enter the Mayan Temple Ruins and head towards the flamingo enclosure. The caribou habitat wraps around the temple up to the
         spider monkey habitat. The caribou enclosure at the zoo is very large, and expands quite far back to the left from the main
         viewing area. Most of the time the caribou can be seen towards the back, right section of the habitat in and around their
         shelter.'''.replace( '\n', ' ' ),
      '''Caribou are suited for the extreme cold, and can be seen year-round in their habitat.''',
      '''Caribou, also known as reindeer in some regions, are medium-to-large Arctic and sub-Arctic ungulates with broad, flat
         hooves and dense fur for insulation. Both males and females grow antlers, though males typically have larger, more branched
         antlers that are shed annually. Their coat changes seasonally, ranging from reddish-brown in summer to silvery-grey in
         winter, providing camouflage and thermal protection.'''.replace( '\n', ' ' ),
      '''Caribou are native to tundra and boreal forest regions across North America, Greenland, and northern Eurasia. They inhabit
         open tundra plains, taiga forests, and mountainous regions, migrating long distances seasonally to find food and breeding
         grounds.'''.replace( '\n', ' ' ),
      '''Caribou are herbivorous, feeding primarily on lichens, mosses, grasses, and shrubs. In winter, lichens (particularly
         reindeer moss) form a critical part of their diet, which they uncover by scraping snow with their hooves. At the zoo, their
         diet is supplemented with hay, browse, and specially formulated herbivore pellets to replicate natural foraging.'''
         .replace( '\n', ' ' ),
      '''Caribou are social and often form large herds, especially during migration. Herds provide safety in numbers against
         predators and facilitate mating interactions. They are highly migratory, travelling tens to hundreds of kilometres each
         year, and exhibit complex social structures with dominant males during the rut.'''.replace( '\n', ' ' ),
      '''Caribou are superbly adapted to cold, harsh environments. Their hollow hair provides insulation and buoyancy, while wide,
         concave hooves act like snowshoes for walking on snow and soft tundra soils. Seasonal antler growth aids in foraging and
         social dominance displays, and their keen sense of smell helps locate food buried beneath snow.'''.replace( '\n', ' ' ),
      '''Breeding occurs in the fall, with males competing for females during the rut. Females give birth to a single calf in late
         spring, timed for abundant food availability. Calves are able to stand and follow the herd within hours. Lifespan in the
         wild is typically 10–15 years, while captive individuals may live longer with proper care.'''.replace( '\n', ' ' ),
      '''The zoo has a herd of six female caribou.'''
   ),
   (
      'Lesser Snow Goose',
      'Anser Caerulescens',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The lesser snow goose habitat can be found by taking the Tundra Trek loop on the left, on the side close to the Caribou
         Cafe. You will see the snow goose enclosure past the first viewing of the Arctic wolves, on the left.'''.replace( '\n', ' ' ),
      '''Lesser snow geese are very well adapted to the snow and cold, and can be viewed in the Tundra Trek year-round.''',
      '''The Lesser Snow Goose is a medium-sized migratory goose best known for its bright white plumage, black wing tips visible in
         flight, and pink legs and bill. Some individuals occur in a dark “blue morph,” with a dark body and white head. Compared to
         the Greater Snow Goose, it is smaller and more compact.'''.replace( '\n', ' ' ),
      '''Lesser Snow Geese breed in the Arctic tundra of northern Canada and Alaska. During migration and winter, they travel south
         to wetlands, agricultural fields, and coastal marshes across southern Canada, the United States, and parts of Mexico. They
         rely heavily on open water and grassy or marshy habitats.'''.replace( '\n', ' ' ),
      '''These geese are herbivorous, feeding on grasses, sedges, roots, tubers, and grains. On breeding grounds, they graze on
         tundra vegetation, while during migration and winter they often forage in agricultural fields. At the zoo, they are fed a
         balanced diet of grains, greens, and formulated waterfowl feed.'''.replace( '\n', ' ' ),
      '''Lesser Snow Geese are highly social and form large flocks, sometimes numbering in the tens of thousands. They are
         monogamous, forming long-term pair bonds. Communication includes loud honking calls used to maintain flock cohesion and
         coordinate movement during flight and feeding.'''.replace( '\n', ' ' ),
      '''These geese are well adapted to long-distance migration and cold environments. Their strong wings enable sustained flight
         over vast distances, while dense feathers provide insulation during Arctic breeding seasons. Their bills are well suited
         for grazing and digging up roots, allowing them to exploit a wide range of plant foods.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late spring on Arctic tundra. Females lay 3–5 eggs in ground nests lined with down. Both parents defend
         the nest and lead goslings to feeding areas shortly after hatching. Goslings grow rapidly and are capable of flight by late
         summer. Lesser Snow Geese can live 15–20 years, with some individuals reaching greater ages.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   ( # Also in Canadian Domain
      'Northern Bald Eagle',
      'Haliaeetus Leucocephalus',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Northern bald eagle can be spotted in two different spots--one in the Tundra Trek, and another in the Canadian Domain.
         To see the eagle in the Tundra Trek, take the loop on the side with the polar bears and head towards the viewing for the
         larger polar bear grass habitat. The eagle enclosure will be on your left. To see the eagle in the domain, head to the
         bottom of the hill, and head towards the female wood bison paddock, not towards the grizzly bears. The eagle habitat will
         be on your left.'''.replace( '\n', ' ' ),
      '''Bald eagles are well adapted to the cold and can stay outside all winter. The eagle in the Tundra Trek can be viewed
         year-round, while the eagle in the domain can be viewed whenver the domain is open.'''.replace( '\n', ' ' ),
      '''The Northern Bald Eagle is a large bird of prey best known for its white head and tail, dark brown body, and powerful
         yellow beak and talons. Juveniles are mottled brown and white and do not develop the iconic white head and tail until about
         five years of age. Adults typically weigh 3–6 kg, with females noticeably larger than males, and have a wingspan of up to
         2.4 metres.'''.replace( '\n', ' ' ),
      '''Bald Eagles are found across much of North America, particularly near large bodies of water such as lakes, rivers, coastal
         shorelines, and wetlands. Northern populations breed in Canada and Alaska, often remaining year-round where open water is
         available. They require tall trees or cliffs for nesting and perching.'''.replace( '\n', ' ' ),
      '''Bald Eagles are primarily piscivorous, feeding mainly on fish, but they are also opportunistic hunters and scavengers.
         Their diet may include waterfowl, small mammals, and carrion. At the zoo, they are fed a varied diet of fish and meat, with
         feeding enrichment designed to encourage tearing, grasping, and natural feeding behaviours.'''.replace( '\n', ' ' ),
      '''Bald Eagles are usually seen alone or in pairs, though they may gather in larger numbers where food is abundant. They form
         long-term pair bonds and often reuse the same nest year after year, gradually building massive structures over time.
         Communication includes vocal calls, posturing, and flight displays.'''.replace( '\n', ' ' ),
      '''These eagles are highly adapted for hunting in cold, aquatic environments. Their keen eyesight allows them to spot prey
         from great distances, while powerful talons provide a secure grip on slippery fish. Broad wings enable efficient soaring
         and gliding, conserving energy during long patrol flights. Dense plumage helps insulate against cold northern climates.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in late winter to early spring. Pairs build large stick nests in tall trees or on cliffs, often near water.
         Females lay 1–3 eggs, which hatch after about 35 days. Chicks fledge at around 10–12 weeks but remain dependent on their
         parents for several more months. Bald Eagles can live 20–30 years in the wild, with captive individuals sometimes living
         longer.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Polar Bear',
      'Ursus Maritimus',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The polar bears can be spotted in several habitats in the Tundra Trek exhibit. Coming at the habitat from the side closer
         to Eurasia, you have the maternity yard, the main pool habitat, and the main grass habitat. In the warmer months the bears
         will likely avoid the grass habitat and either spend their time in the pool habitat and the maternity yard in the shade.
         In the cooler months you are more likely to see bears being active in the grass habitat.'''.replace( '\n', ' ' ),
      '''While visible all year-round, the polar bears at the zoo are far more active during the cooler months. During the summer,
         they are quite lethargic, and spend much of their time resting in the shade. If you want to see the polar bears most
         active, playing with one another, consider visiting in the winter.'''.replace( '\n', ' ' ),
      '''The Polar Bear is the largest land carnivore in the world. Adults have a massive body, long neck, small ears, and a narrow
         skull adapted for hunting seals. Their fur appears white but is actually transparent and hollow, helping trap heat and
         providing camouflage against snow and ice. Beneath the fur, their skin is black, which absorbs solar heat. Adult males
         typically weigh 350–700 kg, while females are smaller at 150–350 kg.'''.replace( '\n', ' ' ),
      '''Polar Bears are native to the circumpolar Arctic, occurring in Canada, Greenland, Russia, Alaska, and Norway. They are
         closely tied to sea ice, which they use as platforms for hunting, resting, and travelling. In Canada, they are found
         primarily in Hudson Bay, the Arctic Archipelago, and along northern coastlines. As sea ice melts seasonally, many bears
         move onto land during summer months.'''.replace( '\n', ' ' ),
      '''Polar Bears are highly specialised carnivores that rely primarily on seals, especially ringed and bearded seals. They hunt
         by waiting at breathing holes in the ice or stalking seals resting on the ice surface. Their diet is extremely high in fat,
         which provides the energy needed to survive the cold. In zoos, Polar Bears are fed a carefully balanced diet of meat, fish,
         and specially formulated supplements, with enrichment feeding designed to encourage problem-solving and natural hunting
         behaviours.'''.replace( '\n', ' ' ),
      '''Polar Bears are mostly solitary, except for females with cubs or during mating season. They have large home ranges and are
         strong swimmers, capable of swimming long distances between ice floes. Although generally quiet, they communicate through
         body language, vocalisations, and scent marking. On land, they may scavenge carcasses or explore coastal areas while
         waiting for sea ice to return.'''.replace( '\n', ' ' ),
      '''Polar Bears are exceptionally adapted to Arctic life. Their thick layer of blubber, which can be over 10 cm deep, provides
         insulation and energy storage. Dense, water-repellent fur keeps them dry and warm after swimming. Large, wide paws act as
         paddles in water and distribute weight on ice, while rough foot pads and sharp claws improve traction. Their powerful sense
         of smell allows them to detect seals from kilometres away or beneath thick ice.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring, but implantation of the fertilised egg is delayed until autumn. Pregnant females enter maternity
         dens in snowbanks, where they give birth to 1–2 cubs in winter. Cubs are born blind, nearly hairless, and weigh less than
         one kilogram. They remain with their mother for about 2.5 years, learning hunting and survival skills. Polar Bears
         typically live 20–25 years in the wild, with some individuals living longer in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to four polar bears, male Hudson, and females Juno, Aurora, and Nikita. The bears go on display in
         pairs of two.'''.replace( '\n', ' ' )
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American Flamingo',
      'Phoenicopterus Ruber',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The American flamingos are part of the Mayan Temple Ruins exhibit, which is accessed be walking through the Tundra Trek.
         Once you reach the waterfall, walk to the right and you will come upon the flamingos.'''.replace( '\n', ' ' ),
      '''American flamingos are a relatively hardy bird, tolerating temperatures as low as 5°C. They can be seen reliably from May
         through to October, but they can also often be seen on warmer days in March, April, and November.'''.replace( '\n', ' ' ),
      '''The American Flamingo is the largest and most vividly coloured of all flamingo species. Adults have bright pink to
         coral-red plumage, long slender legs, and a distinctive downward-curved bill adapted for filter feeding. The bill is pink
         with a black tip, and their legs are typically pink or reddish. Juveniles are greyish with duller colouring, developing
         their characteristic pink plumage over several years.'''.replace( '\n', ' ' ),
      '''American Flamingos are native to the Caribbean, the Galápagos Islands, northern South America, and coastal regions of
         Central America, including the Yucatán Peninsula. They inhabit shallow lagoons, salt flats, mangrove swamps, and coastal
         wetlands where warm, saline or brackish water supports abundant food sources.'''.replace( '\n', ' ' ),
      '''Flamingos are specialised filter feeders, feeding primarily on algae, diatoms, small crustaceans, and aquatic invertebrates.
         Their unique bills work upside down, filtering food from mud and water using comb-like structures called lamellae.
         Carotenoid pigments in their diet are responsible for their pink colouration. At the zoo, American Flamingos are fed a
         nutritionally balanced diet that includes specially formulated pellets and supplements to maintain healthy plumage colour.'''
         .replace( '\n', ' ' ),
      '''American Flamingos are highly social birds that live and breed in large colonies, sometimes numbering in the thousands.
         Social behaviours such as synchronized head-flagging, wing-saluting, and marching displays play an important role in
         communication and breeding. They are monogamous during the breeding season and rely heavily on group cohesion for safety
         and successful reproduction.'''.replace( '\n', ' ' ),
      '''Flamingos are superbly adapted to life in shallow wetlands. Their long legs allow them to wade into deeper water than many
         other birds, while webbed feet help stir up sediment to expose food. Their specialised bills and tongues enable efficient
         filter feeding, and salt glands located near the eyes help them excrete excess salt from saline environments.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in large colonies, often triggered by rainfall and suitable water levels. Flamingos build cone-shaped mud
         nests on raised mounds to protect eggs from flooding. Females typically lay a single egg, which both parents incubate.
         Chicks hatch with grey down and straight bills and are fed nutrient-rich crop milk produced by both parents. Flamingos are 
         ong-lived birds, commonly reaching 30–40 years, with some individuals living even longer in captivity.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a flamboyance American flamingos, including several that are around 50 years old!'''
         .replace( '\n', ' ' )
   ),
   (
      'Red-Legged Seriema',
      'Cariama Cristata',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The red-legged seriemas are part of the Mayan Temple Ruins exhibit, which is accessed by walking through the Tundra Trek.
         The seriema can be found in a habitat in between the flamingos and spider monkeys.'''.replace( '\n', ' ' ),
      '''Red-legged seriemas are outdoor birds that are most reliably visible from May through October. They may also be visible on
         warmer days in March, April, and November, depending on conditions in the outdoor habitat.'''.replace( '\n', ' ' ),
      '''The Red-legged Seriema is a tall, long-legged bird with greyish-brown plumage, a pale belly, red legs, and a red bill. It
         has a distinctive fan-shaped crest of feathers at the base of the bill and long eyelashes around the eyes. The species has
         a ground-dwelling build, with strong legs used for walking, running, and striking at prey.'''.replace( '\n', ' ' ),
      '''Red-legged Seriemas are native to South America, especially open grasslands, savannas, scrublands, and lightly wooded
         habitats in Brazil, Bolivia, Paraguay, Uruguay, and Argentina. They are usually found in dry, open areas where they can
         walk and run while foraging on the ground.'''.replace( '\n', ' ' ),
      '''Red-legged Seriemas are omnivorous, feeding on insects, small reptiles, rodents, birds, eggs, seeds, fruits, and other
         plant material. They are known for subduing larger prey by striking it against the ground. At the zoo, their diet includes
         a balanced mix of appropriate animal protein, produce, and formulated foods.'''.replace( '\n', ' ' ),
      '''These birds are usually seen alone, in pairs, or in small family groups. They spend much of their time walking through open
         habitat in search of food and are strong runners. Red-legged Seriemas are also known for loud, carrying calls that pairs may
         use to communicate and maintain territory.'''.replace( '\n', ' ' ),
      '''Red-legged Seriemas are adapted for life on the ground. Their long legs allow them to run quickly through open habitat, and
         their strong feet help them capture and handle prey. Their crest, alert posture, and cryptic plumage help with communication
         and camouflage in dry grassland environments.'''.replace( '\n', ' ' ),
      '''Breeding pairs build nests in shrubs or low trees. Females usually lay two eggs, and both parents may help care for the
         chicks. Young seriemas leave the nest before they can fly well and follow their parents while learning to forage. The
         species can live for many years under human care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Turkey Vulture',
      'Cathartes Aura',
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The turkey vultures are part of the Mayan Temple Ruins exhibit, which is accessed by walking through the Tundra Trek. The
         turkey vulture can be found in a habitat in between the flamingos and spider monkeys.'''.replace( '\n', ' ' ),
      '''Turkey vultures are outdoor birds that are most reliably visible from May through October. They may also be visible on
         temperate days in March, April, and November, depending on conditions in the outdoor habitat.'''.replace( '\n', ' ' ),
      '''The Turkey Vulture is a large, dark soaring bird with long wings, a small bare red head, and a pale bill. In flight, it
         holds its wings in a shallow V and often rocks from side to side. From below, the flight feathers appear silvery compared
         with the darker body and wing linings.'''.replace( '\n', ' ' ),
      '''Turkey Vultures are widespread across the Americas, from southern Canada through the United States, Central America, and
         much of South America. They use many habitats, including forests, grasslands, wetlands, deserts, agricultural areas, and
         open landscapes where carrion can be located from the air.'''.replace( '\n', ' ' ),
      '''Turkey Vultures are scavengers that feed primarily on carrion. They use an excellent sense of smell to locate food, a rare
         ability among birds. At the zoo, they receive a carefully managed carnivore diet that supports their nutritional needs while
         reflecting their natural scavenging biology.'''.replace( '\n', ' ' ),
      '''Turkey Vultures are often seen soaring for long periods while searching for food. They conserve energy by riding thermals
         and rarely need to flap while gliding. They may roost in groups and rely on body posture, hissing, and other behaviours for
         communication.'''.replace( '\n', ' ' ),
      '''Turkey Vultures are highly adapted for scavenging. Their bare head helps keep feathers clean while feeding, their keen
         sense of smell helps them find carrion hidden under vegetation, and their broad wings make them efficient soaring birds.
         Their strong digestive system allows them to safely consume food that would be unsafe for many other animals.'''
         .replace( '\n', ' ' ),
      '''Turkey Vultures usually nest in sheltered places such as hollow logs, caves, dense vegetation, or abandoned structures
         rather than building a typical nest. Females usually lay one to three eggs, and both parents help incubate and feed the
         young. Young vultures remain dependent on their parents for several weeks after hatching.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Black-Handed Spider Monkey',
      'Ateles Geoffroyi',
      14,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The black-handed spider monkeys are part of the Mayan Temple Ruins exhibit, which is accessed be walking through the Tundra
         Trek. Once you reach the waterfall, walk to the right, and you will find the spider monkeys across from the flamingos. The
         spider monkeys often move through the indoor and outdoor habitats in a given day. Check all of their platforms, along the
         back of the exhibit, and above the glass viewing across from the flamingos. If you don't spot them, then they are likel
         inside for the moment. If you are patient, you may see them venture outside.'''.replace( '\n', ' ' ),
      '''Spider monkeys are warm-weather primates, and struggle to be outside in any temperature below 15°C. They can be reliably
         seen from May through September, but even then, on colder days they opt to spend their time inside.'''.replace( '\n', ' ' ),
      '''The Black-handed Spider Monkey is a slender, long-limbed primate with a small body, elongated arms and legs, and an
         exceptionally long, prehensile tail. The tail acts as a fifth limb and has a bare, sensitive underside at the tip for
         gripping branches. Fur colour ranges from golden brown to dark brown or black, with distinctive black hands and feet. The
         face is mostly hairless with expressive features.'''.replace( '\n', ' ' ),
      '''This species is native to tropical forests of Central America, from southern Mexico through Panama. It inhabits lowland
         rainforests, evergreen forests, and sometimes mangroves, spending most of its life high in the forest canopy. Dense,
         continuous tree cover is essential for its movement and feeding.'''.replace( '\n', ' ' ),
      '''Black-handed Spider Monkeys are primarily frugivorous, feeding mainly on ripe fruits. They also consume leaves, flowers,
         seeds, and occasional insects. Their diet changes seasonally based on food availability. At the zoo, they are fed
         acarefully balanced diet of fruits, vegetables, leafy greens, and primate biscuits, with foraging enrichment to encourage
         natural feeding behaviours.'''.replace( '\n', ' ' ),
      '''These monkeys live in large social groups that split into smaller subgroups throughout the day, a system known as
         fission–fusion social structure. This allows them to efficiently locate food resources across large forest areas. They are
         highly agile and move through the canopy using brachiation, swinging effortlessly from branch to branch. Communication
         includes vocal calls, facial expressions, and body language.'''.replace( '\n', ' ' ),
      '''Black-handed Spider Monkeys are specialised for an arboreal lifestyle. Their long limbs and hook-like hands allow fast,
         energy-efficient brachiation. The prehensile tail provides strength, balance, and fine motor control, enabling them to
         hang or move while carrying food or infants. Reduced thumbs prevent interference during swinging, making their movement
         highly streamlined.'''.replace( '\n', ' ' ),
      '''Females give birth to a single infant after a gestation period of about 7.5 months. Infants cling to their mother’s belly
         and later ride on her back as they grow. Young monkeys learn social and foraging skills over several years. Black-handed
         Spider Monkeys have a long lifespan, typically 20–25 years, with longer lifespans possible in captivity.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of female black-handed spider monkeys.'''
   ),
   (
      'Capybara',
      'Hydrochoerus Hydrochaeris',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The capybara is part of the Mayan Temple Ruins exhibit, which is accessed be walking through the Tundra Trek. You should
         find the capybaras at the bottom of the waterfall.'''.replace( '\n', ' ' ),
      '''The capybara is a warm-weather animal, and is most reliably seen from May until October. The capybara has a viewing pattern
         similar to the flamingos, and may also be viewable outside on warmer March, April, and November days. On days that aren't
         too warm, the capybara may move between her indoor and outdoor habitats.'''.replace( '\n', ' ' ),
      '''The Capybara is the largest rodent in the world, with a heavy, barrel-shaped body, short legs, and a large, blunt head. Its
         coarse, reddish-brown to grey-brown fur helps it blend into wetland environments. Capybaras have small ears and eyes
         positioned high on the head, allowing them to see and hear while mostly submerged. Adults typically weigh 35–65 kg.'''
         .replace( '\n', ' ' ),
      '''Capybaras are native to Central and South America, where they inhabit wetlands, riverbanks, floodplains, and grassy areas
         near water. They are especially common in savannas and tropical forests with permanent water sources. Access to water is
         essential for feeding, thermoregulation, and predator avoidance.'''.replace( '\n', ' ' ),
      '''Capybaras are herbivorous grazers, feeding primarily on grasses, aquatic plants, and reeds. They have specialized teeth
         that grow continuously to compensate for wear from tough vegetation. At the zoo, their diet includes hay, grasses, leafy
         greens, vegetables, and formulated herbivore pellets to ensure proper nutrition.'''.replace( '\n', ' ' ),
      '''Highly social animals, capybaras live in groups that can range from a few individuals to over twenty. Groups typically
         consist of a dominant male, several females, offspring, and subordinate males. They communicate using a variety of
         vocalisations, including whistles, barks, and purrs. Capybaras are excellent swimmers and often rest or escape predators by
         submerging in water.'''.replace( '\n', ' ' ),
      '''Capybaras are well adapted to semi-aquatic life. Their partially webbed feet make them strong swimmers, while their ability
         to hold their breath for several minutes allows them to remain submerged. Eyes, ears, and nostrils positioned high on the
         head enable awareness while in water. Their digestive system efficiently processes fibrous plant material, and they
         practice coprophagy to maximise nutrient absorption.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs during the wet season. Females give birth to litters of 2–8 well-developed young after a
         gestation period of about 150 days. Unlike many rodents, capybara young are born fully furred and begin grazing within
         days. Capybaras generally live 8–10 years in the wild, with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a female capybara, Tootsie, who came from the San Diego Zoo.'''.replace( '\n', ' ' )
   ),

   # Americas Pavilion
   (
      'American Alligator',
      'Alligator Mississipiensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The American alligator can be found in the Costa Rica loop of the Americas Pavilion, through the doors across from the
         North American river otter viewing, and past the bugs.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The American Alligator is a large, heavily built reptile with a broad snout, powerful jaws, and thick, armour-like skin
         reinforced with bony plates called osteoderms. Adults are dark grey to black in colour, while juveniles display bright
         yellow banding that fades with age. Males are significantly larger than females, with large males exceeding 4 metres in
         length and weighing over 400 kg.'''.replace( '\n', ' ' ),
      '''American Alligators are native to the southeastern United States, inhabiting freshwater wetlands such as swamps, marshes,
         rivers, lakes, and slow-moving streams. They are especially associated with warm, shallow waters and often create “gator
         holes,” which provide refuge for other wildlife during dry periods.'''.replace( '\n', ' ' ),
      '''Alligators are opportunistic carnivores. Juveniles feed mainly on insects, crustaceans, and small fish, while adults
         consume fish, turtles, birds, mammals, and occasionally carrion. They ambush prey using stealth and explosive speed. In
         zoos, alligators are fed a controlled diet of meat and fish, with feeding schedules designed to mimic natural
         feast-and-famine cycles.'''.replace( '\n', ' ' ),
      '''American Alligators are generally solitary but may tolerate others in favourable habitats. They are most active during
         warmer months and spend much of their time basking to regulate body temperature. Vocal communication is more complex than
         often assumed; adults produce deep bellows during the breeding season, while juveniles emit high-pitched calls to signal
         distress.'''.replace( '\n', ' ' ),
      '''Alligators are superbly adapted to aquatic ambush hunting. Their eyes and nostrils are positioned on top of the head,
         allowing them to see and breathe while mostly submerged. A powerful tail provides propulsion in water, and a valve in the
         throat prevents water from entering the lungs while submerged. Their bite force is among the strongest of any living
         animal, enabling them to crush bone and shell.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring. Females build large nests of vegetation, where they lay 20–50 eggs. The temperature of the nest
         determines the sex of the hatchlings. Mothers guard the nest and assist hatchlings to the water after hatching. American
         Alligators grow slowly but steadily and can live 35–50 years, with some individuals exceeding 60 years in captivity.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'American Eel',
      'Anguilla Rostrata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The American eel can be found in a tank enclosure towards the end of the pavilion, across from the river otter and snapping
         turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The American Eel is a long, snake-like fish with a smooth, scaleless appearance and a continuous dorsal, caudal, and anal
         fin hat runs along much of its body. Colouration ranges from olive or brownish-yellow in juveniles to dark brown or nearly
         black in mature adults. Despite their resemblance to snakes, they are true fish with gills and fins.'''.replace( '\n', ' ' ),
      '''American Eels are found throughout eastern North America, from Greenland and eastern Canada to the Caribbean and northern
         South America. They inhabit a wide range of freshwater and coastal environments, including rivers, lakes, estuaries, and
         streams. Although they spend most of their lives in freshwater, they migrate to the open ocean to reproduce.'''
         .replace( '\n', ' ' ),
      '''American Eels are opportunistic carnivores. Their diet includes insects, crustaceans, molluscs, small fish, and worms. They
         forage mainly at night, using their strong sense of smell to locate prey. In zoos, they are fed a varied diet of aquatic
         invertebrates and fish to reflect their natural feeding habits.'''.replace( '\n', ' ' ),
      '''American Eels are primarily solitary and nocturnal. During the day, they often hide under rocks, logs, or sediment. They
         are strong swimmers and capable of moving over damp ground, allowing them to bypass obstacles such as small dams or
         barriers. Although generally secretive, they play an important ecological role as both predator and prey.'''
         .replace( '\n', ' ' ),
      '''These eels are highly adaptable and resilient. Their elongated bodies allow them to navigate tight spaces and burrow into
         soft substrates. A tough, mucus-coated skin helps prevent dehydration and protects against injury, enabling short overland
         movements. Their remarkable tolerance for a wide range of salinities allows them to thrive in both freshwater and marine
         environments.'''.replace( '\n', ' ' ),
      '''American Eels have one of the most extraordinary life cycles of any fish. Adults migrate thousands of kilometres from
         freshwater habitats to the Sargasso Sea to spawn, after which they die. Larvae drift back toward North America on ocean
         currents, transforming into glass eels before entering freshwater systems. They may spend 10–25 years growing before making
         the return journey to breed.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'American Lobster',
      'Homarus Americanus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The American lobster can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate
         wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The American Lobster is a large marine crustacean with a hard exoskeleton, long antennae, and five pairs of legs, including
         two large claws. One claw is typically larger and adapted for crushing, while the other is sharper and used for cutting.
         Colouration is usually dark greenish-brown with blue highlights, though rare colour variations can occur.'''
         .replace( '\n', ' ' ),
      '''American Lobsters are found along the Atlantic coast of North America, from Labrador to North Carolina. They inhabit cold,
         rocky ocean bottoms, usually at depths ranging from shallow coastal waters to several hundred metres. Lobsters seek shelter
         in crevices, burrows, and under rocks to avoid predators.'''.replace( '\n', ' ' ),
      '''Lobsters are omnivorous scavengers, feeding on fish, molluscs, crustaceans, worms, algae, and carrion. They play an
         important  in cleaning the ocean floor. At the zoo, lobsters are fed a controlled diet of seafood and plant matter to
         reflect their natural feeding habits.'''.replace( '\n', ' ' ),
      '''American Lobsters are mostly solitary and territorial, particularly when shelter is limited. They are primarily nocturnal,
         emerging from hiding places at night to forage. Lobsters communicate through body postures and chemical signals, especially
         during mating interactions.'''.replace( '\n', ' ' ),
      '''Lobsters are well adapted to life on the ocean floor. Their strong claws allow them to capture prey, defend territory, and
         manipulate objects. A hard exoskeleton provides protection, though it must be shed periodically as the lobster grows.
         Regeneration of lost limbs is possible through successive moults.'''.replace( '\n', ' ' ),
      '''Mating occurs after a female has moulted, when her shell is still soft. Females carry fertilised eggs on their swimmerets
         for up to a year before they hatch into free-swimming larvae. Lobsters grow slowly and may take several years to reach
         maturity. They can live 50 years or more, making them one of the longest-lived marine invertebrates.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Axolotl',
      'Ambystoma Mexicanum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The axolotl can be found in the Costa Rica loop of the Americas Pavilion, through the doors across from the North American
         river otter viewing, and past the bugs. The axolotl shares a habitat with the spotted turtles.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Axolotl is a neotenic salamander, meaning it retains its juvenile features throughout its life. It has a broad, flat
         head, lidless eyes, feathery external gills, and a long, laterally flattened tail for swimming. Colouration varies, with
         wild types being dark brown or black, while captive-bred individuals often appear leucistic (pale pink with red gills) or
         albino.'''.replace( '\n', ' ' ),
      '''Axolotls are native to high-altitude freshwater lakes and canals in the Valley of Mexico, including Xochimilco. They
         inhabit calm, vegetated waters, often hiding among submerged plants and rocks. They are critically endangered in the wild
         due to habitat loss, pollution, and invasive species.'''.replace( '\n', ' ' ),
      '''Axolotls are carnivorous, feeding on worms, small fish, insect larvae, and other aquatic invertebrates. They use suction
         feeding to engulf prey. In zoos, they are fed live or frozen worms, small crustaceans, and specialized amphibian pellets to
         ensure proper nutrition.'''.replace( '\n', ' ' ),
      '''Axolotls are largely solitary but tolerate others in captivity if space is sufficient. They are ambush predators, remaining
         still and striking quickly at passing prey. Communication is limited but may involve subtle movements or body postures,
         particularly during feeding or mating.'''.replace( '\n', ' ' ),
      '''Axolotls are remarkable for retaining gills and remaining fully aquatic throughout life. Their regenerative abilities are
         exceptional, capable of regrowing limbs, spinal cord, heart tissue, and parts of their brain. Their skin secretes
         protective mucus, and their lateral line system detects vibrations and movement in water, aiding hunting and navigation.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in spring and summer. Females lay hundreds of eggs on submerged plants or structures, which hatch in about
         two weeks. Juveniles resemble adults but are smaller. Lifespan in captivity is typically 10–15 years, although some
         individuals live longer with proper care. Axolotls rarely metamorphose naturally in the wild, making them unique among
         amphibians.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Black-Footed Ferret',
      'Mustela Nigripes',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black-footed ferret can be spotted in a small habitat beside the Eastern loggerhead shrike, just before the river
         otters.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Black-footed Ferret is a small, slender carnivorous mammal with a long body, short legs, and a bushy tail. Its fur is
         pale yellowish-tan with black markings on the feet, tip of the tail, and a distinctive mask across the eyes. Adults measure
         about 35–50 cm in body length, with tails adding another 15–20 cm. Their sharp teeth and claws are adapted for hunting.'''
         .replace( '\n', ' ' ),
      '''Black-footed Ferrets are native to the North American Great Plains, historically inhabiting grasslands and prairie
         ecosystems. They rely almost entirely on prairie dog colonies for food and shelter. Today, they are found primarily in
         protected reintroduction sites across the U.S. and Canada.'''.replace( '\n', ' ' ),
      '''These ferrets are obligate carnivores, feeding almost exclusively on prairie dogs. They also eat other small mammals,
         birds, and insects when available. At the zoo, they are fed a diet designed to replicate wild feeding patterns, including
         specially formulated carnivore diets and small prey items.'''.replace( '\n', ' ' ),
      '''Black-footed Ferrets are nocturnal and solitary, spending the day in burrows. They are highly specialised hunters, entering
         prairie dog burrows to locate and capture prey. Communication includes high-pitched squeaks, scent marking, and body
         postures. They exhibit territorial behaviour and maintain specific home ranges.'''.replace( '\n', ' ' ),
      '''These ferrets are superbly adapted to a burrowing, carnivorous lifestyle. Their slender bodies and short legs allow them to
         move easily through underground tunnels. Sharp teeth, retractable claws, and strong jaws aid in capturing and killing prey.
         Their keen sense of smell and hearing help detect prey in dark burrows.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late winter or early spring. Females give birth to 3–5 kits after a gestation period of about 42 days,
         typically within prairie dog burrows. Kits are born blind and helpless, opening their eyes at around 3 weeks. Black-footed
         Ferrets live 5–8 years in the wild, and often longer in captivity, with careful husbandry supporting breeding and
         population recovery.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Bark Scorpion',
      'Centruroides sculpturatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The bark scorpion can be found in the bugs hallway, located before the Costa Rican area through the doors across from
         the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The bark scorpion is a slender, light tan to yellowish scorpion with elongated pincers, a narrow segmented tail, and a
         distinct curved stinger. It is smaller and more delicate in build than many other scorpion species. Its body coloration helps
         it blend into desert bark, rocks, and sandy surfaces. Under ultraviolet light, it glows a bright blue-green due to compounds
         in its exoskeleton.'''.replace('\n', ' '),
      '''This species is native to arid desert and scrubland regions of the southwestern United States and northern Mexico. It is
         commonly found in Arizona, New Mexico, Nevada, and surrounding dry habitats. Unlike many scorpions, it is an excellent
         climber and often shelters under tree bark, in rock crevices, and inside dry human-made structures.'''.replace('\n', ' '),
      '''Bark scorpions feed on insects, spiders, small arthropods, and occasionally other scorpions. They are nocturnal hunters that
         use their pincers to seize prey before delivering venom through the stinger. In managed care, they are typically fed
         crickets,  mealworms, and other small live invertebrates.'''.replace('\n', ' '),
      '''These scorpions are primarily solitary and highly secretive. They spend the day hidden in narrow crevices and emerge at night
         to hunt. They rely on vibration sensing through specialized hairs on their legs to detect prey and danger. While generally
         non-aggressive, they will sting defensively if threatened.'''.replace('\n', ' '),
      '''The bark scorpion is highly adapted for desert survival. Its flattened body allows it to squeeze into tight bark and rock
         crevices, while specialized claws on its feet help it climb vertical surfaces. It has excellent sensory hairs for detecting
         movement and can survive long periods with minimal food and water. Its venom is potent and used both for defense and
         subduing prey.'''.replace('\n', ' '),
      '''Mating involves a courtship dance in which the male guides the female across the ground before depositing a spermatophore.
         Females give birth to live young rather than laying eggs. The young ride on the mother’s back until after their first molt.
         Bark scorpions may live several years in captivity, depending on care and environmental conditions.'''.replace('\n', ' '),
      None                                                           # Animals at the zoo
   ),
   (
      'Black-Widow Spider',
      'Latrodectus Mactans',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black-widow spider can be found in the bugs hallway, located before the Costa Rican area through the doors across from
         the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Black Widow Spiders are small but highly distinctive arachnids. Adult females are glossy black with a characteristic red
         hourglass marking on the underside of the abdomen. Males are smaller, brownish, and less conspicuous. Adult females
         typically measure 1.5–2 cm in body length, while males are about half that size.'''.replace( '\n', ' ' ),
      '''Black Widows are native to much of North America, including Canada, the United States, and Mexico. They inhabit dark,
         undisturbed areas such as rock crevices, hollow logs, sheds, and under debris. They favour warm microhabitats with low
         human disturbance.'''.replace( '\n', ' ' ),
      '''Black Widow Spiders are carnivorous, feeding primarily on insects, other arthropods, and occasionally small vertebrates
         that get trapped in their irregular, sticky webs. They inject venom to immobilize prey before consuming it. In zoo
         settings, they are fed small insects such as crickets and fruit flies to simulate natural feeding.'''.replace( '\n', ' ' ),
      '''Black Widows are generally solitary. Females maintain a territory centred around their web and rarely leave it. Mating is
         risky for males, who may be eaten by the female. Communication is largely vibrational, transmitted through the web to
         detect prey, predators, or mates.'''.replace( '\n', ' ' ),
      '''These spiders have potent neurotoxic venom used to subdue prey and deter predators. Their silk is strong and elastic, ideal
         for constructing irregular, tangled webs. Their small size and cryptic habits help them avoid detection, while their
         nocturnal activity reduces predation risk.'''.replace( '\n', ' ' ),
      '''Mating occurs in summer. Females lay multiple small egg sacs containing hundreds of eggs each, which hatch into tiny
         spiderlings that disperse by “ballooning” on silk threads. Black Widow Spiders live 1–3 years, depending on environmental
         conditions and predation, with females typically outliving males.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Blanding\'s Turtle',
      'Emydoidea Blandingii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Blanding's turtles can be spotted in a shared habitat with the painted turtles near the exit of the pavilion, and on
         the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Blanding’s Turtle is a medium-sized freshwater turtle with a domed, dark brown or black carapace and a distinctive bright
         yellow chin and throat. The plastron (underside) is yellow with dark blotches, and the turtle has relatively long necks and
         strong limbs for swimming and digging. Adults typically measure 20–27 cm in shell length.'''.replace( '\n', ' ' ),
      '''Blanding’s Turtles are native to southern Canada and the northern United States. They inhabit shallow wetlands, marshes,
         ponds, slow-moving rivers, and grassy wetlands with abundant aquatic vegetation and soft mud for burrowing. Clean water and
         undisturbed wetland habitat are essential for survival.'''.replace( '\n', ' ' ),
      '''Blanding’s Turtles are omnivorous, feeding on a mix of aquatic plants, algae, insects, small fish, crustaceans, and
         carrion. They forage in shallow water and along shorelines. At the zoo, they are provided a balanced diet that includes
         aquatic vegetation, insects, and specially formulated turtle pellets.'''.replace( '\n', ' ' ),
      '''These turtles are primarily solitary and spend much of their time submerged or buried in mud, surfacing to bask in the sun.
         They are most active during spring and summer and hibernate in mud at the bottom of wetlands during winter. Communication
         is limited, mostly involving visual and chemical cues.'''.replace( '\n', ' ' ),
      '''Blanding’s Turtles are well adapted to aquatic and semi-aquatic life. Their domed shells protect them from predators, while
         webbed feet allow efficient swimming. Long necks enable them to snap quickly at prey, and their yellow throat may serve as
         a warning or recognition signal. They hibernate for months in cold Canadian winters, reducing metabolic activity to survive
         freezing temperatures.'''.replace( '\n', ' ' ),
      '''Mating occurs in spring. Females lay 10–20 eggs in sandy or loamy soil near water. Hatchlings emerge after 70–90 days and
         are highly vulnerable to predators. Blanding’s Turtles are long-lived, commonly reaching 50 years, and can take 12–14 years
         to reach sexual maturity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Blue And Yellow Macaw',
      'Ara Ararauna',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The blue and yellow macaw can be spotted in the open aviary when you first enter the pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Blue-and-Gold Macaw is a large, striking parrot with bright blue upperparts, golden-yellow underparts, and a greenish
         forehead. It has a strong, curved black beak and white facial skin streaked with fine black lines. Adults measure about 85
         cm in length from head to tail and have a wingspan of up to 1.1 metres.'''.replace( '\n', ' ' ),
      '''Native to tropical South America, Blue-and-Gold Macaws inhabit lowland rainforests, swamp forests, and woodlands near
         rivers. They are often found in pairs or small flocks, favouring areas with tall trees suitable for nesting and foraging.'''
         .replace( '\n', ' ' ),
      '''These macaws are primarily frugivorous and granivorous, eating fruits, nuts, seeds, and occasionally leaves. They use their
         strong beaks to crack open hard nuts and extract seeds. In zoos, they are fed a carefully balanced diet of fresh fruits,
         vegetables, nuts, and formulated parrot pellets to maintain health and vibrant plumage.'''.replace( '\n', ' ' ),
      '''Blue-and-Gold Macaws are highly social and intelligent birds, forming strong pair bonds that often last for life. They
         communicate through loud squawks, whistles, and body language. In the wild, they are often seen flying in pairs or small
         flocks, performing acrobatic manoeuvres and engaging in mutual preening.'''.replace( '\n', ' ' ),
      '''These macaws are adapted for life in the forest canopy. Strong, curved beaks allow them to manipulate and crush seeds,
         while zygodactyl feet (two toes forward, two back) provide a strong grip on branches and food items. Their vibrant plumage
         aids in social signalling and species recognition within dense forests.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring and early summer. Pairs nest in tree cavities, laying 2–3 eggs, which both parents incubate for
         about 28 days. Chicks fledge after approximately 3 months but remain dependent on parents for several more months.
         Blue-and-Gold Macaws can live 50 years or more in the wild, and often longer in captivity.'''.replace( '\n', ' ' ),
      '''The macaws at the zoo are rescues, and were previously kept as pets, and thus their wings are clipped and they cannot fly.'''
         .replace( '\n', ' ' )
   ),
   (
      'Blue Poison Dart Frog',
      'Dendrobates Azureus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The blue poison dart frogs can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Blue Poison Dart Frog is a small, vividly coloured amphibian, measuring around 3–4 cm in length. Its skin is a
         brilliant sky-blue with irregular black spots or marbling. This striking colouration serves as a warning to predators of
         its toxicity. These frogs have slender bodies, long limbs, and sticky pads on their toes for climbing.'''
         .replace( '\n', ' ' ),
      '''Native to the rainforests of southern Suriname and adjacent northern Brazil, Blue Poison Dart Frogs inhabit humid, tropical
         forest floors near small streams and water pools. They thrive in areas with abundant leaf litter and vegetation, which
         provides shelter, hunting grounds, and breeding sites.'''.replace( '\n', ' ' ),
      '''These frogs are insectivorous, feeding on ants, termites, small beetles, and other tiny invertebrates. In the wild, their
         diet contributes to their toxicity, as alkaloids in their prey are incorporated into their skin. In captivity, they are fed
         fruit flies, springtails, and small invertebrates, with careful attention to nutrition.'''.replace( '\n', ' ' ),
      '''Blue Poison Dart Frogs are diurnal and territorial. Males call to establish territory and attract mates, using soft trills
         and chirps. They are generally solitary outside of breeding pairs, and their bright colours serve both as a warning and as
         a signal during social interactions.'''.replace( '\n', ' ' ),
      '''Their bright blue skin acts as aposematic colouring, warning predators of their potent skin toxins. They have highly
         sensitive toes for climbing on vegetation and leaf litter, and a strong jaw suited for capturing small, agile prey. Their
         small size and agility help them evade larger predators in dense rainforest habitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in tropical habitats. Males guard small clutches of 2–10 eggs laid on moist surfaces and often
         transport hatched tadpoles on their backs to small water bodies for development. Tadpoles metamorphose into juvenile frogs
         after several weeks. Blue Poison Dart Frogs typically live 5–10 years in the wild, with some living longer in captivity.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Boa Constrictor',
      'Boa Constrictor',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The boa constrictor can be found near the start of the pavilion, through the doors past the blue and gold macaws, and then
         on the left and around the corner past the Jamaican boa.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Boa Constrictor is a large, heavy-bodied snake with a distinctive pattern of dark saddles or bands along its tan,
         brown, or reddish-grey body. Adults typically reach 2–4 metres in length, though some may exceed 5 metres. Their heads are
         triangular, with heat-sensing pits along the upper lip to detect warm-blooded prey.'''.replace( '\n', ' ' ),
      '''Boa Constrictors are native to Central and South America, inhabiting tropical forests, savannas, and semi-arid regions.
         They prefer areas with dense vegetation, tree cover, or rocky crevices, and are often found near water sources.'''
         .replace( '\n', ' ' ),
      '''These snakes are carnivorous ambush predators, feeding on mammals, birds, and occasionally reptiles. They subdue prey by
         constriction, coiling around it and tightening until the prey suffocates. In zoos, Boa Constrictors are fed appropriately
         sized rodents or rabbits, with feeding schedules designed to mimic natural hunting intervals.'''.replace( '\n', ' ' ),
      '''Boa Constrictors are primarily solitary and mostly nocturnal, though some activity may occur during the day. They are
         excellent swimmers and climbers, using trees and shrubs for ambush hunting. Communication is limited to body posturing,
         tongue flicking, and scent signalling.'''.replace( '\n', ' ' ),
      '''Boa Constrictors are highly adapted for ambush predation. Their muscular, elongated bodies allow effective constriction of
         prey. Heat-sensing pits detect the body heat of mammals and birds, enabling precise strikes in low light. Camouflaged
         colouring provides concealment in leaf litter, branches, and forest floors.'''.replace( '\n', ' ' ),
      '''Mating occurs in the wet season. Females give birth to live young (viviparous), usually 10–65 per litter, depending on
         size. Juveniles are fully independent at birth and grow steadily. Boa Constrictors can live 20–30 years in captivity with
         proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Brazilian Giant Cockroach',
      'Blaberus Giganteus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Brazilian giant cockroach can be found in the bugs hallway, located before the Costa Rican area through the doors
         across from the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Brazilian Giant Cockroach is one of the largest cockroach species in the world, with adults reaching up to 9 cm in
         length. They have a flattened, oval body that is dark brown to black, with lighter markings on the thorax and wings. Their
         long antennae are highly sensitive, aiding navigation and environmental sensing.'''.replace( '\n', ' ' ),
      '''This species is native to the tropical rainforests of Central and South America, including Brazil, Guyana, and surrounding
         regions. They inhabit leaf litter, rotting logs, and other damp, sheltered areas on the forest floor. They are primarily
         nocturnal and avoid light and human disturbance.'''.replace( '\n', ' ' ),
      '''Brazilian Giant Cockroaches are detritivores, feeding on decaying plant material, fallen fruits, and leaf litter. This diet
         plays a critical role in nutrient recycling within rainforest ecosystems. In zoos, they are provided a varied diet of leafy
         greens, fruits, and specially formulated insect feed.'''.replace( '\n', ' ' ),
      '''These cockroaches are primarily solitary but may congregate in damp shelters. They are nocturnal, hiding during the day
         under debris or logs. They communicate through chemical signals (pheromones) and subtle body movements. Predators include
         birds, reptiles, and small mammals.'''.replace( '\n', ' ' ),
      '''Brazilian Giant Cockroaches are adapted to life on the rainforest floor. Their flattened bodies allow them to squeeze into
         narrow spaces to escape predators. Their strong legs and antennae aid in climbing and sensing the environment. The species’ 
         octurnal habits reduce predation risk, and their tough exoskeleton provides protection from physical damage.'''
         .replace( '\n', ' ' ),
      '''Females produce oothecae (egg cases) containing 30–40 eggs, which hatch in several weeks. Nymphs undergo multiple moults
         before reaching adulthood, a process that can take 6–12 months depending on environmental conditions. Lifespan ranges from
         1–2 years, though some individuals live longer in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Brazilian Salmon Pink Bird-Eating Tarantula',
      'Lasiodora Parahybana',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Brazilian salmon pink bird-eating tarantula can be found in the bugs hallway, located before the Costa Rican area
         through the doors across from the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''This tarantula is one of the largest spider species in the world. Adults have a leg span of up to 25 cm and a body length of
         around 8 cm. Their colour is a rich reddish-brown to salmon pink, particularly on the legs, with a dense covering of fine
         hairs that give a velvety appearance. Males are smaller and slimmer than females and have longer legs in proportion to their
         bodies.'''.replace( '\n', ' ' ),
      '''Native to the Atlantic forests of northeastern Brazil, the Brazilian Salmon Pink Bird-Eating Tarantula inhabits scrublands,
         forest edges, and burrows in leaf litter. They prefer humid environments with shelter from predators and suitable substrates
         for burrowing.'''.replace( '\n', ' ' ),
      '''These tarantulas are opportunistic predators, feeding on insects, small rodents, and other small animals. They ambush prey
         using their powerful fangs and inject venom to subdue it. In captivity, they are typically fed crickets, roaches, and
         occasional small vertebrates to mimic their natural diet.'''.replace( '\n', ' ' ),
      '''This species is solitary and primarily nocturnal. During the day, they retreat to burrows or hidden spaces, emerging at
         night to hunt. They use defensive behaviours such as raising their front legs, displaying fangs, or flicking urticating
         hairs to deter predators. Interaction with conspecifics is limited to mating.'''.replace( '\n', ' ' ),
      '''The Brazilian Salmon Pink Tarantula is adapted for a burrowing, predatory lifestyle. Its large size and strong fangs allow
         it to capture and subdue a wide range of prey. Dense body hairs serve both as sensory organs and as defensive urticating
         bristles. It can survive extended periods without food due to a slow metabolism and can tolerate brief drought conditions
         within burrows.'''.replace( '\n', ' ' ),
      '''Mating occurs after the male reaches maturity, usually at 3–4 years of age. Females lay egg sacs containing hundreds of
         eggs, which they guard carefully. Spiderlings disperse after hatching and undergo several moults before reaching adulthood.
         Females can live 15–20 years, while males typically live only 3–4 years after maturity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Butterfly Goodeid',
      'Ameca Splendens',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The butterfly goodeid can be found in an enclosure towards the exit of the pavilion, across from the river otter and
         snapping turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Butterfly Goodeid is a small freshwater fish, typically 6–8 cm in length. Males are brightly coloured, displaying
         golden-orange bodies with black markings along the dorsal and caudal fins, while females are more subdued in colour. They
         have a deep, laterally compressed body and rounded fins, giving them an elegant, butterfly-like appearance in motion.'''
         .replace( '\n', ' ' ),
      '''This species is native to the freshwater streams and lakes of western Mexico, particularly in the states of Jalisco and
         Michoacán. They inhabit shallow, slow-moving waters with abundant aquatic vegetation, which provides shelter and spawning
         sites.'''.replace( '\n', ' ' ),
      '''Butterfly Goodeids are omnivorous, feeding on algae, small invertebrates, and organic detritus in the wild. In captivity,
         they are provided a balanced diet of high-quality flake foods, small live or frozen invertebrates, and plant matter to
         ensure optimal health and colouration.'''.replace( '\n', ' ' ),
      '''These fish are social and typically found in small groups. Males establish territories during the breeding season,
         performing courtship displays that include fin spreading and body vibration to attract females. They are active swimmers
         and use vegetation for hiding and spawning.'''.replace( '\n', ' ' ),
      '''Butterfly Goodeids are adapted to shallow freshwater habitats. Their flattened bodies allow manoeuvrability among dense
         plants, and their bright colouration aids in species recognition and courtship. They are tolerant of variations in water
         conditions but require clean, well-oxygenated water to thrive.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in suitable conditions. Unlike many fish, Goodeids are livebearers: females give birth to fully
         formed young, usually 10–40 per brood. Juveniles are independent immediately and grow quickly, reaching sexual maturity in
         6–8 months. Lifespan is generally 3–5 years, with proper care in captivity sometimes extending this.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crested Tinamou',
      'Eudromia Elegans',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crested tinamou can be spotted in an enclosure near the entrance to the pavilion, just past the blue and gold macaws
         and straight ahead. The crested tinamou shares a habitat with the plush-crested jays.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Crested Tinamou is a medium-sized, ground-dwelling bird, about 35–40 cm in length. It has a grey-brown body with fine
         barring and spotting, a short tail, and a distinctive dark crest on the head. The bird’s legs are strong for running, and
         its wings are short and rounded, used mainly for short bursts of flight.'''.replace( '\n', ' ' ),
      '''Native to southern South America, particularly Argentina, Chile, and Uruguay, Crested Tinamous inhabit open grasslands,
         scrublands, and lightly wooded areas. They favour areas with dense ground vegetation for cover but require open spaces for
         foraging.'''.replace( '\n', ' ' ),
      '''Crested Tinamous are omnivorous, feeding on seeds, fruits, leaves, and small invertebrates. They forage by walking on the
         ground, scratching leaf litter, and pecking at soil and vegetation. In zoos, their diet includes grains, fresh fruits and
         vegetables, and insects to mimic natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''These birds are shy and primarily solitary or in pairs, although small groups may form outside the breeding season. They
         are excellent runners, using speed to evade predators. Flight is short and rapid, used mainly as a last resort. They
         communicate using soft calls and subtle displays, particularly during courtship.'''.replace( '\n', ' ' ),
      '''Crested Tinamous are well adapted for a ground-dwelling lifestyle. Camouflaged plumage conceals them in grasses and shrubs,
         while strong legs and feet allow fast running over uneven terrain. Their short wings reduce energy expenditure during short
         flights, and their keen eyesight helps detect predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the warmer months. Males incubate eggs from multiple females in a ground nest and care for the young
         after hatching. Clutches typically contain 6–10 eggs, which hatch after about 18–21 days. Crested Tinamous can live 8–10
         years in the wild, with longer lifespans in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Cuvier\'s Smooth-Fronted Caiman',
      'Paleosuchus Palpebrosus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Cuvier's smooth-fronted caimans can be found in the Costa Rica loop of the Americas Pavilion, just through the doors
         across from the North American river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Cuvier’s Smooth-Fronted Caiman is a small to medium-sized crocodilian, typically reaching 1.2–1.5 metres in length as
         adults. Its body is dark brown to black with a lighter underbelly, and its head is relatively smooth with a slightly
         upturned snout. Unlike larger caimans, it has a robust, compact build suited for dense forest streams.'''
         .replace( '\n', ' ' ),
      '''Native to northern and central South America, including Brazil, Colombia, Venezuela, and the Guianas, Cuvier’s
         Smooth-Fronted Caiman inhabits slow-moving rivers, streams, and freshwater wetlands within tropical forests. It prefers
         shaded, secluded areas with submerged logs, leaf litter, and dense vegetation for cover.'''.replace( '\n', ' ' ),
      '''This species is carnivorous, feeding on fish, amphibians, crustaceans, small mammals, and insects. They are opportunistic
         ambush predators, striking quickly and using powerful jaws to capture prey. In captivity, they are fed fish, small mammals,
         and invertebrates, carefully balanced for nutrition.'''.replace( '\n', ' ' ),
      '''Cuvier’s Smooth-Fronted Caimans are mostly solitary and secretive. They are primarily nocturnal hunters but may bask in
         shaded areas during the day. They communicate through vocalisations, body postures, and water ripples, especially during
         breeding or territorial disputes.'''.replace( '\n', ' ' ),
      '''These caimans are adapted for life in forested freshwater habitats. Their compact, heavily armored bodies allow movement
         through narrow waterways and thick vegetation. Strong tails provide propulsion in water, while sensory pits detect
         vibrations from potential prey. Their smooth snout aids in capturing small, agile prey in tight spaces.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs during the wet season. Females build mound nests of vegetation and soil near water and lay 15–25 eggs. They
         guard the nest and may assist hatchlings to water. Hatchlings are independent but vulnerable to predation. Cuvier’s
         Smooth-Fronted Caimans can live 20–30 years, with slower growth compared to larger caimans.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Desert Grassland Whiptail',
      'Aspidoscelis Uniparens',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The desert grassland whiptail can be found in an enclosure towards the exit of the pavilion, across from the river otter
         and snapping turtle underwater viewings. The desert grassland whiptail shares a habitat with the San-Esteban Island
         chuckwalla'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Desert Grassland Whiptail is a slender, fast-moving lizard, typically 15–25 cm long, including the tail, which is about
         twice the body length. Its body is tan to light brown with darker longitudinal stripes running from head to tail. Limbs are
         long and agile, suited for rapid movement across open terrain.'''.replace( '\n', ' ' ),
      '''Native to the southwestern United States and northern Mexico, this species inhabits desert grasslands, scrublands, and
         semi-arid regions. It prefers open areas with sandy soil and sparse vegetation that allow quick movement and easy
         sunbathing for thermoregulation.'''.replace( '\n', ' ' ),
      '''Desert Grassland Whiptails are primarily insectivorous, feeding on ants, beetles, spiders, and other small arthropods. They
         hunt actively during the day, using speed and keen eyesight to capture prey. In zoos, they are fed crickets, mealworms, and
         other insects to replicate their natural diet.'''.replace( '\n', ' ' ),
      '''This species is diurnal and highly active, often seen sprinting across open ground. It is mostly solitary but may interact
         during the breeding season. Its speed is its primary defence, allowing it to escape predators quickly. They are capable of
         shedding their tail (autotomy) if threatened, which later regenerates.'''.replace( '\n', ' ' ),
      '''The Desert Grassland Whiptail has several adaptations for survival in arid environments. Its long, powerful legs allow
         rapid sprints to catch prey and avoid predators. Its striped pattern provides camouflage among grasses and sandy soil.
         Uniquely, many populations are all-female and reproduce through parthenogenesis, producing genetically identical offspring
         without males.'''.replace( '\n', ' ' ),
      '''Reproduction occurs via parthenogenesis in most populations, though mating behaviours may still occur as part of courtship
         rituals. Females lay 2–8 eggs per clutch, which hatch after 60–90 days depending on temperature. Hatchlings are fully
         independent. Lifespan in the wild is typically 4–6 years, though they may live longer in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Dyeing Poison Dart Frog',
      'Dendrobates Tinctorius',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The blue poison dart frogs can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Dyeing Poison Dart Frog is a medium-sized, vibrantly coloured amphibian, measuring 3–5 cm in length. Colour patterns
         vary widely, but most have a bright base colour (yellow, blue, or orange) with contrasting black spots or stripes. The
         species’ skin is smooth and highly toxic in the wild, serving as a warning to predators.'''.replace( '\n', ' ' ),
      '''Native to the tropical rainforests of Suriname, French Guiana, and northern Brazil, these frogs inhabit the forest floor
         near streams and shallow pools. They thrive in humid, shaded areas with abundant leaf litter and moss, which provide
         shelter, breeding sites, and hunting grounds.'''.replace( '\n', ' ' ),
      '''Dyeing Poison Dart Frogs are insectivorous, feeding primarily on ants, termites, mites, and small arthropods. In the wild,
         their diet contributes to the production of skin toxins. In captivity, they are fed fruit flies, springtails, and small
         invertebrates, ensuring proper nutrition without producing toxic skin secretions.'''.replace( '\n', ' ' ),
      '''These frogs are diurnal and territorial. Males establish and defend territories through calls and displays, often near
         water or breeding sites. They exhibit complex courtship behaviours, including following, tapping, and vocalisations. Social
         interaction outside breeding is limited.'''.replace( '\n', ' ' ),
      '''Bright aposematic colouration warns predators of their toxicity. They have sticky toe pads for climbing vegetation and
         leaves, and sensitive skin that can absorb moisture and chemicals from their environment. Their small size and agility help
         them evade predators and capture tiny prey efficiently.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in humid rainforest conditions. Females lay 10–30 eggs on moist surfaces, which are guarded by
         the male. Once hatched, males often carry tadpoles to small water pools or bromeliads for further development. Tadpoles
         metamorphose into juveniles after several weeks. Lifespan is typically 5–8 years, longer in captivity with optimal care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Eastern Loggerhead Shrike',
      'Lanius Ludovicianus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Eastern loggerhead shrike ferret can be spotted in a small habitat beside the black-fotted ferret and ust before the
         river otters.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Eastern Loggerhead Shrike is a small to medium-sized songbird, measuring about 22–26 cm in length with a wingspan of
         30–35 cm. It has grey upperparts, a white underside, black wings with white patches, and a distinctive black mask across
         the eyes. Its hooked beak is strong and curved, ideal for catching and killing prey.'''.replace( '\n', ' ' ),
      '''This subspecies of Loggerhead Shrike inhabits open grasslands, agricultural fields, and savannas across eastern North
         America. They favour areas with scattered shrubs or perches for hunting, and open ground for spotting prey.'''
         .replace( '\n', ' ' ),
      '''Eastern Loggerhead Shrikes are carnivorous, feeding on insects, small birds, rodents, and reptiles. They are known for
         their unique behaviour of impaling prey on thorns, barbed wire, or sharp branches to tear it into manageable pieces. In
         zoos, they are fed insects, small rodents, and other appropriately sized prey to replicate natural feeding.'''
         .replace( '\n', ' ' ),
      '''Shrikes are solitary hunters, perching silently to spot prey before swooping down for capture. They are territorial and may
         use vocal calls and displays to defend their territory. Social interaction outside breeding is limited. Their striking
         black mask and vocalisations are key elements of communication.'''.replace( '\n', ' ' ),
      '''Loggerhead Shrikes are uniquely adapted for predation among songbirds. Their hooked beak allows them to kill prey
         efficiently, and their impaling behaviour provides a form of “larder” to store food. Keen eyesight helps detect small prey
         from a distance, and strong wings enable rapid, precise strikes.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring. Females lay 4–7 eggs in well-hidden cup-shaped nests in shrubs or small trees. Both parents
         participate in feeding chicks, which fledge after about 2–3 weeks. Loggerhead Shrikes typically live 9–12 years in the
         wild, with slightly longer lifespans in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Eastern Lubber Grasshopper',
      'Romalea Microptera',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Eastern lubber grasshopper can be found in the bugs hallway, located before the Costa Rican area through the doors
         across from the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Eastern Lubber Grasshopper is a large, striking grasshopper species, measuring 6–8 cm in length. Adults are typically
         black with bright yellow, orange, or red markings along the thorax and wings. Their wings are short and underdeveloped,
         meaning they cannot fly, but they have strong hind legs for hopping. Nymphs are smaller and often display red and black
         warning patterns.'''.replace( '\n', ' ' ),
      '''Native to the southeastern United States, particularly Florida, Georgia, and Louisiana, Eastern Lubber Grasshoppers inhabit
         grasslands, open woodlands, and garden areas. They prefer sunny, warm environments with abundant vegetation for feeding and
         hiding.'''.replace( '\n', ' ' ),
      '''Eastern Lubber Grasshoppers are primarily herbivorous, feeding on a wide variety of plants, including grasses, weeds, and
         garden plants. Their strong mandibles allow them to chew tough plant material. In zoos, they are provided with leafy greens,
         vegetables, and safe plants to replicate their natural diet.'''.replace( '\n', ' ' ),
      '''These grasshoppers are diurnal and relatively slow-moving compared to other grasshopper species. They rely on their bright
         warning colours and toxic secretions for defence rather than speed. They are mostly solitary but may be found in small
         groups when food is abundant. Males exhibit courtship displays to attract females.'''.replace( '\n', ' ' ),
      '''Eastern Lubber Grasshoppers have aposematic (warning) colouration to deter predators, and they can secrete toxic compounds
         from their thoracic glands when threatened. Their strong hind legs allow them to hop away from danger, and their robust
         mandibles are adapted for consuming tough plant material. Being flightless reduces energy expenditure and suits their
         ground-dwelling lifestyle.'''.replace( '\n', ' ' ),
      '''Breeding occurs in summer. Females lay 50–200 eggs in soil or under debris, which hatch in 2–4 weeks depending on
         temperature. Nymphs undergo several moults before reaching adulthood in about 2–3 months. Eastern Lubber Grasshoppers
         typically live 6–12 months, completing one generation per year.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Eyelash Viper',
      'Bothriechis Schlegelii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The eyelash viper can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Eyelash Viper is a small to medium-sized, arboreal venomous snake, usually 55–82 cm long. It is named for the
         distinctive horn-like scales above its eyes, giving it a “lash” appearance. Colouration is highly variable, including
         yellow, green, red, brown, or patterned morphs, which provide camouflage in foliage. Its slender body and prehensile tail
         aid in climbing and grasping branches.'''.replace( '\n', ' ' ),
      '''Native to Central and South America, including southern Mexico, Costa Rica, Panama, and northern South America, Eyelash
         Vipers inhabit tropical rainforests and cloud forests. They favour trees, shrubs, and dense vegetation near water sources,
         where they can hunt effectively while remaining hidden.'''.replace( '\n', ' ' ),
      '''Eyelash Vipers are ambush predators, feeding primarily on small birds, frogs, lizards, and occasionally rodents. They
         strike rapidly and inject hemotoxic venom to immobilize prey. In captivity, they are typically fed appropriately sized mice
         or small amphibians, depending on the individual’s size.'''.replace( '\n', ' ' ),
      '''These vipers are solitary and highly territorial. They are primarily nocturnal but may be active during the day in shaded
         areas. They rely on camouflage and remaining motionless to avoid predators. Communication is limited to body postures and
         threat displays, such as coiling and striking.'''.replace( '\n', ' ' ),
      '''Eyelash Vipers are well adapted for arboreal life. Their prehensile tails allow secure climbing, and their triangular head
         houses venomous fangs for efficient predation. Their variable colouration provides exceptional camouflage among leaves and
         branches, while heat-sensing pits help detect warm-blooded prey in low light conditions.'''.replace( '\n', ' ' ),
      '''Mating occurs in the wet season. Eyelash Vipers are ovoviviparous, giving birth to live young, typically 10–25 per brood.
         Newborns are independent at birth and are capable hunters. Lifespan in the wild is generally 10–15 years, with longer
         lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Ferocious Water Bug',
      'Lethocerus Americanus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Ferocious water bug can be found in the bugs hallway, located before the Costa Rican area through the doors across from
         the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Ferocious Water Bug is a large aquatic insect, often reaching 6–7 cm in length. Its body is flat, elongated, and dark
         brown, with raptorial front legs adapted for grasping prey. The insect has short antennae and prominent compound eyes,
         giving it excellent vision for hunting in water.'''.replace( '\n', ' ' ),
      '''Native to freshwater ponds, lakes, and slow-moving streams across North America, particularly in Canada and the United
         States, these insects prefer calm, vegetated waters. They are typically found near the surface or lurking among submerged
         plants, where they can ambush prey.'''.replace( '\n', ' ' ),
      '''Ferocious Water Bugs are predatory and feed on a variety of aquatic organisms, including small fish, amphibians, tadpoles,
         and insect larvae. They capture prey with their strong front legs and inject digestive enzymes via a piercing beak,
         immobilizing and externally digesting their food. In captivity, they are fed small fish and aquatic invertebrates.'''
         .replace( '\n', ' ' ),
      '''These insects are solitary ambush predators, spending most of their time motionless underwater, waiting for prey. They can
         fly short distances to colonize new water bodies. When threatened, they may bite defensively, delivering a painful, though
         non-lethal, sting to humans. Interaction with conspecifics is minimal outside mating.'''.replace( '\n', ' ' ),
      '''Ferocious Water Bugs are adapted for aquatic hunting. Their flattened bodies and hydrofuge hairs allow them to remain
         submerged while breathing through a short siphon at the water surface. Their raptorial front legs and powerful beak allow
         them to seize and digest prey efficiently. Nocturnal activity reduces predation risk.'''.replace( '\n', ' ' ),
      '''Mating occurs in late spring to summer. Females lay eggs on emergent vegetation above the water, which males may guard in
         some species. Nymphs undergo several moults before reaching adulthood, which takes about a year. Lifespan ranges from 1–2
         years, depending on environmental conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Golden Lion Tamarin',
      'Leontopithecus Rosalia',
      14,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The golden lion tamarins have an indoor viewable habitat, and an outdoor viewable habitat. Theeir outdoor viewing is
         located right near the David C. Onley Boardwalk, which connects the Americas to Africa. If you don't see the monkeys in any
         of these enclosures, head inside the Americas Pavilion and you can spot them inside in the primate wing, just past the
         macaws.'''.replace( '\n', ' ' ),
      '''Golden lion tamarins are a species native to the tropical rainforests of South America, and can only be outside during the
         warmest months of the year. The rest of the time, they can be found excluisvely in their indoor habitat.'''
         .replace( '\n', ' ' ),
      '''The Golden Lion Tamarin is a small primate, about 20–30 cm in body length, with a striking mane of golden-orange fur
         surrounding its face. Its tail is long, approximately 30–40 cm, and covered in the same golden fur. Their expressive faces
         and bright colouration make them easily recognisable.'''.replace( '\n', ' ' ),
      '''Native to the Atlantic coastal forests of Brazil, Golden Lion Tamarins inhabit tropical lowland and secondary forests. They
         prefer areas with dense vegetation, vines, and tree hollows for foraging, nesting, and protection from predators.'''
         .replace( '\n', ' ' ),
      '''These tamarins are omnivorous, feeding on fruits, nectar, flowers, insects, and small vertebrates. Their long fingers help
         them extract insects from crevices and manipulate small food items. In zoos, their diet is carefully balanced with fruits,
         vegetables, protein sources, and enrichment items to stimulate natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Golden Lion Tamarins are highly social, living in family groups of 2–8 individuals. They communicate through vocalisations,
         facial expressions, and scent-marking. Grooming is an important social activity, strengthening bonds and reducing tension
         within the group.'''.replace( '\n', ' ' ),
      '''Golden Lion Tamarins are arboreal and well adapted to life in the forest canopy. Their long, claw-like nails allow them to
         cling to tree trunks and branches, and their agile bodies facilitate jumping between branches. Bright fur helps family
         members recognise each other and may play a role in territorial signalling.'''.replace( '\n', ' ' ),
      '''Breeding occurs once or twice a year. Females typically give birth to twins, with males playing a crucial role in carrying
         and caring for infants. Juveniles remain in the family group until maturity. Lifespan in the wild is about 10–15 years,
         while in captivity they can live up to 20 years.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   ( # Also in Kids Zoo
      'Great Horned Owl',
      'Bubo Virginianus',
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The great horned owl can be seen in the Americas, and in the Kids Zoo. In the Americas, the owl can be seen just outside
         the pavilion, to the right of the doors.'''.replace( '\n', ' ' ),
      '''The great horned owl is a cold-tolerant species, and can stay outside year-round. The owl in the Americas can be seen all
         year, while the one in the Kids Zoo can be seen when the Kids Zoo is open.'''.replace( '\n', ' ' ),
      '''The Great Horned Owl is a large raptor, measuring 45–63 cm in length with a wingspan of 101–145 cm. It has a mottled brown
         and grey body, a white throat patch, and prominent “ear” tufts of feathers that resemble horns. Its powerful talons and
         hooked beak make it an apex predator in North American forests and grasslands.'''.replace( '\n', ' ' ),
      '''This species is widespread across North and South America, inhabiting forests, deserts, urban areas, and open fields. It is
         highly adaptable, nesting in tree cavities, cliffs, or even abandoned buildings.'''.replace( '\n', ' ' ),
      '''Great Horned Owls are carnivorous and opportunistic hunters, preying on mammals such as rabbits, rodents, skunks, and
         raccoons, as well as birds, reptiles, and amphibians. They hunt primarily at night using exceptional vision and hearing.
         In captivity, they are fed a diet of appropriately sized mammals and birds to meet nutritional needs.'''.replace( '\n', ' ' ),
      '''These owls are solitary and territorial. They communicate through deep hooting calls, especially during the breeding 
         eason, and use visual displays to deter intruders. They are mostly nocturnal but may occasionally be active during daylight
         hours. Mating pairs often remain together year-round.'''.replace( '\n', ' ' ),
      '''Great Horned Owls are adapted for nocturnal predation. Their silent flight is enabled by specially structured feathers,
         allowing stealthy approaches to prey. Forward-facing eyes provide excellent binocular vision, while asymmetrical ears give
         acute directional hearing. Strong talons and a powerful beak allow them to capture and kill prey efficiently.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in late winter. Females lay 2–3 eggs in nests made in trees, cliffs, or old nests of other large birds.
         Chicks fledge in 6–7 weeks but remain dependent on parents for several months. Lifespan in the wild is typically 13 years,
         though some individuals live over 20 years in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Green And Black Poison Dart Frog',
      'Dendrobates Auratus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green and black poison dart frog can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Green and Black Poison Dart Frog is a small, vibrantly coloured amphibian, typically 3–4 cm long. Its body is black
         with striking green, blue, or turquoise irregular spots or bands, giving it a marbled appearance. Its smooth skin contains
         potent toxins in the wild, serving as a warning to predators.'''.replace( '\n', ' ' ),
      '''Native to Central and South America, especially Costa Rica, Panama, and northern Colombia, these frogs inhabit humid
         lowland rainforests, forest edges, and shaded areas near streams and pools. They prefer dense vegetation that provides
         shelter and breeding sites.'''.replace( '\n', ' ' ),
      '''Green and Black Poison Dart Frogs are insectivorous, feeding on ants, termites, mites, and small invertebrates. In
         captivity, they are provided small insects such as fruit flies, springtails, and pinhead crickets to replicate their
         natural diet and maintain vibrant colouration.'''.replace( '\n', ' ' ),
      '''These frogs are diurnal and territorial. Males call to establish territory and attract females, while both sexes engage in
         limited interactions outside of breeding. They are active foragers, moving among leaf litter and low vegetation to find
         prey.'''.replace( '\n', ' ' ),
      '''Bright aposematic colouration warns predators of their toxicity. They have adhesive toe pads for climbing leaves, moss, and
         stems, and sensitive skin that absorbs moisture and environmental cues. Their small size and agility allow efficient
         hunting of tiny arthropods and rapid evasion from predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in suitable humid environments. Females lay 5–15 eggs on moist surfaces, often under leaves.
         Males transport tadpoles to small pools or bromeliad axils for development. Tadpoles metamorphose into juvenile frogs
         within several weeks. Lifespan is generally 5–8 years, with longer lifespans in captivity under optimal care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Green Surf Anemone',
      'Anthopleura Xanthogrammica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green surf anemone can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate
         wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Green Surf Anemone is a large, striking sea anemone with a broad, flattened body and numerous short tentacles 
         surrounding a central mouth. When submerged, it appears vivid green due to symbiotic algae within its tissues; when exposed
         at low tide, it often contracts into a dense, rounded mass to retain moisture. Individuals can reach up to 30 cm in
         diameter.'''.replace( '\n', ' ' ),
      '''This species is found along the Pacific coast of North America, from Alaska to Baja California. It inhabits rocky
         intertidal zones, tide pools, and wave-exposed shorelines where it firmly attaches to rocks. Green Surf Anemones thrive in
         areas with strong water movement and changing tidal conditions.'''.replace( '\n', ' ' ),
      '''Green Surf Anemones are opportunistic carnivores. They capture small fish, mussels, sea urchins, and crustaceans using
         venomous tentacles. In addition to active feeding, they receive nutrients from symbiotic algae (zooxanthellae) living in
         their tissues, which photosynthesize and provide energy.'''.replace( '\n', ' ' ),
      '''Although stationary, these anemones are highly responsive to their environment. They retract their tentacles when
         threatened or exposed to air and can slowly relocate if conditions become unfavourable. They play an important ecological
         role in intertidal communities by regulating small invertebrate populations and providing shelter for commensal species'''
         .replace( '\n', ' ' ),
      '''Symbiotic algae give the anemone its green colour and supplement its diet through photosynthesis. Strong adhesive foot
         muscles allow it to withstand powerful waves. Venomous stinging cells (nematocysts) in the tentacles immobilize prey and
         deter predators, while the ability to contract tightly helps prevent dehydration during low tide.'''.replace( '\n', ' ' ),
      '''Green Surf Anemones reproduce both sexually and asexually. Sexual reproduction involves the release of eggs and sperm into
         the water, producing free-swimming larvae. Asexual reproduction occurs through fission, allowing rapid population growth.
         Individuals can live for several decades, making them among the longer-lived invertebrates.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Green-Winged Macaw',
      'Ara Chloropterus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green-winged macaws can be found near the beginning of the pavilion, just through the doors past the blue and gold
         macaws and on the right.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Green-winged Macaw is one of the largest and most vividly coloured parrots in the world. It has a bright red body,
         emerald green wings with blue tips, and a long red-and-blue tail. The face is bare and white, marked with fine red feather
         lines, and the powerful black beak is adapted for cracking hard nuts and seeds.'''.replace( '\n', ' ' ),
      '''This species is native to the tropical forests of Central and South America, including the Amazon Basin. It inhabits
         lowland rainforests, river edges, swamp forests, and palm groves, where tall trees provide nesting sites and abundant food.'''
         .replace( '\n', ' ' ),
      '''Green-winged Macaws are primarily herbivorous, feeding on fruits, nuts, seeds, berries, and leaves. They are especially
         known for eating clay from riverbanks, which helps neutralize toxins found in some unripe fruits and provides essential
         minerals. Their strong beaks allow them to access food sources unavailable to many other animals.'''.replace( '\n', ' ' ),
      '''These macaws are highly social and intelligent birds. They are usually seen in pairs or small family groups and form strong
         lifelong pair bonds. Green-winged Macaws are vocal, using loud calls to communicate over long distances, and they display
         playful, curious behaviour both in the wild and in captivity.'''.replace( '\n', ' ' ),
      '''A massive, hooked beak allows them to crush extremely hard nuts and defend themselves. Zygodactyl feet (two toes facing
         forward and two backward) provide excellent grip for climbing and handling food. Their bright colouration aids in species
         recognition within dense forest environments, while their intelligence supports complex social interactions and
         problem-solving.'''.replace( '\n', ' ' ),
      '''Breeding pairs nest in large tree cavities high above the forest floor. Females typically lay two to three eggs, which
         hatch after about a month. Chicks are cared for by both parents and remain dependent for several months. Green-winged
         Macaws can live over 50 years, especially under human care.'''.replace( '\n', ' ' ),
      '''The macaws at the zoo are rescues, and were previously kept as pets, and thus their wings are clipped and they cannot fly.'''
         .replace( '\n', ' ' )
   ),
   (
      'Guatemalan Beaded Lizard',
      'Heloderma Horridum Charlesbogerti',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Guatemalan beaded lizards can be found in an enclosure towards the exit of the pavilion, across from the river otter
         and snapping turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Guatemalan beaded lizard is a large, heavy-bodied reptile with a black base colour patterned with yellow to orange
         bead-like scales. These raised scales give the skin a rough, armour-like texture. It has a broad head, small eyes, strong
         jaws, and a thick tail used for fat storage. Adults typically reach 70–90 cm in length.'''.replace( '\n', ' ' ),
      '''This subspecies is endemic to eastern Guatemala, where it inhabits dry tropical forests, thorn scrub, and rocky hillsides.
         It relies on burrows, rock crevices, and fallen logs for shelter, spending much of its time underground to avoid extreme
         heat and dehydration.'''.replace( '\n', ' ' ),
      '''Guatemalan beaded lizards are carnivorous and feed primarily on eggs of birds and reptiles, as well as small mammals, birds,
         and occasionally other reptiles. They have a slow metabolism and can go long periods without feeding, relying on fat
         reserves stored in their tails. Prey is located using a highly developed sense of smell.'''.replace( '\n', ' ' ),
      '''This species is solitary and secretive, emerging mainly during cooler evening or nighttime hours. Individuals are generally
         non-aggressive but will stand their ground if threatened, using hissing and defensive postures. Social interactions are
         limited to the breeding season.'''.replace( '\n', ' ' ),
      '''The beaded lizard’s thick, osteoderm-covered skin provides protection from predators. A slow metabolism allows survival in
         harsh, seasonal environments with limited food. Its strong limbs and claws aid in digging burrows and accessing nests,
         while a venomous bite serves as an effective defence against predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season. Females lay several eggs in underground nests, where they incubate for many months.
         Hatchlings emerge during periods of higher food availability and are independent from birth. This species is long-lived,
         with individuals capable of living 20–30 years or more.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Jamaican Boa',
      'Chilabothrus Subflavus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Jamaican boa can be found in an enclosure near the start of the pavilion, through the door at the blue and gold macaws
         and on the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Jamaican Boa is a large, muscular snake with a yellowish-brown to olive body marked by dark blotches along its back.
         Its colouration varies with age, with juveniles often showing stronger contrast than adults. The head is broad and distinct
         from the neck, and the eyes are relatively large, reflecting its partially arboreal lifestyle. Adults typically reach
         1.5–2.3 metres in length.'''.replace( '\n', ' ' ),
      '''This species is endemic to Jamaica, where it inhabits a variety of environments including dry forests, moist limestone
         forests, wetlands, and agricultural areas. Jamaican Boas are often found in trees, caves, and rocky outcrops, as well as
         near human settlements where prey is abundant.'''.replace( '\n', ' ' ),
      '''Jamaican Boas are carnivorous constrictors that feed on birds, bats, rodents, and occasionally lizards. They ambush prey
         and kill by constriction. Young boas primarily eat small lizards and frogs before transitioning to larger prey as they
         grow. In zoos, they are fed appropriately sized rodents and birds.'''.replace( '\n', ' ' ),
      '''This species is mostly solitary and primarily nocturnal. It is an adept climber and often hunts in trees or near cave
         entrances, especially where bats roost. Jamaican Boas are generally calm but will defend themselves if threatened. Social 
         nteraction occurs mainly during the breeding season.'''.replace( '\n', ' ' ),
      '''The Jamaican Boa’s muscular body allows powerful constriction of prey, while heat-sensing pits along the lips help detect
         warm-blooded animals in low light. Its variable colouration provides camouflage in forested and rocky habitats. Strong
         climbing ability enables access to arboreal prey and roosting sites.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally, with females giving birth to live young rather than laying eggs. Litters typically contain 5–20
         offspring. Juveniles are independent at birth and grow steadily over several years. Jamaican Boas can live 20–30 years,
         particularly under human care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Leather Sea Star',
      'Dermasterias Imbricata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The leather sea star can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate
         wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Leather Sea Star is a large, soft-bodied sea star with five broad, tapering arms and a smooth, leathery surface rather
         than the spiny texture typical of many sea stars. Colouration ranges from orange and brown to purple, pink, or mottled
         patterns. Adults commonly reach 25–30 cm across.'''.replace( '\n', ' ' ),
      '''This species is found along the Pacific coast of North America, from Alaska to California. It inhabits rocky subtidal
         zones, kelp forests, and tide pools, usually at depths from the low intertidal to deeper coastal waters. Leather Sea Stars
         prefer areas with strong water movement and abundant prey.'''.replace( '\n', ' ' ),
      '''Leather Sea Stars are carnivorous and feed on sea anemones, sponges, bryozoans, tunicates, and occasionally other
         echinoderms. They feed by everting their stomach over prey and digesting it externally. In aquarium settings, they are
         provided with suitable invertebrate foods to match their natural diet.'''.replace( '\n', ' ' ),
      '''This species is slow-moving and generally solitary, spending much of its time crawling along rocks and kelp-covered
         surfaces. It is most active during periods of strong water flow, which aids feeding. Interactions with other sea stars are
         minimal, except when competing for food resources.'''.replace( '\n', ' ' ),
      '''The Leather Sea Star’s flexible, leathery body allows it to conform to uneven surfaces and resist damage from wave action.
         Tube feet enable strong attachment to rocks, preventing dislodgement by currents. Chemical defences in its tissues help
         deter predators, including fish and sea otters.'''.replace( '\n', ' ' ),
      '''Reproduction occurs through external fertilization, with eggs and sperm released into the water column. Larvae are
         planktonic before settling and developing into juvenile sea stars. Individuals grow slowly and may live 20 years or more,
         depending on environmental conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Lemur Leaf Frog',
      'Agalychnis Phyllomedusa',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The lemur leaf frog can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Lemur Leaf Frog is a small to medium-sized tree frog with smooth skin and a slender body. It is typically light green
         with subtle yellow or cream markings on the flanks and limbs. Large eyes and long legs give it a delicate appearance.
         Adults usually reach 4–6 cm in length, with females slightly larger than males.'''.replace( '\n', ' ' ),
      '''This species is native to Central America, primarily Costa Rica and Panama. It inhabits humid lowland and foothill
         rainforests, where it lives high in the canopy near streams and temporary pools used for breeding. It depends on dense
         vegetation and high humidity to survive.'''.replace( '\n', ' ' ),
      '''Lemur Leaf Frogs are insectivorous, feeding on small insects such as crickets, flies, moths, and beetles. They hunt at
         night, using their agility and vision to capture prey among leaves and branches. In zoos, they are fed appropriately sized
         insects dusted with vitamins and minerals.'''.replace( '\n', ' ' ),
      '''This frog is primarily nocturnal and arboreal, spending daylight hours resting on leaves where it blends in with its
         surroundings. It is generally solitary outside the breeding season. Males vocalize softly to attract females, often from
         elevated perches near water.'''.replace( '\n', ' ' ),
      '''Lemur Leaf Frogs have excellent camouflage, with green colouration that mimics surrounding foliage. Adhesive toe pads allow
         secure climbing on smooth leaves and branches. Their nocturnal habits reduce exposure to predators and daytime heat, while
         sensitive skin helps maintain hydration in humid environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season. Females lay clusters of eggs on leaves overhanging water. When the eggs hatch,
         tadpoles drop into the water below to continue development. Metamorphosis occurs over several weeks. Lifespan is typically
         5–8 years, with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Longnose Dace',
      'Rhinichthys Cataractae',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The longnose dace can be found in an enclosure towards the exit of the pavilion, across from the river otter and snapping
         turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Longnose Dace is a small, slender freshwater fish with a long, pointed snout and a mottled brown, grey, or olive body
         that blends well with rocky streambeds. Dark speckling and faint lateral markings are common. Adults typically measure 7–12
         cm in length. Males may develop brighter colouration and small tubercles during the breeding season.'''.replace( '\n', ' ' ),
      '''This species is widespread across northern North America, including much of Canada and the northern United States. It
         inhabits cold, fast-flowing streams and rivers with clean, well-oxygenated water and gravel or rocky substrates. Longnose
         Dace are especially common in riffles and shallow runs.'''.replace( '\n', ' ' ),
      '''Longnose Dace are opportunistic feeders, consuming aquatic insect larvae such as mayflies, caddisflies, and stoneflies, as
         well as small crustaceans and algae. They forage along the stream bottom, picking food from rocks and sediments. In
         aquarium settings, they are fed small invertebrates and prepared foods suited to bottom-feeding fish.'''.replace( '\n', ' ' ),
      '''These fish are active during the day and are often seen darting quickly between rocks in fast-moving water. They are
         generally solitary or found in loose groups rather than tight schools. Longnose Dace are agile swimmers and rely on quick
         movements to avoid predators.'''.replace( '\n', ' ' ),
      '''The streamlined body and strong pectoral fins of the Longnose Dace allow it to hold position in swift currents. Its mottled
         colouration provides effective camouflage against gravel and stones, reducing predation risk. A downward-oriented mouth is
         well suited for feeding along the streambed.'''.replace( '\n', ' ' ),
      '''Spawning occurs in late spring to early summer. Females scatter eggs over gravel substrates, where they develop without
         parental care. Fry hatch within a few days and grow rapidly during their first year. Longnose Dace typically live 3–5
         years.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Massasauga Rattlesnake',
      'Sistrurus Catenatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Massasauga rattlesnake can be found in an enclosure right at the end of the pavilion, on the right and across from the
         turtle habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Massasauga Rattlesnake is a small to medium-sized rattlesnake with a thick body and a distinctive rattle at the end of
         its tail. Colouration ranges from grey to light brown with dark, rounded blotches along the back and sides. The head is
         triangular, and the pupils are vertical. Adults typically reach 60–90 cm in length.'''.replace( '\n', ' ' ),
      '''In Canada, the Massasauga is found primarily in southern Ontario, while its broader range extends through parts of the
         central and eastern United States. It inhabits wetlands, tallgrass prairies, rocky outcrops, and forest edges, often
         favouring areas near water with ample cover.'''.replace( '\n', ' ' ),
      '''Massasauga Rattlesnakes are carnivorous ambush predators that feed mainly on small mammals such as mice and voles, as well
         as amphibians and small birds. They use venom to subdue prey before swallowing it whole. In captivity, they are fed
         appropriately sized rodents at regular intervals.'''.replace( '\n', ' ' ),
      '''This species is generally shy and secretive, relying on camouflage to avoid detection. It is most active during warmer
         months and may be diurnal or nocturnal depending on temperature. Massasaugas are solitary, except during the breeding
         season or when overwintering in communal hibernation sites.'''.replace( '\n', ' ' ),
      '''Heat-sensing pits between the eyes and nostrils allow detection of warm-blooded prey even in low light. The rattle serves
         as an effective warning system to deter large animals. Cryptic colouration helps the snake blend into its surroundings,
         reducing both predation risk and unnecessary encounters.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring or early summer. Females give birth to live young, typically 5–20 offspring. Juveniles are fully
         venomous at birth and independent. Massasauga Rattlesnakes can live 20 years or more, particularly in protected
         environments.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Mexican Blind Cavefish',
      'Astyanax Mexicanus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Mexican blind cavefish can be found in the Costa Rica loop of the Americas Pavilion, through the doors across from the
         North American river otter viewing, and past the bugs.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Mexican Blind Cavefish is a small freshwater fish, typically 5–7 cm long, with a pale, almost translucent body and no
         functional eyes. Its fins are delicate and translucent, and it lacks pigmentation, giving it a ghostly appearance.
         Juveniles resemble surface-dwelling relatives but gradually lose their eyes and colouration in dark cave environments.'''
         .replace( '\n', ' ' ),
      '''This species is native to the limestone cave systems of northeastern Mexico, including the Sierra de El Abra. It lives in
         complete darkness in subterranean pools and streams, often in nutrient-poor water with low oxygen levels.'''
         .replace( '\n', ' ' ),
      '''Mexican Blind Cavefish are opportunistic feeders. They primarily consume small invertebrates, detritus, and organic matter
         that drifts into cave pools. In captivity, they are fed a diet of finely chopped live or prepared foods suitable for small
         freshwater fish.'''.replace( '\n', ' ' ),
      '''These fish are schooling and social, often swimming in groups to navigate and forage. They rely on mechanosensory systems
         called neuromasts to detect water movement and avoid obstacles. They are highly adapted to low-light or no-light conditions
         and are generally non-aggressive.'''.replace( '\n', ' ' ),
      '''The loss of eyes and pigmentation reduces energy expenditure in a dark environment. Enhanced lateral line systems allow the
         fish to detect changes in water pressure and currents, aiding in navigation and prey detection. Metabolic and behavioural
         adaptations help them survive in nutrient-limited cave systems.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in suitable captive or natural conditions. Females lay eggs that adhere to surfaces in the water,
         and fry hatch fully functional, gradually developing sensory adaptations. Lifespan in captivity is typically 4–6 years,
         sometimes longer under optimal care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Midland Painted Turtle',
      'Chrysemys Picta Marginata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The midland painted turtle can be spotted in a shared habitat with the Blanding's turtles near the exit of the pavilion,
         and on the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Midland Painted Turtle is a small to medium-sized freshwater turtle, with a smooth, domed shell that is olive to dark
         brown on top and brightly patterned with red, yellow, and black markings on the plastron and edges. Adults typically
         measure 12–20 cm in length. Its head, legs, and tail also feature yellow stripes.'''.replace( '\n', ' ' ),
      '''This subspecies is native to central and eastern North America, ranging from southern Canada through the Midwestern United
         States. It inhabits ponds, marshes, slow-moving rivers, and wetlands with soft bottoms and abundant aquatic vegetation for
         cover and foraging.'''.replace( '\n', ' ' ),
      '''Midland Painted Turtles are omnivorous. Their diet includes aquatic plants, algae, insects, crustaceans, tadpoles, and
         small fish. They forage both in water and along shorelines. In captivity, they are fed a balanced diet of leafy greens,
         aquatic vegetation, insects, and commercial turtle foods.'''.replace( '\n', ' ' ),
      '''These turtles are generally solitary but may bask in groups on logs or rocks. They are most active during the day,
         especially in warm weather. Midland Painted Turtles hibernate in the winter, burying themselves in soft mud or sediment at
         the bottom of ponds or streams.'''.replace( '\n', ' ' ),
      '''The streamlined shell and webbed feet allow efficient swimming in aquatic habitats. Bright ventral patterns may play a role
         in species recognition. Hibernation enables survival during cold winters, while a varied diet allows flexibility in
         resource-limited environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring after emergence from hibernation. Females lay clutches of 5–20 eggs in sandy or soft soil near
         water. Eggs incubate for 60–90 days, hatching in late summer. Juveniles are independent at birth. Lifespan is typically
         20–30 years, with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'North American River Otter',
      'Lontra Canadensis',
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The North American river otters can be seen from two main spots. You can see them from above, just past the entrance to the
         pavilion, or venture inside the pavilion, heading past the aquatic area to see them underwater, or inside. The North
         American river otters are a highly active species, and can be usually seen swimming around their water feature during the
         day. If you don't spot them playing in the water, they may be taking a rest, either in their indoor habitat, or in one of
         their toys in their outdoor habitat.'''.replace( '\n', ' ' ),
      '''North American otters can be outside and in the water year-round, but they are always given the option to stay inside, so
         you may have to venture inside the pavilion to see them.'''.replace( '\n', ' ' ),
      '''The North American River Otter is a medium-sized aquatic mammal with a streamlined body, short legs, and a thick, muscular
         tail. Adults typically measure 66–107 cm in body length, with tails adding another 30–45 cm, and weigh 5–14 kg. Fur is
         dense, velvety, and dark brown on the back, fading to lighter brown on the underside. Whiskers, webbed feet, and a
         flattened head help with hunting and swimming.'''.replace( '\n', ' ' ),
      '''River Otters are widespread across freshwater and coastal habitats in Canada, the United States, and northern Mexico. They
         inhabit rivers, lakes, marshes, and estuaries, preferring areas with abundant prey and dense shoreline vegetation for
         shelter. They are highly adaptable and can tolerate areas near human activity if water quality is sufficient.'''
         .replace( '\n', ' ' ),
      '''North American River Otters are opportunistic carnivores, feeding primarily on fish, crayfish, amphibians, molluscs, and
         small mammals. They occasionally eat birds or aquatic insects. They are skilled hunters, using sharp teeth, strong jaws,
         and webbed feet to catch and handle slippery prey. In zoos, they are provided with fish, crustaceans, and enrichment to
         mimic natural hunting behaviour.'''.replace( '\n', ' ' ),
      '''River Otters are social, playful animals often observed sliding on mud or snow, wrestling, and chasing each other. Groups,
         called “rafts,” may include family members. They are active both day and night, though activity peaks at dawn and dusk.
         River Otters communicate through vocalisations, scent marking, and body language. Play is believed to strengthen social
         bonds and develop hunting skills.'''.replace( '\n', ' ' ),
      '''Adaptations for an aquatic lifestyle include a streamlined, flexible body; webbed feet for swimming; dense fur for
         insulation; and the ability to close nostrils and ears underwater. Whiskers detect prey in murky water, and lungs and
         musculature allow prolonged diving. Sharp claws and strong jaws facilitate catching and holding onto prey.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs once a year, usually in late winter. Females experience delayed implantation, with embryos developing
         several months after fertilisation, ensuring births occur in spring. Litters of 1–5 pups are born in dens near water, and
         juveniles remain with the mother for 6–12 months. Lifespan is typically 8–9 years in the wild but can exceed 20 years in
         captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo recently celebrated the birth of three river otter pups. The Toronto Zoo is also home to a pair of adult
         otters, female, Maybelle, and male, RJ. First-time mom, Maybelle is currently spending most of her time behind the scenes,
         bonding with the pups, and recently teaching them how to swim. She may be viewable occasionally in her habitat. RJ is also
         viewing in the Americas Pavilion in the outdoor otter habitat.'''.replace( '\n', ' ' )
   ),
   (
      'Opal-Rumped Tanager',
      'Tangara Velia',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The opal-rumped tanager can be spotted in the tanager aviary, in the Costa Rican section of the pavilion, through the doors
         across from the river otters, and past the bugs and alligators.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Opal-rumped Tanager is a small, colourful songbird, about 13 cm long. Its body is mostly bright green with striking
         blue wings and tail, while the lower back and rump shimmer with an opalescent bluish-purple sheen. Its short, pointed beak
         is well suited for eating fruit and insects.'''.replace( '\n', ' ' ),
      '''This species inhabits tropical lowland forests, secondary forests, and forest edges in northern South America, including
         Colombia, Venezuela, Guyana, and northern Brazil. It prefers areas with dense foliage for foraging and nesting.'''
         .replace( '\n', ' ' ),
      '''Opal-rumped Tanagers are primarily frugivorous but also eat small insects and arthropods. They forage actively among the
         canopy and mid-level branches, using their agile movements to pick fruits and snatch prey from leaves. In captivity, their
         diet is supplemented with soft fruits, insects, and commercial bird diets.'''.replace( '\n', ' ' ),
      '''These tanagers are social, often found in small flocks or mixed-species foraging groups. They communicate with high-pitched
         calls and short whistles. Active and agile, they spend most of the day moving through foliage while searching for food.'''
         .replace( '\n', ' ' ),
      '''Bright plumage aids in species recognition and courtship, while their lightweight bodies and strong wings allow rapid
         flight through dense vegetation. Their short, pointed beak is effective for both fruit consumption and insect hunting.
         Social flocking helps reduce predation risk and increases foraging efficiency.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the wet season when food is abundant. Females build cup-shaped nests in shrubs or low trees and lay
         2–3 eggs. Both parents help feed the hatchlings, which fledge in a few weeks. Lifespan in the wild is typically 5–8 years,
         with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Painted Anemone',
      'Urticina Crassicornis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The painted anemone can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate
         wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Painted Anemone is a large, colourful sea anemone with a cylindrical body and a crown of tentacles surrounding a
         central mouth. Colours vary from red, pink, orange, or purple, often with contrasting tentacle tips. Individuals typically
         reach 15–25 cm in diameter, though tentacles can extend further.'''.replace( '\n', ' ' ),
      '''This species is native to the cold, rocky coastal waters of the North Atlantic and North Pacific, including Canada’s
         Atlantic and Pacific coasts. Painted Anemones attach to rocks, boulders, and other hard substrates in intertidal and 
         subtidal zones, often in areas with moderate water movement.'''.replace( '\n', ' ' ),
      '''Painted Anemones are carnivorous, feeding on small fish, crustaceans, molluscs, and planktonic invertebrates. They capture
         prey using stinging cells (nematocysts) on their tentacles and transport food to the central mouth for digestion. In
         aquaria, they are offered small pieces of seafood to simulate natural feeding.'''.replace( '\n', ' ' ),
      '''This species is mostly solitary but may cluster in areas with abundant food. Painted Anemones are sessile, remaining
         attached to rocks for life. They respond to environmental changes by contracting or retracting their tentacles, and their
         feeding behaviour is mostly passive, waiting for prey to contact their tentacles.'''.replace( '\n', ' ' ),
      '''Tentacles equipped with nematocysts allow efficient capture and immobilisation of prey. Their sticky base firmly attaches
         to substrates to resist wave action. Bright and varied colours may deter predators and signal toxicity. Ability to retract
         reduces water loss during low tide and protects delicate tissues.'''.replace( '\n', ' ' ),
      '''Painted Anemones reproduce both sexually, by releasing eggs and sperm into the water, and asexually, through fission or
         budding. Larvae are planktonic before settling onto a suitable substrate to develop into adult anemones. Individuals can
         live 10–20 years, depending on environmental conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Panamanian Golden Frog',
      'Atelopus Zeteki',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Panamanian golden frog can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Panamanian Golden Frog is a small, brightly coloured amphibian, typically 3–5 cm in length. Its body is vivid yellow to
         golden, sometimes with black spots or markings. The skin is smooth, and its eyes are large and prominent, giving it a
         distinctive, expressive appearance. Its bright colouration serves as a warning to predators of its toxicity.'''
         .replace( '\n', ' ' ),
      '''This species is endemic to the highland streams and forests of central Panama. It inhabits fast-flowing, clear streams and
         adjacent forested areas, often perching on rocks or leaves near water. It requires pristine, humid habitats with consistent
         water flow for breeding and survival.'''.replace( '\n', ' ' ),
      '''Panamanian Golden Frogs are insectivorous, feeding primarily on ants, beetles, termites, and other small arthropods. They
         forage actively among rocks and foliage, using their sticky tongues to capture prey. In captivity, their diet is
         supplemented with appropriately sized insects dusted with vitamins and minerals.'''.replace( '\n', ' ' ),
      '''These frogs are diurnal and highly social, often communicating through visual signals such as leg-waving displays, which
         serve as territorial and courtship signals. They are active hunters during the day and are known for their agile jumping
         and climbing abilities. Their bright colouration helps individuals recognise each other while warning predators.'''
         .replace( '\n', ' ' ),
      '''Bright, aposematic colouring deters predators by signalling toxicity. Their long, sticky tongues and agile limbs allow
         efficient hunting in complex streamside habitats. The species is adapted to humid, cool environments and requires clean,
         oxygen-rich water for reproduction and larval development.'''.replace( '\n', ' ' ),
      '''Breeding occurs in streams, where females lay eggs on rocks or leaves above water. Tadpoles drop into the water upon
         hatching and develop in the fast-flowing stream. Lifespan in the wild is uncertain, but individuals can live up to 10 years
         in captivity. Both eggs and adults are toxic to predators.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Plumose Anemone',
      'Metridium Farcimen',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The plumose anemone can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate
         wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Plumose Anemone is a large, soft-bodied sea anemone with a tall, cylindrical column and feathery tentacles arranged in
         multiple whorls around a central mouth. Colouration ranges from white to pale pink or cream. Individuals can reach 30–50 cm
         in height, with tentacles extending even further.'''.replace( '\n', ' ' ),
      '''This species is native to the northern Pacific Ocean, including the coasts of British Columbia and Alaska. It inhabits
         subtidal zones, often attaching to rocks, docks, pilings, and other hard surfaces in areas with moderate to strong water
         flow.'''.replace( '\n', ' ' ),
      '''Plumose Anemones are carnivorous, capturing plankton, small crustaceans, and larvae with stinging tentacles. Food is
         immobilized by nematocysts and transported to the mouth for digestion. In aquaria, they are fed small invertebrates or
         specialized prepared foods suitable for filter-feeding invertebrates.'''.replace( '\n', ' ' ),
      '''Plumose Anemones are sessile and generally solitary but may cluster in areas with abundant food. They extend their
         tentacles to capture passing prey and retract them when disturbed. While they do not actively move, they can slowly detach
         and drift to a new location if necessary.'''.replace( '\n', ' ' ),
      '''Feathery tentacles increase surface area for capturing prey, while nematocysts provide both defence and hunting capability.
         A muscular base firmly anchors the anemone to substrates, preventing dislodgement by currents. The ability to retract or
         contract protects delicate tissues from predators and environmental stress.'''.replace( '\n', ' ' ),
      '''Plumose Anemones reproduce both sexually and asexually. Sexual reproduction occurs via the release of eggs and sperm into
         the water column, producing free-swimming larvae that settle and mature. Asexual reproduction occurs through budding or
         fission. Individuals can live 20 years or more in stable conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Plush-Crested Jay',
      'Cyanocorax Chrysops',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The plush-crested jays can be spotted in an enclosure near the entrance to the pavilion, just past the blue and gold macaws
         and straight ahead. The plush-crested jays shares a habitat with the crested tinamou.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Plush-Crested Jay is a medium-sized passerine, measuring about 34–38 cm in length. It has striking black, blue, and
         white plumage, with a distinctive plush crest on its head and a long, graduated tail. Its strong, slightly curved beak is
         ideal for feeding on a variety of foods.'''.replace( '\n', ' ' ),
      '''This species is native to South America, primarily found in southern Brazil, Paraguay, Argentina, and Bolivia. It inhabits
         subtropical and tropical forests, forest edges, and gallery forests along rivers. The Plush-Crested Jay adapts well to
         secondary forests and wooded urban areas.'''.replace( '\n', ' ' ),
      '''Plush-Crested Jays are omnivorous, feeding on fruits, seeds, insects, small vertebrates, and occasionally eggs of other
         birds. They forage actively in trees and shrubs, using their strong beaks to probe for insects and manipulate food. In
         zoos, they are provided with a balanced diet of fruits, insects, and supplemental bird feed.'''.replace( '\n', ' ' ),
      '''These jays are highly social and vocal, often observed in noisy groups. They are intelligent and display problem-solving
         behaviours, such as manipulating objects and caching food. Social interactions include cooperative foraging, play, and
         communication through calls and posturing.'''.replace( '\n', ' ' ),
      '''Strong, versatile beaks allow them to consume a varied diet, while long tails and strong wings aid agile movement through
         dense forest canopies. Social behaviour and vocal communication help the species coordinate group activities and avoid
         predators. Bright plumage aids species recognition in forest habitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the wet season. Nests are constructed high in trees, and females typically lay 2–5 eggs. Both
         parents participate in incubation and feeding of hatchlings. Juveniles are independent after several weeks. Lifespan in the
         wild is typically 8–10 years, with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Puerto Rican Crested Toad',
      'Peltophryne Lemur',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Puerto Rican crested toad can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Puerto Rican Crested Toad is a small, stout amphibian, typically 3–5 cm in length. Its body is grey to brown with
         darker blotches, and it has distinctive raised crests over the eyes. The skin is rough and slightly warty, adapted for a
         terrestrial lifestyle.'''.replace( '\n', ' ' ),
      '''This species is endemic to Puerto Rico, inhabiting dry forests, coastal plains, and intermittent freshwater pools. It
         prefers areas with loose soil or leaf litter for burrowing and requires temporary water bodies for breeding.'''
         .replace( '\n', ' ' ),
      '''Puerto Rican Crested Toads are insectivorous, feeding on ants, beetles, spiders, and other small invertebrates. They hunt
         at night, capturing prey with their sticky tongues. In zoos, their diet includes appropriately sized insects dusted with
         vitamins and minerals.'''.replace( '\n', ' ' ),
      '''These toads are primarily nocturnal and fossorial, spending daylight hours buried or hidden under vegetation. They are
         generally solitary except during the breeding season. Males call near temporary pools to attract females, producing loud,
         distinctive croaks.'''.replace( '\n', ' ' ),
      '''Raised cranial crests may deter predators or help shed water during rainfall. Burrowing behaviour allows them to survive
         dry periods and avoid predators. Their skin colouration and patterning provide camouflage in leaf litter and soil.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season when temporary pools form. Females lay eggs in water, and tadpoles develop rapidly
         to take advantage of ephemeral habitats. Juveniles are independent upon metamorphosis. Lifespan is typically 5–8 years,
         with longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Pumpkinseed Sunfish',
      'Lepomis Gibbosus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The pumpkinseed sunfish can be found in the underwater viewing habitat beside the river otters.''',
      None,                                                          # Seasonal viewing tips
      '''The Pumpkinseed Sunfish is a small, brightly coloured freshwater fish, typically 10–18 cm long. Its body is laterally
         compressed with an olive-green to yellow base, adorned with orange, red, and blue markings. A distinctive black spot is
         present at the base of the dorsal fin, and the gill cover often features an iridescent blue streak.'''.replace( '\n', ' ' ),
      '''Native to eastern North America, Pumpkinseed Sunfish inhabit lakes, ponds, rivers, and streams with clear water, abundant
         vegetation, and soft or sandy substrates. They prefer shallow, warm areas with plenty of cover from aquatic plants or
         submerged structures.'''.replace( '\n', ' ' ),
      '''Pumpkinseed Sunfish are omnivorous, feeding on insects, crustaceans, molluscs, small fish, and aquatic vegetation. They
         forage actively along the bottom and among plants, using their small mouths to pick prey from surfaces. In zoos or aquaria,
         they are fed a diet of live or frozen invertebrates, supplemented with commercial fish food.'''.replace( '\n', ' ' ),
      '''These sunfish are diurnal and territorial during the breeding season, with males defending nesting sites aggressively. They
         are often seen in loose groups outside of breeding periods. Their behaviour includes foraging among vegetation, darting
         quickly to capture prey, and basking in sunlit shallow areas.'''.replace( '\n', ' ' ),
      '''Pumpkinseed Sunfish have a laterally compressed body for agile swimming among vegetation. Colouration provides camouflage
         against predators and signalling during courtship. Sharp spines on the dorsal and anal fins serve as a defence mechanism,
         deterring predators from swallowing them.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late spring and summer. Males construct shallow nests in sandy or muddy bottoms, where females lay eggs.
         Males guard the eggs and fry until they become independent. Lifespan is typically 6–10 years, with growth and reproduction
         influenced by water temperature and food availability.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red Island Bird-Eating Tarantula',
      'Cyriopagopus Vonwirthi',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Red Island bird-eating tarantula can be found in the bugs hallway, located before the Costa Rican area through the
         doors across from the river otter viewing.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Red Island Bird-Eating Tarantula is a large, robust spider with a leg span of 15–20 cm. Its body is dark brown to black
         with subtle red or orange hairs on the legs and abdomen. Like other tarantulas, it has eight eyes, strong chelicerae, and
         hairy legs adapted for sensory perception and prey capture.'''.replace( '\n', ' ' ),
      '''This species is native to the island of Madagascar, where it inhabits tropical forests and wooded areas. It typically
         resides in tree holes, under bark, or among leaf litter, favouring humid, sheltered microhabitats that provide protection
         and hunting opportunities.'''.replace( '\n', ' ' ),
      '''Red Island Bird-Eating Tarantulas are carnivorous ambush predators. They feed on insects, small reptiles, amphibians, and
         occasionally small birds. Prey is captured using strong fangs and immobilised with venom. In captivity, their diet consists
         of crickets, roaches, and other appropriately sized invertebrates.'''.replace( '\n', ' ' ),
      '''These tarantulas are largely solitary and nocturnal. They rely on stealth and quick strikes to capture prey. Defensive
         behaviours include raising the front legs, displaying fangs, or retreating to a burrow. Social interactions are minimal
         outside of mating, and females are known to be more aggressive than males.'''.replace( '\n', ' ' ),
      '''Strong, hairy legs provide sensory awareness in low-light conditions. Powerful fangs and venom allow the spider to subdue
         prey larger than itself. Camouflage helps it remain hidden from both predators and prey. Its arboreal lifestyle is
         supported by claws and scopula hairs that enable climbing smooth surfaces.'''.replace( '\n', ' ' ),
      '''Mating occurs when a male locates a female’s burrow and performs a courtship display to avoid being mistaken for prey.
         Females lay eggs in silk egg sacs, which are guarded until spiderlings emerge. Spiderlings are independent immediately.
         Lifespan is 10–15 years for females and 5–7 years for males.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red-Crested Finch',
      'Coryphospingus Cucullatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red-crested finch can be spotted in the tanager aviary, in the Costa Rican section of the pavilion, through the doors
         across from the river otters, and past the bugs and alligators.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Red-Crested Finch is a small, colourful passerine, measuring about 12–13 cm in length. Males display a bright red crest
         and face, with olive-brown upperparts and pale underparts. Females are more subdued, with olive or brown tones and only
         hints of red on the head.'''.replace( '\n', ' ' ),
      '''This species inhabits open woodlands, savannas, shrublands, and forest edges in South America, including Brazil, Bolivia,
         Paraguay, and northern Argentina. It is often found near water sources and areas with dense vegetation for cover.'''
         .replace( '\n', ' ' ),
      '''Red-Crested Finches are primarily granivorous, feeding on seeds from grasses and shrubs, but they also consume small
         insects, particularly during the breeding season. They forage actively on the ground or in low vegetation. In captivity,
         they are provided a diet of seeds, insects, and supplemented bird food.'''.replace( '\n', ' ' ),
      '''These finches are social and often seen in small flocks. They communicate through short, melodious calls and maintain close
         contact with group members. During breeding, pairs may defend small territories and engage in courtship displays involving
         crest-raising and vocalisations.'''.replace( '\n', ' ' ),
      '''The short, strong beak is adapted for seed consumption, while agile flight allows quick escapes from predators. Bright
         crest colouration aids in mate recognition and signalling during social interactions. Group living provides safety in
         numbers and improves foraging efficiency.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the wet season when food is abundant. Females build cup-shaped nests in low shrubs or grasses and
         lay 2–4 eggs. Both parents help feed the chicks until fledging. Lifespan in the wild is typically 3–5 years, with longer
         lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Reticulate Gila Monster',
      'Heloderma Suspectum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The reticulate gila monster can be found in an enclosure towards the exit of the pavilion, across from the river otter and
         snapping turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Reticulate Gila Monster is a large, heavy-bodied lizard with a distinctive bead-like, textured skin. Its colouration
         consists of black or dark brown skin with bright orange or pink reticulated patterns along the back and sides. Adults
         typically measure 40–60 cm in total length, with a stout, thick tail used for fat storage.'''.replace( '\n', ' ' ),
      '''This species is native to the southwestern United States and northern Mexico, inhabiting arid deserts, scrublands, and
         rocky hillsides. It prefers areas with burrows or rock crevices to escape heat and predators and is often associated with
         cacti and other desert vegetation.'''.replace( '\n', ' ' ),
      '''Reticulate Gila Monsters are carnivorous and feed on small mammals, birds, eggs, lizards, and carrion. They have a slow
         metabolism and feed infrequently. Venom is delivered through grooved teeth to subdue prey. In captivity, they are fed
         rodents, eggs, and other protein-rich foods on a controlled schedule.'''.replace( '\n', ' ' ),
      '''These lizards are primarily solitary and spend much of their time underground in burrows or under rocks. They are mostly
         active in the morning or late afternoon to avoid extreme desert heat. Defensive behaviours include hissing, biting, and
         tail coiling. Social interactions occur mainly during the breeding season.'''.replace( '\n', ' ' ),
      '''Beaded skin provides protection against predators and abrasive desert terrain. The thick tail stores fat to survive long
         periods without food. Venom aids in subduing prey and deterring predators. They are well-adapted to extreme temperatures
         and arid environments through burrowing and nocturnal or crepuscular activity.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring, with females laying 4–12 eggs in burrows or under rocks. Eggs incubate for several months before
         hatching. Juveniles are independent at birth. Lifespan in the wild can exceed 20 years, and captive individuals often live
         even longer.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Round Goby',
      'Neogobius Melanostomus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The round goby can be found in an enclosure towards the exit of the pavilion, across from the river otter and snapping
         turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Round Goby is a small, bottom-dwelling freshwater fish, typically 7–12 cm long. It has a robust, elongated body, a
         slightly flattened head, and fused pelvic fins forming a suction cup. Colouration is grey to olive with dark blotches along
         the body and a black spot at the base of the first dorsal fin.'''.replace( '\n', ' ' ),
      '''Native to the Black and Caspian Seas, the Round Goby has become invasive in the Great Lakes and other North American
         waterways. It inhabits shallow waters with rocky or sandy substrates, often near docks, breakwalls, or submerged vegetation. 
         It tolerates a wide range of salinities and temperatures.'''.replace( '\n', ' ' ),
      '''Round Gobies are opportunistic feeders, eating invertebrates such as molluscs, insect larvae, and crustaceans, as well as
         small fish eggs. They use their downward-facing mouth to scavenge along the bottom. In captivity, they are fed small
         invertebrates or prepared fish foods.'''.replace( '\n', ' ' ),
      '''These fish are territorial, particularly during breeding, with males defending nests under rocks or other cover. Outside
         breeding, they may form loose aggregations. Round Gobies are active bottom dwellers, using their suction cup-like pelvic
         fins to cling to substrates in fast currents or turbulent waters.'''.replace( '\n', ' ' ),
      '''Fused pelvic fins function as a suction cup, allowing the fish to cling to rocks and other surfaces in flowing water.
         Camouflaged colouration helps avoid predators. Round Gobies have strong, protruding teeth for crushing molluscs and other
         hard-shelled prey.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring and summer. Males excavate nests and guard eggs laid by females. Fry hatch within days to weeks
         depending on water temperature. Lifespan is typically 3–5 years, though individuals may survive longer under favourable
         conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Rufous-Collared Sparrow',
      'Zonotrichia Capensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The rufous-collared sparrow can be spotted in the tanager aviary, in the Costa Rican section of the pavilion, through the
         doors across from the river otters, and past the bugs and alligators.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Rufous-Collared Sparrow is a small songbird, typically 13–15 cm in length. It has a grey head with a rufous collar
         around the neck, brown streaked upperparts, and pale underparts with subtle streaking. The short, conical beak is ideal for
         seed consumption, and the species is known for its melodious, variable song.'''.replace( '\n', ' ' ),
      '''This species is widespread throughout Central and South America, from Mexico to Tierra del Fuego. It inhabits open
         woodlands, farmland, gardens, and urban areas. Rufous-Collared Sparrows are highly adaptable and can thrive in both lowland
         and highland regions up to 4,000 m.'''.replace( '\n', ' ' ),
      '''Rufous-Collared Sparrows are primarily granivorous, feeding on seeds of grasses and weeds, but they also eat small insects,
         especially during the breeding season. They forage on the ground and in low vegetation. In zoos, their diet is supplemented
         with seeds, insects, and commercial bird feed.'''.replace( '\n', ' ' ),
      '''These sparrows are diurnal and social, often seen in pairs or small flocks. They communicate through complex songs and
         calls, which play roles in mate attraction and territorial defence. Active foragers, they hop on the ground and make short
         flights while searching for food.'''.replace( '\n', ' ' ),
      '''The short, strong beak allows efficient seed consumption, while agile flight enables quick escape from predators.
         Adaptability to a variety of habitats allows them to exploit both natural and human-modified environments. Vocal learning
         and song variability aid in communication and territorial interactions.'''.replace( '\n', ' ' ),
      '''Breeding occurs in response to local environmental cues, often during wet seasons when food is abundant. Females build
         cup-shaped nests in shrubs or on the ground. Clutches typically contain 2–5 eggs, which hatch after about two weeks.
         Juveniles are independent shortly after fledging. Lifespan is typically 3–5 years, with longer lifespans possible in
         captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'San-Esteban Island Chuckwalla',
      'Sauromalus Varius',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The San-Esteban Island  huckwalla can be found in an enclosure towards the exit of the pavilion, across from the river
         otter and snapping turtle underwater viewings. The San-Esteban Island Chuckwalla shares a habitat with the desert grassland
         whiptail.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The San-Esteban Island Chuckwalla is a large, stout lizard, reaching up to 50–55 cm in length. It has a broad, flattened
         body, loose folds of skin along the sides, and a thick, muscular tail. Colouration is typically grey to dark brown, with
         males often displaying brighter patches of orange or yellow during the breeding season.'''.replace( '\n', ' ' ),
      '''This species is endemic to San Esteban Island in the Gulf of California, Mexico. It inhabits rocky, arid landscapes with
         sparse vegetation, often seeking shelter in crevices, under boulders, or in abandoned burrows to escape heat and predators.'''
         .replace( '\n', ' ' ),
      '''Chuckwallas are primarily herbivorous, feeding on leaves, flowers, fruits, and occasionally seeds of desert plants. They
         are active during the day, foraging among rocks and shrubs. In captivity, their diet is supplemented with leafy greens,
         vegetables, and safe fruits.'''.replace( '\n', ' ' ),
      '''San-Esteban Island Chuckwallas are diurnal and generally solitary. They exhibit territorial behaviours, with males often
         displaying head-bobbing and body inflation to warn rivals. When threatened, they retreat into rock crevices and inflate
         their bodies to wedge themselves securely, making extraction by predators difficult.'''.replace( '\n', ' ' ),
      '''Loose skin folds allow the lizard to expand and wedge itself into tight crevices, protecting it from predators. Flattened
         body shape and strong limbs aid climbing among rocky terrain. Colouration provides camouflage in desert landscapes, while a
         herbivorous diet allows survival in nutrient-sparse environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring. Females lay 2–10 eggs in hidden nests in sandy or rocky areas. Hatchlings are independent
         immediately and grow rapidly during their first year. Lifespan is typically 15–20 years, with longer lifespans possible in
         captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Snapping Turtle',
      'Chelydra Serpentina',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The snapping turtle can be spotted in two locations in the Americas Pavilion. One snapping turtle can be found in the Costa
         Rican section of the pavilion, through the doors across from the otters, and across from the alligators. Another can be
         spotted in the underwater viewing habitat beside the river otters.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Snapping Turtle is a large, heavy-bodied freshwater turtle, typically 25–50 cm in shell length, with some adults
         exceeding 70 cm. It has a rugged, ridged carapace that is brown to olive in colour, a long, powerful tail with saw-toothed
         ridges, and a large head with strong jaws. Its limbs are sturdy with webbed feet for swimming.'''.replace( '\n', ' ' ),
      '''Snapping Turtles are widespread across North America, from southern Canada through much of the United States. They inhabit
         rivers, lakes, ponds, marshes, and swamps with soft, muddy bottoms and abundant aquatic vegetation, often preferring
         slow-moving or still waters.'''.replace( '\n', ' ' ),
      '''These turtles are omnivorous, feeding on fish, amphibians, invertebrates, carrion, aquatic plants, and algae. They are
         mostly active at night, ambushing prey from the bottom or foraging along the shoreline. In captivity, they are fed a
         combination of fish, invertebrates, and commercial turtle diets.'''.replace( '\n', ' ' ),
      '''Snapping Turtles are primarily solitary and non-territorial but can display aggressive defensive behaviour when threatened.
         They spend much of their time submerged, emerging to bask occasionally. Mating occurs in water, while females often travel
         to land to lay eggs.'''.replace( '\n', ' ' ),
      '''Powerful jaws and sharp beak allow them to capture and process prey efficiently. Long, muscular tails and strong limbs aid
         swimming and stability. Camouflage provided by the rugged carapace helps avoid predators, and their ability to remain
         submerged for long periods aids both hunting and protection.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring. Females lay 20–50 eggs in sandy or soft soil near water. Hatchlings emerge after about 70–90
         days and are independent immediately. Snapping Turtles can live 30–40 years in the wild, with some individuals exceeding
         50 years in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Spot Prawn',
      'Pandalus Platyceros',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The spot prawn can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the primate wing
         and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Spot Prawn is a large, commercially important shrimp species, reaching up to 25 cm in length. It has a translucent
         reddish-orange body with distinctive white or pale bands on the legs and a white spot on the upper part of the second
         abdominal segment. Long antennae and swimmerets aid in navigation and swimming.'''.replace( '\n', ' ' ),
      '''Spot Prawns are native to the northeastern Pacific Ocean, from Alaska to California. They inhabit deep coastal waters,
         typically 30–450 m below the surface, preferring rocky or soft-bottom substrates. Adults often live in colder waters while
         juveniles occupy shallower regions.'''.replace( '\n', ' ' ),
      '''Spot Prawns are omnivorous scavengers, feeding on plankton, detritus, small invertebrates, and organic matter on the
         seafloor. They are active mostly at night, using their antennae and sensitive legs to locate food. In captivity, they are
         offered small pieces of seafood and commercially prepared shrimp diets.'''.replace( '\n', ' ' ),
      '''Spot Prawns are generally solitary but may congregate in areas with abundant food. They are nocturnal and remain hidden in
         crevices or burrows during the day. Social interactions include molting and competition for shelter or mates. They
         communicate subtly through movement and chemical signals.'''.replace( '\n', ' ' ),
      '''Camouflage and translucent colouring help avoid predators. Long antennae and sensitive legs detect prey and navigate
         low-light environments. Their strong swimmerets allow quick escape from predators. Spot Prawns are adapted to high-pressure,
         cold-water habitats and can survive in deep marine environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs in winter and early spring. Females carry eggs under their abdomens until hatching, which produces
         planktonic larvae that drift with currents for several weeks before settling to the seafloor. Lifespan is typically 5–6
         years, though some individuals may live longer.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Spotted River Stingray',
      'Potamotrygon Motoro',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The spotted river stingray can be found in a tank enclosure in the aquatic section of the Americas Pavilion, after the
         primate wing and before the otters and Costa Rican area.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Spotted River Stingray is a medium-sized freshwater ray with a broad, disc-shaped body typically 30–60 cm across and a
         long, slender tail. Its dorsal surface is brown to olive with numerous distinctive cream or yellow spots, while the
         underside is pale. A venomous stinger is present on the tail for defence.'''.replace( '\n', ' ' ),
      '''This species is native to tropical river systems in South America, including the Amazon, Orinoco, and Paraná basins. It
         prefers slow-moving waters, sandy or muddy bottoms, and areas with submerged vegetation or leaf litter for cover.'''
         .replace( '\n', ' ' ),
      '''Spotted River Stingrays are carnivorous, feeding on fish, crustaceans, molluscs, and worms. They are bottom feeders, using
         electroreception and sensory pits to detect prey buried in sediment. In captivity, they are provided with fish, shrimp, and
         other meaty foods appropriate for bottom-dwelling rays.'''.replace( '\n', ' ' ),
      '''These stingrays are mostly solitary and spend much of their time partially buried in the substrate. They are active during
         the day and night, gliding gracefully along the riverbed in search of food. Social interactions are limited to mating, with
         males following females closely.'''.replace( '\n', ' ' ),
      '''Flattened, disc-shaped bodies and pectoral fins allow efficient movement along the riverbed. Sensory pits and
         electroreception detect hidden prey. Camouflaged colouration provides protection from predators, and the venomous tail
         spine deters threats. Mouths located on the underside facilitate bottom feeding.'''.replace( '\n', ' ' ),
      '''Spotted River Stingrays are viviparous, giving birth to live young after internal gestation. Litters typically contain 4–12
         pups, which are independent immediately. Lifespan in the wild is 10–15 years, with some individuals living longer in
         captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Spotted Turtle',
      'Clemmys Guttata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The spotted turtle can be found in the Costa Rica loop of the Americas Pavilion, through the doors across from the North
         American river otter viewing, and past the bugs. The spotted turtle shares a habitat with the axolotl.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Spotted Turtle is a small, semi-aquatic turtle, typically 8–12 cm in shell length. Its carapace is dark brown to black
         with bright yellow or orange spots evenly distributed across the upper shell. The head, neck, and limbs are dark with
         smaller yellow markings, and the plastron (underside) is yellow or orange with dark blotches.'''.replace( '\n', ' ' ),
      '''Spotted Turtles inhabit shallow freshwater wetlands, marshes, ponds, and slow-moving streams in the eastern United States
         and southern Canada. They prefer areas with soft mud, abundant aquatic vegetation, and access to basking sites like logs
         or rocks.'''.replace( '\n', ' ' ),
      '''These turtles are omnivorous, feeding on aquatic invertebrates, small fish, carrion, and plant matter. They forage along
         the bottom and among vegetation, using their sharp beak to grasp prey. In zoos, they are fed a combination of insects,
         worms, aquatic plants, and commercially prepared turtle food.'''.replace( '\n', ' ' ),
      '''Spotted Turtles are generally solitary but may share basking sites. They are diurnal, spending much of the day foraging,
         basking, and swimming. During cold weather, they hibernate in mud or underwater. Males and females interact primarily
         during the breeding season.'''.replace( '\n', ' ' ),
      '''Camouflaged, spotted carapace helps blend with dappled sunlight and vegetation in wetlands. Strong limbs with webbed feet
         facilitate swimming, digging, and walking on soft substrates. Small size allows them to hide effectively from predators,
         while their omnivorous diet provides flexibility in food-limited habitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring, with females laying 3–8 eggs in soft, sandy soil near water. Eggs incubate for 70–90 days before
         hatching. Hatchlings are independent immediately. Lifespan is typically 20–30 years, with some individuals living longer in
         captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Timber Rattlesnake',
      'Crotalus Horridus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The timver rattlesnake can be found in an enclosure right at the end of the pavilion, on the right and across from the
         turtle habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Timber Rattlesnake is a large, venomous pit viper, typically 100–150 cm in length, with some individuals exceeding 180
         cm. Its colouration ranges from yellowish-brown to grey, with dark, V-shaped or chevron patterns along the back. The tail
         ends with a characteristic rattle used for warning predators. A heat-sensing pit is located between the eyes and nostrils.'''
         .replace( '\n', ' ' ),
      '''This species inhabits deciduous forests, mixed woodlands, and rugged hillsides across the eastern United States, from New
         England to the Midwest and the southern Appalachians. Timber Rattlesnakes prefer areas with rocky outcrops, logs, and
         burrows for shelter and hibernation.'''.replace( '\n', ' ' ),
      '''Timber Rattlesnakes are carnivorous ambush predators, feeding on small mammals, birds, amphibians, and occasionally other
         reptiles. They use their heat-sensing pits to detect warm-blooded prey, striking quickly and delivering venom to immobilize
         it. In captivity, they are fed rodents or other suitable prey items.'''.replace( '\n', ' ' ),
      '''These rattlesnakes are largely solitary except during mating or communal hibernation. They are diurnal or crepuscular
         depending on temperature, often basking to regulate body temperature. When threatened, they coil, hiss, and rattle to deter
         predators. Social interaction is limited, mainly occurring during breeding.'''.replace( '\n', ' ' ),
      '''Venomous fangs and potent venom allow them to subdue prey efficiently. Heat-sensing pits detect warm-blooded prey in
         low-light conditions. Camouflage patterns help them blend into leaf litter and forest floors. The rattle functions as a
         warning signal to avoid unnecessary conflicts with predators or humans.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late summer or early fall, with females storing sperm and laying eggs internally the following spring
         (ovoviviparous). Litters range from 5–20 young, which are independent at birth. Lifespan is typically 15–20 years, with
         longer lifespans possible in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Turquoise Tanager',
      'Tangara Mexicana',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The turquoise tanager can be spotted in the tanager aviary, in the Costa Rican section of the pavilion, through the doors
         across from the river otters, and past the bugs and alligators.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Turquoise Tanager is a medium-sized, vibrantly coloured songbird, measuring about 15–17 cm in length. Its body is
         predominantly bright turquoise-blue, with blackish wings and tail, and a slightly paler head. Its short, pointed beak is
         well-suited for picking fruit and catching insects.'''.replace( '\n', ' ' ),
      '''This species is native to tropical South America, including the Amazon Basin, Colombia, Venezuela, Ecuador, Peru, and
         northern Brazil. Turquoise Tanagers inhabit lowland forests, forest edges, plantations, and secondary growth, often near
         rivers and streams.'''.replace( '\n', ' ' ),
      '''Turquoise Tanagers are omnivorous, feeding on fruits, berries, nectar, and small insects. They forage actively in trees and
         shrubs, often moving in small flocks or mixed-species groups. In captivity, their diet includes fruits, insects, and
         commercially formulated bird diets.'''.replace( '\n', ' ' ),
      '''These tanagers are social and vocal, often found in groups that coordinate foraging. Their calls are high-pitched and
         melodious, aiding group cohesion and territorial awareness. Active and agile, they move quickly through the canopy while
         searching for food.'''.replace( '\n', ' ' ),
      '''Bright plumage aids in species recognition and courtship, while their agile flight allows navigation through dense forest.
         The short, pointed beak is versatile for both fruit consumption and insect hunting. Social flocking behaviour provides
         safety in numbers and enhances foraging efficiency.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season when food is abundant. Females build cup-shaped nests in shrubs or low trees and
         lay 2–3 eggs. Both parents participate in feeding and caring for the young until fledging. Lifespan is typically 5–8 years
         in the wild, with longer lifespans in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Two-Toed Sloth',
      'Choloepus Hoffmanni',
      14,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The two-toed sloths have an indoor viewable habitat, and an outdoor viewable habitat. Theeir outdoor viewing is located
         right near the David C. Onley Boardwalk, which connects the Americas to Africa. If you don't see the sloths in any of these
         enclosures, head inside the Americas Pavilion and you can spot them inside in the primate wing, just past the macaws.'''
         .replace( '\n', ' ' ),
      '''The two-toed sloth is endemic to the rainforests of South America, and is suited to be outside in the warm weather. You
         have a good chance of spotting them outside through May into September, with a chance as well on warm days in April or
         October. Even on warm days, the sloths opt to spend their time inside. During the cooler months, they can exclusively be
         spotted inside.'''.replace( '\n', ' ' ),
      '''The Two-Toed Sloth is a medium-sized arboreal mammal, measuring 50–70 cm in body length and weighing between 4 and 8 kg.
         Its coarse, greyish-brown fur often hosts algae, which provides natural camouflage in the canopy. The species is named for
         the two long, curved claws on each forelimb, which allow it to grasp branches securely while hanging upside down. Its face
         is round with dark markings around the eyes, giving it a mask-like appearance, and its overall body structure is adapted
         for a slow, deliberate lifestyle.'''.replace( '\n', ' ' ),
      '''Two-Toed Sloths are native to the tropical rainforests of Central and South America, with a range extending from Honduras
         through northern Brazil. They inhabit dense, humid forests with high canopies, preferring areas rich in trees and foliage
         for feeding and shelter. Sloths are rarely seen on the forest floor, except when moving between trees or during defecation,
         making them true canopy specialists that rely heavily on arboreal pathways for survival.'''.replace( '\n', ' ' ),
      '''Two-Toed Sloths are primarily folivorous, feeding mainly on leaves but occasionally consuming fruits, flowers, and tender
         shoots. Their diet is low in calories and difficult to digest, so they have developed a multi-chambered stomach that
         ferments plant material over several weeks, allowing efficient nutrient absorption. Sloths are deliberate and slow feeders,
         conserving energy while foraging among branches. In zoo settings, their diet is supplemented with leafy greens, vegetables,
         and select fruits to meet nutritional needs and encourage natural feeding behaviours.'''.replace( '\n', ' ' ),
      '''These sloths are largely solitary, spending most of their lives hanging upside down in the forest canopy. They are
         primarily nocturnal and crepuscular, resting or sleeping during the day and becoming more active at night. Movement is slow
         and energy-conserving, which also helps them avoid predators. Social interactions are limited, mainly occurring during
         mating periods, and young cling to their mother’s belly for several months after birth. Sloths descend to the ground
         infrequently, typically only to defecate, which is a vulnerable time that they navigate cautiously.'''.replace( '\n', ' ' ),
      '''Two-Toed Sloths possess a range of remarkable adaptations that allow them to thrive in the treetops. Their long, curved
         claws and strong limbs enable them to hang securely from branches and move through the canopy with careful, deliberate
         motions. The coarse fur often hosts algae, providing effective camouflage against predators, while their slow metabolism
         allows them to survive on a diet of tough, low-nutrient leaves. Reduced movement and energy-conserving behaviour decrease
         the risk of detection, and a flexible neck allows the sloth to survey its environment and feed efficiently without
         expending unnecessary energy. Together, these traits make the Two-Toed Sloth a highly specialized arboreal folivore,
         perfectly suited to the rainforest environment.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round, though timing may be influenced by food availability. Females give birth to a single offspring
         after a gestation period of 10–12 months. Newborns cling to the mother’s belly for several months, learning to navigate
         branches and forage for leaves. Sexual maturity is reached around three to four years of age. In the wild, Two-Toed Sloths
         can live 20–30 years, with individuals in captivity sometimes exceeding this lifespan due to regular feeding, veterinary
         care, and protection from predators.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has two female two-toed sloths, and younger sloth Sally, and an older sloth, Netta.'''.replace( '\n', ' ' )
   ),
   (
      'Western Blacknose Dace',
      'Rhinichthys Obtusus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Western blacknose dace can be found in an enclosure towards the exit of the pavilion, across from the river otter and
         snapping turtle underwater viewings.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Western Blacknose Dace is a small freshwater fish, typically 5–10 cm in length, with a slender, elongated body. Its
         back is olive-brown, fading to silvery sides and a pale underside. A distinctive dark stripe runs from the nose to the tail
         along each side, giving the species its name. The fins are generally transparent, and the mouth is slightly downturned,
         suited for bottom feeding.'''.replace( '\n', ' ' ),
      '''This species is native to central and eastern North America, inhabiting clear, cool streams and small rivers with gravel or
         sandy bottoms. Western Blacknose Dace prefer shallow, fast-flowing waters with abundant aquatic vegetation or invertebrate
         cover. They are often found near riffles and shallow pools that provide oxygen-rich water and protection from predators.'''
         .replace( '\n', ' ' ),
      '''Western Blacknose Dace are omnivorous, feeding on aquatic invertebrates such as insect larvae, small crustaceans, and algae.
         They forage along the substrate and among aquatic plants, using their small, downward-facing mouths to graze or pick prey.
         In captivity, they are fed small invertebrates, planktonic foods, and commercially prepared fish diets.'''
         .replace( '\n', ' ' ),
      '''These dace are active during the day and often form small schools for protection and efficient foraging. They are agile
         swimmers, capable of quick bursts to escape predators. Social interactions are minimal outside of breeding, but they
         communicate through body movements and subtle changes in swimming patterns.'''.replace( '\n', ' ' ),
      '''The Western Blacknose Dace has evolved several features for life in fast-flowing streams. Its streamlined, slender body
         allows efficient swimming against currents, while the downward-facing mouth aids in feeding along the substrate.
         Camouflaged colouration blends with gravel and sandy streambeds, helping avoid predators. Schooling behaviour increases
         survival by reducing individual predation risk and improving foraging efficiency in variable freshwater habitats.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in spring when water temperatures rise. Females scatter adhesive eggs among gravel and vegetation, which
         hatch after about one to two weeks. Juveniles are independent immediately upon hatching. Lifespan is typically 3–4 years,
         although some individuals may live longer in suitable habitats.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'White-Faced Saki',
      'Pithecia Pithecia',
      14,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The white-faced sakis have an indoor viewable habitat, and an outdoor viewable habitat. Theeir outdoor viewing is located
         right near the David C. Onley Boardwalk, which connects the Americas to Africa. If you don't see them in any of these
         enclosures, head inside the Americas Pavilion and you can spot them inside in the primate wing, just past the macaws.'''
         .replace( '\n', ' ' ),
      '''White-faced sakis are warm weather primates, and are only comfortable outside in the warmer months. They are frequently
         spotted outdoors from May through September, but may also venture outside on other warmer days. On any day, the sakis may
         decide to stay inside. During the cooler months, they can be found exclusively inside.'''.replace( '\n', ' ' ),
      '''The White-Faced Saki is a medium-sized New World monkey, with adults measuring approximately 30–45 cm in body length and
         weighing 2–3 kg. Males are strikingly marked, with black bodies and bright white faces and throat, while females and
         juveniles have more subdued brown or grey colouring with paler facial tones. Their dense, coarse fur, long bushy tails, and
         strong limbs make them agile climbers capable of moving swiftly through the canopy.'''.replace( '\n', ' ' ),
      '''White-Faced Sakis are native to northern South America, including Brazil, Guyana, Suriname, French Guiana, and parts of
         Venezuela. They inhabit lowland tropical rainforests, preferring tall trees and dense canopy cover near rivers and streams.
         They are arboreal specialists, rarely descending to the ground, and require continuous forest to forage and travel
         efficiently.'''.replace( '\n', ' ' ),
      '''These monkeys are primarily frugivorous, feeding on a variety of fruits, seeds, and nuts, but they also consume leaves,
         flowers, and insects. Their strong jaws and sharp teeth are adapted to crack hard seeds and extract nutritious pulp.
         White-Faced Sakis are selective feeders, often choosing ripe fruits and unripe seeds that are less likely to be competitive
         food sources. In zoos, they are offered a carefully balanced diet of fruits, vegetables, seeds, and occasional insect
         protein to mimic their natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''White-Faced Sakis are diurnal and live in small family groups, usually consisting of a monogamous pair and their offspring.
         They are quiet and relatively shy, using stealth and caution to move among branches. Grooming is minimal compared to other
         primates, but vocalisations, body postures, and scent marking help maintain social bonds and territory. They are highly
         territorial and will defend their home range from other groups using loud calls and displays.'''.replace( '\n', ' ' ),
      '''White-Faced Sakis have evolved several adaptations that allow them to thrive in the forest canopy. Their strong limbs and
         prehensile tails enable precise climbing and leaping between branches, while dense fur protects them from rain and insects.
         Powerful jaws and sharp teeth allow them to access seeds that many other animals cannot eat, giving them a competitive
         advantage. Their quiet, deliberate movements reduce detection by predators, and their social monogamy supports efficient
         parental care and territorial defence in dense forest habitats.'''.replace( '\n', ' ' ),
      '''White-Faced Sakis breed year-round, with females giving birth to a single infant after a gestation of about 150–180 days.
         Offspring cling to their mother’s belly for several weeks before riding on her back. Juveniles gradually learn to forage
         and move independently. Sexual maturity occurs around 3–4 years, and individuals can live 15–25 years in the wild, often
         longer in captivity due to veterinary care and consistent nutrition.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female white-faced saki, Cora.'''.replace( '\n', ' ' )
   ),
   (
      'Yellow-Banded Poison Dart Frog',
      'Dendrobates Leucomelas',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The yellow-banded poison dart frogs can be found in an enclosure just past the aquatic area and on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Yellow-Banded Poison Dart Frog is a small, vibrantly coloured amphibian, measuring about 3–4 cm in length. Its body is
         predominantly black with bright yellow bands or stripes across the back and limbs, creating a striking contrast that warns
         predators of its toxicity. The skin is smooth and shiny, and the frog has relatively large eyes for detecting movement and
         locating prey.'''.replace( '\n', ' ' ),
      '''This species is native to the tropical rainforests of northern South America, particularly Venezuela, Guyana, and Brazil.
         It inhabits lowland forests, forest edges, and areas near streams or pools where humidity is high. They prefer leaf litter,
         bromeliads, and other small crevices that provide shelter, moisture, and hunting grounds.'''.replace( '\n', ' ' ),
      '''Yellow-Banded Poison Dart Frogs are carnivorous, feeding primarily on small invertebrates such as ants, termites, and 
         mites. Their diet in the wild contributes to the production of skin toxins, which serve as chemical defences against
         predators. In zoos, they are fed tiny insects like fruit flies, springtails, and pinhead crickets to mimic natural feeding
         and support healthy growth.'''.replace( '\n', ' ' ),
      '''These frogs are diurnal and active hunters, using keen eyesight to stalk and capture prey. They are territorial, with males
         vocalizing to establish dominance and attract females. During breeding, males guard territories and may assist in
         transporting tadpoles to small water-filled pools or bromeliads, demonstrating remarkable parental care.'''
         .replace( '\n', ' ' ),
      '''Yellow-Banded Poison Dart Frogs possess several adaptations for survival in their rainforest habitat. Their bright
         yellow-and-black colouration acts as aposematic signalling, warning predators of their toxicity. Their small size and
         agility allow them to navigate leaf litter and dense vegetation efficiently. Skin toxins provide chemical defence,
         deterring predators and increasing survival odds. Their reproductive behaviour, including male parental care and tadpole
         transport, ensures offspring reach suitable aquatic microhabitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs throughout the year in humid rainforest conditions. Females lay eggs on moist surfaces, often in leaf
         litter, which males guard vigilantly. Once hatched, tadpoles are sometimes carried to small pools in bromeliads or other
         water-filled microhabitats. Juveniles are independent after metamorphosis. Lifespan is typically 5–8 years in the wild,
         often longer in captivity under proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Zebra Finch',
      'Taeniopygia Guttata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The zebra finch can be spotted in the tanager aviary, in the Costa Rican section of the pavilion, through the doors across
         from the river otters, and past the bugs and alligators.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Zebra Finch is a small songbird, approximately 10 cm in length and weighing around 10–15 grams. Males are easily
         identified by their black-and-white barred tail, orange cheeks, and bright beak, while females are plainer with a more
         muted grey body and a pale beak. Both sexes have a compact, agile body suited for quick flight and perching on fine
         branches.'''.replace( '\n', ' ' ),
      '''Zebra Finches are native to Australia, inhabiting dry grasslands, open savannas, and areas near water sources. They are
         highly adaptable and can live in both natural and human-modified environments, including farmland and urban areas, often
         forming large flocks.'''.replace( '\n', ' ' ),
      '''These birds are primarily granivorous, feeding on seeds of grasses and herbs. They also supplement their diet with insects,
         especially during the breeding season when extra protein is needed for chicks. In zoos, they are offered a mix of small
         seeds, grains, and occasional insect treats to mimic natural foraging.'''.replace( '\n', ' ' ),
      '''Zebra Finches are highly social and often found in large flocks. Males sing complex, melodic songs to attract females and
         maintain social cohesion, while females use subtle calls and body language. They are active and fast-moving, frequently
         hopping and flying among branches in search of food and social interaction.'''.replace( '\n', ' ' ),
      '''Zebra Finches are adapted to arid and variable environments. Their small size and agile flight allow quick escape from
         predators, and their social flocking behaviour reduces individual risk. Their diet flexibility, including both seeds and
         insects, supports survival in habitats where food availability changes seasonally. Their vocal learning allows males to
         develop and maintain complex songs, important for mating and group communication.'''.replace( '\n', ' ' ),
      '''Breeding can occur year-round when food and water are available. Pairs build cup-shaped nests in shrubs or trees and lay
         4–6 eggs per clutch. Both parents incubate the eggs and feed the hatchlings, which fledge after about three weeks. Zebra
         Finches can live 5–9 years in the wild and longer in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Canadian Domain
   (
      'Cougar',
      'Puma Concolor',
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The cougars can be spotted by heading partway down the hill of the Canadian domain exhibit. A bit more than halfway down
         the hill, and across from the male wood bison paddock you will find the cougars.'''.replace( '\n', ' ' ),
      '''Cougars are well-adapted to the cold and can stay outside all through the winter. If the domain is open then the cougars
         should be viewable. The cougars at the zoo have access to a behind-the-scenes indoor habitat which they often spend time
         in. The cougars are fairly interested in zoo guests, and thus if you don't see them right away, but wait for a few minutes,
         you may get a close encounter with one of them. Also be sure to check for them inside their cave in the back right corner
         of the habitat, on top of all of the platforms, and along the fence on the left side of the exhibit.'''.replace( '\n', ' ' ),
      '''The cougar, also known as the mountain lion, puma, or panther, is a large, muscular cat, with adults measuring 1.5–2.4 m in
         total length, including the tail, and weighing 50–100 kg. Its coat is short and tawny, ranging from light brown to reddish,
         with a lighter underbelly. The long tail helps with balance while stalking or leaping, and its strong legs and retractable
         claws are adapted for ambushing prey.'''.replace( '\n', ' ' ),
      '''Cougars are native to the Americas, with historical ranges covering nearly all of North and South America. Today, they
         inhabit forests, mountains, deserts, and open grasslands in North America, including Canada. They require large territories
         with sufficient prey populations, often ranging over tens or even hundreds of square kilometres.'''.replace( '\n', ' ' ),
      '''Cougars are obligate carnivores and ambush predators, feeding primarily on deer, elk, and smaller mammals such as rabbits
         or rodents. They rely on stealth, patience, and powerful bursts of speed to capture prey. In zoos, cougars are fed a diet
         of meat that mimics their natural intake, including whole prey items or meat supplemented with vitamins and minerals.'''
         .replace( '\n', ' ' ),
      '''Cougars are solitary, territorial animals, with males defending large territories that may overlap with several females.
         They are mostly nocturnal or crepuscular, becoming more active at dawn and dusk. Cougars communicate through scent
         markings, vocalisations such as growls or screams, and visual cues. Despite their size and power, they are generally
         elusive and rarely seen in the wild.'''.replace( '\n', ' ' ),
      '''Cougars have evolved for stealth and power. Their muscular bodies and long limbs allow them to leap great distances and
         move silently through dense forests. Retractable claws and sharp teeth are designed for gripping and dispatching prey,
         while keen eyesight and hearing aid hunting in low-light conditions. Their large home ranges reflect their need to track
         and secure sufficient food, and solitary behaviour reduces competition for resources.'''.replace( '\n', ' ' ),
      '''Cougars breed year-round, though births peak when prey is abundant. Females give birth to 1–6 kittens in secluded dens.
         Young are born blind and helpless, and remain with the mother for up to two years, learning hunting skills and territory
         navigation. Lifespan is typically 8–13 years in the wild and up to 20 years in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two cougars--a male, Bowen, and a female Teeka. They are on exhibit together for companionship.'''
         .replace( '\n', ' ' )
   ),
   (
      'Grizzly Bear',
      'Ursus Arctos Horribilis',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The grizzly bear habitat is at the bottom of the Canadian domain hill. Once you reach the bottom of the hill, you can stick
         to the right to find the grizzly bear.'''.replace( '\n', ' ' ),
      '''The grizzly bear is viewable seasonably due to its hibernating patterns. Grizzly bears hibernate from sometime in November,
         usually until sometime in March, depending on the exact weather conditions of that year. Leading up to and coming out of
         hibernation, grizzly bears spend more of their time resting, and thus the bears at the zoo may be less visible as they
         spend more of their time resting off-display. The grizzly bear can usually be spotted on exhibit from April through
         October. The grizzly bear at the Toronto Zoo, Shintay, is in her golden years and may choose to spend some of her time
         behind the scenes. She can often be seen resting in the shade near the viewing areas of the exhibit, or by peering through
         the bars into her behind-the-scenes area. She is most active during wild encounters, where she will forage around her
         habitat, enjoying a variety of foods which she retrieves by performing enrichment activities.'''.replace( '\n', ' ' ),
      '''The Grizzly Bear is a large, powerful bear, with adult males weighing 270–360 kg and females 130–200 kg. They stand 1–1.5 m
         at the shoulder and can reach up to 2.5 m in length from nose to tail. Their thick fur ranges from blonde to dark brown,
         often with a silvery or “grizzled” appearance on the shoulders and back, giving the species its common name. They have a
         distinctive hump on their shoulders, strong claws for digging, and large, rounded heads with keen eyesight and smell.'''
         .replace( '\n', ' ' ),
      '''Grizzly Bears are native to North America, inhabiting forests, alpine meadows, tundra edges, and river valleys, primarily
         in Canada, Alaska, and parts of the northwestern United States. They require large territories to support their omnivorous
         diet, with access to food sources that vary seasonally, such as berries, fish, roots, and mammals. They often follow
         seasonal migration routes to track available food.'''.replace( '\n', ' ' ),
      '''Grizzly Bears are omnivorous and opportunistic feeders. They eat a wide variety of foods, including berries, nuts, roots,
         insects, fish, and small to large mammals. Salmon runs in rivers are particularly important for nutrition in coastal areas.
         In zoos, Grizzlies are provided a balanced diet that includes fruits, vegetables, meat, and enrichment foods to stimulate
         foraging behaviours.'''.replace( '\n', ' ' ),
      '''Grizzly Bears are largely solitary, except for females with cubs or temporary gatherings at rich food sources such as
         salmon streams. They are diurnal and crepuscular, spending mornings and evenings foraging. Behaviour includes digging for
         roots, climbing, swimming, and rolling in vegetation. Cubs stay with their mother for up to two and a half years, learning
         survival and hunting skills. Communication occurs through vocalisations, scent marking, and visual displays.'''
         .replace( '\n', ' ' ),
      '''Grizzly Bears possess numerous adaptations for survival in varied habitats. Their strong limbs and long claws are ideal for
         digging, climbing, and catching prey, while thick fur insulates them against cold temperatures. Powerful jaws and teeth
         allow them to consume a wide range of foods. Seasonal hibernation enables them to conserve energy when food is scarce, and
         their keen sense of smell helps locate food over long distances. Social flexibility and territorial behaviour optimize
         survival and resource use in diverse environments.'''.replace( '\n', ' ' ),
      '''Grizzly Bears breed in late spring to early summer, with females giving birth during hibernation to 1–4 cubs. Cubs are born
         blind and weigh less than a kilogram, remaining dependent on the mother’s milk and protection for about two years. Sexual
         maturity occurs at 4–6 years of age. Lifespan is typically 20–25 years in the wild and up to 30 years in captivity.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one elderly grizzly bear, Shintay. Shintay is in her golden years and spends much of her time
         resting. Your best chance of seeing her active is to visit her habitat during a wild encounter.'''.replace( '\n', ' ' )
   ),
   (
      'Raccoon',
      'Procyon Lotor',
      -35,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The raccoons can be spotted on your way down the hill. The raccoon habitat will be the first one you see, up the stairs to
         your left.'''.replace( '\n', ' ' ),
      '''Raccoons can stay outside the extreme cold, and should be viewable when the domain is open.''',
      '''The Raccoon is a small to medium-sized mammal, measuring 40–70 cm in body length with a bushy, ringed tail of 20–40 cm. Its
         fur is grey-brown with a distinctive black “mask” across the eyes and black rings on the tail. Raccoons have nimble, highly
         dexterous front paws and sharp claws, which they use to manipulate food, climb trees, and explore their surroundings.'''
         .replace( '\n', ' ' ),
      '''Raccoons are native to North America and are highly adaptable, inhabiting forests, wetlands, suburban areas, and urban
         environments. They prefer areas near water, such as streams, ponds, or rivers, but can thrive in cities and towns by
         exploiting available food sources and shelter. Their flexible habitat requirements make them one of the most widespread
         North American mammals.'''.replace( '\n', ' ' ),
      '''Raccoons are omnivorous opportunists, feeding on fruits, nuts, insects, small mammals, amphibians, and human-provided foods
         like garbage or pet food. In the wild, they forage mostly at night, using their sensitive front paws to feel and manipulate
         objects. In zoos, their diet includes a variety of fruits, vegetables, protein sources, and enrichment foods to encourage
         natural foraging behaviour.'''.replace( '\n', ' ' ),
      '''Raccoons are primarily nocturnal and largely solitary, though some may gather near abundant food sources. They are
         intelligent and curious, using problem-solving skills to access food or navigate obstacles. Communication occurs through
         vocalisations, body language, and scent marking. Breeding is seasonal, and mothers raise their young alone.'''
         .replace( '\n', ' ' ),
      '''Raccoons are highly adaptable both behaviourally and physically. Their dexterous front paws allow precise manipulation of
         objects, making them excellent foragers and problem-solvers. The dark facial mask may reduce glare and enhance night
         vision, while their omnivorous diet enables survival in diverse environments. Their intelligence and flexible behaviour
         allow them to thrive in both natural and urban habitats.'''.replace( '\n', ' ' ),
      '''Mating occurs in late winter to early spring. Females give birth to 2–5 kits in dens located in hollow trees, burrows, or
         abandoned buildings. Kits remain with the mother for several months, learning foraging and survival skills. Raccoons
         typically live 2–5 years in the wild but can reach 10–15 years in captivity under proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Wood Bison',
      'Bison Bison Athabascae',
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''There are two points in the domain where you can spot wood bison. Partway down the hill, across from the cougars, you will
         find the paddock with the male bison. At the bottom of the hill and heading all the way down the path, and not to the right
         you will find the female herd of bison'''.replace( '\n', ' ' ),
      '''Wood bison can survive extremely harsh conditions, and will be viewable as long as the domain is open.''',
      '''The Wood Bison is a massive, muscular herbivore, with adult males weighing 450–900 kg and females 320–540 kg. They stand
         about 1.8–2.1 m at the shoulder and can reach up to 3.5 m in length, including the head and tail. Their thick dark brown
         fur, large heads, and pronounced shoulder humps distinguish them from plains bison. Both sexes have short, curved horns
         used for defense and social interactions.'''.replace( '\n', ' ' ),
      '''Wood Bison are native to the boreal forests and grasslands of northern Canada and Alaska. They historically roamed vast
         territories but were once near extinction due to overhunting and habitat loss. Today, they inhabit protected areas and
         national parks, often forming herds that travel seasonally in search of forage, water, and shelter from harsh winters.'''
         .replace( '\n', ' ' ),
      '''Wood Bison are herbivorous grazers, feeding on grasses, sedges, shrubs, and aquatic vegetation. Their large, muscular jaws
         and specialized teeth allow them to grind tough plant material efficiently. In captivity, they are fed hay, grasses, and
         specially formulated herbivore diets to mimic their natural intake and maintain health.'''.replace( '\n', ' ' ),
      '''Wood Bison are social and form herds that provide protection and structure. Herds are often led by older females, while
         males may form bachelor groups outside of mating season. Seasonal rutting sees males competing for mating opportunities
         through displays of strength, horn clashes, and vocalizations. Bison are generally peaceful grazers but will defend
         themselves or their young if threatened.'''.replace( '\n', ' ' ),
      '''Wood Bison are adapted to cold, northern environments. Their thick fur insulates against freezing temperatures, while their
         large size reduces heat loss. Powerful shoulders and humps support strong neck muscles for grazing snow-covered grasses in
         winter. Wide hooves provide stability on soft ground and snow. Herding behaviour offers protection from predators, while
         their digestive system efficiently extracts nutrients from fibrous plant material, allowing survival in nutrient-poor
         boreal ecosystems.'''.replace( '\n', ' ' ),
      '''Mating occurs during late summer, with dominant males competing for females. Females give birth to a single calf after a
         gestation of about 9.5 months, usually in late spring when food is abundant. Calves are mobile shortly after birth and
         remain with the mother for the first year. Sexual maturity occurs around 2–3 years for females and 3–4 years for males.
         Lifespan is typically 12–20 years in the wild, often longer in captivity under managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Africa Savanna
   (
      'African Lion',
      'Panthera Leo',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''You will find the African lions by taking the Africa Savanna loop. The lions are between the baboons and zebras, and eland
         and hyenas. There is a cave that has glass viewing into the lion habitat, as well as open-air viewings on either side of
         the cave. The lions can most often be seen from the open-air viewing across from the elands. The lions are one of the most 
         lethargic species at the zoo. They spend much of their time sleeping in the back of their habitat, above the underground
         viewing. Your best chance to see them active is to visit their exhibit first thing in the morning.'''.replace( '\n', ' ' ),
      '''The African lions are more or less viewable year round. During the den of winter they are given access to indoor spaces so
         they may decide to be inside if it is particularly cold or icy. In the winter, they are most often seen in their den, since
         this space is heated. You have the best chance of spotting the lions being active by visiting on a cooler day in the spring
         or fall.'''.replace( '\n', ' ' ),
      '''The African Lion is a large, muscular cat, with males weighing 150–250 kg and females 120–182 kg. Males are distinguished
         by their impressive manes, which vary in colour from golden to dark brown, while females lack manes and are slightly
         smaller and more agile. Lions have powerful legs, retractable claws, and sharp teeth adapted for killing large prey. Their
         tawny coats provide camouflage in the dry savanna grasslands, and their expressive faces, including a short, rounded muzzle,
         are instantly recognizable.'''.replace( '\n', ' ' ),
      '''African Lions inhabit the savannas, grasslands, and open woodlands of sub-Saharan Africa. They prefer areas with sufficient
         prey density, access to water, and some cover for stalking. Historically widespread, their populations have declined due to
         habitat loss, human-wildlife conflict, and hunting. Lions are territorial, with prides occupying areas that can range from
         20 to over 400 km², depending on prey availability.'''.replace( '\n', ' ' ),
      '''Lions are obligate carnivores and apex predators. They primarily hunt large ungulates such as zebras, wildebeest, and
         antelopes, often using cooperative hunting strategies in prides. Females are the primary hunters, relying on stealth,
         teamwork, and bursts of speed to ambush prey. Lions also scavenge when opportunities arise. In zoos, lions are fed a varied
         diet of meat, supplemented with bones for dental health and enrichment to encourage natural hunting behaviours.'''
         .replace( '\n', ' ' ),
      '''African Lions are the most social of all big cats, living in prides consisting of related females, their offspring, and a
         coalition of males. Social bonds are maintained through grooming, vocalizations, and cooperative care of young. Territorial
         males patrol and defend the pride’s range, while females coordinate hunting and cub-rearing. Lions are largely nocturnal or
         crepuscular, resting for up to 20 hours a day to conserve energy for hunting.'''.replace( '\n', ' ' ),
      '''Lions are highly adapted for life as top predators in the savanna. Their muscular bodies, retractable claws, and strong
         jaws allow them to capture and subdue large prey. Their tawny colouration blends with dry grass, aiding in stealth, while
         social hunting increases success rates. Sharp senses of sight, smell, and hearing help detect prey and rivals over long
         distances. Male manes provide protection during fights and may signal strength to rivals and potential mates. Lions’
         endurance and cooperative strategies make them effective hunters and dominant apex predators.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity around 3–4 years, males around 4–5 years. Breeding can occur year-round, with females giving
         birth to 1–4 cubs after a gestation of approximately 110 days. Cubs are born blind and helpless, requiring intensive
         maternal care. They are introduced to the pride gradually, learning social skills and hunting techniques through
         observation and play. Lifespan in the wild is typically 10–14 years, with lions living longer under zoo care.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two female, white African lions named Lemon and Makali.'''.replace( '\n', ' ' )
   ),
   (
      'African Penguin',
      'Spheniscus Demersus',
      2,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The African penguin habitat can be found either at the end or the beginning of the Africa Savanna loop, depending on which
         direction you head in. You can access the penguin habitat across from the watusi cattle. Even on warmer days many of the
         penguins may choose to spend their time indoors. Many of the penguins also enjoy being in shade along the back of their
         enclosure among the trees or in between the rocks. They are most likely to be swimming on temperate days.'''
         .replace( '\n', ' ' ),
      '''African penguins are adapted to handle temperate climates, and thus can be seen outdoors for most of the year. They should
         be viewable on any day between April and November where the temperature is above 0°C and there is no snow on the ground.
         They may additionally be viewable on some days in March. During the coldest months they can be seen exclusively in their
         indoor habitat.'''.replace( '\n', ' ' ),
      '''The African Penguin is a medium-sized seabird, measuring 60–70 cm in height and weighing 2–4 kg. It has distinctive
         black-and-white plumage, with a black facial mask and a series of black spots on its chest, which are unique to each
         individual. Its beak is black and robust, adapted for catching fish, and webbed feet aid in swimming. Adults are sleek and
         streamlined, while chicks have fluffy grey down that they molt before reaching maturity.'''.replace( '\n', ' ' ),
      '''African Penguins are native to the southwestern coasts of Africa, primarily South Africa and Namibia. They inhabit rocky
         islands, coastal beaches, and guano-covered areas where they nest in burrows, under shrubs, or in man-made structures.
         These penguins are highly social, forming large breeding colonies and relying on the nearby ocean for foraging.'''
         .replace( '\n', ' ' ),
      '''These penguins are carnivorous, feeding almost exclusively on small fish such as anchovies and sardines, and occasionally
         squid or crustaceans. They are excellent swimmers and divers, capable of reaching depths of 130 m and speeds up to 20 km/h
         to catch prey. In zoos, they are fed fresh fish diets that mimic natural intake, and enrichment activities encourage diving
         and foraging behaviours.'''.replace( '\n', ' ' ),
      '''African Penguins are highly social, forming large colonies that facilitate breeding and protection against predators. They
         are vocal birds, using braying, trumpeting, and other calls to communicate with mates and chicks. Courtship involves
         elaborate displays, including head bowing and preening. Penguins are monogamous for a breeding season, and both parents
         share responsibilities in incubating eggs and feeding chicks.'''.replace( '\n', ' ' ),
      '''African Penguins are well-adapted to both land and sea. Their streamlined bodies, flipper-like wings, and webbed feet make
         them excellent swimmers and divers, while counter-shaded plumage provides camouflage from predators above and below water.
         Specialized glands remove excess salt from their bodies, allowing them to drink seawater. Nesting behaviour in burrows or
         under cover protects eggs and chicks from heat and predators, ensuring reproductive success in a harsh coastal environment.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs mainly from March to May, but timing can vary. Females lay one or two eggs, which both parents incubate for
         about 38–42 days. Chicks remain in nests for several weeks and are fed regurgitated fish by both parents until fledging.
         Sexual maturity is reached around 3–4 years. African Penguins are long-lived, with lifespans of 10–15 years in the wild and
         longer in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Cheetah',
      'Acinonyx Jubatus',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The cheetahs can be seen on the Africa Savanna loop, between the white rhinos and baboons, and across from the zeberas.
         Most of the time, the cheetahs can be seen in the back right part of their enclosure. Look for a head just past the trees,
         and in Indo-Malaya in the habitat off the boardwalk connecting Indo-Malaya to Africa. Your best chance to see the cheetahs
         active is early in the day.'''.replace( '\n', ' ' ),
      '''The cheetahs are on exhibit year-round. In the coldest months of the year they are given access to indoor spaces, so on
         very cold and/or icy days they may decide to spend their time inside. They are most active on cooler days in the fall and
         spring.'''.replace( '\n', ' ' ),
      '''The Cheetah is a slender, long-legged cat built for speed, weighing 34–56 kg and measuring up to 2.3 m in total length,
         including the tail. Its tan coat is covered in solid black spots, and distinctive black “tear marks” run from the eyes to
         the mouth. Unlike other big cats, cheetahs have a smaller head, lightweight frame, long tail for balance, and
         semi-retractable claws that provide traction during high-speed chases.'''.replace( '\n', ' ' ),
      '''Cheetahs inhabit open savannas, grasslands, and semi-arid regions of sub-Saharan Africa, with a small, critically
         endangered population in Iran. They prefer open habitats where their speed can be fully utilized and where visibility
         allows them to spot prey from a distance. Their range has declined dramatically due to habitat loss, human conflict, and
         competition with other large predators.'''.replace( '\n', ' ' ),
      '''Cheetahs are carnivorous and specialize in hunting medium-sized antelope such as gazelles and impala. Hunts rely on
         daylight vision, stealthy approaches, and explosive sprints rather than ambush or strength. After a successful chase,
         cheetahs must rest before eating due to extreme physical exertion. In zoos, they are fed a carefully managed meat-based
         diet, often with enrichment that encourages stalking or running behaviours.'''.replace( '\n', ' ' ),
      '''Unlike most cats, cheetahs display unique social patterns. Females are solitary except when raising cubs, while males may
         form lifelong coalitions, often with brothers. Cheetahs are primarily diurnal, reducing competition with nocturnal
         predators like lions and hyenas. They communicate using chirps, purrs, and body postures rather than roars.'''
         .replace( '\n', ' ' ),
      '''Cheetahs possess extreme adaptations for speed and acceleration. Their elongated spine increases stride length, while large
         nasal passages and lungs supply oxygen during sprints. Semi-retractable claws act like running spikes, and a long tail
         provides balance during rapid turns. Lightweight bones and reduced muscle mass maximize acceleration, but these adaptations
         come at the cost of strength, making cheetahs vulnerable to larger predators and limiting their ability to defend kills.'''
         .replace( '\n', ' ' ),
      '''Females give birth to 2–6 cubs after a gestation of about 90–95 days. Cubs are born with a mantle of long grey fur along
         their backs, which may provide camouflage or mimic the appearance of honey badgers. Mortality rates are high in the wild
         due to predation. Cheetahs reach sexual maturity around 2–3 years and typically live 10–12 years in the wild, with longer
         lifespans in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a number of cheetahs, but there are only ever one or two on exhibit together.'''
         .replace( '\n', ' ' )
   ),
   (
      'Common Eland',
      'Taurotragus Oryx',
      8,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The eland habitat can be accessed in the Africa Savanna loop across from the white lion habitat.''',
      '''Elands are one of the most-cold resistant antelopes, and can be seen outside during most months of the year through April
         into November. They may also be viewable on warmer March days, or other winter days where there is little to no snow on the
         ground.'''.replace( '\n', ' ' ),
      '''The Common Eland is the largest species of antelope, with adult males weighing up to 900 kg and females up to 600 kg. They
         stand around 1.6–1.8 m at the shoulder and have a heavy, robust build. Their coat ranges from tan to light brown, often
         with faint white vertical stripes along the sides. Both males and females possess long, spiralled horns, which are thicker
         and more tightly coiled in males. A loose fold of skin, or dewlap, hangs from the throat, especially pronounced in males.'''
         .replace( '\n', ' ' ),
      '''Common Eland are widely distributed across eastern and southern Africa. They inhabit savannas, open woodlands, grasslands,
         and lightly forested areas, favouring regions with a mix of grazing and browsing opportunities. They are highly adaptable
         and can tolerate both dry and moderately wooded environments, often moving seasonally in response to rainfall and food
         availability.'''.replace( '\n', ' ' ),
      '''Eland are mixed feeders, consuming both grasses and browse such as leaves, shoots, fruits, and herbs. This flexible diet
         allows them to thrive in a wide range of habitats and cope with seasonal changes in vegetation. In zoos, they are fed hay,
         grasses, browse, and specially formulated herbivore pellets to replicate natural nutritional balance and support digestive
         health.'''.replace( '\n', ' ' ),
      '''Common Eland are social animals, forming herds that may range from a few individuals to several dozen. Herds are often
         segregated by sex outside the breeding season, though mixed groups are common. Despite their size, eland are surprisingly
         agile and can run swiftly and leap over obstacles when threatened. They are generally calm and non-aggressive, relying on
         vigilance and group awareness for protection.'''.replace( '\n', ' ' ),
      '''Common Eland are well adapted to life in open savannas and woodlands. Their large body size allows them to conserve water
         efficiently and survive on lower-quality forage. Long legs and strong muscles enable sustained movement across large
         territories, while their mixed-feeding strategy provides dietary flexibility during dry seasons. Spiral horns serve both as
         defensive tools and as signals during social interactions, reducing the need for physical conflict.'''.replace( '\n', ' ' ),
      '''Breeding typically peaks after the rainy season when food is abundant. Females give birth to a single calf after a
         gestation period of about 9 months. Calves are hidden for the first few weeks of life and then gradually introduced to the
         herd. Sexual maturity is reached around 2–3 years. Common Eland can live 15–20 years in the wild and longer in captivity.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to three eland, which can all be seen on exhibit together.''',
   ),
   (
      'Greater Kudu',
      'Tragelaphus Strepsiceros',
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The greater kudu habitat is located on the Africa Savanna loop. The habitat is large, and has three different viewing areas.
         The most prominent one is located across from the white rhinos. The second one is on a offshoot path between the rhinos and
         hippos, and the third is accessed from inside the Africa Rainforest Pavilion, just past the meerkats. The kudu share a
         habitat with the savanna birds--marabou storks, Southern ground hornbills, and the white-headed vulture.'''
         .replace( '\n', ' ' ),
      '''Kudu are a warm weather antelope with little protection from the cold, and thus they are generally only viewable during the
         warmer months of the year. They can generally be viewed from May until October, and perhaps also on other warm days in
         spring or fall.'''.replace( '\n', ' ' ),
      '''The Greater Kudu is a large, slender antelope known for its impressive spiral horns, which are found only in males and can
         exceed 1.5 m in length. Adults stand about 1.3–1.6 m at the shoulder and weigh 190–270 kg. Their coat is grey-brown with
         6–10 vertical white stripes along the sides, and a white chevron between the eyes. Large ears provide excellent hearing,
         and their long legs and narrow build give them a graceful appearance.'''.replace( '\n', ' ' ),
      '''Greater Kudus are native to eastern and southern Africa, inhabiting savannas, woodlands, scrublands, and areas with dense
         bush cover. They prefer regions that provide a mix of open spaces for movement and thick vegetation for concealment. Kudus
         are well adapted to dry environments and can survive with limited access to surface water.'''.replace( '\n', ' ' ),
      '''Greater Kudus are browsers, feeding primarily on leaves, shoots, vines, fruits, and flowers. Their diet shifts seasonally
         depending on availability, allowing them to cope with drought conditions. In zoological settings, kudus are provided with
         hay, browse, leafy greens, and herbivore pellets to replicate their natural diet and ensure proper nutrition.'''
         .replace( '\n', ' ' ),
      '''Greater Kudus are generally shy and elusive animals. Females and juveniles form small herds, while adult males are more
         solitary or form loose bachelor groups. Kudus rely on vigilance and sudden bursts of speed to escape predators rather than
         confrontation. When threatened, they may freeze in place, relying on camouflage, before leaping away through dense
         vegetation.'''.replace( '\n', ' ' ),
      '''Greater Kudus possess several adaptations for survival in wooded savannas. Their striped coats break up their outline,
         providing effective camouflage in dappled light. Large ears enhance their ability to detect predators, while powerful hind
         legs allow them to leap over obstacles and flee rapidly. Males’ spiral horns are used in ritualized sparring rather than
         lethal combat, reducing injury while maintaining social hierarchy.'''.replace( '\n', ' ' ),
      '''Breeding usually occurs during or shortly after the rainy season. After a gestation period of approximately 8–9 months,
         females give birth to a single calf. Calves remain hidden for several weeks before joining the group. Sexual maturity is
         reached around 1.5–3 years. Greater Kudus typically live 15–20 years in the wild and may live longer in managed care.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to three female greater kudu, which all go out on exhibit together.'''.replace( '\n', ' ' )
   ),
   (
      'Grevy\'s Zebra',
      'Equus Grevyi',
      2,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The Grevy's zebra habitat is found on the Africa Savanna loop, across from the cheetahs. The zebra enclosure is very long
         and has a very different viewing points. The best spot to see them is usually across from the glass viewing area from which
         the cheetahs and baboons can both be seen. The zebras tend to move across their habitat quite a lot as they graze, so you
         may have to wait for them to come your way to get the best view.'''.replace( '\n', ' ' ),
      '''Grevy's zebras are a very hardy species, tolerating temperatures around freezing. They are generally viewable outside from
         ealrly Spring through to the start of winter. On a lot of warmer winter days they would be able to go outside if not for
         the snow/ice on the ground. Zebras have no adaptation to allow them to move across the snow, and if one were to fall, it
         could be life-threatening.'''.replace( '\n', ' ' ),
      '''Grevy’s Zebra is the largest and most distinctive of all zebra species. Adults stand up to 1.6 m at the shoulder and weigh
         350–450 kg. Their narrow, closely spaced black-and-white stripes extend over the entire body, including the belly, and
         contrast with a white rump and large rounded ears. The mane is tall and erect, running from the head to the shoulders.
         Compared to other zebras, Grevy’s zebras have a more mule-like appearance and longer legs.'''.replace( '\n', ' ' ),
      '''Grevy’s Zebras are native to arid and semi-arid regions of northern Kenya and southern Ethiopia. They inhabit dry
         grasslands, savannas, and open plains where vegetation is sparse and water sources are widely spaced. Unlike other zebras,
         they are highly adapted to dry environments and can travel long distances to access water during droughts.'''
         .replace( '\n', ' ' ),
      '''Grevy’s Zebras are primarily grazers, feeding on coarse grasses that many other herbivores avoid. During dry seasons, they
         may also browse on shrubs and herbs. Their digestive system allows them to extract nutrients efficiently from low-quality
         forage. In zoos, they are fed hay, grasses, and specially formulated herbivore diets to replicate their natural intake and
         maintain digestive health.'''.replace( '\n', ' ' ),
      '''Unlike plains zebras, Grevy’s Zebras do not form permanent harems. Females move freely between territories, often forming
         temporary groups with other females and their young. Males defend territories that contain key resources, especially water
         and grazing areas. Communication includes braying calls, ear positioning, and body posture. Foals are strongly bonded to
         their mothers and remain close during early development.'''.replace( '\n', ' ' ),
      '''Grevy’s Zebras possess several adaptations for survival in hot, dry environments. Their narrow stripes may help regulate
         body temperature and deter biting insects. Large ears improve heat dissipation and enhance hearing. Long legs and efficient
         movement allow them to travel great distances between grazing areas and water sources. Their ability to digest tough
         grasses gives them a competitive advantage in arid landscapes where food quality is poor.'''.replace( '\n', ' ' ),
      '''Breeding can occur year-round, though births often peak during periods of increased rainfall. Females give birth to a
         single foal after a gestation of approximately 13 months. Foals are able to stand and walk shortly after birth and rely
         heavily on their mother’s protection. Sexual maturity is reached around 3–4 years. Grevy’s Zebras can live 18–25 years in
         the wild and longer in captivity.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to five grevy's zebras, including some males and some females. They never all go out on exhibit
         together. If you see one zebra on its own, it is likely one of the males. If you see several zebras together, it is likely
         to be the females, but sometimes a male will be on exhibit with the females, particularly for breeding purposes.'''
         .replace( '\n', ' ' )
   ),
   ( # Also in Kids Zoo
      'Marabou Stork',
      'Leptoptilos Crumenifer',
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''There are a couple different spots to spot the marabou storks in the Africa Savanna. They go on exhibit with the kudu and
         can be spotted in that habitat. You may see them from any of the three viewings, at the savanna overlook in the African 
         Rainforest Pavilion by the meerkats, on the offshoot between the hippos and rhinos, or at the main viewing across from the
         white rhinos. You may have the most success on the offshoot path between the hippos and rhinos. The other spot to see them
         is by the zebra enclosure, roughly across from the main cheetah viewing.'''.replace( '\n', ' ' ),
      '''Marabou storks are a warm weather bird and can only go on exhibit in the warmer months, particularly from June to September,
         but perhaps longer than that, depending on the specific weather.'''.replace( '\n', ' ' ),
      '''The Marabou Stork is one of the largest flying birds in Africa, standing up to 1.5 m tall with a wingspan reaching 3.2 m.
         It has a bare, pinkish head and neck, a massive gray bill, long legs, and a distinctive inflatable throat pouch. The body
         is mostly black and white, with loose, shaggy feathers that give it a hunched appearance.'''.replace( '\n', ' ' ),
      '''Marabou Storks are widely distributed across sub-Saharan Africa. They inhabit open savannas, wetlands, floodplains,
         lakeshores, and even urban areas near landfills. Their adaptability allows them to thrive in both natural ecosystems and
         human-modified landscapes.'''.replace( '\n', ' ' ),
      '''Primarily scavengers, Marabou Storks feed on carrion left behind by large predators such as lions and hyenas. They also
         hunt live prey, including fish, frogs, insects, small mammals, and reptiles. Their bald head helps keep them clean while
         feeding inside carcasses, reducing the spread of bacteria.'''.replace( '\n', ' ' ),
      '''Marabou Storks are often seen standing motionless or soaring on thermal currents. They may feed alone or gather in large
         groups at carcasses or feeding sites. Breeding pairs nest in tall trees or on cliffs, often forming loose colonies.
         Courtship includes bill-clattering and inflation of the throat pouch.'''.replace( '\n', ' ' ),
      '''The bald head and neck prevent feathers from becoming fouled during scavenging. Their powerful bill is capable of tearing
         flesh and capturing prey. Large wings allow efficient soaring, conserving energy while covering great distances in search
         of food. The throat pouch may play a role in display and temperature regulation.'''.replace( '\n', ' ' ),
      '''Marabou Storks lay 2–3 eggs in large stick nests. Both parents incubate the eggs and feed the chicks by regurgitation.
         Chicks fledge after about 4 months but may remain dependent on adults for some time. In the wild, Marabou Storks can live
         25 years or more.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Masai Giraffe',
      'Giraffa Camelopardalis Tippelskirchi',
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The Masai giraffe enclosure can be found near the start or end of the Africa Savanna loop, across from the entrance to the
         African Rainforest Pavilion near the lemurs. One of the viewings of the giraffes' outdoor habitat is located up the
         elevated pathway behind the hippo habitat.'''.replace( '\n', ' ' ),
      '''Masai giraffes are warm-weather animals and have little protection against the cold. They can usually be seen outside from
         May until October and on other days above 10°C. If you don't see them outside, you can stop by the giraffe house, right
         beside their outdoor habitat and see them inside.'''.replace( '\n', ' ' ),
      '''The Masai giraffe is the tallest land animal on Earth, instantly recognizable by its towering height and bold, irregular
         star-shaped patches. These patches are darker and more jagged than those of other giraffe subspecies, with uneven edges
         that resemble vine leaves. Adults typically stand 4.5–5.7 m (15–18.7 ft) tall, with males heavier and slightly taller than
         females. Their long legs, elongated necks, and horn-like structures called ossicones give them a striking and unmistakable
         silhouette on the savanna.'''.replace( '\n', ' ' ),
      '''Masai giraffes inhabit savannas, open woodlands, and acacia-dominated grasslands of southern Kenya and Tanzania. They favor
         landscapes that provide scattered trees for browsing and open sightlines to detect predators. Seasonal movements are common,
         following rainfall patterns that influence plant growth. Unlike some migratory ungulates, giraffes generally remain within
         broad home ranges rather than undertaking long-distance migrations.'''.replace( '\n', ' ' ),
      '''Masai giraffes are specialized browsers, feeding primarily on leaves, flowers, and seed pods from tall trees, especially
         acacias. Their long, prehensile tongues, which can reach 45–50 cm, are darkly pigmented to reduce sun damage and dexterous
         enough to strip leaves from between sharp thorns. An adult giraffe may consume 30–45 kg of vegetation per day, gaining most
         of its water from food and often going days without drinking. Their height allows them access to food sources unavailable
         to other herbivores, reducing direct competition.'''.replace( '\n', ' ' ),
      '''Masai giraffes live in loose, fluid social groups that change frequently. These groups may include females with calves,
         bachelor males, or mixed assemblages. There is no fixed herd structure, and individuals come and go freely. Adult males
         engage in ritualized combat known as necking, where they swing their necks and strike opponents with their heads to
         establish dominance. Despite their size, giraffes are generally calm, alert animals that rely on height and vision rather
         than aggression for safety.'''.replace( '\n', ' ' ),
      '''The Masai giraffe’s body is a masterclass in extreme specialization. Its neck contains only seven vertebrae, the same
         number as most mammals, but each is greatly elongated. A powerful heart weighing up to 11 kg generates high blood pressure
         to pump blood to the brain, while a complex system of valves and elastic blood vessels prevents dangerous pressure changes
         when the giraffe lowers or raises its head. Their long legs provide both height and speed, allowing giraffes to run up to
         60 km/h (37 mph) over short distances. Thick skin on the legs helps protect against kicks from predators, while large eyes
         and elevated vantage points allow early detection of danger across open landscapes.'''.replace( '\n', ' ' ),
      '''After a gestation period of about 15 months, females give birth standing up, with calves dropping nearly 2 m to the ground
         at birth. Newborns are already about 1.8 m (6 ft) tall and can stand and walk within hours. Calves remain vulnerable to
         predators during their first year, with lions being the primary threat. Females often form loose nursery groups, keeping
         watch over multiple calves. In the wild, Masai giraffes can live 20–25 years, with longer lifespans possible under human
         care.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a female Masai giraffe calf, Imara, and her mother, Mstari. Imara was born on February 22nd, and
         is still in the critical early stages of her development and requires plenty of private bonding time with her mother. In
         these critical stages for Imara the giraffes' visibility may be limited.'''.replace( '\n', ' ' )
   ),
   (
      'Olive Baboon',
      'Papio Anubis',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The olive baboons can be spotted on the Africa Savanna loop in between the cheetahs and lions, and across from the zebras.''',
      '''The olive baboons can generally be seen year-round. In the coldest months they may be given access to indoor spaces, but
         they can generally be seen outside, most often on their main structure in the center of their enclosure.'''
         .replace( '\n', ' ' ),
      '''The olive baboon is a large, powerfully built monkey with a dog-like muzzle, heavy brow ridge, and long limbs adapted for
         life on the ground. Its coat ranges from olive-green to brownish-grey, created by multi-banded hairs rather than true green
         colouration. Males are substantially larger than females and possess prominent canine teeth and a mane of longer hair
         around the shoulders. Adults typically measure 50–70 cm in body length, with males weighing up to 30 kg, making them among
         the largest monkey species in Africa.'''.replace( '\n', ' ' ),
      '''Olive baboons have the widest distribution of any baboon, occurring across much of central and eastern Africa, from
         savannas and open woodlands to forest edges and even rocky semi-desert. Their adaptability allows them to live near human
         settlements, agricultural areas, and degraded habitats. Access to sleeping cliffs or tall trees and reliable water sources
         strongly influences their local distribution.'''.replace( '\n', ' ' ),
      '''Olive baboons are highly opportunistic omnivores, with diets that change seasonally and regionally. They feed on fruits,
         seeds, leaves, roots, and grasses, as well as insects, eggs, and small vertebrates. Baboons are skilled diggers, using
         their hands to uncover underground tubers and corms during dry periods. Their dietary flexibility is a key reason for their
         ecological success, though it can also bring them into conflict with humans when crops are available.'''.replace( '\n', ' ' ),
      '''Olive baboons live in large, multi-male multi-female troops that may include 20 to over 100 individuals. Their societies
         are highly structured, with complex dominance hierarchies, especially among females, whose rank is inherited matrilineally.
         Social grooming plays a central role in maintaining bonds, reducing tension, and reinforcing alliances. Males often compete
         for status and mating opportunities, while females form the stable social core of the group. Baboons communicate through a
         rich array of facial expressions, vocalizations, and body postures, making them one of the most socially complex non-human
         primates.'''.replace( '\n', ' ' ),
      '''The olive baboon’s success lies in its behavioural intelligence and physical versatility. Long limbs and strong hands allow
         efficient ground travel and dexterous food handling, while tough skin and thickened ischial callosities enable long periods
         of sitting on hard surfaces. Large canine teeth provide defense and social signaling rather than routine predation. Their
         highly developed brains support problem-solving, memory, and social awareness, allowing baboons to navigate dominance
         hierarchies and adapt quickly to environmental change.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity around 4–6 years, while males mature later and often leave their natal troop. After a
         gestation of about 6 months, a single infant is born. Newborns cling to their mother’s fur and gradually become more
         independent. Infant survival is closely tied to the mother’s social rank, with higher-ranking females generally having
         greater reproductive success. Olive baboons can live 25–30 years in the wild, with longer lifespans under human care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Ostrich',
      'Struthio Camelus',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The ostrich habitat has two main vantage points in the Africa Savanna. One is between the lions and the baboons, while the
         other is across from the top of the hill that yields access to the Canadian domain. The ostrich moves across its enclosure
         quite regularly, and its enclosure is quite large, so you may struggle to get a close view at times.'''.replace( '\n', ' ' ),
      '''Ostriches are quite adaptive birds, comfortable in temperatures down to around 0°C. They can be fairly reliably seen
         between Apirl and November, and other non-freezing days where there is not much snow on the ground.'''.replace( '\n', ' ' ),
      '''The ostrich is the largest living bird in the world, instantly recognizable by its towering height, long bare neck, small
         head, and powerful legs. Adults can stand up to 2.7 m tall and weigh 90–150 kg. Males are strikingly patterned with black
         body feathers and white wing and tail plumes, while females and juveniles are more subdued, with grey-brown plumage that
         provides camouflage. Unlike flying birds, ostriches have loose, fluffy feathers that lack the interlocking structure needed
         for flight.'''.replace( '\n', ' ' ),
      '''Ostriches are native to sub-Saharan Africa, where they inhabit open landscapes such as savannas, grasslands, semi-deserts,
         and scrublands. They avoid dense forests and areas with heavy vegetation, relying instead on wide visibility to detect
         predators. Ostriches often share habitats with large grazing mammals and benefit from these mixed-species environments by
         spotting danger early.'''.replace( '\n', ' ' ),
      '''Ostriches are primarily omnivorous grazers, feeding on grasses, seeds, leaves, flowers, and fruits, supplemented by insects,
         small reptiles, and other invertebrates. They swallow small stones and grit, which collect in the muscular gizzard and help
         grind tough plant material. Ostriches can survive long periods without drinking water, obtaining much of their moisture
         from food and conserving water efficiently.'''.replace( '\n', ' ' ),
      '''Ostriches are typically found in loose groups ranging from small family units to mixed herds that may include antelope or
         zebras. These associations increase predator detection, as ostriches rely heavily on their exceptional eyesight. While
         generally wary and cautious, ostriches can become aggressive if threatened, especially when defending nests or young. They
         communicate using body postures, wing displays, hissing sounds, and deep booming calls produced by males during the
         breeding season.'''.replace( '\n', ' ' ),
      '''The ostrich is a masterpiece of evolutionary specialization for life on the open savanna. Its long, muscular legs allow it
         to run at speeds of up to 70 km/h, making it the fastest bird on land. Each foot has only two toes, a unique adaptation
         that reduces weight and improves running efficiency. Powerful legs also serve as formidable weapons, capable of delivering
         kicks strong enough to deter or injure large predators. Large eyes—among the biggest of any land animal—provide excellent
         long-distance vision, while flightlessness allows energy to be redirected into growth, strength, and speed.'''
         .replace( '\n', ' ' ),
      '''During the breeding season, dominant males establish territories and attract multiple females. Several females lay their
         eggs in a single communal nest, a shallow scrape in the ground. The largest female and the dominant male take turns
         incubating the eggs, with the male’s dark plumage providing camouflage at night. Ostrich eggs are the largest of any living
         animal, weighing up to 1.5 kg each. Chicks hatch after about 42 days and are precocial, able to walk and feed themselves
         shortly after hatching, though they remain under adult protection.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a male ostrich, Omelette, who loves to dance and interact with his caretakers.'''
         .replace( '\n', ' ' )
   ),
   (
      'River Hippopotamus',
      'Hippopotamus Amphibius',
      14,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The river hippo habitat can be found on the Africa Savanna loop, in between the warthogs and giraffes, and white rhinos and
         kudus.'''.replace( '\n', ' ' ),
      '''River hippos are native to sub-Saharan African and have exposed skin, and are thus not very adapted to the cold. At the zoo,
         they can be seen outside reliably from May through the warmer part of October, and occasionally on other warm spring and
         fall days.'''.replace( '\n', ' ' ),
      '''The river hippopotamus is a massive, semi-aquatic mammal, weighing 1,500–1,800 kg for adult males and 1,300–1,500 kg for
         females, with lengths of 3.3–5 m and shoulder heights up to 1.5 m. Its barrel-shaped body is supported by short, stout legs,
         and it has a large, wide mouth with tusk-like canine teeth that can grow over 50 cm in males. The skin is grayish-brown and
         nearly hairless, secreting a natural red-coloured “sunscreen” substance that protects from UV radiation and infection.'''
         .replace( '\n', ' ' ),
      '''River hippos are native to sub-Saharan Africa, inhabiting rivers, lakes, floodplains, and swamps. They are highly dependent
         on water, using it to regulate body temperature and maintain skin moisture. Hippos typically remain submerged during the
         day, emerging at night to graze on grass along riverbanks. Their habitats often overlap with other large savanna mammals,
         but their reliance on aquatic environments distinguishes them ecologically.'''.replace( '\n', ' ' ),
      '''Hippos are herbivorous grazers, feeding almost entirely on short grasses. Adults consume 30–50 kg of vegetation per night,
         venturing several kilometers from water to feed. Despite their bulk and aquatic lifestyle, they are surprisingly agile on
         land and able to navigate complex terrain in search of food. In zoos, they are provided a combination of hay, grasses, and
         specially formulated herbivore diets to replicate natural feeding and maintain health.'''.replace( '\n', ' ' ),
      '''River hippos are social but territorial in water, forming groups called pods, schools, or bloats, typically consisting of
         10–30 individuals, led by a dominant male. On land, they are more solitary while grazing. Hippos are highly vocal,
         communicating through grunts, bellows, and even underwater sounds. Despite their seemingly placid appearance, hippos are
         highly aggressive when defending territory or offspring, and they have one of the most powerful bites among land mammals.'''
         .replace( '\n', ' ' ),
      '''Hippos are exquisitely adapted for a semi-aquatic lifestyle. Their eyes, ears, and nostrils are positioned on top of the
         head, allowing them to see, hear, and breathe while mostly submerged. Their skin secretes hipposudoric acid, which
         functions as both sunscreen and antibacterial barrier. Massive jaws and tusks are used for defense and social dominance,
         while webbed feet aid in movement through water. Despite being poor swimmers, they can walk along riverbeds and hold their
         breath underwater for up to 5 minutes. Their unique physiology allows them to tolerate high body temperatures and low
         oxygen conditions during extended submersion.'''.replace( '\n', ' ' ),
      '''Hippos reach sexual maturity at 7–9 years for females and 9–12 years for males. Breeding occurs in water, where males
         defend territories and mate with females in their pods. Females give birth to usually a single calf, often in water, after
         a gestation period of 8 months. Calves can weigh 45–50 kg at birth and are able to swim almost immediately, staying close
         to their mother for protection. River hippos can live 40–50 years in the wild and sometimes longer in managed care.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female river hippopotamus, Perky.'''.replace( '\n', ' ' )
   ),
   (
      'Southern Ground Hornbill',
      'Bucorvus Leadbeateri',
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''Southern ground hornbills can be spotted in two habitats in the Africa Savanna. Some of the hornbills share a habitat with
         the kudus and other savanna birds. They can be viewed in this habitat from any of the three viewings: the savanna outlook
         in the African Rainforest Pavilion near the meerkats, on the offshoot path between the rhinos and hippos, or in the main
         viewing across from the white rhinos, but they may be most reliably seen at the viewing on the offshoot path. The other
         spot that they can be viewed is in the small enclosure between the lions and hyenas, and across from the elands.'''
         .replace( '\n', ' ' ),
      '''Southern ground hornbills are warm-weather birds which are usually only viewable during the warmest months of the year,
         roughly from June through the end of September.'''.replace( '\n', ' ' ),
      '''TThe Southern Ground Hornbill is a large, striking bird with predominantly black plumage, vivid red facial and throat skin,
         and a long, thick bill used for foraging and display. Adults measure 90–130 cm in length, with a wingspan of 1.2–1.8 m, and
         weigh 3–6 kg. Males typically display more extensive red facial skin than females. Juveniles have duller, more muted
         colouration that gradually brightens as they mature.'''.replace( '\n', ' ' ),
      '''Southern Ground Hornbills inhabit savannas, open woodlands, and grasslands across southern Africa, including South Africa,
         Botswana, Zimbabwe, and parts of Mozambique. They prefer areas with large, mature trees for nesting and roosting, but spend
         most of their time on the ground foraging. They are largely non-migratory but maintain large territories that they defend
         vigorously.'''.replace( '\n', ' ' ),
      '''These hornbills are primarily terrestrial foragers, hunting small vertebrates such as lizards, snakes, frogs, and insects.
         They also eat seeds and fruits opportunistically. Using their strong bills, they dig, probe, and capture prey on the
         ground. In zoo care, they are provided a diet of meat, insects, and fruits to replicate their natural nutritional
         requirements.'''.replace( '\n', ' ' ),
      '''Southern Ground Hornbills are highly social and territorial, typically living in extended family groups of 4–15 birds.
         Groups include a dominant breeding pair and helper birds, often offspring from previous years. They communicate using deep
         booming calls that can carry for kilometers across the savanna. Cooperative behaviours include hunting, territory defense,
         and feeding young, making them an excellent example of advanced social structure in birds.'''.replace( '\n', ' ' ),
      '''Southern Ground Hornbills are specialized for ground foraging, with strong legs and large feet adapted for walking long
         distances and digging for prey. Their massive bills allow them to handle tough prey and dig efficiently. The bright red
         skin may function in visual communication, signaling age, sex, and social status. Their long lifespan and slow reproduction
         rate are offset by strong family cooperation, helping ensure survival of young in predator-rich environments.'''
         .replace( '\n', ' ' ),
      '''Breeding is slow and cooperative. The dominant female lays 1–3 eggs in tree cavities, but usually only one chick survives
         to fledging. Incubation lasts about 40 days, and both parents and helpers feed the chick. Juveniles remain in the family
         group for several years before dispersing. Southern Ground Hornbills are long-lived, with a lifespan of 50–60 years in the
         wild, making them one of the longest-lived bird species in Africa.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Southern White Rhinoceros',
      'Ceratotherium Simum Simum',
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The Southern white rhinos can be found in the Africa Savanna loop, across from the kudu, and between the zebra and hippos.''',
      '''Southern white rhinoceroses are warm-weather animals and have exposed skin, and are only viewable outside during the warmer
         months of the year. They can be reliably seen from May through October, and on other warm spring or fall days.'''
         .replace( '\n', ' ' ),
      '''The Southern White Rhino is a massive herbivore, with adult males weighing 2,000–2,300 kg and females 1,400–1,700 kg,
         making it the second-largest land mammal after elephants (though no elephants are at Toronto Zoo). They measure 3.4–4.2 m
         in length and stand 1.8–2 m at the shoulder. White rhinos have a wide, square-shaped mouth adapted for grazing, and two
         horns on the snout, with the front horn typically 60–150 cm long. Their skin is thick and gray, forming deep folds that
         provide protection and flexibility.'''.replace( '\n', ' ' ),
      '''Southern White Rhinos are native to southern Africa, including South Africa, Namibia, Zimbabwe, and Kenya. They prefer
         grasslands, savannas, and floodplains where they can graze on short grasses. Though historically widespread, populations
         are now largely restricted to protected areas due to poaching and habitat loss.'''.replace( '\n', ' ' ),
      '''White rhinos are grazers, feeding almost exclusively on grasses. Their wide lips allow them to clip vegetation efficiently.
         Adults can consume 50–70 kg of grass per day, often for several hours at a time. They require fresh water for drinking and
         wallowing, which also helps regulate body temperature and remove parasites. Zoo diets replicate their natural grazing with
         grass, hay, and formulated herbivore pellets.'''.replace( '\n', ' ' ),
      '''Southern White Rhinos are socially flexible. Adult males are territorial, marking areas with dung and urine to ward off
         rivals. Females and subadult males are more tolerant of each other, sometimes forming loose groups. Despite their bulk,
         rhinos are capable of surprising bursts of speed—up to 50 km/h—to escape threats. Vocal communication, scent marking, and
         horn displays are important in maintaining social structure and territory boundaries.'''.replace( '\n', ' ' ),
      '''White rhinos are superbly adapted to grazing and grassland survival. Their wide, prehensile lips and massive jaws allow
         them to harvest large amounts of grass efficiently. Thick skin provides protection against predators and environmental
         hazards, while deep folds help channel water and mud during wallowing. Horns are made of keratin and serve as defensive
         weapons, social signals, and tools for digging or clearing vegetation. Strong limbs and a heavy, muscular body support
         movement across uneven terrain, while acute hearing and smell compensate for relatively poor eyesight.'''
         .replace( '\n', ' ' ),
      '''Females reach sexual maturity at 6–7 years, males at 10–12 years. Gestation lasts about 16 months, usually resulting in a
         single calf weighing 40–65 kg at birth. Calves are nursed for 12–18 months but may start grazing earlier. Lifespan in the
         wild is 40–50 years, and they can live slightly longer in managed care. Calf survival depends heavily on maternal care and
         habitat security.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to four Southern white rhinoceros. There is an adult male, Tom, adult females Sabi and Zohari, and
         youngster Kifaru. Kifaru is a male and was born in December of 2023. Sabi, Zohari, and Kifaru all go on exhibit together,
         while Tom is solitary.'''.replace( '\n', ' ' )
   ),
   (
      'Spotted Hyena',
      'Crocuta Crocuta',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The spotted hyena habitat can be found in the Africa Savanna, close to where the Canadian Domain is accessed, and across
         from the watusi.'''.replace( '\n', ' ' ),
      '''The spotted hyenas can generally be seen year-round, but during the coldest months they may be given indoor spaces, and
         decide to spend their time inside, specifically on the coldest and snowiest day. On the coldest days, look for them in
         their den, viewable from the glass viewing across from the watusi, which is heated.'''.replace( '\n', ' ' ),
      '''Spotted hyenas are medium-to-large carnivores, measuring 95–165 cm in body length and standing 70–90 cm at the shoulder,
         with adults weighing 45–80 kg. They have a stocky build, sloping back, and powerful forequarters. Their coarse fur is
         yellow-brown with irregular dark spots, which are unique to each individual, like fingerprints. Large, rounded ears and
         strong jaws give them a distinctive appearance. Their powerful bite can crush bones, which is central to their feeding
         strategy.'''.replace( '\n', ' ' ),
      '''Spotted hyenas are native to sub-Saharan Africa, occupying savannas, grasslands, woodlands, and semi-deserts. They are
         highly adaptable, often thriving near human settlements, where they may scavenge refuse or livestock. Hyenas require large
         home ranges, sometimes exceeding 40–100 km², to support their foraging and hunting needs.'''.replace( '\n', ' ' ),
      '''Spotted hyenas are opportunistic carnivores and scavengers. They consume a wide range of prey, from small rodents to
         wildebeest, and can digest almost every part of a carcass, including bones. Cooperative hunting allows them to take down
         larger ungulates. In managed care, their diet includes meat, bones, and enrichment items to stimulate natural foraging
         behaviours.'''.replace( '\n', ' ' ),
      '''Spotted hyenas live in complex social groups called clans, which may include up to 80 individuals. Their societies are
         matriarchal, with females dominating males and inheriting social rank from their mothers. Communication is elaborate,
         including whoops, growls, giggles, and scent markings, allowing coordination in hunting and social hierarchy reinforcement.
         They are highly intelligent, with problem-solving abilities rivaling some primates, and exhibit coordinated hunting
         strategies and communal care of young.'''.replace( '\n', ' ' ),
      '''Spotted hyenas are highly specialized predators and scavengers. Their extremely strong jaws and digestive systems allow
         them to consume and extract nutrients from bones and other tough materials. Muscular forequarters and long stamina give
         them endurance for chasing prey over long distances. Their complex social cognition enables coordination during hunts and
         navigation of hierarchical interactions within clans. Night vision and acute hearing enhance hunting success, while scent
         marking maintains territory boundaries.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity around 2–3 years, males slightly later. After a gestation period of 110 days, females give
         birth to 1–2 cubs in secluded dens. Cubs are born with teeth and spotted coats, helping with camouflage. High-ranking
         females have higher reproductive success, and survival is strongly influenced by maternal rank and clan support. Spotted
         hyenas can live 12–25 years in the wild, often longer in zoos.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to several hyenas. Unlike their wild counterparts, the hyenas at the zoo are solitary, and thus you
         will only ever see one on exhibit at a time.'''.replace( '\n', ' ' )
   ),
   (
      'Warthog',
      'Phacochoerus Africanus',
      16,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The warthog habitat can be found in the Africa Savanna loop, in between the giraffes and hippos. The warthog is one of the
         more difficult species to see at the zoo--timing is everything. They can be most often be seen by looking directly down
         from their viewing. One of the warthogs at the zoo likes to rest right near the close fence of the enclosure. You have a
         better chance of seeing them active in the morning, or closer to dusk.'''.replace( '\n', ' ' ),
      '''Warthogs are very sensitive to the cold, and thus are only viewable outside during the warmest months, late May to
         September, and on other warm days.'''.replace( '\n', ' ' ),
      '''The warthog is a medium-sized wild pig with a distinctive, rugged appearance. Adults measure 90–150 cm in body length and
         stand 63–85 cm at the shoulder, weighing 50–150 kg. They have a large head, prominent facial warts, and two pairs of tusks:
         upper tusks curve outward and can reach 25–45 cm, while lower tusks are smaller and sharper. Sparse bristly hair covers
         their bodies, and a thin mane runs along the spine.'''.replace( '\n', ' ' ),
      '''Warthogs inhabit savannas, grasslands, and lightly wooded areas throughout sub-Saharan Africa. They prefer open areas near
         water sources and often use abandoned burrows for shelter. Their range overlaps with many other savanna species, and they
         are well adapted to seasonal droughts and fires.'''.replace( '\n', ' ' ),
      '''Warthogs are omnivorous grazers and foragers, feeding primarily on grasses, roots, tubers, fruits, and occasionally insects
         or carrion. They often kneel on their front knees while grazing, using their snouts and tusks to dig for edible roots. In
         zoos, they are fed a mix of hay, vegetables, grains, and enrichment items to simulate natural foraging.'''
         .replace( '\n', ' ' ),
      '''Warthogs live in small family groups called sounders, usually consisting of females and their young, while adult males are
         mostly solitary. They are highly alert and rely on speed and burrows to escape predators. Despite their rugged appearance,
         warthogs can run at up to 48 km/h (30 mph). Social interactions include grooming, nuzzling, and mutual defense of young.'''
         .replace( '\n', ' ' ),
      '''Warthogs are well-adapted to harsh savanna life. Their tusks serve as weapons against predators and rivals, while their
         facial warts protect sensitive areas during fights. Kneeling during grazing is enabled by calloused pads on their forelimbs,
         protecting them from hard or rocky ground. Burrow use provides shelter from predators and extreme heat, and their sparse
         hair and tough skin help regulate body temperature. Their ability to survive long periods without water is another key
         adaptation for semi-arid habitats.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity at 12–18 months, males at around 2 years. After a gestation of about 5–6 months, females give
         birth to 2–4 piglets in burrows. Piglets remain hidden and well-camouflaged for the first few weeks, then gradually join
         the family group. Warthogs can live 12–18 years in the wild and slightly longer in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Watusi Cattle',
      'Bos Taurus',
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The watusi cattle habitat can be found near the part of the Africa Savanna where you access the Canadian Domain, across
         from the spotted heynas.'''.replace( '\n', ' ' ),
      '''The watusi cattle can generally be seen outside year-round, as they have been bred to have a very high tolerance against
         the cold. On the iciest days, they may opt to stay inside as they need to move around a lot each day to graze.'''
         .replace( '\n', ' ' ),
      '''Watusi cattle are among the most visually dramatic cattle breeds in the world, defined by their massive, lyre-shaped horns,
         which may span up to 2.4 meters (8 feet) and weigh over 45 kg combined. These horns sit atop a long, narrow head and a
         lean, tall body supported by long legs. Coat colouration varies widely, including deep red, chestnut, black, white,
         brindled, or speckled patterns. Adults typically weigh 450–730 kg, with bulls larger and heavier than cows.'''
         .replace( '\n', ' ' ),
      '''The breed originated in East Africa, particularly within Uganda, Rwanda, Burundi, and adjacent regions. For centuries,
         Watusi cattle were raised in open savanna, grassland, and semi-arid environments, often in areas with intense heat and
         seasonal water scarcity. Today, they are found globally in managed care, including zoological parks and
         conservation-focused breeding programs.'''.replace( '\n', ' ' ),
      '''Watusi cattle are grazing herbivores, feeding primarily on grasses and other coarse vegetation. They are well adapted to
         survive on low-nutrient forage, requiring less food than many other large cattle breeds. In zoos, their diet consists of
         pasture grass, hay, and nutritionally balanced supplements to support overall health and horn development.'''
         .replace( '\n', ' ' ),
      '''Highly social and herd-oriented, Watusi cattle maintain structured group dynamics. Herds are generally calm and tolerant,
         though dominance hierarchies—especially among bulls—are established through posturing rather than frequent physical
         conflict. Their temperament is typically docile, making them well suited to mixed or walk-by exhibit environments.'''
         .replace( '\n', ' ' ),
      '''The most remarkable adaptation of Watusi cattle lies in their horn physiology. Unlike solid horns, Watusi horns contain an
         extensive network of blood vessels, allowing heat to dissipate as blood circulates through the horn surface—functioning as
         a natural radiator system in hot climates. Their lean body shape, large skin surface area, and heat tolerance further
         reduce thermal stress. Additionally, they exhibit resilience to drought conditions and some resistance to regional
         parasites, reflecting long-term adaptation to challenging environments.'''.replace( '\n', ' ' ),
      '''Females typically reach sexual maturity between 2 and 3 years of age. After a gestation period of approximately 280 days, a
         single calf is born. Calves remain close to their mothers for several months, nursing and gradually integrating into the
         herd’s social structure. In managed care, Watusi cattle can live 20–25 years, with some individuals exceeding this under
         optimal conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'White-Breasted Cormorant',
      'Phalacrocorax Lucidus',
      2,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The white-breasted cormorant lives in the Africa Savanna in the African penguin habitat, across from the watusi cattle.''',
      '''The white-breasted cormorant can handle temperate environments, and can thus be outside for most of the year, but cannot
         handle snow or ice. During the coldest months, from December through most of March, these birds are only visible indoors.
         When weather permits, this bird can normally be seen outside by the water's edge in the outdoor African penguin habitat.'''
         .replace( '\n', ' ' ),
      '''The white-breasted cormorant is a large, dark waterbird distinguished by its glossy black body, white throat and upper
         chest, and long, hooked bill. Adults measure 70–85 cm in length with a wingspan of up to 1.4 meters. During the breeding
         season, small white feather patches may appear on the head and neck. Males and females are similar in appearance, though
         males are typically slightly larger.'''.replace( '\n', ' ' ),
      '''This species is found throughout sub-Saharan Africa, particularly along coastlines, large lakes, rivers, and reservoirs. It
         favors open water with abundant fish and nearby perches such as rocks, trees, or artificial structures. Although often
         associated with marine environments, it is equally at home in freshwater habitats.'''.replace( '\n', ' ' ),
      '''White-breasted cormorants are piscivorous, feeding primarily on fish. They are skilled pursuit divers, using powerful feet
         to propel themselves underwater while chasing prey. Fish are captured with the hooked bill and swallowed whole, usually at
         the surface. Individuals may forage alone or in loose groups, sometimes cooperating to herd fish.'''.replace( '\n', ' ' ),
      '''Cormorants are generally gregarious, often seen roosting or nesting in colonies. After fishing, they frequently perch with
         their wings spread, a behaviour thought to help dry their feathers and regulate body temperature. While not highly vocal,
         they communicate through grunts and body postures, especially at breeding sites.'''.replace( '\n', ' ' ),
      '''This species has several adaptations for an aquatic lifestyle, including webbed feet, dense bones that reduce buoyancy, and
         partially wettable feathers that allow efficient diving. Their streamlined bodies minimize water resistance, and keen
         underwater vision enables them to track fast-moving prey.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in colonies, with nests built in trees, on cliffs, or on the ground near water. Females lay 2–4
         eggs, which are incubated by both parents for about 25–30 days. Chicks are fed regurgitated fish and fledge after several
         weeks. White-breasted cormorants can live 15–20 years in the wild or managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'White-Headed Vulture',
      'Trigonoceps Occipitalis',
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The zoo is home to one white-headed vulture, Lloyd, and he is one of the more reclusive residents. He resides in the
         enclosure with the kudu and other savanna birds. He may be spotted from any of the three viewing areas for this exhibit:
         the savanna outlook in the African Rainforest Pavilion near the meerkats, on the offshoot path between the hippos and
         rhinos, or at the main viewing across from the white rhinos, but you will have the best chance at the offshoot viewing
         followed by the main viewing area.'''.replace( '\n', ' ' ),
      '''The white-headed vulture is a warm-weather bird which can only be seen outside during the warmest months, from June to
         September.'''.replace( '\n', ' ' ),
      '''The white-headed vulture is a medium-sized but powerfully built vulture with a distinctive appearance. Adults have a bright
         white head and neck, contrasting sharply with a dark brown to black body. The face often shows pink or reddish skin, and
         the wings display bold white patches visible in flight. Body length ranges from 72–85 cm, with a wingspan of up to 2.1
         meters. Females are slightly larger than males.'''.replace( '\n', ' ' ),
      '''This species is native to sub-Saharan Africa, occurring primarily in open savanna, woodland, and grassland ecosystems. It
         prefers areas with scattered trees for nesting and perching, often near regions that support large herbivores. White-headed
         vultures are typically less common than other African vultures and are usually seen alone or in pairs rather than large
         flocks.'''.replace( '\n', ' ' ),
      '''White-headed vultures are carnivorous scavengers, feeding mainly on the carcasses of large mammals. Unlike many vultures,
         they often arrive early at kills and may feed alongside or even displace smaller scavengers. Their strong, hooked bill
         allows them to tear through tough skin and access muscle tissue, making them less dependent on other species to open
         carcasses.'''.replace( '\n', ' ' ),
      '''This vulture is relatively solitary, usually seen alone or with a mate rather than in large groups. Pairs are strongly
         bonded and may maintain territories around nesting sites. In flight, they soar high on thermals, using keen eyesight to
         locate food across vast areas of savanna.'''.replace( '\n', ' ' ),
      '''The white-headed vulture’s bare head and neck reduce feather contamination when feeding on carcasses and help regulate body
         temperature. Its exceptionally strong bill and neck muscles allow it to access parts of carcasses that other scavengers
         cannot. Excellent vision, broad wings for soaring, and a highly acidic digestive system enable it to efficiently locate,
         consume, and safely process decaying meat.'''.replace( '\n', ' ' ),
      '''Breeding pairs typically build large stick nests high in trees. A single egg is laid and incubated for approximately 55
         days. Both parents care for the chick, which remains dependent for several months after hatching. White-headed vultures are
         long-lived birds, with lifespans of 30 years or more in the wild and managed care.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one white-headed vulture, a male named Lloyd. Lloyd is one of just two white-headed vultures in
         North America.'''.replace( '\n', ' ' )
   ),

   # African Rainforest Pavilion
   (
      'African Clawed Frog',
      'Xenopus Laevis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The African clawed frog can be found in a terrarium in an enclosure between the dwarf crocodiles and Lake Malawai display
         and the gorillas.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The African clawed frog is a fully aquatic frog with a flattened body, smooth, slippery skin, and powerful hind legs. Its
         colouration ranges from olive-gray to brown, often mottled for camouflage. Unlike many frogs, it lacks a tongue and
         external eardrums. Each hind foot has three sharp, black claws, which give the species its common name. Adults typically
         measure 5–13 cm in length, with females larger than males.'''.replace( '\n', ' ' ),
      '''This species is native to sub-Saharan Africa, where it inhabits slow-moving rivers, ponds, lakes, and flooded forest pools,
         including rainforest environments. African clawed frogs are highly adaptable and can survive in both permanent and
         temporary water bodies. Due to introductions, they now occur in parts of Europe, North America, and South America, where
         they are considered invasive.'''.replace( '\n', ' ' ),
      '''African clawed frogs are opportunistic carnivores. They feed on aquatic invertebrates, insects, worms, small fish, tadpoles,
         and carrion. Without a tongue, they use their clawed hind feet to tear food apart and push it into their mouths. Sensitive
         fingers and a keen sense of smell help them locate prey in murky water.'''.replace( '\n', ' ' ),
      '''These frogs are mostly solitary and active both day and night. They spend nearly their entire lives underwater, surfacing
         only to breathe air. African clawed frogs are known for their vocalizations, especially during breeding, with males
         producing clicking sounds to attract females.'''.replace( '\n', ' ' ),
      '''The African clawed frog shows strong adaptation to an aquatic lifestyle. Its flattened body and webbed feet allow efficient
         swimming, while its lateral line system—similar to that of fish—detects vibrations in the water. The claws aid in feeding
         and defense, and the ability to tolerate low oxygen levels allows survival in stagnant or temporary waters.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in water, often triggered by rainfall or environmental changes. Females can lay hundreds to thousands of
         eggs, which are fertilized externally. Eggs hatch within a few days, and tadpoles undergo metamorphosis over several weeks.
         African clawed frogs are long-lived, with lifespans of 15–20 years, and sometimes longer in managed care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'African Spoonbill',
      'Platalea Alba',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The African spoonbills can be found in a mixed-species habitat, shared with the sacred ibis and South African shelduck,
         near the pygmy hippos, and softshell turtle.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The African spoonbill is a large white wading bird easily recognized by its long, flattened, spoon-shaped bill. Adults
         stand about 80–90 cm tall with a wingspan reaching 1.3 meters. The plumage is entirely white, contrasted by a pinkish face
         and legs. During the breeding season, adults develop a yellow patch on the chest. Males and females are similar i
         appearance.'''.replace( '\n', ' ' ),
      '''This species is widespread across sub-Saharan Africa and Madagascar, inhabiting shallow wetlands, floodplains, marshes,
         lake edges, and slow-moving rivers. Although not restricted to rainforests, African spoonbills frequently use forested
         wetlands and river systems within rainforest regions.'''.replace( '\n', ' ' ),
      '''African spoonbills feed primarily on small fish, aquatic insects, crustaceans, and mollusks. They forage by sweeping their
         bill side to side through shallow water, snapping it shut when prey is detected by touch. This feeding method allows them
         to hunt effectively even in muddy or low-visibility water.'''.replace( '\n', ' ' ),
      '''Spoonbills are generally social birds, often seen feeding in small groups or mixed-species flocks with herons and storks.
         They are mostly quiet but may produce low grunts at nesting colonies. When not feeding, they rest communally in trees or on
         sandbanks.'''.replace( '\n', ' ' ),
      '''The species’ most notable adaptation is its sensitive, spoon-shaped bill, which enables tactile feeding without relying on
         sight. Long legs allow efficient wading through shallow wetlands, while broad wings provide energy-efficient soaring
         between feeding sites. Their white plumage may help reduce heat absorption in open, sunlit wetlands.'''.replace( '\n', ' ' ),
      '''African spoonbills nest in colonies, often in trees, reeds, or on islands protected from predators. Females lay 2–5 eggs,
         which are incubated by both parents for about 24–26 days. Chicks fledge after several weeks but remain dependent on adults
         for a short time afterward. The species can live 20 years or more in the wild and managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Aldabra Tortoise',
      'Aldabrachelys Gigantea',
      20,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The outdoor Aldabra tortoise habitat, where the tortoises can be found on very warm summer days, can be found near the
         entrance to the pavilion by the gorillas and the Africa restaurant. The habitat is on the other side of the entrance from
         the outdoor gorilla habitat. When indoors, the tortoises share a habitat with the ring-tailed lemurs and crowned cranes,
         located at the other entrance to the pavilion, near the giraffes.'''.replace( '\n', ' ' ),
      '''The Aldabra tortoises only thrive in very warm weather and thus can only be reliably seen outdoors in the peak of summer,
         during July and August, and other very warm days. The rest of the time they can be seen inside the African Rainforest
         pavilion in their shared habitat with the ring-tailed lemurs and the grey-necked crowned cranes.'''.replace( '\n', ' ' ),
      '''Aldabra tortoises are among the largest tortoises in the world, easily recognized by their massive domed shells, thick
         column-like legs, and relatively small heads with blunt, keratinized beaks. Adult males can exceed 250 kg, with shell
         lengths over 1.2 meters, while females are slightly smaller. Their skin is gray and leathery, and the shells vary from dark
         brown to gray, often with subtle growth rings. The size and robust form of this species make it one of the most impressive
         reptiles in any exhibit. Hatchlings are small and vulnerable, measuring only 8–10 cm, yet grow rapidly under ideal
         conditions.'''.replace( '\n', ' ' ),
      '''Native to the Aldabra Atoll in the Seychelles, these tortoises inhabit coastal grasslands, scrub forests, mangrove edges,
         and lowland forests. They are highly adapted to environments that experience seasonal drought and occasional flooding,
         allowing them to exploit a range of vegetation types. While not true rainforest dwellers, their adaptability makes them
         excellent representatives in rainforest-themed enclosures, illustrating how giant reptiles can thrive in varied tropical
         habitats.'''.replace( '\n', ' ' ),
      '''Aldabra tortoises are herbivorous grazers and browsers, consuming a diverse diet of grasses, leaves, shrubs, fruits, and
         succulent plants. They are capable of standing on hind legs to reach higher branches and can pull vegetation with their
         strong, beak-like jaws. Their slow metabolism and large digestive system enable them to process tough, fibrous plant matter
         efficiently. In managed care, zookeepers provide a mix of hay, leafy greens, vegetables, and occasional enrichment foods,
         which encourages foraging and natural feeding behaviours.'''.replace( '\n', ' ' ),
      '''Though often perceived as solitary, Aldabra tortoises exhibit interesting social behaviours. Males occasionally engage in
         head-butting contests to establish dominance, particularly during the mating season. In groups, tortoises show mutual
         tolerance and may cluster near water or sunlit areas, demonstrating thermoregulatory social behaviour. Daily activity
         patterns are influenced by temperature: they forage and move in cooler morning and evening hours, resting in shaded areas
         or wallowing in mud during the heat of the day. Observing these behaviours in a zoo setting provides insight into the
         complex lives of slow-moving reptiles, which are often underestimated.'''.replace( '\n', ' ' ),
      '''Aldabra tortoises have evolved a suite of adaptations that allow them to thrive in harsh, variable environments. Their
         massive, domed shells provide protection from predators and environmental hazards while supporting their enormous bodies.
         Thick, column-like legs give them the strength to move across uneven terrain and dig shallow wallows for resting or
         thermoregulation. They are highly efficient at processing fibrous plant material, thanks to a large digestive tract and a
         slow metabolism, allowing them to survive periods when food is scarce. The tortoise’s long lifespan is itself an adaptation,
         supported by slow growth, robust immunity, and energy-efficient physiology, which ensures they can reproduce multiple times
         over many decades. Additionally, their ability to withstand both drought and occasional flooding illustrates the species’
         flexibility in coping with fluctuating island climates.'''.replace( '\n', ' ' ),
      '''Sexual maturity is reached slowly: females may not breed until 20–30 years, with males slightly older. Breeding is seasonal,
         influenced by rainfall and food availability. Females lay 9–25 eggs in shallow nests dug into sandy soil, with an
         incubation period of 8–10 months, during which temperature can influence the sex of the hatchlings. Juveniles are small and
         vulnerable, requiring protective behaviours such as hiding in vegetation. Slow growth, delayed maturity, and long lifespan
         allow Aldabra tortoises to maintain population stability over decades, even in variable environments. Lifespan in managed
         care can extend beyond 150 years, making them one of the longest-lived vertebrates on the planet.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two female Aldabra tortoises Queenie and Malila, who returned to the zoo in 2018. They
         originally arrived at the zoo in 1976. They are currently estimated to be between 50 and 60 years old.'''.replace( '\n', ' ' )
   ),
   (
      'Black Crake',
      'Amaurornis Flavirostra',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black crake can be found in the small aviary area between the gorillas and dwarf crocodiles.''',
      None,                                                          # Seasonal viewing tips
      '''Blake’s crake is a small, secretive waterbird, measuring approximately 18–20 cm in length. It has olive-brown upperparts,
         grayish underparts, and a slightly reddish bill, allowing it to blend into marshy vegetation. Legs are long and slender,
         adapted for walking on soft substrates, and toes are unwebbed but broad, aiding in stability on mud and floating plants.
         Its plumage is subtle, but its bright bill and cautious movements make it distinctive once observed closely.'''
         .replace( '\n', ' ' ),
      '''This species inhabits marshes, swamps, and shallow wetlands within tropical rainforest regions of South America,
         particularly in slow-moving streams, flooded forest edges, and dense vegetation near water. It relies on dense cover for
         protection from predators and foraging, making it difficult to spot in the wild. Blake’s crake is highly localized and
         sensitive to habitat disturbance, highlighting the importance of wetland conservation.'''.replace( '\n', ' ' ),
      '''Blake’s crake is primarily insectivorous and carnivorous, feeding on aquatic invertebrates, small crustaceans, insect
         larvae, and occasionally small fish or plant matter. It uses its long bill to probe mud and shallow water, detecting prey
         by touch and quick flicking movements. The bird is a patient forager, often moving slowly and carefully through dense
         vegetation, minimizing disturbance to its surroundings.'''.replace( '\n', ' ' ),
      '''This species is solitary and secretive, preferring to hide in dense reeds or submerged roots rather than openly swimming.
         It communicates through soft calls and occasional clucking sounds, primarily during breeding or territorial disputes.
         Blake’s crake is highly adapted to stealthy movement, often walking on floating vegetation or along muddy banks, and will
         dive into cover when threatened.'''.replace( '\n', ' ' ),
      '''Blake’s crake shows several adaptations for life in marshy rainforest environments. Its long legs and wide, unwebbed toes
         distribute weight over soft substrates, preventing sinking into mud. Its long, sensitive bill allows precise detection of
         hidden prey, while its cryptic colouration reduces visibility to predators. The species’ body shape is flattened,
         facilitating movement through reeds and low vegetation, and its keen hearing and vigilance help it avoid danger in dense,
         noisy habitats.'''.replace( '\n', ' ' ),
      '''Breeding usually occurs in the wet season, when water levels are higher and food is abundant. Females lay 2–4 eggs in nests
         built from reeds and grasses close to the water surface. Both parents participate in incubation, which lasts about 18–20
         days, and in feeding the chicks once hatched. Juveniles remain hidden in dense vegetation for several weeks before gaining
         independence. Lifespan in the wild is not well documented, but similar small crakes can live 5–8 years, with longer
         lifespans possible in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Blue-Bellied Roller',
      'Coracias Cyanogaster',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The blue-bellied roller can be found in the small aviary on the elevated pathway near the mixed waterfowl enclosure.''',
      None,                                                          # Seasonal viewing tips
      '''The blue-bellied roller is a medium-sized passerine, measuring 28–30 cm in length with a wingspan of 50–55 cm. Its most
         striking feature is the vivid blue underparts, contrasting with greenish upperparts, a rufous-brown back, and a pale head.
         The bill is slightly hooked and dark, suited for capturing insects, and the eyes are dark with a sharp, alert expression.
         Both sexes appear similar, though males may show slightly more vivid colouration during courtship displays.'''
         .replace( '\n', ' ' ),
      '''This species inhabits open woodland, forest edges, and secondary growth within West and Central African rainforests, often
         near rivers or clearings. It prefers areas where tall perches allow it to survey the ground for prey. While it can tolerate
         lightly disturbed habitats, dense primary rainforest and heavily urbanized areas are generally avoided.'''
         .replace( '\n', ' ' ),
      '''Blue-bellied rollers are primarily insectivorous, feeding on grasshoppers, beetles, crickets, and occasionally small
         reptiles or amphibians. They use a sit-and-wait hunting strategy, perching conspicuously before swooping down to catch prey
         with precision. Their strong, slightly hooked bill allows them to grasp and subdue active prey efficiently. In captivity,
         their diet is supplemented with insects, mealworms, and small portions of chopped fruits to support health and feather
         colouration.'''.replace( '\n', ' ' ),
      '''These birds are generally solitary or seen in pairs, often performing spectacular aerial displays, including twisting,
         rolling dives during courtship, which give the species its name. Their calls are harsh, squawking sounds used to
         communicate territory or alarm. They are highly territorial around feeding and nesting sites, defending perches vigorously
         against intruders.'''.replace( '\n', ' ' ),
      '''The blue-bellied roller exhibits several adaptations for a life of open-perch hunting. Its strong, slightly curved bill
         allows it to seize and handle active prey. Vivid plumage aids in courtship signaling, while its aerodynamic body enables
         agile, acrobatic flight for both hunting and display. The feet are adapted for perching on branches, providing stability
         while scanning for prey or watching for predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs in tree cavities or abandoned nests of other birds. Females lay 2–4 eggs, which are incubated for about
         17–19 days by both parents. Chicks are altricial, dependent on adults for feeding and protection for several weeks.
         Lifespan in the wild is typically 5–8 years, though birds in managed care can live longer with optimal nutrition and
         protection from predators.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Grey-Necked Crowned Crane',
      'Balearica Regloides',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The grey-necked crowned cranes can be found in a shared habitat with the ring-tailed lemurs, just inside the entrance to
         the pavilion near the giraffes.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The grey-necked crowned crane is a tall, elegant bird, standing approximately 100 cm (3.3 feet) tall with a wingspan of
         180–200 cm. It is immediately recognizable by its golden, spiky crown of feathers, contrasting with a grey neck and chest,
         white cheeks, and a dark, metallic body. Its long legs and slender build support walking and foraging in shallow wetlands.
         The black and white facial pattern highlights its bright red throat pouch, and both sexes are visually similar, though
         males are often slightly larger.'''.replace( '\n', ' ' ),
      '''This species inhabits wetlands, floodplains, and grasslands across eastern and southern Africa, including marshy rainforest
         edges and open savanna corridors. It requires shallow water and open spaces for feeding, dancing displays, and nesting,
         while nearby trees or shrubs provide roosting sites. The grey-necked crowned crane is sensitive to habitat disturbance,
         relying on intact wetlands for survival.'''.replace( '\n', ' ' ),
      '''Grey-necked crowned cranes are omnivorous, feeding on a variety of insects, small vertebrates, seeds, grasses, and aquatic
         invertebrates. They forage by walking through shallow water or grass, pecking and probing for prey. Their diet flexibility
         allows them to thrive in seasonal wetlands, switching between animal and plant matter depending on availability.'''
         .replace( '\n', ' ' ),
      '''These cranes are social and highly expressive, often observed in pairs or small flocks. They are renowned for their
         elaborate courtship dances, which include bowing, jumping, wing flapping, and synchronized calls. Outside of breeding, they
         maintain loose family groups, communicating with a variety of honks, grunts, and rattling sounds. Their upright stance and
         vocalizations also serve as territorial signals, deterring rivals and coordinating movements within flocks.'''
         .replace( '\n', ' ' ),
      '''The grey-necked crowned crane exhibits several adaptations for wetland and open-habitat living. Its long legs and toes
         allow efficient walking on soft, marshy ground, while broad wings support both flight and display behaviours. The spiky
         golden crown is used for visual signaling during courtship, and its powerful bill is adapted for foraging a wide variety of
         foods, from small animals to tough seeds. Its ability to tolerate shallow water and move gracefully across wet terrain
         demonstrates a combination of structural, behavioural, and ecological adaptations.'''.replace( '\n', ' ' ),
      '''Nesting occurs in dense vegetation close to water, with females laying 2–5 eggs per clutch. Both parents share incubation
         duties for about 27–31 days, after which chicks are cared for jointly until fledging several weeks later. Lifespan in the
         wild ranges from 15–20 years, while individuals in managed care may live up to 25 years, benefiting from regular food,
         veterinary care, and protection from predators.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Gaboon Viper',
      'Bitis Gabonica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Gaboon viper can be found an enclosure just through the entrance to the pavilion near the giraffes.''',
      None,                                                          # Seasonal viewing tips
      '''The Gaboon viper is a large, heavy-bodied snake with a broad, triangular head and striking geometric patterns that resemble
         fallen leaves. Adults typically measure 1.8–2.1 meters, with some exceeding 2.5 meters, and weigh up to 12–15 kg. Its
         colouration includes shades of brown, tan, gray, and purple, creating nearly perfect camouflage among rainforest leaf
         litter. The species is also known for having the longest fangs of any snake, up to 5 cm, which it uses to deliver potent
         venom.'''.replace( '\n', ' ' ),
      '''Gaboon vipers are found in West and Central African rainforests, secondary forests, and forested savannas. They prefer
         dense undergrowth, fallen logs, and areas with thick leaf litter, which allow them to remain hidden while ambushing prey.
         Although mostly terrestrial, they may occasionally climb low branches to access prey or bask in filtered sunlight.'''
         .replace( '\n', ' ' ),
      '''This viper is an ambush predator, feeding primarily on small to medium mammals, birds, and occasionally amphibians. Using
         its cryptic colouration and remarkable patience, it lies motionless for hours or even days until prey comes within striking
         distance. When striking, the Gaboon viper delivers a quick, deep bite with its long fangs, injecting potent hemotoxic venom
         that immobilizes prey almost instantly. Its broad body and strong muscles allow it to constrict slightly while subduing
         larger prey items.'''.replace( '\n', ' ' ),
      '''Gaboon vipers are solitary and sedentary, spending most of their time hidden beneath leaves or fallen logs. They rarely
         move far except to hunt or mate, conserving energy with their ambush strategy. When threatened, they rely on camouflage and
         freezing behaviour, only striking if directly provoked. During the breeding season, males may encounter each other and
         engage in brief combat rituals to compete for females, but interactions are generally limited and non-lethal.'''
         .replace( '\n', ' ' ),
      '''The Gaboon viper’s adaptations make it one of the rainforest’s most effective ambush predators. Its cryptic, leaf-like
         pattern conceals it from both prey and predators. Its long fangs and potent venom allow it to subdue relatively large prey
         with minimal effort. Broad, muscular body and slow metabolism enable extended periods of inactivity without feeding. The
         shape of its head, with horn-like scales above the nostrils, further breaks up its outline among leaves. These adaptations
         together allow the viper to thrive in dense, low-light rainforest floors where stealth is key to survival.'''
         .replace( '\n', ' ' ),
      '''Gaboon vipers are ovoviviparous, giving birth to 20–40 live young after a gestation period of 5–6 months. Neonates are
         independent immediately, relying on camouflage and instinct to survive. In the wild, they live approximately 12–15 years,
         though in managed care, some individuals can live over 20 years. Their reproductive strategy and relatively large litter
         sizes help maintain populations in their natural habitat, despite predation and habitat pressures.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Hamerkop',
      'Scopus Umbretta',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The hamerkop can be found in the aviary between the gorillas ,and the dwarf crocodiles and the Lake Malawi exhibit.''',
      None,                                                          # Seasonal viewing tips
      '''The hamerkop is a medium-sized wading bird, measuring 50–56 cm in length with a wingspan of about 80–95 cm. It is named for
         its distinctive hammer-shaped head, formed by a flat-topped crown and elongated bill. Plumage is uniformly brownish, with a
         slight reddish tinge, and its legs are long and sturdy for wading. Its head shape and overall profile make it instantly
         recognizable among African wetlands.'''.replace( '\n', ' ' ),
      '''Hamerkops are found throughout sub-Saharan Africa, inhabiting wetlands, rivers, lakes, marshes, and flooded grasslands.
         They prefer shallow water with open areas for foraging and nearby trees or reeds for roosting and nesting. Though they can
         occur at forest edges, they are mostly associated with wetland ecosystems and are sensitive to changes in water
         availability.'''.replace( '\n', ' ' ),
      '''Hamerkops are primarily carnivorous, feeding on fish, amphibians, aquatic insects, and small crustaceans. They hunt by
         walking slowly in shallow water, using their bill to probe mud and capture prey. They may also hunt along muddy banks or in
         flooded grasslands. Their feeding strategy relies on patience and careful movement to avoid alerting prey.'''
         .replace( '\n', ' ' ),
      '''Hamerkops are generally solitary or found in small groups, but they may gather in larger numbers near abundant food sources.
         They are renowned for their large, elaborate nests, sometimes up to 1.5 meters across, built from sticks and mud, often
         reused over multiple years. Outside of breeding, hamerkops are quiet and secretive, using low calls to communicate with
         nearby birds.'''.replace( '\n', ' ' ),
      '''The hamerkop’s hammer-shaped head and long bill are key adaptations for probing mud and shallow water for prey. Its long
         legs allow wading through varying water depths, and its body shape supports efficient flight between feeding and roosting
         sites. The species’ nest-building behaviour is also an adaptive strategy, providing protection from predators and
         environmental conditions for its eggs and chicks.'''.replace( '\n', ' ' ),
      '''Hamerkops build large, domed nests in trees or shrubs close to water. Females lay 2–5 eggs, which are incubated by both
         parents for about 25–30 days. Chicks are altricial and require parental care for several weeks before fledging. Lifespan in
         the wild is not well documented, but they may live 10–15 years, with slightly longer lifespans possible in managed care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Lake Malawi Cichlids',
      None,                                                          # Latin name
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Lake Malawai cichlids live in a large tank in the Lake Malawi exhibit, located between the gorilla rainforest and the
         rest of the pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Lake Malawi cichlids are small to medium-sized freshwater fish, ranging from 5–20 cm depending on the species. They display
         vivid colouration, including blues, yellows, oranges, and stripes, which often differentiate species and sexes. Males are
         usually brighter and more vividly patterned than females, especially during breeding. Body shapes vary, with some species
         elongated and laterally compressed, while others are more rounded, reflecting their ecological niches.'''
         .replace( '\n', ' ' ),
      '''These cichlids are native to Lake Malawi in East Africa, one of the world’s largest and most biodiverse rift lakes. They
         occupy a wide range of habitats, from rocky shorelines and sandy bottoms to open water and vegetated areas. Many species
         are highly territorial, particularly around breeding sites, and depend on stable water conditions with abundant food
         resources.'''.replace( '\n', ' ' ),
      '''Lake Malawi cichlids exhibit diverse feeding strategies, including algae scraping, invertebrate hunting, and mollusk
         crushing. Some species are planktivores, capturing tiny organisms from the water column, while others are specialized
         mouthbrooders, feeding opportunistically near their nests. In captivity, diets typically include high-quality flakes,
         pellets, and live or frozen invertebrates, mimicking their natural preferences and supporting colouration.'''
         .replace( '\n', ' ' ),
      '''These cichlids are highly social and territorial, with males often defending distinct territories against rivals. Complex
         behaviours include courtship displays, chasing, and colour changes, which communicate dominance, mating readiness, or
         aggression. Many species exhibit hierarchical social structures, with dominant males securing the best territories and
         mates, while subordinate individuals must wait or move elsewhere.'''.replace( '\n', ' ' ),
      '''Lake Malawi cichlids have evolved specialized adaptations for their lake environment. Their body shapes and jaw structures
         reflect feeding niches, allowing species to exploit algae, invertebrates, or small fish efficiently. Bright colouration in
         males functions in mate attraction and territory signaling, while camouflage helps some species avoid predators. The
         ability to defend territories and adapt to various microhabitats contributes to their high diversity and survival in a
         competitive ecosystem.'''.replace( '\n', ' ' ),
      '''Most Lake Malawi cichlids are maternal mouthbrooders, with females carrying eggs and fry in their mouths for protection,
         typically 2–3 weeks until the young are independent. Clutch sizes vary, usually ranging from 10–50 eggs. Sexual maturity is
         reached within 6–12 months, depending on species, and lifespan in captivity can extend 5–10 years, longer than in many wild
         populations due to reduced predation.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Leopard Ctenopoma',
      'Ctenopoma Acutirostre',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The leopard ctenopoma live in a tank in the Lake Malawi exhibit, located between the gorilla rainforest and the rest of the
         pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The leopard ctenopoma is a small, elongated freshwater fish, typically 10–15 cm in length. Its body is covered in irregular
         dark spots on a light brown or olive background, giving it a distinctive “leopard” pattern that provides camouflage among
         submerged vegetation. It has large, slightly upturned eyes suited for low-light hunting and a wide mouth adapted for
         capturing live prey. The fins are rounded and flexible, aiding in precise, stealthy movements.'''.replace( '\n', ' ' ),
      '''This species is native to slow-moving rivers, swamps, and floodplains in Central and West Africa. It prefers areas with
         dense aquatic vegetation, submerged roots, and leaf litter, which provide cover for both hunting and protection. Leopard
         ctenopomas are sensitive to water quality and rely on shaded, oxygen-rich microhabitats in their rainforest environments.'''
         .replace( '\n', ' ' ),
      '''Leopard ctenopomas are carnivorous ambush predators, feeding on small fish, insects, crustaceans, and aquatic invertebrates.
         They rely on slow, deliberate stalking and sudden lunges to capture prey. Their large mouths and expandable jaws allow them
         to take prey nearly half their own size. In captivity, they are often fed live or frozen invertebrates and small fish to
         encourage natural hunting behaviours.'''.replace( '\n', ' ' ),
      '''These fish are generally solitary and territorial, particularly in confined spaces. They are nocturnal or crepuscular, most
         active during low-light periods, which aligns with their stealth-based hunting strategy. Movement is deliberate and
         measured, relying on camouflage to avoid detection. While not social, individuals can tolerate conspecifics in large,
         well-structured exhibits that provide hiding spaces.'''.replace( '\n', ' ' ),
      '''Leopard ctenopomas possess several adaptations for survival in dense, slow-moving waters. Their spotted camouflage allows
         them to blend seamlessly with leaves and vegetation. Large, sensitive eyes enhance low-light vision, while their expansive
         mouth and flexible jaws facilitate efficient prey capture. Their fins allow precise positioning and slow stalking in
         cluttered aquatic habitats, reflecting adaptations for an ambush-predator lifestyle.'''.replace( '\n', ' ' ),
      '''Breeding is believed to occur in shallow, vegetated areas, with females scattering eggs among plants. Exact clutch sizes
         are not well documented, but juveniles are independent shortly after hatching. Leopard ctenopomas reach sexual maturity
         within 8–12 months and can live 5–7 years in captivity under optimal conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Mantella (Poison Frog)',
      'Mantella ssp.',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The mantella frog can be found in a terrarium in an enclosure between the dwarf crocodiles and Lake Malawai display, and
         the gorillas.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Mantella frogs are small, brightly coloured amphibians, typically measuring 2–3 cm in length. Their skin displays striking
         combinations of yellow, red, green, or blue, often contrasted with black markings, serving as a warning to potential
         predators. They have slender bodies, long legs, and adhesive toe pads, which allow agile movement across leaf litter and
         low vegetation. Males and females are similar in appearance, though males are slightly smaller and may have vocal sacs used
         during mating calls.'''.replace( '\n', ' ' ),
      '''These frogs are native to humid forests and rainforest floors of Madagascar, inhabiting leaf litter, low vegetation, and
         mossy areas near streams or puddles. They require moist environments to maintain skin hydration and support egg and tadpole
         development. Habitat loss and deforestation are major threats, making them important conservation ambassadors.'''
         .replace( '\n', ' ' ),
      '''Mantella frogs are insectivorous, feeding on ants, termites, small beetles, and other tiny invertebrates. They actively
         hunt on the forest floor, using their sticky tongues to capture prey. Their diet in the wild is closely linked to their
         toxicity, as they derive defensive alkaloids from consuming certain ants and arthropods. In captivity, they are fed a
         variety of small invertebrates to maintain health and colouration.'''.replace( '\n', ' ' ),
      '''These frogs are diurnal and relatively solitary, though males are territorial during breeding season. They communicate using
         high-pitched calls, particularly during mating periods, and are active hunters, constantly moving among leaf litter. Their
         small size and agility help them evade predators, while bright colouration serves as a warning signal to potential threats.'''
         .replace( '\n', ' ' ),
      '''Mantella frogs’ most notable adaptations include their aposematic colouration, which signals toxicity to predators, and
         specialized feeding habits, which allow them to sequester defensive chemicals from their prey. Their adhesive toe pads
         facilitate climbing and precise movement across slippery or uneven surfaces, while their small size allows them to exploit
         microhabitats inaccessible to larger animals. Their skin’s permeability enables cutaneous respiration, an adaptation to
         humid rainforest environments, but also requires constant moisture to prevent desiccation.'''.replace( '\n', ' ' ),
      '''Breeding occurs in moist areas, often in small puddles or water-filled leaf axils. Females lay 10–30 eggs, which males may
         guard and keep moist until hatching. Tadpoles develop in small pools or water pockets, feeding on detritus or unfertilized
         eggs in some species. Sexual maturity is typically reached in 6–12 months, depending on species, and lifespan in captivity
         can reach 5–7 years, slightly shorter in the wild.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Naked Mole Rat',
      'Heterocephalus Glaber',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The naked mole rats can be found in a tunnel-like habitat in the hallway in between the Lake Malawi exhibit and the stairs
         towards the pygmy hippos, waterfowl, and lemurs, and beside the Lau banded iguanas.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Naked mole-rats are small, hairless rodents, measuring 8–10 cm in length and weighing about 30–35 grams. They have pinkish
         wrinkled skin, tiny eyes, large incisors that protrude outside the mouth, and minimal fur, adaptations for their
         subterranean lifestyle. Their long, thin bodies and short limbs are specialized for burrowing, and their tail is short and
         hairless, aiding in balance underground.'''.replace( '\n', ' ' ),
      '''Naked mole-rats are native to arid regions of East Africa, including Kenya, Ethiopia, and Somalia. They live in extensive
         underground burrow systems that can span hundreds of meters, protecting them from predators and extreme surface
         temperatures. Their subterranean environment is humid and stable in temperature, which suits their specialized physiology.'''
         .replace( '\n', ' ' ),
      '''These rodents are herbivorous, feeding primarily on underground tubers and roots, which they locate using sensitive teeth
         and tactile whiskers. They can survive long periods with minimal water, extracting moisture directly from their food.
         Colonies may store food within burrow chambers to ensure survival during scarce periods.'''.replace( '\n', ' ' ),
      '''Naked mole-rats are eusocial, one of the few mammal species exhibiting a true caste system similar to social insects.
         Colonies consist of a single breeding queen, a few breeding males, and numerous non-breeding workers who maintain tunnels,
         forage, and care for the young. Workers are divided into “soldiers” for defense and “foragers” for food collection,
         demonstrating remarkable cooperation. Communication occurs via vocalizations, body contact, and vibration signals, allowing
         coordination within the dark tunnels.'''.replace( '\n', ' ' ),
      '''The naked mole-rat exhibits extraordinary adaptations for life underground. Its large incisors and powerful jaws allow
         efficient burrowing without soil entering the mouth. Hairlessness and nearly insensitive skin reduce friction while moving
         through tunnels. It has low metabolic rate and insensitivity to certain types of pain, adaptations for hypoxic burrow
         conditions. Remarkably, naked mole-rats show resistance to cancer, exceptional longevity (up to 30 years), and remarkable
         social cohesion, all adaptations for survival in challenging subterranean environments.'''.replace( '\n', ' ' ),
      '''Reproduction is restricted to the queen, who can produce 10–20 pups per litter, often multiple times per year. Non-breeding
         workers assist in raising the young. Sexual maturity occurs only in the queen and select males, while other colony members
         remain sterile. Lifespan is exceptionally long for rodents, often 25–30 years, allowing stable colony structure and
         multigenerational social continuity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Ngege',
      'Opsaridium microlepis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The ngege live in a tank in the Lake Malawi exhibit, located between the gorilla rainforest and the rest of the pavilion.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The ngege is a small to medium-sized cichlid, typically measuring 12–20 cm in length. It has a slender, laterally
         compressed body with silvery scales and faint vertical bands. Males often develop slightly brighter colours during breeding,
         with subtle iridescence, while females are more muted. The species has a terminal mouth adapted for picking food from the
         substrate or water column.'''.replace( '\n', ' ' ),
      '''Ngege are native to Lake Victoria and surrounding rivers in East Africa. They inhabit shallow coastal areas, rocky
         shorelines, and vegetated margins, preferring clear water where they can forage efficiently. They are territorial,
         particularly during breeding, and rely on structured habitats for protection from predators and access to food.'''
         .replace( '\n', ' ' ),
      '''The ngege is omnivorous, feeding on algae, small invertebrates, and detritus. They often graze on submerged surfaces or
         pick invertebrates from plants and rocks. Their feeding behaviour helps control algae growth and maintain ecological
         balance in freshwater habitats. In captivity, diets include flake foods, algae wafers, and live or frozen invertebrates.'''
         .replace( '\n', ' ' ),
      '''Ngege are semi-social, often forming loose groups while feeding but becoming territorial during breeding. Males display
         courtship behaviours, including colour changes, fin displays, and circling females. They communicate with subtle body
         movements and posturing, which helps maintain social hierarchies and breeding territories.'''.replace( '\n', ' ' ),
      '''This species has several adaptations for life in Lake Victoria. Its laterally compressed body allows agile movement among
         rocks and vegetation, while a versatile mouth enables feeding on both plant and animal matter. colouration provides
         camouflage against predators, and territorial behaviours help males secure prime breeding and feeding sites.'''
         .replace( '\n', ' ' ),
      '''Ngege are maternal mouthbrooders, with females carrying eggs and fry in their mouths for 2–3 weeks until juveniles are
         ready to fend for themselves. Clutch sizes are typically 50–100 eggs, depending on the size of the female. Sexual maturity
         is reached at about 6–8 months, and lifespan in captivity can reach 5–8 years with proper care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Nile Soft-Shelled Turtle',
      'Trionyx Triunguis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The nile soft-shelled turtle can be found in a habitat towards the end of the pavilion with the lemurs, up the path from
         that entrance, and before the pgymy hippos.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Nile soft-shelled turtle is a large freshwater turtle, with adults reaching 60–90 cm in carapace length and weighing
         30–50 kg. Unlike hard-shelled turtles, its carapace is leathery and flexible, brown to olive in colour, with small ridges
         and scattered dark spots. It has a long, tubular snout with nostrils at the tip, allowing it to breathe while mostly
         submerged. Limbs are broad and webbed, with strong claws for digging and grasping prey.'''.replace( '\n', ' ' ),
      '''This species is native to rivers, lakes, and wetlands across the Nile Basin, eastern Africa, and parts of the Middle East.
         It prefers slow-moving or still waters with sandy or muddy bottoms, often burying itself under sediment to hide from
         predators or ambush prey. Submerged logs, rocks, and vegetation provide additional cover and hunting perches.'''
         .replace( '\n', ' ' ),
      '''Nile soft-shelled turtles are carnivorous, feeding primarily on fish, amphibians, crustaceans, and other aquatic
         invertebrates. They are ambush predators, often lying buried under sand or mud with only their head exposed, striking
         quickly when prey passes by. Their tubular snout allows them to breathe while remaining hidden, increasing hunting
         efficiency.'''.replace( '\n', ' ' ),
      '''Generally solitary, these turtles spend most of their time submerged or partially buried, conserving energy and avoiding
         predators. They are mostly nocturnal or crepuscular hunters, active during early morning or evening. When threatened, they
         may retreat to deeper water or use their flexible shell and burrowing ability to hide. During mating, males may become
         more active and display courtship behaviour by nudging or circling females.'''.replace( '\n', ' ' ),
      '''The Nile soft-shelled turtle exhibits several adaptations for aquatic ambush predation. Its leathery carapace and flattened
         body allow streamlined movement and partial burial in sand. The long tubular snout enables stealthy breathing at the
         water’s surface. Powerful, webbed limbs aid in swimming and sudden lunges to capture prey. Its sensory adaptations,
         including keen sight and vibration detection, allow it to locate prey while remaining largely concealed.'''
         .replace( '\n', ' ' ),
      '''Females lay 20–40 eggs per clutch in sandy riverbanks, digging shallow nests to protect the eggs. Incubation lasts 8–12
         weeks, depending on temperature, with temperature influencing sex ratios. Hatchlings are independent from birth. Lifespan
         in the wild is estimated at 20–30 years, while in managed care, individuals can live even longer under optimal conditions.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Pygmy Hippopotamus',
      'Choeropsis Liberiensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The pygmy hippopotamus habitat can be found in between the lemurs and the path towards the pavilion entrance/exit near the
         giraffes, and the rest of the pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The pygmy hippopotamus is a compact, semi-aquatic mammal, typically measuring 1.5–1.75 meters in length and weighing
         180–275 kg. It has a dark brown to slate-gray skin, smooth and nearly hairless, which secretes a natural, reddish
         “sunscreen” to protect against dehydration and infection. Unlike the common hippopotamus, the pygmy hippo has
         proportionally smaller, rounded eyes and ears, positioned higher on the head for underwater vision while keeping most of
         the body submerged. Its limbs are short and sturdy, supporting movement on soft forest floors and in shallow streams.'''
         .replace( '\n', ' ' ),
      '''Pygmy hippos are native to the dense forests and swamps of West Africa, particularly Liberia, Sierra Leone, Guinea, and
         Ivory Coast. They inhabit freshwater swamps, forested rivers, and marshy areas, requiring both land and water to meet
         feeding, thermoregulation, and safety needs. Unlike their larger relatives, pygmy hippos are more forest-adapted, relying
         on cover and shade rather than open waters.'''.replace( '\n', ' ' ),
      '''Pygmy hippos are herbivorous, feeding mainly at night. Their diet consists of leaves, ferns, fruits, grasses, and aquatic
         vegetation, which they forage in forested areas near water. They may also feed on fallen fruits in swampy areas. Foraging
         is argely solitary, and their digestive system is adapted to ferment and extract nutrients from fibrous plant material.'''
         .replace( '\n', ' ' ),
      '''Pygmy hippos are mostly solitary, coming together primarily for mating. They are nocturnal or crepuscular, avoiding daytime
         heat. They communicate through vocalizations, scent marking, and body postures, and can be surprisingly agile both in water
         and on land. Unlike the social common hippo, pygmy hippos have small, well-defined home ranges and tend to avoid encounters
         with other adults outside of breeding.'''.replace( '\n', ' ' ),
      '''Pygmy hippos exhibit several adaptations for a semi-aquatic, rainforest lifestyle. Their high-set eyes and ears allow them
         to remain mostly submerged while observing their surroundings. Smooth, nearly hairless skin secretes protective oils to
         prevent drying and infection, while short, strong legs enable walking through soft, muddy substrates. Pygmy hippos are also
         strong swimmers, using webbed toes to navigate streams efficiently. Their nocturnal behaviour reduces heat stress and
         predation risk, and they are adapted to forage on nutrient-poor forest vegetation, making them highly specialized
         herbivores.'''.replace( '\n', ' ' ),
      '''Pygmy hippos breed year-round, with a gestation period of about 6–7 months. Females typically give birth to a single calf,
         which is precocial and able to follow its mother within hours of birth. Calves are dependent for the first few months but
         quickly learn to swim and forage. Sexual maturity occurs at 3–5 years, and pygmy hippos can live 30–35 years in managed
         care, slightly less in the wild due to predation and habitat pressures.'''.replace( '\n', ' ' ),
      '''The zoo is home to a breeding pair of pygmy hippos, a male Harvey and a female Kindia. Unless they are being put together
         for breeding, they can each be seen in on of their two habitats in the African Rainforest Pavilion. Female, Kindia, is
         pregnant and expecting a calf in late July.'''.replace( '\n', ' ' )
   ),
   (
      'Radiated Tortoise',
      'Astrochelys Radiata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The radiated tortoises can be found in an enclosure in the hallway between the chameleons, iguanas, and naked mole rats,
         and the ramped pathway towards the pygmy hippos and lemurs.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The radiated tortoise is a medium-sized land tortoise, typically measuring 35–45 cm in length and weighing 8–14 kg, with
         some individuals reaching over 20 kg. Its high-domed shell is dark brown or black with striking yellow or orange star-like
         patterns radiating from the center of each scute, giving the species its name. The head is relatively small, with a pointed
         beak for grazing, and the limbs are thick and sturdy, equipped with scales and claws for walking on rough terrain.'''
         .replace( '\n', ' ' ),
      '''Radiated tortoises are native to southern Madagascar, where they inhabit dry forests, thorny scrublands, and spiny bush
         areas. They rely on open patches for basking and dense vegetation for cover from predators. Their habitat requires access
         to freshwater sources and seasonal vegetation, which sustains their herbivorous diet.'''.replace( '\n', ' ' ),
      '''These tortoises are strict herbivores, feeding on grasses, leaves, fruits, and succulent plants. They are well-adapted to
         dry, nutrient-poor environments, able to digest fibrous vegetation efficiently. In captivity, diets typically include a mix
         of leafy greens, vegetables, and hay, with occasional fruits to mimic natural food variety. Their grazing behaviour also
         helps seed dispersal in their native ecosystems.'''.replace( '\n', ' ' ),
      '''Radiated tortoises are generally solitary, though they may gather in small groups around abundant food sources or water.
         They are slow-moving and diurnal, spending the day foraging, basking, or resting in shaded areas. Communication is limited,
         mainly involving head bobbing or mild vocalizations during social interactions or mating. Despite their slow pace, they are
         capable of rapid retreats if threatened.'''.replace( '\n', ' ' ),
      '''The radiated tortoise’s high-domed, star-patterned shell provides protection from predators and camouflage among
         sun-dappled forest floors. Its strong, clawed limbs allow it to traverse rocky and sandy terrain, while its digestive
         system extracts nutrients efficiently from tough, fibrous plants. Its ability to store water and survive periods of drought
         is a key adaptation for Madagascar’s dry seasons. These adaptations make it highly specialized for survival in arid and
         semi-arid environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally, with females laying 5–15 eggs per clutch in shallow burrows. Incubation lasts approximately
         8–10 months, with temperature influencing sex ratios. Hatchlings are small but independent, relying on camouflage and
         instinct for survival. Radiated tortoises are long-lived, with wild individuals reaching 40–50 years, and some in managed
         care living over 60 years.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red River Hog',
      'Potamochoerus Porcus',
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The red river hog habitat can be found around the outside of the African Rainforest Pavilion. From the entrance near the
         giraffes, when facing tha pavilion turn to the right and they will be on the left just past the entrance to the giraffe
         house. From the entrance near the gorillas, go to the left and you will find the hogs just pace the Multi-faith prayer
         room.'''.replace( '\n', ' ' ),
      '''Red river hogs do surprisingly well in cooler temperatures can usually be seen outside from April until November, and
         perhaps from even earlier in the year.'''.replace( '\n', ' ' ),
      '''Red river hogs are medium-sized wild pigs, measuring 90–130 cm in body length and weighing 45–115 kg, with males typically
         larger than females. They are instantly recognizable by their rich reddish-brown fur, black legs, white facial markings,
         and large, tufted ears. Both sexes have prominent tusks, though those of males are longer and more curved, used for defense
         and foraging. Their elongated snouts are highly sensitive, equipped with tactile receptors to locate food underground.
         Piglets are born with striped coats that provide camouflage among forest leaf litter.'''.replace( '\n', ' ' ),
      '''Red river hogs are native to West and Central African forests, including countries like Nigeria, Cameroon, Gabon, and the
         Congo Basin. They inhabit dense lowland rainforests, swamps, riverine forests, and secondary forests, often close to water.
         Their habitats must provide ample cover for hiding from predators, such as leopards and large birds of prey, as well as
         soft soil and leaf litter for rooting. Seasonal flooding and wetland areas are particularly valuable, as they provide
         wallowing sites and abundant food resources.'''.replace( '\n', ' ' ),
      '''These hogs are omnivorous opportunists, with diets including roots, tubers, fruits, fungi, insects, small mammals,
         amphibians, and carrion. Their flexible snouts and tusks allow them to dig through soil, leaf litter, and decaying wood to
         uncover hidden food. Feeding is typically crepuscular, occurring during early morning or late afternoon, although hogs may
         forage at night in areas with human disturbance. Their foraging also contributes to seed dispersal and soil aeration,
         making them important ecosystem engineers.'''.replace( '\n', ' ' ),
      '''Red river hogs are highly social animals, living in sounders of 6–20 individuals, usually comprised of females and their
         young. Adult males are more solitary but maintain overlapping territories with multiple sounders. Within groups, hogs
         communicate via grunts, squeals, and alarm calls, often supplemented by body language and scent marking. Social hierarchies
         exist, and cooperative behaviours include group foraging and vigilance against predators. They display playful behaviours,
         such as chasing each other, nudging, and mock-fighting, which help strengthen social bonds and practice defensive skills.'''
         .replace( '\n', ' ' ),
      '''Red river hogs are highly adapted to their forested and wetland habitats. Their reddish fur provides camouflage, while
         black legs and white facial markings may facilitate visual communication within dense vegetation. Tusks and strong jaws are
         used both for rooting and for defending against predators. Their long, mobile snouts allow precise foraging underground,
         while large, sensitive ears detect distant sounds. Wallows in mud help regulate body temperature, reduce parasite load, and
         provide skin protection. Omnivorous flexibility and territorial intelligence allow them to survive in dynamic,
         predator-rich rainforest environments.'''.replace( '\n', ' ' ),
      '''Breeding is year-round, but peaks in wet seasons when food is abundant. Females give birth to 2–6 piglets after a gestation
         of approximately 120–130 days. Piglets are precocial, covered with striped fur that fades with age, and are able to follow
         the mother and sounder almost immediately. Weaning occurs at 3–4 months, and juveniles begin rooting and foraging alongside
         adults. Sexual maturity is reached around 18–24 months, and red river hogs can live 10–12 years in the wild, with zoo
         individuals sometimes exceeding 15 years due to reduced predation and consistent food supply.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a family of four red river hogs.'''
   ),
   (
      'Ring-Tailed Lemur',
      'Lemur Catta',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The ring-tailed lemurs can be seen in a mixed-species habitat with the crowned cranes and Aldabra tortoise near the
         entrance to the pavilion near the giraffes.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Ring-tailed lemurs are medium-sized primates, typically weighing 2.2–3.5 kg and measuring 39–46 cm in body length, with an
         additional 45–55 cm tail. Their most striking feature is the long, bushy tail with alternating black and white rings, which
         is not prehensile but used for balance and social signaling. Fur on the body is gray to rosy-brown, with white underparts
         and a dark face framed by white facial markings. Eyes are bright amber or orange, and their expressive faces help convey
         social cues within the group.'''.replace( '\n', ' ' ),
      '''Ring-tailed lemurs are native to southern and southwestern Madagascar, inhabiting dry forests, spiny bush areas, gallery
         forests, and scrublands. Unlike many lemurs that live primarily in dense forests, ring-tailed lemurs often spend time on
         the ground and in open areas, foraging and sunbathing. They rely on trees for sleeping, safety, and food, but are highly
         adaptable to varying terrain.'''.replace( '\n', ' ' ),
      '''These lemurs are omnivorous, feeding primarily on fruit, leaves, flowers, bark, and sap, supplemented occasionally with
         insects or small vertebrates. Their diet changes seasonally depending on fruit availability. Ring-tailed lemurs spend
         significant time foraging in groups, using their keen sense of smell to locate ripe fruit and edible plant parts. In
         managed care, diets are supplemented with a variety of fruits, vegetables, leafy greens, and specialized primate pellets to
         meet nutritional needs.'''.replace( '\n', ' ' ),
      '''Ring-tailed lemurs are highly social, living in groups called troops that range from 10 to 30 individuals, often led by a
         dominant female. Their social hierarchy is matriarchal, with females dominating males in access to food, resting spots, and
         mates. Group life involves complex vocal communication, including alarm calls, territorial calls, and social chatter, as
         well as grooming behaviours that strengthen social bonds. Males engage in scent-marking using wrist and chest glands,
         sometimes rubbing scent on trees to mark territory or communicate dominance.'''.replace( '\n', ' ' ),
      '''Ring-tailed lemurs have several adaptations for both arboreal and terrestrial life. Their hands and feet are adapted for
         climbing and gripping branches, while their strong legs allow agile movement on the ground. Their long tails are used for
         visual communication during group movement, and sunbathing behaviour in the morning helps thermoregulate in cooler
         conditions. A highly developed sense of smell aids in social signaling and foraging. Social behaviour itself is an
         adaptation, increasing survival through group defense against predators and cooperative care of young.'''
         .replace( '\n', ' ' ),
      '''Ring-tailed lemurs breed seasonally, with mating occurring April–June. Females give birth to a single offspring after a
         gestation of about 135 days, usually in September–October. Infants cling to their mothers for the first weeks and gradually
         integrate into group activities. Sexual maturity is reached at 2–3 years, and lifespan in managed care can reach 20–25
         years, though wild individuals often live shorter lives due to predation and habitat pressures.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a family of five ring-tailed lemurs.'''
   ),
   (
      'Royal Python',
      'Python Regius',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The royal python can be found an enclosure just through the entrance to the pavilion near the giraffes.''',
      None,                                                          # Seasonal viewing tips
      '''Royal pythons are small to medium-sized snakes, typically 90–120 cm in length, with females generally larger than males.
         Their skin is patterned with dark brown or black blotches outlined in gold or tan, giving them a striking appearance. The
         head is triangular, with heat-sensitive pits along the upper lip that aid in detecting warm-blooded prey. These snakes have
         a thick, muscular body and smooth scales, and are non-venomous constrictors.'''.replace( '\n', ' ' ),
      '''Royal pythons are native to West and Central Africa, inhabiting grasslands, savannas, open forests, and agricultural areas.
         They spend much of their time underground or in burrows, using abandoned mammal dens, termite mounds, or natural crevices
         to hide during the day and avoid predators. They prefer humid microclimates but are adaptable to a range of conditions
         within their range.'''.replace( '\n', ' ' ),
      '''These pythons are carnivorous constrictors, feeding primarily on small mammals, birds, and occasionally amphibians. Hunting
         is mostly nocturnal. They strike quickly, coil around their prey, and use muscular constriction to subdue it before
         swallowing whole. In captivity, their diet is typically appropriately sized rodents, fed at intervals depending on size and
         age.'''.replace( '\n', ' ' ),
      '''Royal pythons are solitary and secretive, spending much of their time hidden. They are nocturnal hunters, emerging at night
         to search for food. When threatened, they exhibit a defensive coiling behaviour, curling into a tight ball with the head
         protected in the center — a behaviour that gives them the name “ball python.” They are generally docile in captivity, which
         contributes to their popularity in educational exhibits and the pet trade.'''.replace( '\n', ' ' ),
      '''Royal pythons have evolved numerous adaptations for ambush predation. Heat-sensitive pits allow detection of warm-blooded
         prey even in darkness. Their muscular bodies enable efficient constriction of prey, and their flexible jaws allow
         swallowing animals larger than their head diameter. Cryptic colouration provides camouflage in leaf litter and burrows,
         while their coiling defense behaviour reduces predation risk. Burrowing and nocturnal activity also help them avoid
         predators and harsh daytime conditions.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the dry season, with females laying 4–10 eggs in warm, secure sites such as burrows or rotting
         vegetation. Eggs incubate for 55–60 days, and hatchlings emerge fully independent. Royal pythons reach sexual maturity at
         2–5 years, depending on growth and size. Lifespan in captivity can reach 20–30 years, while wild individuals generally live
         shorter lives due to predation and environmental hazards.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Sacred Ibis',
      'Threskiornis Aethiopicus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The sacred ibis can be found in a shared exhibit with other waterfowl--the African spoonbill, and South African shelduck,
         near the soft-shelled turtle and pygmy hippos.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The sacred ibis is a medium-sized wading bird, measuring 65–75 cm in length with a wingspan of 112–124 cm. It has a white
         body contrasted with black head, neck, and legs, and a long, downward-curved bill adapted for probing mud and shallow water.
         Eyes are dark, and the bird has bare skin on the head and face, which may help reduce parasite buildup. Its legs are long
         and slender, allowing it to wade efficiently in wetlands.'''.replace( '\n', ' ' ),
      '''Sacred ibises are native to sub-Saharan Africa and parts of the Nile Valley, inhabiting wetlands, marshes, riverbanks, and
         shallow lakes. They favor areas with muddy substrates for foraging and trees or reed beds for nesting. Although they often
         live near water, they are also capable of foraging in flooded grasslands and cultivated areas.'''.replace( '\n', ' ' ),
      '''The sacred ibis is an omnivorous forager, feeding on insects, crustaceans, small fish, amphibians, worms, and occasionally
         seeds. It uses its long, curved bill to probe mud and shallow water for hidden prey. Feeding is often done in groups, with
         multiple birds foraging together, which may increase foraging efficiency and provide safety in numbers.'''
         .replace( '\n', ' ' ),
      '''These birds are social and colonial, often nesting and foraging in large groups. Nests are built in trees, reed beds, or
         shrubs, and colonies may consist of hundreds of pairs. Vocal communication is common, with various honking and squawking
         calls used to maintain contact or alert others to predators. During foraging, they exhibit coordinated probing and feeding,
         minimizing competition while maximizing efficiency.'''.replace( '\n', ' ' ),
      '''Sacred ibises have several adaptations for wetland life. Their long, curved bill allows them to reach prey in mud or
         shallow water, while long legs and partially webbed feet enable wading in varying depths. Bare skin on the head and neck
         reduces parasite load during feeding in muddy environments. Their social lifestyle provides predator detection and
         cooperative foraging, while their strong flight muscles allow rapid travel between feeding and nesting sites.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs in seasonal colonies, often during the rainy season. Females lay 2–5 eggs in nests made of sticks, reeds,
         and other vegetation. Both parents share incubation duties, which lasts approximately 21–28 days. Chicks are altricial,
         hatching blind and featherless, but fledge in about 35–45 days. Sacred ibises can live 10–15 years in the wild, and
         slightly longer in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Slender-Tailed Meerkat',
      'Suricata Suricatta',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The slender-tailed meerkats can be found in a mixed-species habitat with the South African crested porcupine in a part of
         the pavilion in between the Lake Malwai exhibit and gorilla rainforest and the rest of the pavilion. The enclosure is
         located in the hallway towards the savanna overlook, peering into the kudu habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Slender-tailed meerkats are small, slender carnivores, measuring 25–35 cm in body length, with tails of 20–25 cm. They
         weigh 0.6–1 kg, making them highly agile. Their fur is tan to light brown with gray undertones, featuring distinct dark
         bands across the back. The face has dark eye patches that reduce glare from the sun, and the tail is tipped with black,
         which serves as a visual signal during group movement. Their sharp claws are well adapted for digging, and their eyes are
         large and forward-facing, providing good binocular vision for spotting predators and prey.'''.replace( '\n', ' ' ),
      '''Slender-tailed meerkats are native to southern Africa, including Botswana, Namibia, South Africa, and Angola. They inhabit
         arid and semi-arid savannas, open plains, and scrublands, favoring areas with sandy soils suitable for burrowing. Their
         extensive underground burrow networks provide shelter from heat, predators, and harsh weather, as well as nursery chambers
         for raising young.'''.replace( '\n', ' ' ),
      '''These meerkats are omnivorous, feeding primarily on insects, spiders, scorpions, small reptiles, eggs, and occasionally
         small mammals or plants. They forage in groups during the day, using keen eyesight and acute sense of smell to locate prey.
         Adults often dig to uncover insects or grubs, while juveniles learn hunting skills under adult supervision. Their diet and
         cooperative hunting behaviours are essential for survival in the resource-sparse environments they inhabit.'''
         .replace( '\n', ' ' ),
      '''Slender-tailed meerkats are highly social, living in cohesive groups called mobs or clans, typically containing 10–30
         individuals, but sometimes larger. Groups are organized with a dominant breeding pair, while other members serve as
         helpers, foraging, babysitting, and maintaining vigilance. Meerkats are diurnal, and sentinel behaviour is a hallmark: one
         individual stands guard on a mound, scanning for predators while others forage. Vocalizations include alarm calls, social
         chirps, and contact calls, coordinating group activities and signaling threats. Play, grooming, and cooperative care
         strengthen social bonds and teach young essential survival skills.'''.replace( '\n', ' ' ),
      '''Meerkats exhibit adaptations for desert and semi-arid life. Their slender bodies and light fur help regulate body
         temperature in the hot sun, while dark eye patches reduce glare. Sharp, curved claws enable efficient digging of extensive
         burrow systems, which provide protection and temperature control. Their cooperative social structure enhances survival,
         with sentinels detecting predators and helpers ensuring food distribution and pup care. They also have resistance to
         certain venoms, allowing them to prey on scorpions safely.'''.replace( '\n', ' ' ),
      '''Breeding is typically dominated by the alpha pair, though subordinate females may occasionally reproduce. Gestation lasts
         about 11 weeks, producing 2–5 pups per litter. Pups are born blind and hairless, spending the first few weeks in the burrow
         under the care of helpers. They emerge at 3–4 weeks, gradually learning to forage and participate in sentinel duties.
         Sexual maturity is reached around 12 months, and lifespan in the wild is usually 6–8 years, while in managed care they may
         live up to 12–14 years.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'South African Crested Porcupine',
      'Hystrix Africaeaustralis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The South African crested porcupine can be found in a mixed-species habitat with the slender-tailed meerkats in a part of
         the pavilion in between the Lake Malwai exhibit and gorilla rainforest and the rest of the pavilion. The enclosure is
         located in the hallway towards the savanna overlook, peering into the kudu habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''South African crested porcupines are large rodents, measuring 60–83 cm in body length with a tail of 20–30 cm and weighing
         10–18 kg. They are notable for their long, sharp quills, which are black and white-banded and raised along the back when
         threatened. The body is stocky and rounded, with coarse dark fur covering non-quilled areas. Their face features small eyes,
         strong incisor teeth, and prominent whiskers. The tail also bears quills used for defense and warning signals.'''
         .replace( '\n', ' ' ),
      '''This species inhabits southern and eastern Africa, including South Africa, Namibia, Botswana, Zimbabwe, and Mozambique.
         They are found in savannas, open forests, rocky hills, and scrublands, often near burrowable soil. They spend daylight
         hours in underground burrows to avoid heat and predators, emerging at night to forage.'''.replace( '\n', ' ' ),
      '''South African crested porcupines are herbivorous and nocturnal foragers, feeding on roots, tubers, bulbs, bark, fruits, and
         occasionally small invertebrates. Their strong incisor teeth allow them to gnaw tough plant material and even dig up
         subterranean food sources. They play an important ecological role by aerating soil through burrowing and dispersing seeds
         through their feeding activities.'''.replace( '\n', ' ' ),
      '''Porcupines are primarily nocturnal and crepuscular, emerging at dusk to forage in small family groups or pairs. They are
         generally docile unless threatened, relying on quill displays, foot-stamping, and teeth gnashing as warning signals. When
         attacked, they may charge backward toward a predator, embedding sharp quills as a defense. Social interactions are subtle
         but include mutual grooming, scent marking, and vocalizations such as grunts and squeaks.'''.replace( '\n', ' ' ),
      '''The most notable adaptation is their quills, which provide an effective deterrent against predators. Quills are modified
         hairs, some with barbed tips that can become embedded in attackers. Their strong, robust claws and teeth allow efficient
         burrowing and root extraction. Nocturnal habits reduce heat stress and predation risk, while keen senses of smell and
         hearing help detect food and danger. Their slow metabolism and ability to digest tough plant material allow survival in
         resource-variable environments.'''.replace( '\n', ' ' ),
      '''Porcupines are monogamous, often forming long-term pairs. Females give birth to 1–3 well-developed young after a gestation
         of about 90–112 days. The young are born with soft quills that harden within a few days, and they remain dependent on the
         mother for several weeks. Sexual maturity is reached around 2 years, and these porcupines can live 15–18 years in the wild
         and slightly longer in captivity.'''.replace( '\n', ' ' ),
      '''The zoo is home to a male porcupine named Mr. P.'''
   ),
   (
      'South African Shelduck',
      'Tadorna Cana',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The South African shelduck can be found in a shared exhibit with other waterfowl--the African spoonbill, and sacred ibis,
         near the soft-shelled turtle and pygmy hippos.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The South African shelduck is a medium-sized waterfowl, measuring 54–58 cm in length with a wingspan of 90–100 cm. Males
         have a chestnut-brown body with white wing patches, a dark green head, and a white neck collar, while females are slightly
         duller with less pronounced colouration. Both sexes have bright red bills and legs, making them easily identifiable.
         Juveniles are duller and take several months to develop adult plumage.'''.replace( '\n', ' ' ),
      '''This species is native to southern Africa, including South Africa, Namibia, Botswana, and Zimbabwe, inhabiting freshwater
         lakes, rivers, estuaries, and marshes. They are semi-migratory, often moving seasonally between inland wetlands and coastal
         areas depending on water availability and breeding needs.'''.replace( '\n', ' ' ),
      '''South African shelducks are omnivorous, feeding on aquatic invertebrates, insects, small crustaceans, seeds, and plant
         matter. They typically forage by dabbling or grazing along shorelines, occasionally tipping forward in shallow water to
         access submerged food. Foraging often occurs in pairs or small groups, and they may form larger flocks during non-breeding
         seasons.'''.replace( '\n', ' ' ),
      '''Shelducks are social birds, forming monogamous pairs during the breeding season and joining larger flocks outside of
         reproduction. They are diurnal, with activity peaks during the morning and late afternoon. Flight is strong and direct, and
         birds often communicate through loud, honking calls used for mate communication, flock cohesion, or warning of potential
         threats.'''.replace( '\n', ' ' ),
      '''South African shelducks have adaptations for both terrestrial and aquatic life. Their partially webbed feet allow efficient
         swimming and wading, while strong wings facilitate long-distance flight during seasonal movements. The bill is adapted for
         dabbling and grazing, allowing a flexible diet. Their social flocking behaviour increases predator detection and foraging
         efficiency.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the southern hemisphere spring and early summer, with females laying 8–12 eggs in burrows, tree
         cavities, or abandoned nests of other birds. Both parents help defend the nest, though the female primarily incubates for
         28–30 days. Chicks are precocial and leave the nest shortly after hatching, capable of feeding themselves under parental
         supervision. Lifespan in the wild is typically 10–12 years, with longer survival in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Speckled Mousebird',
      'Colius Striatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The speckled mousebird can be found in the small aviary on the elevated pathway near the mixed waterfowl enclosure.''',
      None,                                                          # Seasonal viewing tips
      '''Speckled mousebirds are small to medium-sized birds, measuring 25–30 cm in length, with a long, thin tail that accounts for
         about half of their total length. Their plumage is soft gray-brown with fine white speckling, giving a subtly mottled
         appearance. They have a small, rounded head with a short crest, and dark eyes with a short, slightly curved bill adapted
         for feeding on fruit and foliage. Their legs are strong, allowing them to climb and scurry along branches in a mouse-like
         fashion, which gives the species its common name.'''.replace( '\n', ' ' ),
      '''Speckled mousebirds are native to sub-Saharan Africa, including countries such as South Africa, Botswana, Zimbabwe, and
         Kenya. They inhabit savannas, woodland edges, gardens, and scrublands, often near fruiting trees and shrubs. They are
         highly arboreal but will move on the ground or between branches when foraging.'''.replace( '\n', ' ' ),
      '''These birds are primarily herbivorous, feeding on fruits, berries, leaves, buds, and flowers. They forage in small groups,
         often moving slowly and deliberately through foliage. Their diet provides essential nutrients and fiber, and their foraging
         behaviour also contributes to seed dispersal. Occasionally, they may nibble on insects or other small invertebrates to
         supplement their diet.'''.replace( '\n', ' ' ),
      '''Speckled mousebirds are highly social, usually found in small flocks of 6–20 individuals. They are active and agile, using
         their strong feet and flexible toes to grasp branches and move in a climbing or hanging posture. Mousebirds are vocal,
         communicating with soft chirps and whistles. Social behaviours include mutual preening, huddling for warmth, and
         cooperative alertness against predators.'''.replace( '\n', ' ' ),
      '''Mousebirds have several unique adaptations for arboreal life. Their strong feet with reversible outer toes allow them to
         climb, hang upside down, and move efficiently through foliage. The long tail aids balance during movement, while their soft
         plumage provides insulation. Their diet and digestive system are adapted to process fibrous plant material, and their
         social behaviour increases survival through shared vigilance and cooperative care of young.'''.replace( '\n', ' ' ),
      '''Breeding occurs during times of food abundance, often synchronized with fruiting seasons. Females lay 2–6 eggs in small,
         loosely constructed nests made of twigs and leaves, usually located in dense foliage. Both parents help incubate the eggs
         for about 13–16 days, and chicks are altricial, requiring care and feeding for several weeks before fledging. Lifespan in
         the wild is typically 6–8 years, with longer survival in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Spider Tortoise',
      'Pyxis Arachnia',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The spider tortoise can be found in a habitat between the gorillas and the dwarf crocodiles.''',
      None,                                                          # Seasonal viewing tips
      '''Spider tortoises are small, terrestrial turtles, measuring 8–15 cm in length and weighing 200–300 grams. Their high-domed
         carapace is dark brown to black with radiating yellow or cream lines on each scute, resembling a spiderweb, which gives the
         species its common name. The head is relatively small with a pointed snout, and the legs are thick and covered in scales,
         equipped with claws for digging. They have short tails, and their skin is dark gray to brown, complementing their cryptic
         shell pattern.'''.replace( '\n', ' ' ),
      '''Spider tortoises are endemic to southwestern Madagascar, primarily inhabiting spiny forests and scrublands with sandy,
         well-drained soils. They prefer areas with dense leaf litter and scattered shrubs, which provide cover and microhabitats
         for foraging and shelter. Seasonal rainfall heavily influences their activity patterns, as the species relies on moisture
         for feeding and reproduction.'''.replace( '\n', ' ' ),
      '''These tortoises are herbivorous, feeding on succulent plants, leaves, fruits, and flowers. They forage primarily during the
         wet season, when plant material is more abundant, and may burrow or hide during the dry season to conserve water. Their
         diet contributes to seed dispersal and vegetation management in their native ecosystems. In zoos, they are fed a diet of
         leafy greens, vegetables, and occasional fruits, carefully balanced to mimic natural nutrition.'''.replace( '\n', ' ' ),
      '''Spider tortoises are solitary and secretive, spending much of their time hidden under leaf litter, shrubs, or in shallow
         burrows. They are primarily diurnal during cooler periods but may reduce activity during the hottest parts of the day.
         Communication is limited, with interactions mostly occurring during breeding season. Despite their small size, they are
         curious and cautious, often retracting into their shells when threatened.'''.replace( '\n', ' ' ),
      '''Spider tortoises have several adaptations for survival in arid, spiny forests. Their high-domed, radiated shell provides
         camouflage among dry leaves and shrubs while offering protection from predators. Strong, clawed legs allow digging for
         shelter or food, and their ability to conserve water and remain inactive during dry periods helps them endure harsh
         seasonal conditions. Their herbivorous diet and selective feeding on moisture-rich plants optimize water and nutrient
         intake in their environment.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs during the wet season, when females lay 1–3 small, hard-shelled eggs in shallow nests dug into
         sandy soil. Incubation lasts 60–90 days, depending on temperature and humidity. Hatchlings are independent immediately but
         face high predation and environmental risks. Sexual maturity is reached around 5–7 years, and lifespans can exceed 50
         years in captivity, though wild individuals often have shorter lifespans due to predation and habitat pressures.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Straw Coloured Fruit Bat',
      'Eidolon Helvum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The straw coloured fruit bats can be seen by facing the mixed waterfowl enclosure and looking up and to the left.''',
      None,                                                          # Seasonal viewing tips
      '''Straw-coloured fruit bats are large megabats, with a wingspan of 1.2–1.5 meters and a body length of 15–20 cm, weighing
         300–600 grams. Their fur is typically straw-yellow to light brown, contrasting with darker flight membranes. They have a
         fox-like face with large eyes, a long snout, and prominent rounded ears, adaptations that enhance their sensory perception.
         Unlike insectivorous bats, they lack echolocation and rely on keen vision and smell to locate food.'''.replace( '\n', ' ' ),
      '''These bats are native to sub-Saharan Africa, ranging from Senegal to Ethiopia and south to South Africa. They inhabit
         tropical forests, savannas, and urban areas, often roosting in large trees, forest edges, and sometimes in city parks.
         Straw-coloured fruit bats are highly mobile, undertaking seasonal migrations of hundreds of kilometers in search of
         fruiting trees.'''.replace( '\n', ' ' ),
      '''They are frugivorous, feeding primarily on figs, mangoes, guavas, and other native and cultivated fruits. They may also
         consume nectar and flowers occasionally. Foraging occurs at night, with bats traveling long distances to locate abundant
         food sources. Their feeding behaviour makes them key seed dispersers, facilitating the regeneration of tropical forests
         across vast areas.'''.replace( '\n', ' ' ),
      '''Straw-coloured fruit bats are highly social, forming colonies of thousands to millions in roosting trees. Social
         hierarchies are subtle, with large numbers offering safety in numbers against predators such as owls, snakes, and humans.
         They are nocturnal, resting during the day in shaded trees and emerging at dusk to feed. Colonies are noisy, filled with
         squawks, chatter, and wing-flapping, which also aids in group cohesion and territorial spacing.'''.replace( '\n', ' ' ),
      '''These bats are adapted for long-distance flight and nocturnal foraging. Their large wings with high aspect ratios allow
         energy-efficient travel, while strong eyes and an acute sense of smell guide them to ripe fruit. Their teeth and jaws are
         adapted for biting and chewing soft fruit, and their digestive system allows rapid seed dispersal. Roosting in large
         colonies reduces predation risk and facilitates thermoregulation through huddling.'''.replace( '\n', ' ' ),
      '''Breeding is seasonally synchronized, typically coinciding with periods of abundant fruit availability. Females give birth
         to a single pup after a gestation of about 5–6 months. Pups cling to their mothers for the first few weeks and are
         gradually weaned after 2–3 months. Sexual maturity is reached at 1–2 years, and in captivity, they can live 15–20 years,
         while ifespans in the wild are slightly shorter due to predation and migration challenges.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Tomato Frog',
      'Dyscophus Antongilii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tomato frog can be found in a terrarium in an enclosure between the dwarf crocodiles and Lake Malawai display, and the
         gorillas.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Tomato frogs are medium-sized amphibians, with females larger than males, measuring 6–10 cm in length. Their most
         distinctive feature is their bright red to orange-red colouration, which serves as a warning to predators. Males are
         smaller and slightly duller. They have rounded bodies, short limbs, and large, protruding eyes, giving them a robust, squat
         appearance. The skin is smooth and slightly sticky, with mucus glands that can secrete a mild toxin when threatened.'''
         .replace( '\n', ' ' ),
      '''Tomato frogs are endemic to northeastern Madagascar, inhabiting lowland forests, marshes, and wetlands, often near
         slow-moving streams or temporary pools. They prefer areas with moist soil and dense leaf litter, which provides cover and
         suitable conditions for burrowing and egg-laying. Seasonal rains are important for triggering breeding activity.'''
         .replace( '\n', ' ' ),
      '''These frogs are carnivorous, feeding on insects, worms, and other small invertebrates. They use a sit-and-wait hunting
         strategy, remaining partially buried or hidden among leaves and striking prey with their sticky tongues. In captivity,
         their diet is typically supplemented with crickets, mealworms, and other appropriately sized invertebrates.'''
         .replace( '\n', ' ' ),
      '''Tomato frogs are mostly solitary, spending much of their time burrowed or camouflaged in leaf litter. They are nocturnal,
         emerging at night to forage and mate. When threatened, they inflate their bodies and secrete sticky toxins, which can deter
         predators. Vocal communication is limited but includes low croaks during breeding season.'''.replace( '\n', ' ' ),
      '''Tomato frogs have several adaptations for defense and survival in wetland habitats. Their bright colouration acts as
         aposematic signaling, warning potential predators of toxicity. Burrowing behaviour allows them to avoid desiccation and
         extreme temperatures, while sticky secretions discourage predation. Their robust, squat bodies are adapted for both digging
         and absorbing moisture from the environment.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, when males call to attract females. Females lay hundreds of eggs in shallow water
         or moist soil, which hatch into aquatic tadpoles within a few days. Tadpoles undergo metamorphosis over 6–8 weeks, emerging
         as fully formed juvenile frogs. Sexual maturity is reached at 1–2 years, and lifespans in captivity can reach 5–7 years,
         slightly shorter in the wild due to predation and environmental challenges.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Veiled Chameleon',
      'Chamaeleo Calyptratus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The veiled chameleon can be found in a habitat in the hallway in between the Lake Malawi exhibit and the stairs towards the
         pygmy hippos, waterfowl, and lemurs, and beside the Lau banded iguanas.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Veiled chameleons are medium-sized lizards, with males larger than females, measuring 40–60 cm in total length including
         the tail, and weighing 100–200 grams. They have laterally compressed bodies, zygodactylous feet, and prehensile tails
         adapted for climbing. Their most distinctive feature is the casque, a tall helmet-like structure on the head, especially
         pronounced in males. Skin colouration ranges from bright green to yellow, brown, or even blue, with patterns that change
         depending on mood, temperature, or social signals. Eyes are large and independently mobile, allowing nearly 360-degree
         vision.'''.replace( '\n', ' ' ),
      '''Veiled chameleons are native to Yemen and southwestern Saudi Arabia, inhabiting tropical and subtropical mountain regions,
         shrublands, and areas with scattered trees. They are primarily arboreal, spending most of their lives in trees and bushes,
         but can descend to forage on the ground. Adequate sunlight, humidity, and vertical structures are critical for
         thermoregulation, hydration, and mobility.'''.replace( '\n', ' ' ),
      '''They are primarily insectivorous, feeding on crickets, locusts, flies, moths, and other small arthropods. Large adults may
         occasionally eat plant material such as leaves or fruits. They use a long, sticky tongue that can rapidly extend to capture
         prey, relying on precise visual targeting and lightning-fast reflexes. In captivity, diets are supplemented with gut-loaded
         insects and occasional leafy greens.'''.replace( '\n', ' ' ),
      '''Veiled chameleons are largely solitary, interacting primarily during the breeding season. They exhibit territorial
         behaviours, with males displaying bright colours, head bobbing, and swaying to intimidate rivals or attract females.
         Despite their solitary nature, they are highly alert and visually oriented, constantly scanning the environment for prey
         and predators. Movement is slow and deliberate, using hand-over-hand climbing and tail-assisted balance.'''
         .replace( '\n', ' ' ),
      '''Veiled chameleons possess extraordinary adaptations for arboreal life and predation. colour-changing skin allows camouflage,
         thermoregulation, and communication. Zygodactylous feet and prehensile tails enhance gripping and climbing stability, while
         independently mobile eyes provide nearly panoramic vision. The rapid, extendable tongue enables efficient prey capture, and
         their slow, deliberate movement reduces detection by predators.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round in favorable conditions, though peaks often align with the rainy season. Females lay 20–70 eggs
         in a burrow dug into moist soil. Eggs incubate for 6–12 months, depending on temperature, before hatching as miniature
         replicas of adults. Sexual maturity is reached in 6–12 months, and lifespans in captivity typically reach 5–8 years, though
         wild lifespans are often shorter due to predation and environmental stressors.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Violaceous Plantain Eater',
      'Crinifer Violaceus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The violaceous plantain eater can be found in the aviary between the gorillas ,and the dwarf crocodiles and the Lake Malawi
         exhibit.''',
      None,                                                          # Seasonal viewing tips
      '''The violaceous plantain-eater is a large, colourful bird, measuring 50–60 cm in length with a wingspan of 75–90 cm. Its
         plumage is primarily purplish-gray, with white and black barring on the wings and a distinctive bushy crest on the head.
         The beak is short, slightly curved, and strong, suitable for feeding on fruits. Eyes are pale yellow, and legs are sturdy,
         adapted for perching. Juveniles are slightly duller in colouration than adults.'''.replace( '\n', ' ' ),
      '''This species is native to West and Central Africa, inhabiting tropical forests, forest edges, and wooded savannas. They
         prefer areas with fruit-bearing trees and are often seen perching high in the canopy, where they can spot ripe fruits and
         potential predators.'''.replace( '\n', ' ' ),
      '''Violaceous plantain-eaters are primarily frugivorous, feeding on figs, plantains, papayas, and other soft fruits, though
         they may occasionally consume leaves and flowers. Foraging is often done solitarily or in pairs, and they use their strong
         beaks to pluck and manipulate fruit, swallowing it whole. Their feeding behaviour plays a significant role in seed
         dispersal, helping to maintain healthy forest ecosystems.'''.replace( '\n', ' ' ),
      '''These birds are generally solitary or found in pairs, but they can form small groups when food is abundant. They are
         diurnal, resting quietly during the hottest parts of the day and feeding in the morning and late afternoon. Vocalizations
         include loud, repetitive calls used for territorial communication or mate contact. They are relatively sedentary but can
         fly short distances between fruiting trees.'''.replace( '\n', ' ' ),
      '''Violaceous plantain-eaters have several adaptations for arboreal life and frugivory. Their strong, slightly curved beak
         allows them to efficiently pluck and swallow fruit. Zygodactyl feet provide a secure grip on branches, while their
         colouration provides camouflage among canopy foliage. Their role as seed dispersers is a key ecological adaptation,
         allowing them to influence forest regeneration.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs during periods of fruit abundance. Females lay 2–3 eggs in a simple stick nest placed high in a
         tree. Both parents participate in incubation and feeding the chicks, which fledge after approximately 4–5 weeks. Sexual
         maturity is reached at 1–2 years, and lifespan in the wild is estimated at 10–12 years, with longer survival in managed
         care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'West African Dwarf Crocodile',
      'Osteolaemus Tetraspis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The West African dwarf crocodile can be found in a habitat in between the gorillas and the Lake Malawi exhibit.''',
      None,                                                          # Seasonal viewing tips
      '''West African dwarf crocodiles are the smallest of African crocodiles, with adults typically 1.2–1.5 meters in length and
         weighing 18–32 kg. They have a stocky body, broad snout, and rough, bony scales that give a heavily armored appearance.
         colouration is generally dark brown to olive, providing camouflage in forested waterways. Their eyes are positioned
         dorsally, allowing them to see while mostly submerged, and their powerful jaws are adapted for crushing prey.'''
         .replace( '\n', ' ' ),
      '''This species is native to West and Central Africa, including countries such as Liberia, Ghana, Cameroon, and Gabon. They
         inhabit slow-moving rivers, swamps, marshes, and forested streams, preferring areas with dense vegetation and submerged
         cover. They are primarily nocturnal, spending daylight hours hidden in burrows or under overhanging roots and vegetation.'''
         .replace( '\n', ' ' ),
      '''West African dwarf crocodiles are carnivorous opportunists, feeding on fish, crustaceans, amphibians, small mammals, and
         invertebrates. They are nocturnal hunters, ambushing prey at night using stealth and quick strikes. Their strong jaws and
         sharp teeth allow them to crush hard-shelled prey such as crabs and mollusks.'''.replace( '\n', ' ' ),
      '''These crocodiles are primarily solitary, interacting mainly during the breeding season. They are mostly aquatic, moving
         slowly along riverbanks or submerged in water, and are rarely seen in open areas. Vocalizations, including hissing and
         grunting, are used for communication between individuals, particularly during courtship or territorial disputes.'''
         .replace( '\n', ' ' ),
      '''West African dwarf crocodiles have several adaptations for forested aquatic environments. Their small size and stocky build
         allow them to navigate narrow waterways and dense vegetation. Eyes and nostrils positioned dorsally let them remain mostly
         submerged while observing surroundings. Their armored scales provide protection from predators, while nocturnal habits
         reduce competition and predation risk. Strong jaws allow them to exploit hard-shelled prey, giving them a unique ecological
         niche among African crocodiles.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, when females lay 10–25 eggs in shallow nests made of mud and vegetation near water.
         Incubation lasts 90–100 days, with temperature influencing sex determination of hatchlings. Young are independent at
         hatching but face high predation rates. Sexual maturity is reached at 5–7 years, and these crocodiles can live 40–50 years
         in captivity, though wild lifespans are often shorter.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'African Spurred Tortoise',
      'Centrochelys Sulcata',
      14,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The African spurred tortoise can be found in the African Savanna pavilion, where it inhabits a warm, dry terrestrial exhibit
         designed to reflect its native grassland and desert-edge environment.'''.replace( '\n', ' ' ),
      '''African spurred tortoises are best viewed on warmer days, when they are most active and may be seen walking, grazing, or
         basking under heat sources. During cooler conditions, they may remain more stationary under lamps or sheltered areas.'''
         .replace( '\n', ' ' ),
      '''African spurred tortoises are the largest mainland tortoise species in Africa and the third largest tortoise species in the
         world. Adults commonly reach 45–75 cm in shell length and may weigh 30–80 kg, with some exceptionally large males exceeding
         100 kg. Their shell is tan to sandy brown with prominent growth rings, and their thick, scaly forelimbs are covered in large
         protective scales. The species is named for the large spurs located on the backs of their hind legs.'''
         .replace( '\n', ' ' ),
      '''This species is native to the southern edge of the Sahara Desert across North-Central Africa, including countries such as
         Senegal, Mali, Chad, Sudan, and Ethiopia. They inhabit arid grasslands, savannas, thorn scrub, and semi-desert regions where
         temperatures are high and vegetation is sparse. They often dig extensive burrows to escape heat and conserve moisture.'''
         .replace( '\n', ' ' ),
      '''African spurred tortoises are herbivores, feeding primarily on grasses, leaves, flowers, and succulents. Their diet is high
         in fibre and low in protein, which supports healthy shell growth. In managed care they are often offered grasses, hay, leafy
         greens, and calcium-rich vegetables. They spend much of the day grazing slowly across their habitat.'''
         .replace( '\n', ' ' ),
      '''These tortoises are generally solitary and spend most of their time moving slowly through their habitat in search of food or
         suitable basking areas. They may interact peacefully in shared spaces but are not highly social. Males can become territorial,
         especially during breeding season, using ramming and shell-butting behaviours to compete for mates.'''
         .replace( '\n', ' ' ),
      '''African spurred tortoises are highly adapted to hot, dry climates. Their thick scaly skin reduces water loss, while their
         powerful forelimbs and flattened claws allow them to dig deep burrows that remain cool and humid. Their domed shell provides
         protection from predators and environmental extremes, and their efficient herbivorous digestion helps them survive on tough,
         fibrous vegetation.'''
         .replace( '\n', ' ' ),
      '''Breeding usually occurs during the warmer months, with females laying clutches of 15–30 eggs in shallow nests dug into sandy
         soil. Incubation typically lasts 90–120 days depending on temperature. Hatchlings emerge fully independent and grow steadily
         over many years. Sexual maturity may take 10–15 years, and this species can live for over 70 years in captivity.'''
         .replace( '\n', ' ' ),
      None                                                            # Animals at the zoo
   ),
   (
      'Western Lowland Gorilla',
      'Gorilla Gorilla Gorilla',
      12,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The Toronto Zoo houses two groups of gorillas which go on display separately--the family troop, containing the females, and
         the bachelor troop containing the adult males. When it is warm enough, you can find one of the groups, usually the females
         outside, and the other group, usually the males, inside. If it is too cold for the gorillas to be outside, then you will
         find one group in the main indoor habitat, and the other in the day room across from the main habitat.'''
         .replace( '\n', ' ' ),
      '''Western lowland gorillas are warm weather primates and are only comfortable outside during the warmer months of the year,
         usually from May to October, and perhaps on other warmer days, specifically in the later part of April. When it is warm
         enough for the gorillas to be outside, you will find some of them outside, and the others inside. If it is too cold for the
         gorillas to be outside, then you will only find them inside.'''.replace( '\n', ' ' ),
      '''Western lowland gorillas are the smallest of the gorilla subspecies, yet still powerful. Adult males reach 140–180 cm in
         height and weigh 140–200 kg, while females are smaller, at 110–140 cm tall and 70–90 kg. They have stocky, muscular builds,
         broad chests, and long arms, suited for knuckle-walking on the ground and climbing in trees. Adult males develop a silver
         patch of fur on their backs, giving the name “silverback.” Their faces are mostly bare, with large expressive eyes,
         pronounced brow ridges, and wide nostrils, conveying a range of emotions. Their hands and feet are strong, with opposable
         thumbs and big toes, allowing precise manipulation of objects and efficient climbing. Juveniles and subadults are darker
         and smaller, and their facial expressions are often highly animated, signaling curiosity, fear, or playfulness.'''
         .replace( '\n', ' ' ),
      '''These gorillas inhabit dense tropical rainforests of central Africa, including Cameroon, the Central African Republic,
         Equatorial Guinea, Gabon, and the Republic of Congo. They prefer lowland swamp forests, secondary forests, and areas rich
         in fruiting trees, sometimes venturing into upland forests when food is available. Home ranges are typically 5–20 km², and
         gorillas move daily to forage efficiently while avoiding humans and predators. Their choice of habitat is influenced by
         food availability, water sources, and forest structure, as they require thick understory for protection and canopy cover
         for nesting sites. Seasonal changes affect their movement patterns, with wet seasons encouraging expansion into flooded
         areas rich in fruit, while dry seasons may concentrate them near reliable water sources.'''.replace( '\n', ' ' ),
      '''Western lowland gorillas are primarily herbivorous, feeding on leaves, stems, shoots, fruits, seeds, and flowers, and
         occasionally small invertebrates like ants or termites. They are selective feeders, often stripping leaves, peeling bark,
         or choosing specific fruit ripeness. Fruit availability strongly influences daily movements, group cohesion, and social
         interactions, as they may travel long distances to access high-yield fruiting trees. Gorillas also practice intentional
         foraging behaviours, such as using sticks to probe water depth or to gather insects. In captivity, diets are carefully
         balanced with fresh fruits, vegetables, leafy greens, and specially formulated primate food to replicate nutritional needs
         while encouraging natural foraging behaviours.'''.replace( '\n', ' ' ),
      '''Gorillas live in stable social groups called troops, typically led by a dominant silverback male. Troops usually include
         5–20 individuals, comprising adult females, infants, juveniles, and sometimes subordinate males. Silverbacks mediate
         conflicts, guide troop movements, and protect members from predators or rival males. Social interactions include grooming,
         play, chest-beating, vocalizations, facial expressions, and tool use, which reinforce social bonds and hierarchy. Infants
         and juveniles learn foraging, nesting, and communication skills through play and observation. Communication is highly
         nuanced, including soft grunts for coordination, loud roars for defense, and subtle gestures like eyebrow raising or lip
         movements. Gorillas are diurnal, building sleeping nests nightly from branches and leaves, which they often reconstruct for
         comfort and hygiene.'''.replace( '\n', ' ' ),
      '''Western lowland gorillas have numerous adaptations for forest survival and social life. Powerful arms and hands enable
         climbing, object manipulation, and knuckle-walking. Thick fur insulates against cooler understory temperatures, while large
         molars and jaw muscles efficiently process fibrous plant material. Their colour vision, intelligence, and memory allow
         recognition of edible plants, social partners, and threats. Tool use is observed both in the wild and captivity, such as
         using sticks to measure water depth, leaves as drinking tools, or branches for play and enrichment. Social cohesion,
         learned behaviours, and complex communication are critical adaptations for living in dense, competitive rainforest
         environments.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity at 8–10 years, and males at 10–12 years, with silverbacks achieving full dominance slightly
         later. Breeding occurs year-round but is influenced by food abundance and troop dynamics. Gestation lasts about 8.5 months,
         with females typically producing one infant at a time. Infants cling to their mothers and are weaned after 3–4 years,
         remaining socially dependent for learning foraging, nesting, and social skills. Lifespan in the wild is 35–40 years, and in
         captivity up to 50 years. Silverbacks play a key role in protecting young, mediating troop conflicts, and teaching social
         norms, ensuring troop stability.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two groups of gorillas. They have a bachelor troop of two recently matured males, Sadiki and
         Nassir, who are usually visible in the indoor habitat. There is also a family troop of females, Ngozi, Nneka and Charlie,
         and silverback, Zwalani. Zwalani arrived at the zoo in the summer of 2025, and just recently started spending all of his
         time in the family troop with the females.'''.replace( '\n', ' ' )
   ),

   # Indo-Malaya Pavilion
   (
      'Asian Brown Tortoise',
      'Manouria Emys',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Asian brown tortoise can be found in the tortoise habitat just past the carp tank and before the outdoor orangutan
         habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Asian brown tortoises are large, terrestrial tortoises, with adults measuring 50–70 cm in length and weighing 20–40 kg.
         Their domed carapace is dark brown with subtle growth rings, and their plastron is lighter, often yellowish or
         cream-coloured. The head is relatively small with strong, beak-like jaws for cutting vegetation. Their thick, scaly legs
         are equipped with stout claws for digging and navigating uneven forest floors.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, including Myanmar, Thailand, Malaysia, and parts of Indonesia, inhabiting moist
         tropical and subtropical forests. They are primarily terrestrial, often found in areas with leaf litter, undergrowth, and
         soft soil suitable for burrowing and nesting. They require humid, shaded environments to avoid desiccation and maintain
         healthy skin and shell conditions.'''.replace( '\n', ' ' ),
      '''Asian brown tortoises are omnivorous, feeding on leaves, grasses, fallen fruits, fungi, and occasionally invertebrates.
         They are slow-moving foragers, consuming a variety of plant materials available on the forest floor. In captivity, diets
         are supplemented with leafy greens, vegetables, and occasional fruits, ensuring balanced nutrition while mimicking natural
         feeding habits.'''.replace( '\n', ' ' ),
      '''They are largely solitary, interacting minimally except during breeding. These tortoises are mostly diurnal, active during
         cooler periods and resting in sheltered areas or shallow burrows during midday heat. Their slow, deliberate movement and
         reliance on camouflage help them avoid predators, while occasional defensive behaviours include retracting limbs and head
         into their shell.'''.replace( '\n', ' ' ),
      '''Adaptations for terrestrial forest life include a domed, strong shell for protection, clawed feet for digging, and the
         ability to digest fibrous plant material efficiently. Their colouration allows camouflage on the forest floor, and their
         slow metabolism supports long periods of limited food availability.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, when females lay 5–15 eggs in shallow nests dug into soft soil. Incubation lasts
         approximately 90–120 days, depending on temperature and humidity. Hatchlings are independent at birth but are highly
         vulnerable to predation. Sexual maturity is reached at 8–12 years, and lifespan in the wild is 50–70 years, with longer
         survival possible in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Bighead Carp',
      'Hypophthalmichthys Nobilis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The bighead carp can be found in the carp tank just past the waterfall, found by taking the path on the left once you enter
         the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must backtrack
         slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Bighead carp are large freshwater fish, commonly reaching 60–100 cm in length, with some individuals exceeding 1 meter and
         weighing over 20 kg. They have a large, blunt head, giving the species its common name, and a silver-gray body with a
         slightly darker back. Their eyes are located low on the head, below the mouth, an adaptation for filter-feeding near the
         water surface.'''.replace( '\n', ' ' ),
      '''Native to eastern Asia, including China and Siberia, bighead carp inhabit slow-moving rivers, lakes, and reservoirs. They
         prefer warm, eutrophic waters with abundant plankton. In many regions outside their native range, they have become
         invasive, affecting local ecosystems by outcompeting native fish for food.'''.replace( '\n', ' ' ),
      '''Bighead carp are filter feeders, consuming phytoplankton, zooplankton, and suspended organic matter. They swim with open
         mouths, straining water through gill rakers, which allows them to efficiently consume large quantities of microscopic food.
         This feeding behaviour can significantly alter the composition of aquatic ecosystems, reducing plankton available for
         native species. In zoos or aquaria, they are fed plankton substitutes, commercially prepared diets, or finely ground greens
         to mimic natural feeding habits.'''.replace( '\n', ' ' ),
      '''These carp are schooling fish, often moving in groups that provide protection and aid in foraging. They are diurnal feeders,
         swimming actively through the water column to access plankton-rich areas. Social interactions are limited to schooling
         behaviour, and there are no complex hierarchies.'''.replace( '\n', ' ' ),
      '''Bighead carp have several adaptations for efficient filter feeding. Their large mouths and ventrally placed eyes allow them
         to detect and consume plankton near the surface. Gill rakers strain microscopic organisms from the water, and their
         streamlined bodies allow them to swim efficiently in flowing rivers and lakes. Their schooling behaviour reduces predation
         risk and increases feeding efficiency.'''.replace( '\n', ' ' ),
      '''Spawning occurs in warm, flowing water during the spring and summer. Females release hundreds of thousands of eggs, which
         drift with the current until hatching. Juveniles feed on plankton immediately, growing rapidly. Sexual maturity is reached
         at 3–4 years, and lifespan can reach 15–20 years in natural conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Black Carp',
      'Mylopharyngodon Piceus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black carp can be found in the carp tank just past the waterfall, found by taking the path on the left once you enter
         the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must backtrack
         slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Black carp are large freshwater fish, typically reaching 60–100 cm in length, with some individuals exceeding 1.2 meters
         and weighing over 20 kg. They have a long, cylindrical body with a dark, bluish-black to gray colouration and a broad,
         flattened head. Their jaws are strong, and their teeth are molariform, specialized for crushing mollusk shells, giving them
         a distinctive feeding adaptation.'''.replace( '\n', ' ' ),
      '''Black carp are native to eastern Asia, primarily China and Vietnam, inhabiting rivers, lakes, and reservoirs with
         slow-moving or still water. They prefer warm, vegetated freshwater habitats with abundant mollusks. Outside their native
         range, they have sometimes been introduced for aquaculture or invasive control, though such introductions can impact local
         ecosystems.'''.replace( '\n', ' ' ),
      '''Black carp are molluscivorous, feeding mainly on snails, clams, and other shelled invertebrates. Their powerful molar-like
         pharyngeal teeth crush the hard shells, allowing them to consume prey that other fish cannot. In captivity, they are fed
         snails, clams, and mollusk substitutes to replicate natural feeding behaviour. Their specialized diet makes them important
         for controlling snail populations, including species that carry parasites such as the liver fluke.'''.replace( '\n', ' ' ),
      '''These fish are largely solitary or found in loose aggregations, with minimal social interaction beyond feeding. They are
         diurnal and bottom-oriented, often foraging along riverbeds or the substrate of ponds and lakes. Their slow, deliberate
         movement and cryptic colouration help avoid predators in the wild.'''.replace( '\n', ' ' ),
      '''Black carp have several adaptations for their specialized diet and freshwater habitat. Their molars crush hard-shelled
         prey, while strong jaws and a broad head facilitate feeding on mollusks. Streamlined bodies allow them to navigate rivers
         and ponds efficiently, and their dark colouration provides camouflage on the bottom of silty or vegetated waters. They are
         also long-lived and slow-growing, which supports survival in variable freshwater environments.'''.replace( '\n', ' ' ),
      '''Spawning occurs in warm, flowing water, with females laying hundreds of thousands of eggs that drift downstream. Juveniles
         begin feeding on small invertebrates before transitioning to their mollusk-based diet. Sexual maturity is reached at 3–5
         years, and lifespans can reach 15–20 years in natural conditions or slightly longer in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Black-Breasted Leaf Turtle',
      'Geoemyda Spengleri',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black-breasted leaf turtle can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The Black-Breasted Leaf Turtle is a small, terrestrial turtle, with adults measuring 15–18 cm in shell length and weighing
         500–800 grams. Its carapace is dark brown to black, low-domed, and often covered in moss or debris, helping with camouflage.
         The plastron is distinctively dark with lighter markings, giving the “black-breasted” name. Head and limbs are scaled,
         dark-coloured, and retractable, and the eyes are relatively large for alertness on the forest floor. Its small size and
         cryptic colouration make it well-adapted to blending in among leaves and forest debris.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, including Vietnam and southern China, inhabiting moist lowland forests and hilly
         woodlands. It is terrestrial and secretive, often hiding under leaf litter, fallen logs, or dense understory vegetation. It
         prefers humid, shaded areas with abundant cover and soft soil suitable for burrowing and nesting.'''.replace( '\n', ' ' ),
      '''Black-breasted leaf turtles are omnivorous, feeding on fallen fruits, fungi, leaves, and small invertebrates. They are
         slow-moving foragers, using their keen sense of smell to locate food among leaf litter. In captivity, they are provided
         with a varied diet of fruits, vegetables, worms, and specially formulated turtle food, encouraging natural feeding
         behaviour and proper nutrition.'''.replace( '\n', ' ' ),
      '''These turtles are largely solitary and secretive, interacting minimally outside of breeding. They are mostly diurnal,
         emerging during cooler parts of the day to forage, and retreating to hiding places during high heat. Defensive behaviours
         include retracting the head and limbs into the shell and remaining motionless, which is highly effective due to their
         cryptic colouration.'''.replace( '\n', ' ' ),
      '''Adaptations include a low, mossy carapace that provides camouflage, strong limbs and claws for digging and maneuvering
         through leaf litter, and a slow metabolism that allows survival during periods of limited food availability. Their
         colouration, shape, and behaviour make them well-suited to life on the forest floor, where concealment is key to avoiding
         predation.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, with females laying 2–5 eggs in shallow nests dug into soft soil. Incubation lasts
         approximately 60–90 days, with hatchlings emerging fully independent. Juveniles are highly vulnerable to predation, and
         sexual maturity is reached at 5–7 years. Lifespan in the wild is estimated at 20–30 years, with longer survival possible
         in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Black-Throated Laughing Thrush',
      'Garrulax Chinensis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The black-throated laughing thrush can be spotted in a small aviary just through the entrance to the pavilion and on the
         left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Black-throated Laughing Thrush is a medium-sized bird, measuring 25–28 cm in length. Its plumage is mainly rich brown
         with a black throat and face mask, contrasting with white wing edges and pale underparts. The bird has strong legs and
         slightly curved bill, suited for foraging on the forest floor. Eyes are dark and expressive, and its overall appearance is
         robust and slightly chunky, typical of laughing thrushes.'''.replace( '\n', ' ' ),
      '''This species is native to southern China, northern Vietnam, and Laos, inhabiting subtropical and tropical forests, forest
         edges, and dense shrublands. It prefers thick undergrowth where it can forage safely and avoid predators, often staying low
         to the ground but occasionally moving into lower branches.'''.replace( '\n', ' ' ),
      '''Black-throated Laughing Thrushes are omnivorous, feeding on insects, small invertebrates, berries, and seeds. They are
         active foragers, often hopping through leaf litter while using their sharp bills to probe for insects. In zoos, their diet
         is supplemented with insects, fruits, and seeds, encouraging natural foraging behaviour and maintaining optimal health.'''
         .replace( '\n', ' ' ),
      '''These birds are social and often found in small groups, communicating through a variety of loud, musical calls, including
         the characteristic “laughing” calls that give the species its name. Group cohesion is maintained through vocalizations and
         cooperative foraging, and they are diurnal, most active during morning and late afternoon. They display territorial
         behaviours during breeding but are otherwise tolerant of conspecifics in their social group.'''.replace( '\n', ' ' ),
      '''Adaptations include strong legs and agile movements for ground foraging, a curved bill for probing leaf litter, and vocal
         abilities for communication within dense forests. Their colouration allows camouflage among shadows and leaf litter,
         reducing predation risk. Social foraging increases feeding efficiency and helps detect predators quickly.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs primarily in the spring, with pairs constructing cup-shaped nests in shrubs or low trees. Females lay 2–4
         eggs, which are incubated for about 14–16 days. Both parents participate in feeding and caring for the chicks, which fledge
         after approximately 14–18 days. Sexual maturity is reached at 1–2 years, and lifespan in captivity can reach 8–10 years,
         though wild lifespans are generally shorter due to predation.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Burmese Star Tortoise',
      'Geochelone Platynota',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Burmese star tortoise can be found in the tortoise habitat just past the carp tank and before the outdoor orangutan
         habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Burmese star tortoise is a medium-sized terrestrial tortoise, measuring 20–25 cm in length and weighing 2–3 kg. Its
         domed carapace is marked with distinct yellow or tan radiating patterns on a dark brown to black background, resembling a
         star, which gives the species its name. The plastron is light-coloured with dark markings, and the head and limbs are
         scaled, with stout claws for digging. Juveniles display more vibrant star patterns, which fade slightly with age.'''
         .replace( '\n', ' ' ),
      '''This species is native to dry and scrubby regions of central Myanmar, inhabiting thorn forests, grasslands, and seasonal
         dry forests. It prefers areas with sandy or loamy soil, which allows for burrowing and nesting. Burmese star tortoises rely
         on leaf litter and low vegetation for cover, and seasonal rains influence their activity patterns and foraging behaviour.'''
         .replace( '\n', ' ' ),
      '''Burmese star tortoises are herbivorous, feeding on grasses, leaves, flowers, and fallen fruits. They are slow-moving
         foragers, selectively grazing on nutrient-rich vegetation. In zoos, diets are supplemented with leafy greens, vegetables,
         and specialized tortoise pellets, ensuring balanced nutrition while encouraging natural feeding behaviour. Their grazing
         plays a role in maintaining plant community structure and seed dispersal.'''.replace( '\n', ' ' ),
      '''These tortoises are largely solitary, interacting mainly during courtship and mating. They are diurnal, basking in sunlight
         to regulate body temperature and seeking shade or burrows during the hottest parts of the day. Defensive behaviours include
         retracting the head and limbs into the shell and remaining motionless. During the breeding season, males may engage in
         courtship displays, nudging or circling females.'''.replace( '\n', ' ' ),
      '''Adaptations include a domed shell for protection against predators, stout limbs and claws for digging burrows and moving
         over rough terrain, and a slow metabolism that allows survival during periods of limited food availability. Their
         star-patterned carapace provides camouflage among grasses and leaf litter, reducing predation risk. behavioural adaptations,
         such as burrowing and selective basking, help them cope with seasonal temperature fluctuations.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, with females laying 4–8 eggs in shallow nests dug into sandy soil. Incubation
         lasts 90–120 days, depending on temperature and humidity. Hatchlings are fully independent but vulnerable to predation.
         Sexual maturity is reached at 5–7 years, and lifespans can exceed 50 years, especially in managed care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Cattle Egret',
      'Bubulcus Ibis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The cattle egret can be found in the main aviary in the Indo-Malaya pavilion, which sits in the center of the pavilion. The
         best area to view the birds in the aviary is in between the stairs leading down from the elevated orangutan viewing, up
         until you are across from the doors leading you to the outdoor orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The cattle egret is a small, stocky heron, standing about 45–55 cm tall with a wingspan of 85–95 cm. Outside the breeding
         season it is almost entirely white, with a short yellow bill and dark legs. During breeding, adults develop buff-orange
         plumes on the head, chest, and back, and the bill and legs may take on reddish tones. Compared to other egrets, it appears
         shorter-necked and more compact, often giving it a hunched profile when at rest.'''.replace( '\n', ' ' ),
      '''Originally native to Africa, southern Europe, and parts of Asia, the cattle egret has expanded naturally and now occurs on
         every continent except Antarctica. It inhabits open grasslands, wetlands, savannas, agricultural fields, and floodplains,
         often far from open water. Its close association with grazing animals makes it especially common in pastures and livestock
         areas, where prey is easily disturbed.'''.replace( '\n', ' ' ),
      '''Cattle egrets feed primarily on insects and small vertebrates, including grasshoppers, beetles, flies, frogs, and small
         reptiles. Rather than waiting at water’s edge like many herons, they actively forage on land, often following large mammals
         such as cattle, antelope, or even farm machinery. As these animals move, they flush prey from the grass, allowing the egret
         to capture food with quick, precise strikes. In managed care, their diet includes insects, small fish, and prepared avian
         diets.'''.replace( '\n', ' ' ),
      '''This species is highly social, often seen feeding in loose groups and roosting communally. Cattle egrets are strong fliers
         and migrate or disperse widely, which has contributed to their remarkable global spread. They are most active during the
         day and frequently shift feeding locations depending on the movement of grazing animals. Breeding occurs in large
         mixed-species colonies, often in trees near wetlands.'''.replace( '\n', ' ' ),
      '''Cattle egrets are exceptionally adaptable birds. Their ability to exploit prey disturbed by large animals allows them to
         thrive in open habitats where other wading birds cannot. Strong flight capabilities enable long-distance dispersal, helping
         the species colonize new regions rapidly. Their flexible diet and tolerance of human-altered landscapes, such as farmland
         and pasture, have made them one of the most successful herons globally.'''.replace( '\n', ' ' ),
      '''Breeding typically coincides with rainy seasons, when food availability is high. Females lay 2–5 eggs in stick nests built
         in trees or shrubs within dense colonies. Both parents incubate the eggs for about 23 days and feed the chicks by
         regurgitation. Young birds fledge after roughly 30 days. Cattle egrets can live 15–20 years, with longer lifespans
         occasionally recorded in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Concave Casqued Hornbill',
      'Ceratogymna Levigata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The concave casqued hornbill can be found in an aviary just before you exit the pavilion, on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The concave casqued hornbill is a large, unmistakable forest bird, measuring 80–100 cm in length. It has a predominantly
         black body, a white tail with a bold black band, and a massive curved bill topped by a concave casque. The casque is pale
         yellow to ivory in colour and curves upward toward the tip, giving the species its name. Males typically have reddish eyes
         and throat skin, while females have darker eyes and bluish throat skin. The wings are broad, producing a loud, rhythmic
         wingbeat in flight.'''.replace( '\n', ' ' ),
      '''This species is found across South and Southeast Asia, including India, Myanmar, Thailand, Malaysia, Indonesia, and
         southern China. It inhabits lowland and hill tropical rainforests, usually favoring mature forests with large fruiting
         trees. Because it relies on tall trees for nesting, it is particularly sensitive to logging and forest fragmentation.'''
         .replace( '\n', ' ' ),
      '''Concave casqued hornbills are primarily frugivorous, feeding on a wide variety of forest fruits, especially figs. They also
         consume insects, small reptiles, and other animal matter, particularly during the breeding season when protein demands
         increase. Their feeding behaviour involves swallowing fruits whole and later regurgitating or passing seeds, making them
         key seed dispersers in rainforest ecosystems. In zoos, they are provided with mixed fruits, vegetables, insects, and
         formulated diets to replicate this balance.'''.replace( '\n', ' ' ),
      '''These hornbills are usually seen in pairs or small family groups, though they may gather at abundant fruiting trees. They
         are strong but deliberate fliers, traveling long distances between feeding and nesting sites. Vocalizations are loud and
         far-carrying, used to maintain contact through dense forest. Outside the breeding season, pairs remain bonded and often
         forage together.'''.replace( '\n', ' ' ),
      '''The large bill allows hornbills to reach, manipulate, and swallow sizable fruits that many other birds cannot access. The
         casque may function in visual signaling, sound resonance, and species recognition, and may help reinforce the bill during
         feeding. Their strong neck muscles support the heavy bill, while their broad wings enable efficient travel across large
         forest territories. Dependence on fruiting trees ties their life cycle closely to rainforest health.'''.replace( '\n', ' ' ),
      '''Breeding behaviour is one of the most remarkable among birds. The female seals herself inside a tree cavity nest using
         mud, fruit pulp, and droppings, leaving only a narrow slit. She remains inside for the entire incubation and early
         chick-rearing period, relying completely on the male to deliver food. Females lay 1–2 eggs, with incubation lasting about
         30 days. Chicks remain in the cavity for several months before fledging. Concave casqued hornbills can live 30–40 years,
         especially in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crested Wood Partridge',
      'Rollulus Rollulus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crested wood partridge can be found in the main aviary in the Indo-Malaya pavilion, which sits in the center of the
         pavilion. The best area to view the birds in the aviary is in between the stairs leading down from the elevated orangutan
         viewing, up until you are across from the doors leading you to the outdoor orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The crested wood partridge is a small, compact ground bird, measuring about 25–28 cm in length. Males are striking, with
         glossy dark green-black plumage, a bright red bill and legs, and a distinctive curled red crest on the head. Females are
         more subtly coloured, with greenish-brown plumage, a shorter crest, and duller facial features. Both sexes have short,
         rounded wings and strong legs adapted for walking rather than prolonged flight.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, including Thailand, Malaysia, Indonesia, and surrounding regions. It inhabits
         dense tropical and subtropical forests, particularly lowland rainforests and bamboo thickets, where thick undergrowth
         provides cover. Crested wood partridges spend most of their time on the forest floor and are rarely seen in open areas,
         making them vulnerable to deforestation and habitat fragmentation.'''.replace( '\n', ' ' ),
      '''Crested wood partridges are omnivorous foragers, feeding on seeds, fallen fruits, leaves, insects, worms, and other small
         invertebrates. They forage by walking slowly through leaf litter, using their bills to pick food items from the ground
         rather than scratching vigorously. In managed care, they are offered grain mixes, leafy greens, fruits, and protein sources
         such as insects to mirror their varied natural diet.'''.replace( '\n', ' ' ),
      '''These birds are typically seen alone, in pairs, or in small family groups. They are shy and secretive, relying on
         camouflage and stillness rather than flight when threatened. When startled, they may burst into short, rapid flight to
         escape into dense cover. Vocalizations are soft but distinctive and are used to maintain contact between mates in thick
         vegetation.'''.replace( '\n', ' ' ),
      '''The crested wood partridge’s strong legs and compact body are well suited for a ground-dwelling lifestyle, allowing it to
         move quietly through dense forest undergrowth. Its cryptic colouration helps it blend into shadowed leaf litter, reducing
         detection by predators. The male’s bright crest and facial colouration play a role in courtship and species recognition,
         standing out sharply in low forest light while remaining concealed from above.'''.replace( '\n', ' ' ),
      '''Breeding usually occurs during periods of higher rainfall. Females lay 4–6 eggs in a shallow ground nest concealed by
         vegetation. Incubation lasts about 18–20 days, and chicks are precocial, able to walk and feed shortly after hatching. Both
         parents may assist in protecting and guiding the young. In the wild, crested wood partridges likely live 8–10 years, with
         individuals in managed care sometimes reaching 15 years or more.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crocodile Lizard',
      'Shinisaurus Crocodilurus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crocodile lizard can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The crocodile lizard is a medium-sized, heavily armored-looking reptile, reaching 40–45 cm in total length, much of which
         is tail. Its name comes from the large, keeled scales along the tail, which resemble those of a crocodile. The body is
         typically dark brown to olive, often patterned with lighter bands or spots, providing excellent camouflage among wet rocks
         and vegetation. The head is broad and flattened, with strong jaws and alert eyes adapted for spotting prey along stream
         edges.'''.replace( '\n', ' ' ),
      '''This species has a very restricted natural range, occurring in southern China and northern Vietnam. It inhabits cool,
         shaded forest streams, where clean, slow-moving water flows through dense vegetation. Crocodile lizards are highly
         dependent on intact riparian forests, making them especially vulnerable to habitat loss, water pollution, and climate
         change.'''.replace( '\n', ' ' ),
      '''Crocodile lizards are carnivorous, feeding primarily on insects, spiders, small fish, tadpoles, and other small
         vertebrates. They hunt using a sit-and-wait strategy, remaining motionless along stream banks or partially submerged before
         striking quickly at passing prey. In zoos, they are fed a carefully balanced diet of insects and small aquatic prey,
         adjusted to match their low metabolism.'''.replace( '\n', ' ' ),
      '''These lizards are slow-moving, secretive, and largely solitary. They spend much of their time resting on branches or rocks
         overhanging water and will drop into the stream to escape predators. Crocodile lizards are most active during cooler parts
         of the day and are unusually tolerant of lower temperatures compared to many reptiles, reflecting their montane forest
         habitat.'''.replace( '\n', ' ' ),
      '''The crocodile lizard’s armored tail scales provide protection and may help deter predators. Its semi-aquatic lifestyle is
         supported by strong limbs and a laterally compressed tail that aids in swimming. Cryptic colouration allows it to blend
         seamlessly into mossy rocks and shaded stream banks. Unlike many reptiles, it is adapted to cool, humid environments, with
         a physiology that functions efficiently at lower temperatures.'''.replace( '\n', ' ' ),
      '''Crocodile lizards are ovoviviparous, meaning females give birth to live young rather than laying eggs. Litters are small,
         usually 2–12 offspring, and young are born fully formed and independent. Growth is slow, and sexual maturity may take
         several years. In the wild, lifespan is not well documented, but in managed care crocodile lizards may live 10–15 years or
         more under stable conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Crocodile Newt',
      'Tylototriton Verrucosus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The crocodile newt can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''Crocodile newts are robust, heavily textured salamanders, typically measuring 12–20 cm in length depending on species. They
         have dark brown to black bodies with bright orange or yellow markings along the head, limbs, tail, and raised rib nodules.
         These nodules give the animal a rough, armored appearance reminiscent of a crocodile. The skin is thick and granular, and
         the head is broad with small, dark eyes.'''.replace( '\n', ' ' ),
      '''Species of crocodile newt occur in Southeast and East Asia, including China, Vietnam, Laos, Thailand, and Myanmar. They
         inhabit cool, humid forests, spending much of their time on land in leaf litter or burrows, but returning to ponds and
         slow-moving streams to breed. They are strongly associated with clean, undisturbed freshwater habitats.'''
         .replace( '\n', ' ' ),
      '''Crocodile newts are carnivorous, feeding on insects, worms, snails, and other small invertebrates. They forage primarily at
         night, using slow, deliberate movements to capture prey. In managed care, they are provided with earthworms, insects, and
         other invertebrates, reflecting their natural diet.'''.replace( '\n', ' ' ),
      '''These newts are generally solitary and secretive, spending much of the year hidden under logs, stones, or leaf litter.
         During the breeding season, they gather in aquatic habitats, where males may display subtle courtship behaviours. When
         threatened, crocodile newts adopt a rigid posture, emphasizing their bright warning colours.'''.replace( '\n', ' ' ),
      '''One of the crocodile newt’s most notable adaptations is its toxic defense system. The raised rib nodules contain poison
         glands that secrete toxins when the animal is stressed, making it unpalatable or dangerous to predators. Bright colouration
         serves as aposematic warning, advertising this toxicity. Their rough skin also helps reduce water loss and provides
         protection in rugged forest environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs in water, where females lay strings or clusters of eggs attached to submerged vegetation. Eggs hatch into
         aquatic larvae that later undergo metamorphosis into terrestrial juveniles. Growth is slow, and sexual maturity may take
         several years. In the wild, crocodile newts likely live 10–15 years, while individuals in managed care can reach 20 years
         or more under optimal conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Edward\'s Pheasant',
      'Lophura Edwardsi',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Edward's pheasant can be found in the main aviary in the Indo-Malaya pavilion, which sits in the center of the
         pavilion. The best area to view the birds in the aviary is in between the stairs leading down from the elevated orangutan
         viewing, up until you are across from the doors leading you to the outdoor orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Edward’s pheasant is a medium-sized, elegant ground bird, measuring about 58–65 cm in length. Males are striking, with
         glossy deep blue-black plumage, a white facial patch, and a long, dark tail with subtle patterning. Females are more
         subdued, showing brown and chestnut plumage with fine barring that provides excellent camouflage on the forest floor. Both
         sexes have strong legs adapted for walking and scratching through leaf litter.'''.replace( '\n', ' ' ),
      '''This species is endemic to central Vietnam, where it historically occupied lowland and foothill evergreen forests. Edward’s
         pheasant is closely tied to dense, undisturbed forest understory, making it extremely vulnerable to deforestation, logging,
         and agricultural expansion. In the wild, it is considered Critically Endangered and may be functionally extinct in much of
         its former range.'''.replace( '\n', ' ' ),
      '''Edward’s pheasants are omnivorous, feeding on seeds, fruits, shoots, insects, and other small invertebrates. They forage by
         slowly walking along the forest floor, using their bills and feet to uncover food beneath leaf litter. In zoo care, they
         are offered a balanced diet of grains, fruits, greens, and protein sources to replicate their natural feeding habits.'''
         .replace( '\n', ' ' ),
      '''These birds are shy and secretive, usually seen alone or in pairs. They rely on stillness and dense cover rather than
         flight to avoid predators. Edward’s pheasants are most active during the early morning and late afternoon, when they forage
         quietly along forest edges and understory paths.'''.replace( '\n', ' ' ),
      '''Edward’s pheasant’s cryptic colouration—especially in females—provides camouflage against the forest floor. Strong legs and
         a sturdy body allow efficient ground movement through dense vegetation. The male’s glossy plumage plays a role in courtship
         displays, helping females identify healthy mates in low-light forest conditions.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in the warmer months. Females lay 4–6 eggs in shallow ground nests concealed by vegetation.
         Incubation lasts approximately 22–24 days, and chicks are precocial, able to walk and feed shortly after hatching. In the
         wild, lifespan is estimated at 8–12 years, while individuals in managed care may live 15 years or more.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   ( # Also in Malayan Woods Pavilion
      'Giant Gourami',
      'Osphronemus Goramy',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The giant gourami can be spotted in the Indo-Malaya Pavilion in the carp tank just past the waterfall, found by taking the
         path on the left once you enter the pavilion, and in the Malayan Woods Pavilion, on the left just past the entrance.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The giant gourami is one of the largest freshwater fish commonly displayed in zoos and aquariums, capable of reaching 60–70
         cm in length and weighing several kilograms. Adults have a deep, laterally compressed body with thick lips and a blunt head.
         colouration ranges from silvery gray to brown, often darkening with age. Juveniles usually display faint vertical striping
         that fades as they mature.'''.replace( '\n', ' ' ),
      '''Native to Southeast Asia, giant gouramis are found in slow-moving rivers, lakes, floodplains, and swamps, particularly in
         Indonesia, Thailand, Vietnam, and surrounding regions. They tolerate warm, low-oxygen waters, allowing them to thrive in
         habitats where many other fish cannot survive.'''.replace( '\n', ' ' ),
      '''Giant gouramis are omnivorous with a strong plant preference. In the wild, they feed on aquatic vegetation, algae, fruits,
         seeds, and invertebrates. Their powerful jaws allow them to crop tough plant material. In managed care, they are offered
         leafy greens, vegetables, pellets, and occasional protein sources, reflecting their flexible diet.'''.replace( '\n', ' ' ),
      '''These fish are generally slow-moving and calm, though large adults can become territorial, especially during breeding.
         Giant gouramis are intelligent by fish standards and often recognize regular caretakers. They spend much of their time
         cruising slowly through the water column or resting near structures.'''.replace( '\n', ' ' ),
      '''Like other gouramis, this species possesses a labyrinth organ, allowing it to breathe atmospheric air. This adaptation
         enables survival in warm, stagnant waters with low dissolved oxygen. Their large size helps deter predators, while their
         flexible diet allows them to exploit a wide range of food sources.'''.replace( '\n', ' ' ),
      '''Breeding involves the construction of a floating nest made of plant material, built by the male. Females may lay thousands
         of eggs, which are guarded by the male until hatching. Fry develop quickly but take several years to reach full adult size.
         In the wild, giant gouramis may live 15–20 years, while individuals in managed care can reach 25 years or more under stable
         conditions.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Grass Carp',
      'Ctenopharyngodon Idella',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The grass carp can be found in the carp tank just past the waterfall, found by taking the path on the left once you enter
         the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must backtrack
         slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''Grass carp are large, streamlined freshwater fish, commonly reaching 80–120 cm in length and weighing over 30 kg in
         exceptional individuals. They have an elongated, torpedo-shaped body with large, neatly edged scales that give them a
         crosshatched appearance. colouration is typically olive to gray-green on the back, fading to pale silver on the belly. The
         head is broad with a terminal mouth adapted for grazing.'''.replace( '\n', ' ' ),
      '''Native to eastern Asia, particularly major river systems of China and Siberia, grass carp inhabit large rivers, lakes, and
         floodplain waters. They prefer slow-moving or still freshwater with abundant vegetation. Due to their usefulness in
         vegetation control, grass carp have been widely introduced around the world, including North America, where their use is
         carefully regulated.'''.replace( '\n', ' ' ),
      '''Grass carp are primarily herbivorous, feeding almost exclusively on aquatic plants. An adult can consume its own body
         weight in vegetation daily, making it one of the most efficient plant grazers among freshwater fish. This feeding behaviour
         has made grass carp valuable for managing invasive aquatic plants, but it can also dramatically alter ecosystems if not
         controlled.'''.replace( '\n', ' ' ),
      '''These fish are generally non-aggressive and slow to moderately active swimmers. They often cruise steadily through open
         water or along vegetated edges while feeding. Grass carp are not strongly social but may be seen in loose groupings in
         suitable habitat.'''.replace( '\n', ' ' ),
      '''Grass carp possess strong pharyngeal teeth that grind tough plant material, allowing them to digest fibrous vegetation
         efficiently. Their elongated body and powerful tail support sustained swimming in rivers. Rapid growth helps them quickly
         reach sizes that reduce vulnerability to predators.'''.replace( '\n', ' ' ),
      '''In the wild, grass carp spawn in large, fast-flowing rivers, where eggs drift downstream before hatching. Females can
         release hundreds of thousands to over a million eggs during a single spawning event. Juveniles grow rapidly in their first
         few years. Grass carp may live 20–30 years, with longer lifespans more common in managed or protected environments.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Green Crested Basilisk',
      'Basiliscus Plumifrons',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The green crested basilisk can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The green crested basilisk is a large, slender lizard, typically reaching 70–90 cm in total length, most of which is tail.
         Adults are bright emerald green, often accented with blue or turquoise highlights along the sides and around the eyes.
         Males are larger than females and bear tall, serrated crests on the head, back, and tail, used in visual display and
         species recognition. Females are smaller and have shorter crests, and both sexes have long toes with fringes, a broad head,
         and strong limbs adapted for climbing and rapid escape. Juveniles are paler with more prominent striping, which fades as
         they mature.'''.replace( '\n', ' ' ),
      '''Green crested basilisks are native to Central American rainforests, ranging from southern Mexico through Guatemala,
         Honduras, Nicaragua, Costa Rica, and western Panama. They inhabit humid lowland and foothill tropical forests, favoring
         areas adjacent to rivers, streams, and forested wetlands. They rely on dense vegetation for cover and access to water,
         often staying within a few meters of riparian zones. Seasonal rainfall strongly influences activity, feeding, and
         reproduction.'''.replace( '\n', ' ' ),
      '''These lizards are omnivorous opportunists. They eat a mix of insects, small vertebrates (like frogs and lizards), fruits,
         flowers, and leaves, with diet composition shifting seasonally. Green crested basilisks forage both on the ground and among
         low vegetation, using their strong jaws and agility to capture mobile prey. In managed care, their diet is supplemented
         with crickets, mealworms, small fish, leafy greens, and tropical fruits, promoting natural foraging and maintaining optimal
         health.'''.replace( '\n', ' ' ),
      '''Green crested basilisks are diurnal and highly alert, spending daylight hours basking, foraging, or patrolling territories.
         Males are generally solitary and territorial, while females are more tolerant of each other. When threatened, the
         basilisk’s signature escape strategy is rapid locomotion toward water, where it can sprint across the surface. These
         lizards are agile climbers, frequently moving along branches and trunks, and they communicate visually through head bobbing,
         crest displays, and tail movements.'''.replace( '\n', ' ' ),
      '''The green crested basilisk is famous for its ability to run on water, an adaptation that helps it evade predators in
         riparian habitats. Specialized fringed toes increase surface area to support short bursts of “water-running,” while the
         long tail provides balance. Its bright green colouration aids in camouflage among dense foliage, while males’ crests serve
         in courtship and intraspecific signaling. Strong limbs and claws allow it to climb efficiently, escape predation, and
         access food both on the ground and in low vegetation. This combination of locomotion, camouflage, and display makes it a
         model example of rainforest reptile adaptations.'''.replace( '\n', ' ' ),
      '''Breeding occurs primarily during the rainy season. Females lay 10–20 eggs in shallow nests dug into moist soil near water.
         Eggs incubate for 2–3 months, depending on temperature and humidity. Hatchlings are fully independent at birth and grow
         rapidly, reaching sexual maturity at around 1–2 years. Lifespan in the wild is typically 7–10 years, but in captivity,
         green crested basilisks can live 12 years or more, benefiting from stable conditions and regular feeding.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Hamilton\'s Pond Turtle',
      'Rhinoclemmys Pulcherrima',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Hamilton's pond turtle can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''Hamilton’s pond turtle is a medium-sized freshwater turtle, typically reaching 38–40 cm in shell length. It is immediately
         recognizable by its dark brown to black carapace marked with bold yellow radiating stripes, giving a starburst appearance.
         The shell is high-domed with a pronounced central keel, while the plastron is yellow with dark blotches. The head is dark
         with yellow striping, and the limbs are strong and webbed, reflecting its semi-aquatic lifestyle. Females are generally
         larger than males.'''.replace( '\n', ' ' ),
      '''This species is native to the Indian subcontinent, primarily found in northern and central India, Bangladesh, and parts of
         Pakistan. Hamilton’s pond turtle inhabits slow-moving rivers, ponds, marshes, oxbow lakes, and floodplain wetlands. It
         prefers areas with soft muddy bottoms, abundant aquatic vegetation, and seasonal flooding, which play a key role in feeding
         and reproduction.'''.replace( '\n', ' ' ),
      '''Hamilton’s pond turtles are omnivorous, feeding on aquatic plants, fruits, mollusks, insects, crustaceans, and carrion.
         They forage mostly in shallow water, using their strong jaws to crush hard-shelled prey. Their flexible diet allows them to
         exploit changing wetland conditions throughout the year, especially during seasonal floods.'''.replace( '\n', ' ' ),
      '''These turtles are generally solitary and secretive, spending much of their time submerged or resting on the bottom. They
         are more active during warm daylight hours, surfacing periodically to breathe. During the dry season, individuals may
         aestivate in mud or seek deeper water to avoid extreme conditions. Basking is occasional but less frequent than in many
         other freshwater turtles.'''.replace( '\n', ' ' ),
      '''Hamilton’s pond turtle is well adapted to life in turbid, slow-moving wetlands. Its high-domed, strongly keeled shell
         provides protection from predators, while bold striping may help break up its outline in dappled light underwater. Webbed
         feet support efficient swimming, and the ability to tolerate fluctuating water levels allows survival in seasonal
         floodplain habitats. Its omnivorous feeding strategy is another key adaptation, enabling it to persist in variable
         environments.'''.replace( '\n', ' ' ),
      '''Breeding typically coincides with the monsoon season. Females lay 20–30 eggs in nests dug into sandy or loamy soil near
         water bodies. Incubation lasts several months, and hatchlings emerge during favorable wet conditions. Juveniles grow
         slowly, taking many years to reach maturity. In the wild, Hamilton’s pond turtles may live 30–40 years, with potentially
         longer lifespans in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Iridescent Shark Catfish',
      'Pangasianodon Hypophthalmus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The iridescent shark catfish can be found in the pond just before waterfall, found by taking the path on the left once you
         enter the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must
         backtrack slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The iridescent shark catfish is a large, sleek-bodied freshwater fish that can reach 100–130 cm in length and weigh over 40
         kg in the wild. It has a silvery-gray body with a darker dorsal surface and a pale belly, often showing a subtle iridescent
         sheen that gives the species its name. The head is broad and flattened with two pairs of long barbels around the mouth,
         used for detecting food. Juveniles display darker lateral stripes that fade as they mature.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, primarily within the Mekong and Chao Phraya river systems of Vietnam, Cambodia,
         Laos, and Thailand. Iridescent shark catfish inhabit large, fast-flowing rivers, but also move into floodplains and
         seasonal wetlands during periods of high water. They are highly migratory, traveling long distances in response to seasonal
         flooding and spawning cycles.'''.replace( '\n', ' ' ),
      '''Iridescent shark catfish are omnivorous, feeding on aquatic plants, algae, insects, crustaceans, mollusks, and small fish.
         They are active, mid-water feeders, using their sensitive barbels to locate food in turbid conditions. In aquaculture and
         zoo care, they readily accept pellets, vegetables, and protein-rich foods, reflecting their adaptable feeding strategy.'''
         .replace( '\n', ' ' ),
      '''These catfish are active, schooling fish, particularly when young. Adults may form looser aggregations but still display
         coordinated movement, especially during migrations. They are strong, continuous swimmers and are known to startle easily,
         sometimes colliding with objects in confined spaces. Activity is primarily diurnal, with increased movement during feeding
         times.'''.replace( '\n', ' ' ),
      '''The iridescent shark catfish is adapted for life in large, turbid river systems. Its streamlined body and powerful tail
         allow sustained swimming in strong currents. Sensitive barbels and well-developed lateral line systems help it detect food
         and navigate in low-visibility water. Rapid growth reduces vulnerability to predators, while seasonal migrations allow it
         to exploit flooded habitats rich in food and breeding sites.'''.replace( '\n', ' ' ),
      '''In the wild, spawning occurs during the rainy season, triggered by rising water levels. Females can release hundreds of
         thousands of eggs, which drift downstream before hatching. Juveniles grow quickly, reaching substantial size within a few
         years. In natural conditions, iridescent shark catfish may live 20–25 years, with similar or slightly longer lifespans in
         managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Luzon Bleeding-Heart Dove',
      'Gallicolumba Luzonica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Luzon bleeding-heart dove can be found in the main aviary in the Indo-Malaya pavilion, which sits in the center of the
         pavilion. The best area to view the birds in the aviary is in between the stairs leading down from the elevated orangutan
         viewing, up until you are across from the doors leading you to the outdoor orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Luzon bleeding-heart dove is a medium-sized ground-dwelling pigeon, measuring about 29–31 cm in length. It is best
         known for the striking blood-red patch on its white breast, which appears as though the bird has been wounded. The head is
         pale gray with a soft lavender wash, the back and wings are rich chestnut-brown, and the tail is darker. The eyes are red,
         and the bill is short and dark. Sexes appear similar, though males are often slightly larger.'''.replace( '\n', ' ' ),
      '''This species is endemic to the Philippines, found only on the island of Luzon and a few nearby islands. It inhabits
         lowland and foothill tropical forests, particularly areas with dense understory and deep leaf litter. The dove relies
         heavily on intact forest cover, making it especially vulnerable to deforestation and habitat fragmentation.'''
         .replace( '\n', ' ' ),
      '''Luzon bleeding-heart doves are primarily frugivorous, feeding on fallen fruits, seeds, and berries gathered from the forest
         floor. They also consume small invertebrates occasionally. Their feeding behaviour involves slow, deliberate foraging among
         leaf litter, where their subdued colouration helps them remain concealed from predators.'''.replace( '\n', ' ' ),
      '''These doves are shy and secretive, spending most of their time on the forest floor rather than in trees. They are usually
         encountered alone or in pairs and tend to flush suddenly into low branches when disturbed. Vocalizations are soft and low,
         suited to communication in dense forest. Their elusive behaviour makes them difficult to observe in the wild.'''
         .replace( '\n', ' ' ),
      '''The Luzon bleeding-heart dove is well adapted to a terrestrial forest lifestyle. Its rounded body and strong legs support
         ground foraging, while muted upper-body colouration provides camouflage among leaf litter. The dramatic red breast patch is
         thought to play a role in mate recognition and display, standing out against otherwise subtle plumage. Short flights into
         understory vegetation allow quick escape without prolonged exposure.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs during periods of high food availability. Nests are shallow platforms of twigs placed low in
         shrubs or small trees. Females usually lay one or two eggs, which both parents help incubate and care for. Chicks grow
         slowly and remain dependent for several weeks. In managed care, Luzon bleeding-heart doves can live 15–20 years, with
         slightly shorter lifespans expected in the wild.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Malayan Bonytongue',
      'Scleropages Formosus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Malayn bonytongue can be found in a habitat just past the doors to the outdoor orangutan habitat, on the right.''',
      None,                                                          # Seasonal viewing tips
      '''The Malayan bonytongue is a large, elongated freshwater fish, commonly reaching 60–90 cm in length, with some individuals
         growing larger. It has a flattened, bony head, large metallic scales, and a long dorsal and anal fin that extend toward the
         tail, giving it a ribbon-like swimming motion. Two prominent barbels on the lower jaw are used for sensory detection.
         colouration varies by population, ranging from silver to green, gold, or red hues.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, occurring in slow-moving rivers, flooded forests, peat swamps, and lakes in
         countries such as Malaysia, Indonesia, Thailand, and Cambodia. It favors warm, low-oxygen waters with dense vegetation and
         submerged structure, often inhabiting blackwater systems rich in organic material.'''.replace( '\n', ' ' ),
      '''Malayan bonytongues are carnivorous surface feeders, preying on fish, insects, crustaceans, and small vertebrates. They
         hunt primarily near the water’s surface, using their upward-facing mouth to snatch prey with rapid strikes. Their diet
         reflects their role as top predators in many freshwater ecosystems.'''.replace( '\n', ' ' ),
      '''These fish are generally solitary and territorial, especially as adults. They are slow, deliberate swimmers, often cruising
         near the surface or hovering beneath overhanging vegetation. Activity is mostly crepuscular, with increased feeding during
         dawn and dusk.'''.replace( '\n', ' ' ),
      '''The Malayan bonytongue belongs to an ancient group of fishes with several specialized traits. Its bony tongue plate helps
         grasp prey, while the upturned mouth and surface-oriented vision support ambush feeding. A modified swim bladder allows
         limited air breathing, enabling survival in oxygen-poor waters. Large, armor-like scales provide protection from predators.'''
         .replace( '\n', ' ' ),
      '''Breeding occurs during periods of seasonal flooding. After spawning, the male mouthbroods the eggs and young, protecting
         them until they are large enough to survive independently. Growth is slow, and sexual maturity may take several years. In
         the wild and in managed care, Malayan bonytongues can live 20–30 years or more.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Malaysian Painted Turtle',
      'Cuora Marmorata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Malaysian painted turtle can be found in a shared habitat with the tomistoma, which is accesssed by heading up to the
         right, towards the elevated orangutan viewing once you enter the pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Malaysian painted turtle is a large river turtle, with adults commonly reaching 50–60 cm in shell length. The carapace
         is smooth and oval, typically olive-brown to gray, while the plastron is pale yellow. During the breeding season, males
         develop striking colouration, including a white to pale-blue head, bright red or orange facial markings, and a bluish tinge
         to the limbs, making them among the most colourful freshwater turtles. Females are larger but lack the intense breeding
         colours.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, found mainly in Malaysia, southern Thailand, Indonesia, and parts of Cambodia. It
         inhabits large rivers, estuaries, and coastal floodplains, often moving between freshwater and brackish environments. Sandy
         riverbanks are essential for nesting, and the species is closely tied to seasonally dynamic river systems.'''
         .replace( '\n', ' ' ),
      '''Malaysian painted turtles are primarily herbivorous, feeding on aquatic vegetation, fruits, leaves, and algae, though
         juveniles may consume small invertebrates. Their strong jaws and broad beak are adapted for cropping and processing plant
         material in flowing water habitats.'''.replace( '\n', ' ' ),
      '''These turtles are mostly aquatic, spending much of their time swimming or resting on river bottoms. Basking occurs but is
         less frequent than in many pond turtles. They are generally non-territorial and may gather in suitable feeding areas,
         particularly during periods of high water.'''.replace( '\n', ' ' ),
      '''The Malaysian painted turtle shows several adaptations to large river and estuarine environments. Its streamlined shell
         aids efficient swimming, while powerful limbs support movement in currents. Seasonal colour changes in males function in
         courtship and mate recognition, and tolerance for brackish water allows access to productive coastal habitats.
         Long-distance movements along river systems help locate nesting and feeding sites.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the dry season, when females migrate to sandy riverbanks to nest. Clutches can contain 20–40 eggs,
         which incubate for several months. Hatchlings emerge at the onset of favorable conditions and make their way to the water.
         Growth is slow, and individuals may take 10–15 years to reach maturity. In the wild, Malaysian painted turtles can live
         40–60 years, with similar or longer lifespans in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Mekong Barb',
      'Puntius Ornatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Mekong barb can be found in the carp tank just past the waterfall, found by taking the path on the left once you enter
         the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must backtrack
         slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Mekong barb is one of the largest carp species in the world, capable of reaching 150–180 cm in length and weighing over
         300 kg in exceptional individuals. It has a deep, heavy-bodied shape with large, reflective silver scales and a blunt head.
         The mouth is small and downward-facing, lacking prominent barbels, and is adapted for grazing rather than predation.
         Juveniles are slimmer and more streamlined, becoming deeper-bodied with age.'''.replace( '\n', ' ' ),
      '''This species is native to mainland Southeast Asia, occurring primarily in the Mekong, Chao Phraya, and Mae Klong river
         systems of Thailand, Cambodia, Laos, and Vietnam. Mekong barbs inhabit large rivers, deep pools, and floodplains, moving
         seasonally into inundated forests and wetlands during the rainy season. Their life cycle is closely tied to natural flood
         pulses.'''.replace( '\n', ' ' ),
      '''Mekong barbs are primarily herbivorous, feeding on aquatic plants, algae, fruits, and seeds that fall into the water during
         seasonal flooding. They graze along river bottoms and flooded vegetation, using their specialized mouth to crop plant
         material. This diet makes them important seed dispersers within floodplain ecosystems.'''.replace( '\n', ' ' ),
      '''Adults are generally slow-moving and non-aggressive, often encountered singly or in small groups. Juveniles may form looser
         schools. The species undertakes long-distance seasonal migrations, moving upstream to spawn and downstream or into
         floodplains to feed. Activity is mainly diurnal, with feeding concentrated during periods of high water.'''
         .replace( '\n', ' ' ),
      '''The Mekong barb is adapted to life in vast, dynamic river systems. Its large body size provides protection from most
         predators, while strong muscles allow sustained swimming in currents. A highly efficient digestive system enables the
         processing of fibrous plant material. Seasonal migrations allow the species to exploit nutrient-rich floodplains and
         synchronize reproduction with optimal environmental conditions.'''.replace( '\n', ' ' ),
      '''Spawning occurs during the rainy season, triggered by rising water levels. Females release large numbers of eggs into
         flowing water, where they drift before hatching. Growth is relatively slow, and individuals take many years to reach full
         size and maturity. Mekong barbs are long-lived, with lifespans estimated at 40–50 years or more in the wild, and
         potentially longer in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Monocled Cobra',
      'Naja Kaouthia',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The monocled cobra can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The monocled cobra is a medium to large venomous snake, typically measuring 1.2–1.8 m in length, with some individuals
         growing larger. Its body is smooth-scaled and cylindrical, ranging in colour from olive, brown, gray, to nearly black. When
         threatened, it raises the front of its body and spreads a broad hood marked with a single circular “monocle” pattern on the
         back, a key feature distinguishing it from related cobras. The head is slightly flattened with round pupils.'''
         .replace( '\n', ' ' ),
      '''This species is widespread across South and Southeast Asia, including India, Bangladesh, Myanmar, Thailand, Cambodia, Laos,
         Vietnam, and southern China. Monocled cobras inhabit a wide range of environments, from forests, grasslands, and wetlands
         to agricultural areas and village edges. Their adaptability allows them to persist even in human-altered landscapes,
         provided prey and shelter are available.'''.replace( '\n', ' ' ),
      '''Monocled cobras are carnivorous, feeding on rodents, frogs, lizards, birds, eggs, and other snakes. They are active hunters,
         relying on stealth and quick strikes. Venom is used primarily to subdue prey, after which the snake swallows its meal whole.
         Their diet makes them important controllers of rodent populations in many regions.'''.replace( '\n', ' ' ),
      '''These snakes are generally solitary and mostly nocturnal, though they may be active during the day in cooler or undisturbed
         conditions. When confronted, monocled cobras prefer to escape but will display defensively if cornered, raising the body,
         spreading the hood, and hissing loudly. They are known for being alert and responsive, traits that contribute to their
         reputation as a formidable species.'''.replace( '\n', ' ' ),
      '''The monocled cobra’s venom is a powerful neurotoxin, disrupting nerve function and rapidly immobilizing prey. The
         expandable hood is formed by elongated ribs and serves as a visual warning, making the snake appear larger and more
         dangerous. Good eyesight and chemosensory ability aid hunting, while a flexible body allows efficient movement through
         dense vegetation, burrows, and human structures.'''.replace( '\n', ' ' ),
      '''Breeding typically occurs in the warm season. Females lay 15–30 eggs in sheltered sites such as burrows or under debris and
         may guard the clutch until hatching. Hatchlings are fully venomous from birth and disperse soon after emerging. In the
         wild, monocled cobras are thought to live 15–20 years, with individuals in managed care sometimes living 20 years or more.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Palawan Peacock-Pheasant',
      'Polyplectron Napoleonis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Palawan peacock-pheasant can be found in the main aviary in the Indo-Malaya pavilion, which sits in the center of the
         pavilion. The best area to view the birds in the aviary is in between the stairs leading down from the elevated orangutan
         viewing, up until you are across from the doors leading you to the outdoor orangutan habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Palawan peacock-pheasant is a medium-sized, ground-dwelling pheasant, measuring about 40–50 cm in length. Males are
         especially striking, with dark iridescent blue-green plumage densely patterned with metallic ocelli (eye-spots) on the
         wings and tail. The face is pale with a bold black eye line, and the crest is short and neat. Females are more subdued,
         brownish with faint patterning, providing camouflage. Both sexes have strong legs adapted for terrestrial movement.'''
         .replace( '\n', ' ' ),
      '''This species is endemic to the Philippine island of Palawan, where it inhabits lowland and foothill tropical forests,
         particularly areas with dense understory and leaf litter. It depends on intact forest cover and is rarely found far from
         undisturbed habitat, making it sensitive to logging and land conversion.'''.replace( '\n', ' ' ),
      '''Palawan peacock-pheasants are omnivorous ground foragers, feeding on seeds, fruits, fallen berries, insects, worms, and
         other small invertebrates. They forage quietly among leaf litter, using their bill to probe and flick aside debris. This
         feeding behaviour contributes to seed dispersal and invertebrate control within the forest ecosystem.'''.replace( '\n', ' ' ),
      '''These birds are secretive and shy, typically encountered alone or in pairs. Males are known for elaborate courtship
         displays, spreading their wings and tail to showcase shimmering eye-spots while performing slow, deliberate movements.
         Outside the breeding season, activity is mostly limited to foraging and avoiding detection. Vocalizations are low and
         infrequent.'''.replace( '\n', ' ' ),
      '''The species is well adapted to a terrestrial forest lifestyle. Cryptic colouration in females provides camouflage while
         nesting, while males’ iridescent plumage plays a key role in sexual selection. Strong legs allow efficient movement across
         uneven forest floors, and keen vision helps detect predators in dim understory light.'''.replace( '\n', ' ' ),
      '''Breeding occurs during periods of high food availability. Nests are shallow scrapes on the ground, often hidden beneath
         dense vegetation. Females typically lay 1–2 eggs, which they incubate alone. Chicks are precocial and able to move shortly
         after hatching but remain dependent for protection. In the wild, Palawan peacock-pheasants may live 10–15 years, with
         lifespans of 15–20 years possible in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red-Lined Torpedo Barb',
      'Sahyadria Denisonii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red-lined torpedo barb can be found in the carp tank just past the waterfall, found by taking the path on the left once
         you enter the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must
         backtrack slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The red-lined torpedo barb is a slender, streamlined freshwater fish reaching about 12–15 cm in length. Its silver body is
         marked by a bold black horizontal stripe running from the snout to the tail, overlaid by a vivid red stripe on the head and
         upper body. The dorsal fin often shows red or yellow highlights, and the tail fin is edged with black and yellow bands.
         Males are typically more brightly coloured, especially during breeding periods.'''.replace( '\n', ' ' ),
      '''This species is endemic to southwestern India, where it inhabits clear, fast-flowing rivers and streams in the Western
         Ghats. It prefers waters with rocky substrates, strong currents, and high oxygen levels, often sheltering among submerged
         roots and boulders. Its limited range and reliance on clean waterways make it particularly sensitive to environmental
         change.'''.replace( '\n', ' ' ),
      '''Red-lined torpedo barbs are omnivorous, feeding on algae, plant matter, small insects, crustaceans, and organic debris.
         They forage actively in mid-water and near the bottom, grazing on surfaces and picking drifting food items from the
         current. Their varied diet supports their energetic swimming behaviour.'''.replace( '\n', ' ' ),
      '''This species is highly active and social, typically forming schools that move together through flowing water. Schooling
         helps reduce predation risk and allows efficient navigation of strong currents. They are diurnal and spend much of the day
         swimming continuously, making them visually engaging in aquarium and exhibit settings.'''.replace( '\n', ' ' ),
      '''The red-lined torpedo barb’s streamlined body and strong tail allow sustained swimming in fast currents. Its bold striping
         may help maintain school cohesion in turbulent water. High oxygen demand reflects adaptation to well-aerated streams, while
         strong sensory abilities aid in detecting food and navigating complex river habitats.'''.replace( '\n', ' ' ),
      '''Spawning occurs during seasonal rainfall, when water levels rise and conditions are favorable. Eggs are scattered among
         gravel or vegetation, with no parental care after spawning. Growth is moderate, and individuals typically reach maturity
         within a few years. In the wild and in managed care, red-lined torpedo barbs can live 5–8 years, with optimal conditions
         supporting longer lifespans.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Reticulated Python',
      'Malayopython Reticulatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The reticulated python can be found in an enclosure just before the second, lower-down viewing area of the orangtuans.''',
      None,                                                          # Seasonal viewing tips
      '''The reticulated python is one of the longest snake species in the world, commonly reaching 4–6 m, with exceptional
         individuals surpassing 7 m. Its body is muscular, cylindrical, and patterned with intricate geometric markings of gold,
         brown, and black, creating a “reticulated” network that provides excellent camouflage in forested and riverine habitats.
         The head is elongated, with heat-sensing pits along the upper and lower jaws to detect warm-blooded prey. Males are
         generally longer and more slender, while females are thicker-bodied and heavier.'''.replace( '\n', ' ' ),
      '''Reticulated pythons are native to Southeast Asia, including Indonesia, Malaysia, the Philippines, Thailand, and Myanmar,
         inhabiting rainforests, mangroves, grasslands, and river edges. They are highly adaptable, able to navigate both dense
         forest and human-modified landscapes. These snakes are semi-aquatic, often found swimming in rivers or resting near water,
         reflecting their preference for environments with abundant prey and cover.'''.replace( '\n', ' ' ),
      '''These pythons are ambush predators, feeding primarily on mammals and birds, ranging from rodents to deer and occasionally
         pigs. They kill by constriction, wrapping around prey to immobilize it before swallowing whole. Juveniles consume smaller
         prey like rats and birds, while adults can tackle significantly larger animals. They have flexible jaws and expandable
         bodies, allowing ingestion of prey much larger than their head diameter.'''.replace( '\n', ' ' ),
      '''Reticulated pythons are generally solitary and mostly nocturnal, relying on stealth rather than speed. During the day, they
         often hide in vegetation or submerged in water, conserving energy. Despite their size, they are agile swimmers and
         climbers. Males may engage in ritual combat during the breeding season, intertwining their bodies in contests for access to
         females. Hatchlings disperse immediately after emerging from the eggs.'''.replace( '\n', ' ' ),
      '''The reticulated python possesses several key adaptations that make it an apex predator in Southeast Asian ecosystems. Its
         constricting musculature allows it to subdue large prey, while heat-sensing pits detect warm-blooded animals even in
         darkness. The intricate reticulated patterning provides camouflage in forests and riverbanks, helping it avoid predators
         and ambush prey. Semi-aquatic habits allow it to swim and hunt effectively in rivers, and a slow metabolism enables
         survival during long periods between meals. Its flexible jaw and expandable body permit ingestion of prey much larger than
         its head, making it an extremely efficient predator within its environment.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally, often timed with rainy periods. Females lay 15–80 eggs in protected nests such as leaf litter,
         hollow logs, or burrows, and exhibit brooding behaviour, coiling around the eggs to regulate temperature and humidity
         through muscular contractions. Hatchlings are independent from birth, measuring about 70–90 cm. Sexual maturity occurs at
         3–5 years, and in the wild, reticulated pythons can live 20–30 years, with longer lifespans in managed care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Spiny Turtle',
      'Heosemys Spinosa',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The spiny turtle can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The spiny turtle is a small to medium-sized freshwater turtle, typically reaching 20–25 cm in shell length. Its carapace is
         dark brown to black and covered with prominent, sharp-edged ridges or spines along the vertebral region, giving the species
         its name. The plastron is lighter, often yellowish, and the head and limbs are dark with subtle yellow or orange markings.
         Juveniles are more vividly patterned, with pronounced ridges that become less distinct with age. Both sexes appear similar,
         though males may be slightly smaller and have longer tails.'''.replace( '\n', ' ' ),
      '''Spiny turtles are native to Southeast Asian rainforests, including Malaysia, Thailand, Sumatra, Borneo, and surrounding
         islands. They inhabit humid lowland and foothill forests, often near slow-moving streams, shallow ponds, or wet forest
         floors. They are secretive and rely on dense leaf litter and vegetation for cover, making intact forest critical for
         survival.'''.replace( '\n', ' ' ),
      '''This species is omnivorous, feeding on fallen fruits, berries, seeds, fungi, insects, and small invertebrates. Foraging
         occurs mostly on the forest floor, where their slow, deliberate movements help avoid predators. Their varied diet helps
         disperse seeds and maintain ecosystem balance.'''.replace( '\n', ' ' ),
      '''Spiny turtles are mostly solitary and secretive, spending much of their time hiding in leaf litter or shallow water. They
         are diurnal but cryptic, emerging to feed and bask occasionally. When threatened, they can withdraw completely into their
         heavily ridged shell, and their slow, deliberate movement reduces detection.'''.replace( '\n', ' ' ),
      '''The spiny turtle’s spiked carapace provides defense against predators, while its muted colouration aids in camouflage on
         the forest floor. Its short, sturdy limbs and webbed feet allow efficient movement through leaf litter and shallow water,
         and its omnivorous diet ensures flexibility in changing seasonal food availability. The spiny ridges may also deter
         predation by making the turtle difficult to swallow. Overall, the species is highly adapted to a humid, forested, riparian
         environment, combining concealment, protection, and feeding efficiency.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the rainy season, when females lay 3–7 eggs in shallow nests dug into soil or leaf litter near
         water. Incubation lasts several months, and hatchlings are independent immediately after emerging. Spiny turtles grow
         slowly, reaching sexual maturity around 5–7 years, and can live 25–30 years in the wild, with longer lifespans in managed
         care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Sumatran Orangutan',
      'Pongo Abelii',
      8,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The Sumatran orangutans have an indoor and outdoor habitat in the Indo-Malaya Pavilion. Their indoor habitat can be viewed
         from three different vantage points. The first is the elevated viewing point, accessed by sticking to the right once you
         enter the pavilion. The other two viewing points can be reached by walking around the pavilion, and accessing the back half.
         The outdoor habitat can be accessed by walking around halfway through the pavilion, and taking the doors heading outside.
         The orangutans at the zoo are still getting used to their new outdoor habitat, and thus viewing them in this habitat is far 
         from given. Your best chance of seeing them is to visit early in the day. The Toronto zoo has seven orangutans, but
         orangutans are not a highly social species like most other apes and primates. In each of the habitats you will only ever
         see one or two orangutans on exhibit at a time.'''.replace( '\n', ' ' ),
      '''Sumatran orangutans are warm weather primates, and can only be outside during the warmer months. During the warmer months
         you may find these apes in their new, state-of-the-art outdoor habitat which opened in 2023, and their indoor habitat. The
         orangutans can be seen year-round in their indoor habitat.'''.replace( '\n', ' ' ),
      '''The Sumatran orangutan is a large, arboreal great ape characterized by long, reddish-brown hair, a robust body, and long,
         powerful arms adapted for brachiation and climbing. Adult males develop prominent cheek flanges and a throat pouch, which
         serve as visual and vocal signals to other orangutans. Females are smaller, with less pronounced facial features. Adults
         typically weigh 50–90 kg for males and 30–50 kg for females, with arm spans exceeding 2 meters, allowing them to reach
         across large gaps in the forest canopy. Their hands and feet are prehensile, with long fingers and opposable thumbs and big
         toes, giving them exceptional grip and maneuverability.'''.replace( '\n', ' ' ),
      '''Sumatran orangutans are endemic to the northern part of the Indonesian island of Sumatra, occupying lowland and montane
         tropical rainforests. They prefer dense, primary forests but may venture into secondary forests when food is scarce. They
         are highly arboreal, rarely descending to the forest floor, and require continuous canopy cover to travel, forage, and
         build nests. Deforestation, palm oil plantations, and human encroachment have dramatically reduced their habitat, making
         intact forest corridors essential for survival.'''.replace( '\n', ' ' ),
      '''These orangutans are primarily frugivorous, with fruit making up 60–90% of their diet, depending on seasonal availability.
         They also consume leaves, bark, flowers, insects, and occasionally small vertebrates. Sumatran orangutans have been
         observed using tools to extract insects, open fruits, or access honey, demonstrating advanced cognitive skills. Foraging is
         mostly solitary, and adults travel 1–2 km per day within their home ranges of 5–20 km², adjusting movement patterns to
         follow fruiting cycles.'''.replace( '\n', ' ' ),
      '''Sumatran orangutans are semi-solitary, with loose social networks rather than large permanent groups. Adult males are
         largely solitary, while females are accompanied by dependent offspring. Social interactions include vocalizations,
         displays, grooming, and play among juveniles. They are highly intelligent, capable of problem-solving, tool use, and
         complex communication, including long calls by males to advertise territory and attract mates. Nest building is a daily
         behaviour: orangutans construct sleeping nests in trees each night, using branches and leaves for support and comfort.'''
         .replace( '\n', ' ' ),
      '''The Sumatran orangutan exhibits numerous adaptations for an arboreal, forest-dwelling lifestyle. Its long, muscular arms
         and curved fingers enable efficient climbing and brachiation across gaps in the canopy. Prehensile hands and feet provide
         precise gripping for foraging and nest-building. Dense, reddish fur protects against rain and sun exposure, while flexible
         joints allow extreme reach and maneuverability. Cognitive adaptations, including advanced memory, tool use, and
         problem-solving, support survival in a highly dynamic environment with patchy fruit resources. Slow reproductive rates and
         extended parental care are adaptations to maximize offspring survival in a complex, competitive habitat.'''
         .replace( '\n', ' ' ),
      '''Sumatran orangutans have one of the slowest reproductive rates among mammals. Females reach sexual maturity at 8–10 years,
         and males mature around 12–15 years. Gestation lasts about 8.5 months, typically producing a single offspring. Infants
         cling to their mothers for 2–3 years, with extended weaning around 5–6 years, and juveniles may remain in close association
         with the mother for up to a decade. Females reproduce approximately once every 7–9 years, and lifespans in the wild can
         reach 35–45 years, with captive individuals sometimes living 50 years or more.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to seven orangutans. Puppe was born in 1967 and is the oldest orangutan in North America. The zoo
         also has adult males Budi and Kembali, and females Jingga, Rami, and Sekali. Youngster Wali, is a male born in 2022. Puppe
         is the only orangutan who goes on exhibit by herself, so if you see just one orangutan in one of the habitats then it is
         likely her. Kembali and Jingga, and Budi and Rami form adult pairs on exhibit. Wali goes on exhibit with his mother,
         Sekali.'''.replace( '\n', ' ' )
   ),
   (
      'Tentacled Snake',
      'Erpeton Tentaculatum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tentacled snake can be found in an enclosure just after the first white-handed gibbon viewing.''',
      None,                                                          # Seasonal viewing tips
      '''The tentacled snake is a small, aquatic snake, typically reaching 50–70 cm in length. Its most distinctive feature is a
         pair of short, fleshy tentacles protruding from the snout, which aid in detecting prey. The body is thick, cylindrical, and
         usually gray to brown, often mottled to blend with murky water and submerged vegetation. The head is flattened and
         triangular, with eyes positioned high for surface surveillance. Both sexes are similar in appearance, though males are
         generally slimmer.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, including Thailand, Malaysia, Indonesia, and Vietnam, inhabiting slow-moving
         rivers, ponds, swamps, and flooded rice paddies. Tentacled snakes are fully aquatic, rarely leaving the water except during
         flooding or dispersal events. They prefer habitats with dense submerged vegetation that provides both cover and ambush
         points.'''.replace( '\n', ' ' ),
      '''Tentacled snakes are specialist ambush predators, feeding almost exclusively on fish. They employ an extraordinary hunting
         strategy: remaining motionless in the water, they use body undulations to create a “bow wave”, triggering reflex movements
         in fish. The snake then strikes with precise timing, often with a lateral snap of the head, capturing prey in a single
         motion. This method relies on extremely fast reflexes and the ability to read prey behaviour almost instinctively.'''
         .replace( '\n', ' ' ),
      '''Tentacled snakes are solitary and highly sedentary, spending most of their time anchored to vegetation or submerged
         structures. They are nocturnal to crepuscular, with peak hunting activity during low light conditions. They do not display
         social behaviours and interact only for mating or territorial disputes. Hatchlings exhibit the same hunting strategy as
         adults, indicating a strong innate component to their behaviour.'''.replace( '\n', ' ' ),
      '''The tentacled snake exhibits remarkable adaptations to a fully aquatic, fish-hunting lifestyle. Its tentacles function as
         mechanosensory organs, detecting water movement from nearby prey. Flattened, streamlined body and laterally compressed tail
         allow silent maneuvering through water and minimal disturbance to prey. Eyes are positioned for surface scanning, while
         subtle camouflage enables it to remain virtually invisible in muddy, vegetated waters. The species’ reflexive hunting
         strategy demonstrates an evolutionary specialization rare among snakes, combining sensory, muscular, and behavioural
         adaptations into a highly efficient predator.'''.replace( '\n', ' ' ),
      '''Tentacled snakes are ovoviviparous, giving birth to live young rather than laying eggs. Litter sizes range from 6–20
         neonates, which are fully independent at birth and capable of hunting fish immediately. Females reproduce once or twice per
         year depending on environmental conditions. Lifespan in the wild is estimated at 8–12 years, with similar longevity in
         managed care if conditions are stable.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Tinfoil Barb',
      'Barbonymus Schwanenfeldii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tinfoil barb can be found in the carp tank just past the waterfall, found by taking the path on the left once you enter
         the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must backtrack
         slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The tinfoil barb is a large, elongated freshwater fish, typically reaching 35–40 cm in length in the wild, with some
         individuals growing up to 50 cm. Its body is silvery, reflecting light like tinfoil, with a subtle bronze or green sheen
         along the dorsal surface. The fins are bright red or orange, particularly the caudal, dorsal, and pelvic fins, making it
         highly noticeable in school formations. Juveniles are smaller and slightly less colourful, but develop vibrant fin
         colouration as they mature.'''.replace( '\n', ' ' ),
      '''Tinfoil barbs are native to Southeast Asia, including Thailand, Malaysia, Sumatra, and Borneo, inhabiting large rivers,
         floodplains, and lowland freshwater habitats. They prefer open water areas with moderate to strong currents, often near
         submerged vegetation or woody debris. Seasonal flooding influences their movement and feeding, and they are capable of
         navigating a variety of freshwater habitats.'''.replace( '\n', ' ' ),
      '''This species is omnivorous, feeding on algae, aquatic plants, fruits, insects, and small invertebrates. They are active
         foragers, moving in midwater and near the surface, often grazing on plant material and picking drifting food from the
         current. Their feeding behaviour supports nutrient cycling in freshwater ecosystems and contributes to maintaining
         vegetation balance.'''.replace( '\n', ' ' ),
      '''Tinfoil barbs are highly social, forming large, active schools that move in coordinated patterns, which helps reduce
         predation risk. They are diurnal and very active swimmers, often occupying mid-water zones and frequently interacting with
         other schooling fish. This schooling behaviour also makes them visually engaging in aquarium and zoo exhibits.'''
         .replace( '\n', ' ' ),
      '''The tinfoil barb is adapted to a riverine, schooling lifestyle. Its streamlined, silvery body allows for efficient swimming
         in flowing water, while bright fins serve as visual signals within schools, helping maintain group cohesion. Strong muscles
         and flexible body aid in sudden directional changes to avoid predators. Omnivorous feeding allows the species to exploit
         seasonally variable food sources, making it resilient in dynamic river habitats.'''.replace( '\n', ' ' ),
      '''Tinfoil barbs spawn during seasonal floods, releasing thousands of eggs into open water where they drift until hatching.
         There is no parental care, and juveniles are independent immediately. Growth is relatively rapid in the first year, and
         individuals can reach sexual maturity in 2–3 years. Lifespan in the wild is estimated at 8–12 years, with similar or
         slightly longer lifespans in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Tomistoma',
      'Tomistoma Schlegelii',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tomistoma can be found in a shared habitat with the Malaysian painted turtle, which is accesssed by heading up to the
         right, towards the elevated orangutan viewing once you enter the pavilion.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''TThe Tomistoma is a large freshwater crocodilian, typically reaching 3–4 m in length, with some males exceeding 5 m. It has
         a long, narrow snout lined with sharp, interlocking teeth, adapted specifically for catching fish. The body is robust with
         dark olive to gray colouration and lighter ventral scales. Juveniles are smaller and display a more pronounced pattern of
         yellow stripes, which fades as they mature. The eyes and nostrils are positioned for surface surveillance, enabling
         stealthy hunting while mostly submerged.'''.replace( '\n', ' ' ),
      '''Tomistomas are native to Southeast Asia, including Indonesia, Malaysia, and southern Thailand, inhabiting slow-moving
         rivers, swamps, peatlands, and freshwater lakes. They prefer areas with dense submerged vegetation and calm waters.
         Seasonal flooding allows them to access wider areas for hunting, dispersal, and breeding.'''.replace( '\n', ' ' ),
      '''Tomistomas are carnivorous, feeding mainly on fish, amphibians, and small aquatic vertebrates. They use their slender snout
         to snap rapidly at prey, relying on stealth and submerged ambush tactics. Young individuals feed on insects and small fish
         until they grow large enough to tackle larger prey. Hunting efficiency and specialization make them apex predators in their
         aquatic environments.'''.replace( '\n', ' ' ),
      '''Tomistomas are mostly solitary and territorial, with individuals occupying defined stretches of river or swamp. They are
         largely nocturnal hunters, remaining hidden during the day under vegetation or in shallow water. Breeding males may be more
         aggressive during the mating season, and females select nesting sites on elevated riverbanks or in dense vegetation.
         Hatchlings are immediately independent but vulnerable to predation.'''.replace( '\n', ' ' ),
      '''The Tomistoma exhibits specialized adaptations for a fish-eating, aquatic lifestyle. Its elongated, narrow snout and sharp
         teeth allow it to capture fish with precision, while eyes and nostrils positioned atop the head enable it to remain mostly
         submerged, minimizing detection by prey. Its muscular tail provides powerful propulsion for swimming, and its armored
         scales protect it from both predators and intraspecific conflicts. Camouflaged colouration blends with muddy waters and
         vegetation, enhancing stealth. These adaptations make the Tomistoma a highly efficient predator in slow-moving freshwater
         habitats.'''.replace( '\n', ' ' ),
      '''Breeding occurs during seasonal floods. Females construct mound nests of vegetation and soil, where they lay 20–60 eggs.
         Incubation lasts approximately 90–100 days, depending on temperature. Hatchlings are fully independent at birth. Tomistomas
         grow slowly, with sexual maturity reached at 10–12 years, and can live 40–50 years in the wild, with similar or longer
         lifespans in managed care.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a male Tomistoma named Fernando.'''
   ),
   (
      'Tri-Coloured Shark',
      'Epalzeorhynchos Ehrenbergi',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The tri-coloured shark can be found in the carp tank just past the waterfall, found by taking the path on the left once you
         enter the pavilion. If you decide to go up to the elevated orangutan viewing, when you go down the stairs, you must
         backtrack slightly by going to the left.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The tri-coloured shark is a medium-sized freshwater fish, typically reaching 20–25 cm in length. Its body is sleek and
         elongated, primarily dark gray to black, with a bright white belly, a red or orange dorsal fin, and fins edged with black.
         Juveniles are smaller and often exhibit more subtle colouration, which intensifies as they mature. Their streamlined body
         is well-suited for swimming in fast-flowing waters.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asia, including Thailand, Malaysia, and Sumatra, where it inhabits fast-flowing rivers,
         streams, and floodplain channels. Tri-coloured sharks prefer areas with rocky or sandy substrates, moderate to strong
         current, and some submerged vegetation or debris for cover. Seasonal floods influence their movements and feeding activity.'''
         .replace( '\n', ' ' ),
      '''Tri-coloured sharks are omnivorous, feeding on algae, plant matter, detritus, and small invertebrates. They actively graze
         along rocks and submerged surfaces, using their specialized mouths to scrape algae or pick small prey items from the
         substrate. Their feeding contributes to nutrient cycling in freshwater ecosystems and helps control algal growth.'''
         .replace( '\n', ' ' ),
      '''Tri-coloured sharks are active and social, often forming loose schools in larger water bodies. They are diurnal, swimming
         actively throughout the day, and use schooling both to reduce predation risk and improve foraging efficiency. They can be
         territorial in confined spaces but are generally non-aggressive in spacious, well-structured exhibits.'''
         .replace( '\n', ' ' ),
      '''The tri-coloured shark is adapted to fast-flowing, riverine habitats. Its streamlined body and strong fins allow sustained
         swimming against currents, while the bright dorsal fin and contrasting belly may help maintain school cohesion and
         communicate with conspecifics. Its mouth is specialized for scraping algae and detritus, enabling an omnivorous diet in
         variable seasonal conditions. The species’ schooling behaviour, agility, and flexible diet all contribute to its success in
         dynamic freshwater environments.'''.replace( '\n', ' ' ),
      '''Tri-coloured sharks spawn in response to rainy season floods, scattering eggs over submerged vegetation or substrates.
         There is no parental care, and juveniles are independent immediately. Growth is moderate, with sexual maturity reached at
         1–2 years, and individuals can live 6–10 years in the wild, with similar or slightly longer lifespans in captivity.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'White-Handed Gibbon',
      'Hylobates Lar',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The white-handed gibbons can be seen just past the second viewing area for the indoor orangutan habitat.''',
      None,                                                          # Seasonal viewing tips
      '''The white-handed gibbon is a medium-sized primate with slender, agile limbs and a light to dark brown coat. Its most
         distinctive feature is the white “hands” and feet”, along with a pale face ring that contrasts with darker facial fur.
         Adult males and females are similar in appearance, though males may be slightly larger, averaging 5–7 kg in weight and
         about 45–60 cm in body length, with arm spans up to 1.2 m. Their long arms and hook-like hands are perfectly adapted for
         brachiation (swinging through trees).'''.replace( '\n', ' ' ),
      '''White-handed gibbons are native to the forests of Southeast Asia, including Thailand, Malaysia, Myanmar, and parts of
         Indonesia, inhabiting primary and secondary tropical rainforests. They are strictly arboreal, rarely descending to the
         ground, and rely on continuous forest canopy for movement, foraging, and protection from predators. Habitat fragmentation
         and logging are major threats to their survival, emphasizing the importance of large, connected forest reserves.'''
         .replace( '\n', ' ' ),
      '''These gibbons are primarily frugivorous, with fruit making up the bulk of their diet, supplemented by leaves, flowers, buds,
         and occasionally insects or small invertebrates. They are selective feeders, often choosing ripe, high-energy fruits and
         moving efficiently through the canopy to access resources. Their diet supports seed dispersal, making them vital
         contributors to forest regeneration.'''.replace( '\n', ' ' ),
      '''White-handed gibbons are highly social, living in monogamous family groups composed of a mated pair and their dependent
         offspring. Family groups defend territories through loud vocalizations, with males and females performing complex duets
         that can carry over kilometers. These calls reinforce pair bonds and advertise territory to neighboring groups. Gibbons are
         diurnal and extremely agile, spending nearly all their time in the canopy, moving through brachiation, climbing, and
         leaping. Juveniles engage in play and social learning, which develops motor skills and social bonds.'''.replace( '\n', ' ' ),
      '''White-handed gibbons are superbly adapted for arboreal life in dense tropical forests. Their elongated arms and hook-shaped
         hands allow rapid brachiation, while strong shoulder joints and flexible wrists provide remarkable reach and grip.
         Lightweight, muscular bodies aid in aerial movement and energy efficiency, while keen eyesight and hearing help locate food
         and detect predators. Their vocal duetting is an adaptation for maintaining social cohesion and territorial defense in
         dense forests. Cognitive abilities support complex problem-solving, foraging, and social interactions, making them highly
         intelligent and sensitive to environmental changes.'''.replace( '\n', ' ' ),
      '''White-handed gibbons reach sexual maturity around 6–8 years, and females typically give birth to a single infant every 2–3
         years. Infants cling to the mother for about 18 months, with weaning occurring around 2 years, though juveniles remain
         with the family group for several more years. Lifespan in the wild can reach 25–30 years, with individuals in zoos
         sometimes living 35–40 years. Extended parental care and slow reproduction are strategies for maximizing survival in
         complex forest environments.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a family of three white-handed gibbons--father Mel, mother Manju, and daugther Mileena.''',
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Babyrousa Babyrussa',
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The babirusa has an outdoor and indoor habitat. The outdoor habitat can be found outside the greater one-horned rhinoceros
         building and on the left. If you don't see the babirusa outside, check inside the Indian rhino building. The babirusa
         shares this space with the rhino, and is sometimes viewable inside.'''.replace( '\n', ' ' ),
      '''Babirusa are a tropical species of pig and thus can only be outside in the warmer months, mostly from May to October, plus
         other warmer days. The rest of the time they can be viewed inside the greater one-horned rhino building.'''
         .replace( '\n', ' ' ),
      '''The babirusa, often called the “deer-pig,” is a unique wild pig native to Sulawesi and nearby Indonesian islands. Adults
         typically weigh 50–100 kg, with males slightly larger than females. Their most striking feature is the long, upward-curving
         tusks of the upper canines, which grow through the skin of the snout and may even curve back toward the forehead. Their
         body is sparsely haired, with coarse brown to gray skin, long legs, and a stocky frame adapted for walking through dense
         forest and wet areas.'''.replace( '\n', ' ' ),
      '''Babirusas inhabit tropical rainforests, swamps, and riverbanks in Sulawesi and surrounding islands. They prefer areas with
         dense vegetation, soft soil for rooting, and access to freshwater, which they use for wallowing and cooling. They are
         generally shy and avoid human settlements.'''.replace( '\n', ' ' ),
      '''Babirusas are omnivorous, feeding on roots, fruits, leaves, and small invertebrates. They use their strong jaws and tusks
         to dig and root in the soil for edible items. Their foraging contributes to seed dispersal and soil turnover, playing an
         important ecological role in their habitats.'''.replace( '\n', ' ' ),
      '''Babirusas are solitary or live in small groups, typically composed of a female and her offspring. Males are often solitary
         outside of the breeding season. They are diurnal to crepuscular, foraging mostly in the early morning and late afternoon.
         When threatened, they rely on stealth and dense cover to evade predators. Vocalizations are rare but can include grunts and
         squeals during social interactions or displays.'''.replace( '\n', ' ' ),
      '''The babirusa has several adaptations for life in dense tropical forests. Its strong, curved tusks are used in male–male
         competition during mating displays, though they are less effective as weapons than for visual signaling. Strong legs and
         hooves allow movement through muddy forest floors, while sparse hair and tough skin provide protection against undergrowth.
         Its omnivorous diet and flexible foraging behaviour allow it to exploit a wide range of food sources, making it well-suited
         to seasonal variations in fruit and root availability.'''.replace( '\n', ' ' ),
      '''Breeding occurs year-round but often peaks during periods of food abundance. Females give birth to 1–3 piglets after a
         gestation of about 4 months. Piglets are born with striped coats for camouflage and stay with the mother for several months
         before becoming independent. Babirusas can live 15–20 years in the wild and slightly longer in captivity, with slow
         reproduction emphasizing survival of fewer offspring.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female babirusa named Olive.'''.replace( '\n', ' ' )
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Rhinoceros Unicornis',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The greater one-horned rhinoceros shares its indoor space with the babirusa. They rotate between the on-exhibit and
         off-exhibit spaces, and thus the rhino may not always be viewable. Your best chance of spotting him involves visiting the
         rhino house in the afternoon, and checking both sides of the indoor habitat.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Greater One-Horned Rhinoceros is a massive, heavily armored herbivore, with adult males weighing 2,000–3,000 kg and
         females slightly smaller at 1,600–2,500 kg. Its most recognizable feature is a single black horn on the snout, which can
         reach 60–100 cm in length. The thick, gray skin forms large, folded plates, giving an appearance of natural armor. Short,
         strong legs support its heavy body, and a prehensile upper lip aids in grasping grasses and aquatic vegetation.'''
         .replace( '\n', ' ' ),
      '''This species is native to northern India and Nepal, inhabiting floodplains, tall grasslands, and riverine forests. They
         prefer areas with shallow water or swampy regions, which they use for wallowing to regulate body temperature and protect
         against parasites. Historically widespread, populations are now concentrated in protected national parks due to habitat
         loss and poaching.'''.replace( '\n', ' ' ),
      '''Greater One-Horned Rhinos are herbivorous, primarily grazing on tall grasses, leaves, and aquatic plants. They may also
         browse shrubs, fruits, and bark. Their selective feeding helps maintain the structure of grassland ecosystems, influencing
         plant diversity and supporting other herbivores.'''.replace( '\n', ' ' ),
      '''These rhinos are mostly solitary, except for mothers with calves or small aggregations in favorable feeding areas. They are
         diurnal and crepuscular, spending mornings grazing and afternoons wallowing in mud or water. Territorial males mark areas
         with dung piles and wallows, using vocalizations, scent, and body displays to communicate. Mothers are highly protective of
         calves for up to 3 years, and juveniles gradually learn foraging and social behaviours.'''.replace( '\n', ' ' ),
      '''The Greater One-Horned Rhinoceros has several adaptations for life in floodplain and grassland habitats. Its thick, folded
         skin acts as armor against predators and intraspecific fights, while the single horn is used for defense, dominance
         displays, and digging for water or minerals. A prehensile upper lip allows efficient grasping of grasses and aquatic
         vegetation. Wallowing behaviour regulates body temperature and provides protection against parasites, and strong legs
         support movement across soft, marshy terrain. Their size, strength, and sensory abilities make them formidable herbivores
         and ecosystem engineers.'''.replace( '\n', ' ' ),
      '''Mating occurs year-round, though peaks often coincide with the wet season. Females give birth to a single calf after a
         gestation of approximately 16 months. Calves are dependent on their mothers for 2–3 years, during which they learn feeding
         and social skills. Sexual maturity is reached at 5–7 years for females and 7–10 years for males. Lifespan in the wild
         ranges from 35–45 years, with individuals in captivity occasionally surpassing 50 years.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has one male greater one-horned rhinoceros, Vishnu. Vishnu has had some skin problems recently, which is
         why you may see bandages on his body. His condition has made the outdoor rhino habitat unusable for him, due to the changes
         in terrain. There have been efforts made to smoothen the terrain to make it accessible for him, so hopefully in the future,
         Vishnu will be able to spend more time outdoors.'''.replace( '\n', ' ' )
   ),
   (
      'Indian Peafowl',
      'Pavo Cristatus',
      -15,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Indian peafowl can be spotted in the long barn across from the Indian rhino house.''',
      '''The Indian peafowl are very well adapted to stay in the cold, but they also have access to indoor spaces in the winter, so
         they may choose to go inside on colder days.'''.replace( '\n', ' ' ),
      '''TThe Indian peafowl, commonly called the peacock (male) or peahen (female), is a large, ground-dwelling bird. Males
         typically reach 2.2 m in total length, including the spectacular tail (train) feathers, while females are smaller at 90–100
         cm. Males have iridescent blue-green plumage, a metallic sheen on the neck and chest, and an elongated train of tail
         feathers adorned with eye-shaped ocelli used in display. Females have brownish plumage with subtle patterning for
         camouflage, and a smaller crest atop the head.'''.replace( '\n', ' ' ),
      '''Indian peafowl are native to India, Sri Lanka, and parts of Southeast Asia, inhabiting open forests, scrublands, farmland
         edges, and near human settlements. They are terrestrial but roost in trees at night to avoid predators. They thrive in
         areas that provide a combination of open foraging spaces and nearby cover for protection.'''.replace( '\n', ' ' ),
      '''These birds are omnivorous, feeding on seeds, fruits, insects, small reptiles, and invertebrates. They forage mostly on the
         ground, using their strong legs and beaks to scratch and peck for food. Their diet contributes to seed dispersal and helps
         control insect populations in their habitats.'''.replace( '\n', ' ' ),
      '''Indian peafowl are diurnal and social, often forming small groups or loosely associated flocks outside the breeding season.
         Males perform elaborate courtship displays, fanning their long trains and shaking the feathers to produce rattling sounds
         while vocalizing to attract females. Females choose mates based on display size, feather quality, and vigor. They are alert
         to predators and will flee on foot or fly short distances to roost in trees. Vocalizations include loud calls during the
         mating season or when alarmed.'''.replace( '\n', ' ' ),
      '''The Indian peafowl’s adaptations combine visual signaling, terrestrial mobility, and predator avoidance. The male’s train
         feathers with eye patterns are used in sexual selection, while their strong legs and clawed feet allow for efficient
         scratching and foraging. Camouflaged female plumage protects nesting sites, and the ability to fly short distances enables
         escape from predators. Their omnivorous diet allows them to exploit a wide range of food sources across forest edges and
         open areas, making them resilient to seasonal and habitat changes.'''.replace( '\n', ' ' ),
      '''Breeding occurs during the spring and early summer, when females lay 3–6 eggs in a ground nest lined with leaves and grass.
         Eggs incubate for 24–28 days, with chicks fully mobile shortly after hatching. Juveniles remain under maternal care for
         several months before becoming independent. Lifespan in the wild is 15–20 years, and in managed care, they can live up to
         25 years.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   # Malayan Woods Pavilion
   (
      'Asian Giant Millipede',
      'Archispirostreptus Giganteus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Asian giant millipede can be found in the bugs are of the Malayan Woods Pavilion, just before the clouded leopards.''',
      None,                                                          # Seasonal viewing tips
      '''The Asian giant millipede is one of the largest millipede species in the world, reaching lengths of 25–33 cm and diameters
         up to 2–3 cm. Its body is cylindrical and segmented, with more than 200 legs, two per segment, moving in a wave-like motion.
         Adults have a dark brown to black exoskeleton, shiny and slightly ridged, while juveniles are lighter and smaller. The head
         features short antennae used for sensory detection and navigating through leaf litter.'''.replace( '\n', ' ' ),
      '''Asian giant millipedes are native to Southeast Asian tropical forests, including Malaysia, Indonesia, and surrounding
         islands. They inhabit moist, leaf-littered forest floors, often hiding under logs, rocks, and decomposing plant material.
         They require high humidity and stable microclimates to maintain their soft exoskeleton and respiratory function.'''
         .replace( '\n', ' ' ),
      '''They are detritivores, feeding primarily on decaying plant material, fallen leaves, and rotting wood. By breaking down
         organic matter, they contribute to nutrient recycling and soil fertility, supporting plant growth in their forest habitats.'''
         .replace( '\n', ' ' ),
      '''Asian giant millipedes are solitary and slow-moving, relying on their armored exoskeleton for protection. When threatened,
         they can curl into a tight coil, protecting their softer underside and exposing only the hard exoskeleton. They are mostly
         nocturnal, emerging at night to feed and avoid daytime predators such as birds, small mammals, and reptiles.'''
         .replace( '\n', ' ' ),
      '''Their cylindrical, heavily segmented body and numerous legs allow efficient movement through leaf litter and decaying   
         vegetation. The exoskeleton provides physical protection, while curling behaviour deters predators. Millipedes also secrete
         a mild chemical defense, producing toxins or irritating fluids to ward off small predators. Their digestive system is
         adapted to process fibrous plant material, making them effective decomposers in forest ecosystems.'''.replace( '\n', ' ' ),
      '''Breeding occurs in moist conditions, with females laying dozens of eggs in soil or decaying organic matter. Juveniles hatch
         with fewer body segments and legs, which increase with each molt. Growth is slow, and adult millipedes can live 7–10 years,
         a relatively long lifespan for invertebrates.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Clouded Leopard',
      'Neofelis Nebulosa',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The clouded leopard habitat can be found towards the end of the Malayan Woods Pavilion. The clouded leopard is a nocturnal
         species, and thus your best chance of seeing them active is to visit their habitat earlier in the morning.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The clouded leopard is a medium-sized wild cat, typically weighing 11–23 kg, with a body length of 60–110 cm and a tail
         almost as long as the body (60–90 cm) for balance in trees. Its distinctive coat is light brown to gray, patterned with
         large, irregular, cloud-like spots outlined in black. The head is broad with a short muzzle, large eyes, and sharp canine
         teeth proportionally the longest of any living cat relative to skull size, adapted for securing prey.'''
         .replace( '\n', ' ' ),
      '''Clouded leopards are native to Southeast Asia, including Malaysia, Thailand, Borneo, and Sumatra, inhabiting tropical
         lowland and montane rainforests, often near rivers or streams. They are highly arboreal, relying on forest canopy
         connectivity for hunting, traveling, and avoiding larger predators. Dense forests with mature trees are critical for their
         survival.'''.replace( '\n', ' ' ),
      '''Clouded leopards are carnivorous apex predators, preying on birds, monkeys, small ungulates, and rodents. They use stealth
         and ambush tactics, often attacking from trees or dense vegetation. Their long canines and powerful bite allow them to
         tackle prey larger than themselves, while their agility permits hunting both on the ground and in the canopy.'''
         .replace( '\n', ' ' ),
      '''Primarily solitary, clouded leopards maintain territorial ranges, marked with scent and claw scratches. They are mostly
         nocturnal, active at night when hunting, and rest in trees or dense foliage during the day. Mating pairs form briefly, and
         females rear young alone. Vocalizations are limited, but they can produce growls, hisses, and purrs.'''.replace( '\n', ' ' ),
      '''Clouded leopards are superbly adapted for arboreal hunting and climbing. Their long tail aids balance, while short, stocky
         legs and large paws with sharp, retractable claws allow secure movement on branches. Flexible ankle joints let them climb
         down trees headfirst, a rare ability among cats. Camouflaged coat patterns enable stealth in the dappled forest light.
         Their elongated canines and strong jaws allow effective predation, and their solitary, territorial behaviour reduces
         competition for resources.'''.replace( '\n', ' ' ),
      '''Females reach sexual maturity around 2–3 years, with males maturing slightly later. After a 90–100 day gestation, females
         give birth to 1–5 cubs, which remain hidden in dense vegetation for several months. Cubs nurse for about 3–4 months,
         staying with the mother until around 12 months. Lifespan in the wild is approximately 11–14 years, with captive individuals
         living up to 17 years.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of clouded leopards, a male Mingma and a female Pavarti. Only one is ever on exhibit at a 
         time.'''.replace( '\n', ' ' )
   ),
   (
      'Gooty Sapphire Ornamental Tarantula',
      'Poecilotheria Metallica',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The gooty sapphire ornamental tarantula can be found in the bugs are of the Malayan Woods Pavilion, just before the clouded
         leopards.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Gooty Sapphire Ornamental Tarantula is a small-to-medium arboreal spider, with a leg span of about 12–15 cm. Its most
         striking feature is the iridescent metallic blue colouration covering much of its body and legs, with contrasting black and
         white patterns on the abdomen and leg joints. Females are larger and more robust than males, which are slimmer and slightly
         more agile. Its body is covered in fine hairs that serve as sensory organs.'''.replace( '\n', ' ' ),
      '''This tarantula is endemic to a tiny forest patch in Karnataka, India, inhabiting moist deciduous forests. It is strictly
         arboreal, living in tree hollows and under bark, rarely descending to the forest floor. Its restricted range makes it
         highly sensitive to habitat disturbance.'''.replace( '\n', ' ' ),
      '''The Gooty Sapphire is carnivorous, feeding on insects and other small invertebrates. It is a sit-and-wait predator,
         ambushing prey from tree cavities and using venom to immobilize captured insects before feeding. Its hunting strategy is
         highly efficient within its arboreal microhabitat.'''.replace( '\n', ' ' ),
      '''Primarily solitary, these tarantulas defend their retreats and show little social interaction except during mating. They
         are nocturnal, emerging at night to hunt. If threatened, they can deliver a venomous bite, though they are generally
         non-aggressive toward humans unless provoked.'''.replace( '\n', ' ' ),
      '''This species exhibits specialized adaptations for arboreal life. Its strong, spiny legs allow climbing and gripping smooth
         bark. Fine hairs on its body detect vibrations and air currents, alerting it to approaching prey or predators. Its venom
         efficiently immobilizes prey, while cryptic colouration within tree hollows provides camouflage from both predators and
         prey. Arboreal nesting behaviour minimizes competition and predation risk.'''.replace( '\n', ' ' ),
      '''Females lay 50–200 eggs in silk sacs within tree cavities. Spiderlings hatch and disperse shortly after molting, remaining
         independent from birth. Females have a lifespan of 7–12 years, while males live 3–4 years, dying shortly after reaching
         sexual maturity and mating.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Malayan Walking Stick',
      'Medauroidea Extradentata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Malayan walking stick can be found in the bugs are of the Malayan Woods Pavilion, just before the clouded leopards.'''
         .replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The Malayan walking stick is a long, slender insect that can reach 20–25 cm in length, with a stick-like body and legs that
         mimic twigs or small branches. Its colouration ranges from brown to green, often matching the surrounding vegetation
         perfectly. Adults have a flattened, elongated body and thin antennae that help detect nearby movement. Both sexes are
         similar, though females tend to be slightly larger and heavier.'''.replace( '\n', ' ' ),
      '''This species is native to tropical forests in Malaysia and surrounding Southeast Asian regions, inhabiting trees, shrubs,
         and understory vegetation. They rely on dense foliage for both camouflage and protection, rarely descending to the forest
         floor. Walking sticks are highly sensitive to habitat disturbance, as their survival depends on continuous forest cover.'''
         .replace( '\n', ' ' ),
      '''Malayan walking sticks are herbivorous, feeding primarily on leaves from various rainforest plants. They move slowly and
         feed quietly, minimizing detection by predators. Their selective feeding contributes to leaf turnover and plant health
         without causing significant damage to host vegetation.'''.replace( '\n', ' ' ),
      '''Walking sticks are solitary and cryptic, relying on their camouflage for protection rather than active defense. When
         threatened, they may remain motionless or sway gently to mimic a twig in the wind. They are mostly nocturnal feeders,
         hiding during daylight hours among leaves or branches.'''.replace( '\n', ' ' ),
      '''This species exhibits remarkable adaptations for camouflage and predator avoidance. Its elongated, twig-like body,
         colouration, and slow swaying motion make it nearly invisible in its natural environment. Its legs and antennae are adapted
         for grasping branches and sensing environmental cues. Walking sticks also rely on minimal movement to conserve energy and
         avoid detection.'''.replace( '\n', ' ' ),
      '''Females lay eggs that resemble seeds, dropping them to the forest floor or attaching them to leaves. Juveniles hatch fully
         formed, resembling miniature adults, and grow through successive molts. Adults typically live 1–2 years, with survival
         dependent on predator avoidance and habitat stability.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Malaysian Stick Insect Jungle Wood Nymph',
      'Heteropteryx Dilatata',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The Malaysian stick insect jungle wood nymph can be found in the bugs area of the Malayan Woods Pavilion, just before the
         clouded leopards.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''This species is one of the largest and heaviest stick insects in the world. Adult females are broad-bodied and usually
         leaf-green, with a chunky, thorn-lined body, stout legs, and shortened wings that do not support flight. Males are much
         slimmer, typically brown, and have longer wings than females. Both sexes have strong spines on the legs and body, giving
         them a heavily armoured appearance.'''.replace( '\n', ' ' ),
      '''Malaysian stick insect jungle wood nymphs are native to humid tropical forests of the Malay Peninsula and nearby parts of
         Southeast Asia, where they live among shrubs and low tree branches. They depend on warm, moist environments with dense
         vegetation that provides camouflage, food, and sheltered places to rest during the day.'''.replace( '\n', ' ' ),
      '''These insects are herbivores that feed on leaves and tender plant growth. They usually browse quietly at night, using
         strong jaws to chew foliage from host plants. In managed care, they are commonly offered a variety of leafy browse such as
         bramble, oak, or other suitable leaves.'''.replace( '\n', ' ' ),
      '''They are mostly nocturnal and spend daylight hours staying still to avoid detection. When threatened, they may sway, open
         their wings in a warning display, stridulate, or use their spiny hind legs defensively. Juveniles may rest in small
         groups, while older individuals are more often seen alone.'''.replace( '\n', ' ' ),
      '''Its bulky, leaf-like form and natural colour provide excellent camouflage among rainforest vegetation. Strong grasping legs
         help it cling to branches, while spines along the body and hind legs discourage predators. Females also have an adapted
         egg-laying structure that allows eggs to be placed into soil, protecting them during development.'''.replace( '\n', ' ' ),
      '''Females lay eggs individually in soil or loose substrate. Depending on temperature and humidity, eggs can take many months
         to hatch. Nymphs resemble tiny adults and grow through a series of molts before reaching maturity, with males maturing
         sooner than the larger females. Adults can live for well over a year in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Red-Tailed Green Ratsnake',
      'Gonyosoma Oxycephalum',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The red-tailed green ratsnake can be seen right before you exit the pavilion.''',
      None,                                                          # Seasonal viewing tips
      '''The Red-Tailed Green Ratsnake is a slender, non-venomous snake, typically reaching 2–2.5 meters in length, with some
         individuals growing up to 3 meters. Its body is bright green, providing camouflage among foliage, while the tail is
         reddish-orange, creating a distinctive contrast. Juveniles are lighter green with more pronounced patterning, which fades
         as they mature. It has a pointed head, large eyes, and smooth scales suited for climbing.'''.replace( '\n', ' ' ),
      '''This species is native to Southeast Asian tropical forests, including Malaysia, Indonesia, and Thailand. It is primarily
         arboreal, inhabiting trees, shrubs, and forest edges, often near water sources. Dense canopy and abundant branches provide
         shelter, hunting perches, and safety from terrestrial predators.'''.replace( '\n', ' ' ),
      '''Red-Tailed Green Ratsnakes are carnivorous, feeding mainly on small mammals, birds, lizards, and eggs. They are active
         hunters, using their climbing ability to access nests and ambush prey. Their slender, flexible body allows them to navigate
         branches and tight spaces with ease.'''.replace( '\n', ' ' ),
      '''This snake is mostly solitary, interacting with others primarily during mating. It is diurnal and crepuscular, active
         during the day and early evening. When threatened, it may inflate its body, hiss, or bite, relying on intimidation rather
         than venom. Arboreal habits allow it to avoid many ground-based predators.'''.replace( '\n', ' ' ),
      '''The Red-Tailed Green Ratsnake exhibits several adaptations for arboreal predation. Its bright green colouration provides
         excellent camouflage among leaves, while the red tail may distract predators or prey. Long, muscular body and prehensile
         movements enable climbing and striking from branches. Sharp, backward-curved teeth secure slippery prey, and keen eyesight
         aids in detecting movement in complex forest environments.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally in suitable climates, with females laying 6–15 eggs in hidden, humid spots. Eggs incubate for
         6–10 weeks, depending on temperature and humidity. Hatchlings are independent from birth. Lifespan in the wild is typically
         10–15 years, with slightly longer lifespans in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Wrinkled Hornbill',
      'Rhabdotorrhinus Corrugatus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The wrinkled hornbill can be found just beside the elevated orangutan viewing area. When you enter the pavilion head to the
         left and up the stairs. The hornbill can be found just past the orangutan viewing and on the right.'''.replace( '\n', ' ' ),
      None,                                                          # Seasonal viewing tips
      '''The wrinkled hornbill is a large, tropical bird, measuring 90–100 cm in length with a wingspan of 120–150 cm. It has
         predominantly black plumage, a white belly, and a striking curved bill topped with a prominent casque, which is ridged and
         brightly coloured in adults. The face around the eyes is yellow or reddish, and the eyes are surrounded by bare skin. Males
         and females are similar, though males usually have larger casques.'''.replace( '\n', ' ' ),
      '''Wrinkled hornbills are native to lowland and montane tropical forests in Southeast Asia, including Malaysia, Borneo, and
         Sumatra. They inhabit dense, old-growth forests and are often associated with fruiting trees and river valleys. They are
         arboreal and highly mobile, moving across forest canopies in search of food.'''.replace( '\n', ' ' ),
      '''Wrinkled hornbills are primarily frugivorous, feeding on figs, fruit, and berries, though they will occasionally eat
         insects, small reptiles, and bird eggs. They play a vital role as seed dispersers, helping maintain forest regeneration.
         Using their large, curved bills, they pluck and manipulate fruits efficiently while perched or flying between trees.'''
         .replace( '\n', ' ' ),
      '''Wrinkled hornbills are social birds, typically seen in pairs or small family groups. They are diurnal, spending most of the
         day foraging. During breeding, females seal themselves inside tree cavities to lay eggs, leaving a small opening through
         which the male passes food. This remarkable nesting strategy protects eggs and chicks from predators. Males exhibit strong
         parental care, feeding the female and chicks throughout the nesting period.'''.replace( '\n', ' ' ),
      '''The wrinkled hornbill has several adaptations for arboreal life and frugivory. Its large bill and casque allow efficient
         fruit handling and may aid in vocal resonance. Strong feet and zygodactyl toes provide excellent grip on branches, while
         powerful wings allow agile flight through dense canopy. Nesting in tree cavities with a sealed entrance minimizes
         predation, and its bright bill and casque play roles in species recognition and sexual signaling.'''.replace( '\n', ' ' ),
      '''Breeding occurs during periods of fruit abundance. Females lay 1–2 eggs in tree cavities, sealing themselves inside with a
         mud and feces barrier. The male provides all food until chicks are large enough for the female to break free and join him.
         Juveniles fledge after 10–12 weeks, remaining dependent on parents for several more weeks. Lifespan in the wild can reach
         30–35 years, with some individuals living longer in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Goat World
   (
      'Domestic Goat',
      'Capra Hircus',
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The domestic goats can be seen across from the Discovery Zone in the Goat World habitat.'''.replace( '\n', ' ' ),
      '''Goats can stand very cold temperatures, and are viewable outside year-round.''',
      '''The domestic goat is a small-to-medium herbivore, typically weighing 45–90 kg, depending on breed and sex. Males (bucks)
         are generally larger than females (does). Goats have cloven hooves, a short tail, and curved horns that vary in shape and
         size by breed. Their coat ranges from white, brown, black, or spotted, and some breeds have long hair or undercoats adapted
         for cold climates. Goats have rectangular pupils, which give them excellent peripheral vision for detecting predators.'''
         .replace( '\n', ' ' ),
      '''Domestic goats are highly adaptable and found worldwide in human-managed environments. They thrive in pastures, rocky
         hillsides, and forest edges, demonstrating agility and climbing ability. While they originally descend from the wild Bezoar
         goat of the Middle East, domestication has spread them globally.'''.replace( '\n', ' ' ),
      '''Goats are herbivorous browsers, eating leaves, shrubs, grasses, and woody plants. Unlike many grazers, goats prefer
         selective feeding and can consume vegetation that is rough or otherwise avoided by livestock. Their flexible diet allows
         them to survive in diverse habitats and marginal lands.'''.replace( '\n', ' ' ),
      '''Domestic goats are social animals, forming hierarchical herds. They communicate with bleats, body posture, and tail
         movements. Goats are curious, intelligent, and agile, capable of climbing steep terrain, jumping fences, and navigating
         rough ground. In managed settings, they are often friendly with humans, making them ideal for educational and petting
         areas.'''.replace( '\n', ' ' ),
      '''Goats possess several adaptations for agility and survival in variable habitats. Their cloven hooves provide grip on rocky
         or uneven terrain, and strong neck muscles allow browsing on shrubs and small trees. Rectangular pupils give wide-angle
         vision, helping detect predators while foraging. Their digestive system can process high-fiber plant material, allowing
         survival in areas with sparse vegetation.'''.replace( '\n', ' ' ),
      '''Goats reach sexual maturity around 5–12 months, depending on breed and environment. Females typically give birth to 1–3
         kids after a gestation of approximately 150 days. Kids are mobile within hours and begin grazing within a few weeks,
         though they continue nursing for several months. Lifespan ranges from 10–15 years, with some individuals living longer
         under care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),

   # Kids Zoo
   (
      'Abyssinian Ground Hornbill',
      'Bucorvus Abyssinicus',
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The Abyssinian ground hornbill can be found in the Kidz Zoo.''',
      '''Abyssinian ground hornbills are warm-weather birds which are usually only viewable during the warmest months of the year.'''
         .replace( '\n', ' ' ),
      '''The Abyssinian ground hornbill is a large, black bird standing 90–120 cm tall, with a wingspan of 1.2–1.8 m. Its face and
         throat are bare, red skin, contrasting with glossy black plumage. Both sexes look similar, though males have larger throat
         wattles. It has a large, downward-curved bill, used for foraging and displaying. The legs are long and powerful, adapted
         for walking and running across the savanna or forest edge.'''.replace( '\n', ' ' ),
      '''This hornbill is native to sub-Saharan Africa, inhabiting savannas, open woodlands, and grasslands. It prefers areas with
         scattered trees for nesting but spends most of its time on the ground searching for food. Its terrestrial habits make it
         unique among hornbills, which are often arboreal.'''.replace( '\n', ' ' ),
      '''Abyssinian ground hornbills are omnivorous, feeding on insects, reptiles, amphibians, small mammals, seeds, and fruits.
         They use their large bill to dig, flip over debris, and probe for prey. Their opportunistic feeding helps control insect
         and small vertebrate populations.'''.replace( '\n', ' ' ),
      '''These hornbills are social birds, usually seen in pairs or small family groups. They are mostly diurnal, walking long
         distances while foraging. They perform elaborate displays and vocalizations, including booming calls that carry across long
         distances. Breeding involves cooperative behaviours, with older offspring helping parents feed chicks.'''
         .replace( '\n', ' ' ),
      '''The Abyssinian ground hornbill is adapted for a terrestrial, open-habitat lifestyle. Its strong legs and large feet allow
         fast running and digging, while the large bill handles diverse prey and vegetation. Bare facial skin reduces overheating,
         and deep calls allow communication across distances. Its social structure improves survival, as group members share
         vigilance and chick-rearing duties.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally, with females laying 1–3 eggs in tree cavities. Only one chick usually survives, with parents
         and helper birds feeding it for several months. Sexual maturity is reached around 4–5 years, and individuals can live 50
         years or more in the wild and in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Common Raven',
      'Corvus Corax',
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The common raven can be found in the Kidz Zoo.''',
      '''The common raven is adapted to handle extremely cold temperatures and can be seen whenever the Kids Zoo is open.''',
      '''The Common Raven is a large passerine bird, measuring 54–67 cm in length with a wingspan of 115–150 cm. Its plumage is
         glossy black with a slightly iridescent sheen, and it has a thick, powerful bill and shaggy throat feathers. Both sexes are
         similar, though males are typically slightly larger. Its wedge-shaped tail and strong wings enable agile flight and
         soaring.'''.replace( '\n', ' ' ),
      '''Common ravens are highly adaptable and found across the Northern Hemisphere, including forests, mountains, deserts, tundra,
         and urban areas. They thrive in both wild and human-modified landscapes, demonstrating exceptional ecological versatility.'''
         .replace( '\n', ' ' ),
      '''Ravens are omnivorous and opportunistic feeders, consuming carrion, small mammals, insects, seeds, berries, and human food
         scraps. They are skilled problem-solvers and may use tools or group hunting strategies to access difficult-to-reach food.'''
         .replace( '\n', ' ' ),
      '''Ravens are social and intelligent birds, often seen in pairs or small groups. They display complex behaviours, including
         play, cooperative problem-solving, and vocal mimicry. They are territorial during breeding but may form large roosts in
         winter. Their vocalizations are highly varied, used for communication, coordination, and even warning conspecifics of
         danger.'''.replace( '\n', ' ' ),
      '''The Common Raven is adapted for intelligence and survival across diverse habitats. Strong wings and agile flight enable
         long-distance travel and predator avoidance. Its large, versatile bill allows manipulation of objects, feeding on diverse
         foods, and tool use. Keen eyesight and memory support complex navigation, problem-solving, and social interaction. Their
         vocal abilities enhance communication within pairs and groups.'''.replace( '\n', ' ' ),
      '''Breeding occurs in spring, with females laying 3–7 eggs in tree cavities, cliff ledges, or other sheltered sites. Both
         parents feed and protect the chicks until fledging at 5–6 weeks. Ravens reach sexual maturity at 3–4 years and can live
         10–15 years in the wild, with some individuals surviving over 20 years in captivity.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Eurasian Eagle Owl',
      'Bubo Bubo',
      -25,                                                           # Minimum temperature (only for animals with outdoor viewing)
      '''The Eurasian eagle owl can be found in the Kidz Zoo.''',
      '''The Eurasian eagle owl is adapted to handle very cold temperatures and can be seen whenever the Kids Zoo is open.''',
      '''The Eurasian Eagle Owl is one of the largest owl species in the world, with a wingspan of 160–188 cm and a body length of
         60–75 cm. Adults weigh 2–4 kg, with females slightly larger than males. They have prominent ear tufts, large orange eyes,
         and a broad, heavily feathered body that aids in silent flight. Plumage is mottled brown, black, and cream, providing
         excellent camouflage against rocks and forested habitats.'''.replace( '\n', ' ' ),
      '''This owl is native to Europe and Asia, inhabiting forests, rocky cliffs, and open landscapes. They prefer areas with ample
         cover for nesting and perching and open spaces for hunting. Their range spans from Scandinavia and Russia to the Middle
         East and parts of Central Asia.'''.replace( '\n', ' ' ),
      '''Eurasian Eagle Owls are apex nocturnal predators, feeding on mammals, birds, amphibians, and occasionally fish. They use
         keen eyesight and silent flight to ambush prey, often striking from a perch. Powerful talons and a strong beak allow them
         to capture and kill prey efficiently.'''.replace( '\n', ' ' ),
      '''These owls are mostly solitary, maintaining large territories. They are nocturnal hunters but may be active at dusk or
         dawn. Vocalizations include deep, resonant hoots used for territory defense and mate communication. Pairs often maintain
         long-term bonds, and both parents care for chicks during the nesting period.'''.replace( '\n', ' ' ),
      '''The Eurasian Eagle Owl exhibits adaptations for nocturnal predation. Silent flight is enabled by specialized fringe
         feathers on the wings. Large eyes enhance low-light vision, while acute hearing allows detection of prey even under snow or
         vegetation. Powerful talons and a strong beak ensure effective hunting. Camouflaged plumage and stealthy behaviour minimize
         detection by both prey and potential threats.'''.replace( '\n', ' ' ),
      '''Breeding occurs in late winter to early spring. Females lay 2–4 eggs in rock crevices, tree cavities, or cliff ledges,
         incubated for 28–36 days. Chicks fledge after 6–7 weeks but remain dependent on parents for several months. Sexual maturity
         is reached at 2–3 years, and lifespan can reach 20 years in the wild, with longer lifespans in managed care.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Guinea Pig',
      'Cavia Porcellus',
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      '''The guinea pig can be found in the Kidz Zoo.''',
      None,                                                          # Seasonal viewing tips
      '''The guinea pig is a small, stocky rodent, typically weighing 700–1,200 grams and measuring 20–25 cm in length. They have
         short legs, rounded bodies, and no tail, with a variety of fur colours and patterns including brown, black, white, and
         spotted combinations. Their ears are small and rounded, and their eyes are large and dark, adapted for wide-field vision to
         detect predators.'''.replace( '\n', ' ' ),
      '''Originally domesticated from wild cavies in South America, guinea pigs now live worldwide in human-managed habitats. In the
         wild, ancestors inhabited grasslands, rocky outcrops, and shrublands, sheltering in burrows or crevices. Domestic guinea
         pigs require safe, enclosed areas with hiding spaces, fresh water, and access to vegetation.'''.replace( '\n', ' ' ),
      '''Guinea pigs are herbivorous, feeding on grasses, leafy vegetables, hay, and fruits. They have continuously growing teeth
         and require high-fiber diets to maintain dental health. Their selective grazing and nibbling behaviour make them important
         analogs for teaching about herbivore feeding strategies.'''.replace( '\n', ' ' ),
      '''Guinea pigs are social animals, often forming small groups in the wild or domestication settings. They communicate through
         vocalizations, such as squeaks, purrs, and whistles, to express contentment, alarm, or curiosity. They are mostly diurnal,
         active during daylight hours, and use hiding and freezing behaviours to avoid predators.'''.replace( '\n', ' ' ),
      '''Guinea pigs are adapted for social living and herbivory. Their strong incisors continuously grow to handle fibrous plant
         material. Acute hearing and wide-field vision help detect threats, while their social structures improve survival and
         reduce stress. Their small size and agility allow them to quickly take cover in dense vegetation or burrows.'''
         .replace( '\n', ' ' ),
      '''Females reach sexual maturity at 3–4 weeks, and males at 6–8 weeks. Gestation lasts about 59–72 days, producing 1–6
         well-developed pups, which are precocial — born with fur, open eyes, and able to move and feed independently within hours.
         Guinea pigs can live 4–8 years, with some reaching up to 10 years in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Harris\'s Hawk',
      'Parabuteo Unicinctus',
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      '''The Harris's hawk can be found in the Kidz Zoo.''',
      '''The Harris's hawk can handle moderate temperatures, and should be visible when the Kids Zoo is open.''',
      '''Harris’s hawks are medium-large raptors, measuring 46–76 cm in length with a wingspan of 1.1–1.2 m and weighing 0.9–1.5 kg.
         They have dark brown plumage, with chestnut-red shoulders, thighs, and wing linings, and a white-tipped tail. Their hooked
         beak and sharp talons are adapted for catching and holding prey. Both sexes look similar, though females are generally
         larger.'''.replace( '\n', ' ' ),
      '''Native to the southwestern United States, Central, and South America, Harris’s hawks inhabit deserts, scrublands, savannas,
         and woodland edges. They are highly adaptable, often nesting in trees or tall cacti. They rely on open areas for hunting
         but need perches for observation and launching attacks.'''.replace( '\n', ' ' ),
      '''Harris’s hawks are carnivorous, feeding primarily on small mammals, birds, and reptiles. They are famous for cooperative
         hunting, often working in groups of 2–6 individuals to flush and capture prey. This strategy allows them to take down
         larger prey than they could individually.'''.replace( '\n', ' ' ),
      '''Unlike most raptors, Harris’s hawks are social and cooperative, living in family groups. They use complex communication,
         including calls, postures, and aerial displays. Groups share responsibilities for hunting, territory defense, and raising
         young. They are diurnal hunters, active during the day.'''.replace( '\n', ' ' ),
      '''Harris’s hawks are adapted for cooperative hunting and versatility. Their sharp talons, hooked beak, and keen eyesight
         allow effective capture of prey. Group hunting reduces energy expenditure and increases success rates. Strong wings and
         maneuverable flight enable agile pursuit of prey through open terrain and among obstacles. Their social behaviour increases
         survival and reproductive success.'''.replace( '\n', ' ' ),
      '''Breeding occurs seasonally. Females lay 2–4 eggs in nests built in trees or cacti. Both parents, and sometimes helpers,
         feed and protect the chicks. Juveniles fledge after 6–7 weeks but may remain with the group to learn cooperative hunting.
         Harris’s hawks can live 10–15 years in the wild and up to 20 years in managed care.'''.replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   ),
   (
      'Rabbit',
      'Oryctolagus Cuniculus',
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      '''The rabbits can be found in the Kidz Zoo.''',
      '''Rabbits can handle colder temperatures, and should be visible when the Kids Zoo is open.''',
      '''Rabbits are small mammals, typically weighing 1–2.5 kg, with body lengths of 30–50 cm. They have long ears, large eyes on
         the sides of the head for wide-field vision, strong hind legs, and a short, fluffy tail. Their fur varies in colour
         depending on breed or wild population, commonly ranging from brown, gray, white, or spotted patterns.'''
         .replace( '\n', ' ' ),
      '''Domestic rabbits descend from wild European rabbits and now live worldwide in managed habitats, farms, and homes. Wild
         ancestors inhabited grasslands, scrublands, and woodland edges, often digging burrows for shelter. Rabbits require areas
         for digging, hiding, and foraging, even in captive settings.'''.replace( '\n', ' ' ),
      '''Rabbits are herbivores, feeding primarily on grass, leafy greens, hay, and vegetables. They have continuously growing
         teeth and require a high-fiber diet for proper digestion and dental health. Rabbits are also coprophagous, consuming some
         of their soft fecal pellets to extract additional nutrients.'''.replace( '\n', ' ' ),
      '''Rabbits are social animals, forming groups in the wild for protection and communication. They are mostly crepuscular,
         active at dawn and dusk. They communicate through vocalizations, body posture, and thumping their hind legs to signal
         danger. Burrowing and hiding behaviour help them avoid predators.'''.replace( '\n', ' ' ),
      '''Rabbits are adapted for speed, vigilance, and herbivory. Strong hind legs allow rapid hopping and sudden escapes, while
         wide-field vision and acute hearing detect predators. Teeth and digestive adaptations support a fibrous plant diet, and
         social behaviours improve survival by enabling group vigilance.'''.replace( '\n', ' ' ),
      '''Rabbits reach sexual maturity around 3–6 months, depending on breed. Females (does) give birth to 4–12 kits per litter
         after a gestation of 28–31 days. Young are born altricial, with eyes closed and minimal fur, relying entirely on the
         mother. Domestic rabbits can live 5–10 years, while wild rabbits often have shorter lifespans due to predation.'''
         .replace( '\n', ' ' ),
      None                                                           # Animals at the zoo
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Animal (
                              SPECIES,
                              LATIN_NAME,
                              MIN_TEMPERATURE,
                              GENERAL_VIEWING_TIPS,
                              SEASONAL_VIEWING_TIPS,
                              IDENTIFICATION,
                              HABITAT_AND_RANGE,
                              DIET_AND_FEEDING,
                              BEHAVIOUR_AND_SOCIAL_LIFE,
                              ADAPTATIONS,
                              REPRODUCTION_AND_LIFE_CYCLE,
                              ANIMALS_AT_THE_ZOO
                           ) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', animals )
