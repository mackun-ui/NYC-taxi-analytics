// ==========================================
// NYC TAXI ANALYTICS - MAIN JAVASCRIPT
// ==========================================

// === CONFIGURATION ===
const API_BASE_URL = 'http://localhost:5000/api'; // Backend API endpoint (adjust when backend is ready)

// === STATE MANAGEMENT ===
let tripData = [];
let filteredData = [];
let charts = {};

// === INITIALIZE APP ===
document.addEventListener('DOMContentLoaded', () => {
    console.log('NYC Taxi Analytics - Initializing...');
    
    // Initialize filter event listeners
    initializeFilters();
    
    // Load initial data
    loadData();
});

// === DATA LOADING ===
async function loadData() {
    try {
        // TODO: Replace with actual API call when backend is ready
        // const response = await fetch(`${API_BASE_URL}/trips`);
        // tripData = await response.json();
        
        // For now, use mock data for testing
        tripData = generateMockData();
        filteredData = [...tripData];
        
        // Update UI with data
        updateStatistics();
        initializeCharts();
        updateTable();
        
        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// === MOCK DATA GENERATOR (temporary - remove when backend is ready) ===
function generateMockData() {
    const boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'];
    const locations = ['Times Square', 'Central Park', 'JFK Airport', 'Brooklyn Bridge', 'Flushing', 'Port Richmond', 'Yankee Stadium'];
    const payments = ['Credit Card', 'Cash', 'Mobile'];
    
    const mockData = [];
    const now = new Date();
    
    for (let i = 0; i < 100; i++) {
        const distance = (Math.random() * 45 + 0.5).toFixed(2);
        const fare = (parseFloat(distance) * 3.5 + Math.random() * 10 + 5).toFixed(2);
        const tip = (parseFloat(fare) * 0.15 + Math.random() * 5).toFixed(2);
        
        mockData.push({
            id: `NYC-${String(i + 1000).padStart(6, '0')}`,
            pickupTime: new Date(now - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
            pickupLocation: locations[Math.floor(Math.random() * locations.length)],
            dropoffLocation: locations[Math.floor(Math.random() * locations.length)],
            borough: boroughs[Math.floor(Math.random() * boroughs.length)],
            distance: parseFloat(distance),
            fare: parseFloat(fare),
            tip: parseFloat(tip),
            total: (parseFloat(fare) + parseFloat(tip)).toFixed(2),
            payment: payments[Math.floor(Math.random() * payments.length)],
            hour: Math.floor(Math.random() * 24)
        });
    }
    
    return mockData;
}

// === UPDATE STATISTICS ===
function updateStatistics() {
    const totalTrips = filteredData.length;
    const avgFare = (filteredData.reduce((sum, trip) => sum + trip.fare, 0) / totalTrips).toFixed(2);
    const avgDistance = (filteredData.reduce((sum, trip) => sum + trip.distance, 0) / totalTrips).toFixed(2);
    const totalRevenue = filteredData.reduce((sum, trip) => sum + parseFloat(trip.total), 0).toFixed(0);
    
    document.getElementById('total-trips').textContent = totalTrips.toLocaleString();
    document.getElementById('avg-fare').textContent = `$${avgFare}`;
    document.getElementById('avg-distance').textContent = `${avgDistance} mi`;
    document.getElementById('total-revenue').textContent = `$${parseInt(totalRevenue).toLocaleString()}`;
}

// === INITIALIZE FILTERS ===
function initializeFilters() {
    // Range sliders
    const distanceSlider = document.getElementById('distance-range');
    const fareSlider = document.getElementById('fare-range');
    
    distanceSlider.addEventListener('input', (e) => {
        document.getElementById('distance-value').textContent = `0 - ${e.target.value} mi`;
    });
    
    fareSlider.addEventListener('input', (e) => {
        document.getElementById('fare-value').textContent = `$0 - $${e.target.value}`;
    });
    
    // Apply filters button
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
    
    // Reset filters button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

// === APPLY FILTERS ===
function applyFilters() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const borough = document.getElementById('borough').value;
    const maxDistance = parseFloat(document.getElementById('distance-range').value);
    const maxFare = parseFloat(document.getElementById('fare-range').value);
    
    filteredData = tripData.filter(trip => {
        // Date filter
        if (startDate && new Date(trip.pickupTime) < new Date(startDate)) return false;
        if (endDate && new Date(trip.pickupTime) > new Date(endDate)) return false;
        
        // Borough filter
        if (borough !== 'all' && trip.borough.toLowerCase() !== borough.toLowerCase()) return false;
        
        // Distance filter
        if (trip.distance > maxDistance) return false;
        
        // Fare filter
        if (trip.fare > maxFare) return false;
        
        return true;
    });
    
    // Update UI
    updateStatistics();
    updateCharts();
    updateTable();
    
    console.log(`Filters applied: ${filteredData.length} trips found`);
}

// === RESET FILTERS ===
function resetFilters() {
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    document.getElementById('borough').value = 'all';
    document.getElementById('distance-range').value = 50;
    document.getElementById('fare-range').value = 200;
    document.getElementById('distance-value').textContent = '0 - 50 mi';
    document.getElementById('fare-value').textContent = '$0 - $200';
    
    filteredData = [...tripData];
    
    updateStatistics();
    updateCharts();
    updateTable();
    
    console.log('Filters reset');
}

// === UPDATE TABLE ===
function updateTable() {
    const tbody = document.getElementById('trips-table-body');
    tbody.innerHTML = '';
    
    // Show first 10 trips
    const displayTrips = filteredData.slice(0, 10);
    
    displayTrips.forEach(trip => {
        const row = document.createElement('tr');
        
        const pickupDate = new Date(trip.pickupTime);
        const formattedDate = `${pickupDate.toLocaleDateString()} ${pickupDate.toLocaleTimeString()}`;
        
        row.innerHTML = `
            <td>${trip.id}</td>
            <td>${formattedDate}</td>
            <td>${trip.pickupLocation}</td>
            <td> ${trip.dropoffLocation}</td>
            <td>${trip.distance} mi</td>
            <td>$${trip.fare.toFixed(2)}</td>
            <td>$${trip.tip.toFixed(2)}</td>
            <td><strong>$${trip.total}</strong></td>
            <td><span style="color: ${trip.payment === 'Cash' ? '#fbbf24' : trip.payment === 'Credit Card' ? '#1e40af' : '#10b981'}">${trip.payment}</span></td>
        `;
        
        tbody.appendChild(row);
    });
}

console.log('App.js loaded successfully');
