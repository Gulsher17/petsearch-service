// /mongo-seed/init-pets.js
db = db.getSiblingDB('pet_database');

db.pets.insertMany([
  {
    name: "Mochi",
    breed: "Siamese",
    description: "A calm, gentle Siamese kitten who enjoys quiet naps and soft playtime.",
    age: 1,
    gender: "Female",
    temperament: ["calm", "affectionate", "gentle"],
    specialNeeds: [],
    energyLevel: "Low",
    careInstructions: "Indoor home preferred. Needs soft bedding and soft food.",
    location: "Toronto",
    listingType: "shelter",
    status: "Available",
    tags: ["kitten", "quiet", "loving", "indoor"]
  },
  {
    name: "Buddy",
    breed: "Golden Retriever",
    description: "A friendly and loyal dog who loves fetch, long walks and enjoys being around kids.",
    age: 3,
    gender: "Male",
    temperament: ["friendly", "energetic", "good-with-kids"],
    specialNeeds: [],
    energyLevel: "High",
    careInstructions: "Daily outdoor exercise and regular brushing.",
    location: "Mississauga",
    listingType: "shelter",
    status: "Available",
    tags: ["family", "active", "good-with-kids", "outgoing"]
  },
  {
    name: "Max",
    breed: "Bulldog",
    description: "Strong but calm dog who enjoys indoor relaxation and gentle attention.",
    age: 4,
    gender: "Male",
    temperament: ["loyal", "calm", "independent"],
    specialNeeds: ["Short walks only"],
    energyLevel: "Low",
    careInstructions: "Limit exercise, keep cool, avoid overheating.",
    location: "Brampton",
    listingType: "shelter",
    status: "Available",
    tags: ["lazy", "cuddly", "relaxed"]
  },
  {
    name: "Lucy",
    breed: "Poodle",
    description: "Smart, loving, and obedient companion. Great with families and learns commands quickly.",
    age: 2,
    gender: "Female",
    temperament: ["intelligent", "playful", "alert"],
    specialNeeds: [],
    energyLevel: "Medium",
    careInstructions: "Mental stimulation and weekly grooming required.",
    location: "Oakville",
    listingType: "shelter",
    status: "Available",
    tags: ["small", "smart", "trainable", "friendly"]
  },
  {
    name: "Shadow",
    breed: "Mixed Breed",
    description: "Loyal and protective dog with a calm nature, great for apartment-friendly lifestyle.",
    age: 5,
    gender: "Male",
    temperament: ["calm", "loyal", "obedient"],
    specialNeeds: [],
    energyLevel: "Medium",
    careInstructions: "Daily walks and patient handling.",
    location: "Hamilton",
    listingType: "personal",
    isPersonalListing: true,
    status: "Available",
    tags: ["loyal", "protective", "calm"]
  }
]);

print("Seeded enhanced pets into pet_database.pets collection");
