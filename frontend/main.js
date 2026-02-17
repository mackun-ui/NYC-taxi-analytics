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
        const response = await fetch(`${API_BASE_URL}/trips`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        tripData = await response.json();
        filteredData = [...tripData];
        
        // Update UI with data
        updateStatistics();
        initializeCharts();
        updateTable();
        
        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Failed to load data. Please ensure the backend server is running.');
    }
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

// === INITIALIZE CHARTS ===
function initializeCharts() {
    // Daily Trip Volume Chart
    charts.dailyTrips = new Chart(document.getElementById('daily-trips-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Trips',
                data: [],
                borderColor: '#1e40af',
                backgroundColor: 'rgba(30, 64, 175, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Revenue by Borough Chart
    charts.revenueBorough = new Chart(document.getElementById('revenue-borough-chart'), {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Revenue',
                data: [],
                backgroundColor: '#fbbf24'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Trip Distribution by Borough Chart
    charts.tripDistribution = new Chart(document.getElementById('trip-distribution-chart'), {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['#1e40af', '#7c3aed', '#ef4444', '#10b981', '#fbbf24']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
    
    // Average Fare by Hour Chart
    charts.fareHour = new Chart(document.getElementById('fare-hour-chart'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Fare',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Distance Distribution Chart
    charts.distanceDistribution = new Chart(document.getElementById('distance-distribution-chart'), {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Count',
                data: [],
                backgroundColor: '#1e40af'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Payment Methods Chart
    charts.paymentMethods = new Chart(document.getElementById('payment-methods-chart'), {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['#1e40af', '#fbbf24', '#10b981']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
    
    // Initial chart update
    updateCharts();
}

// === UPDATE CHARTS ===
function updateCharts() {
    // Daily Trip Volume
    const dailyData = calculateDailyTrips(filteredData);
    charts.dailyTrips.data.labels = dailyData.labels;
    charts.dailyTrips.data.datasets[0].data = dailyData.values;
    charts.dailyTrips.update();
    
    // Revenue by Borough
    const revenueData = calculateRevenueByBorough(filteredData);
    charts.revenueBorough.data.labels = revenueData.labels;
    charts.revenueBorough.data.datasets[0].data = revenueData.values;
    charts.revenueBorough.update();
    
    // Trip Distribution by Borough
    const tripDistData = calculateTripDistribution(filteredData);
    charts.tripDistribution.data.labels = tripDistData.labels;
    charts.tripDistribution.data.datasets[0].data = tripDistData.values;
    charts.tripDistribution.update();
    
    // Average Fare by Hour
    const fareHourData = calculateFareByHour(filteredData);
    charts.fareHour.data.labels = fareHourData.labels;
    charts.fareHour.data.datasets[0].data = fareHourData.values;
    charts.fareHour.update();
    
    // Distance Distribution
    const distanceData = calculateDistanceDistribution(filteredData);
    charts.distanceDistribution.data.labels = distanceData.labels;
    charts.distanceDistribution.data.datasets[0].data = distanceData.values;
    charts.distanceDistribution.update();
    
    // Payment Methods
    const paymentData = calculatePaymentMethods(filteredData);
    charts.paymentMethods.data.labels = paymentData.labels;
    charts.paymentMethods.data.datasets[0].data = paymentData.values;
    charts.paymentMethods.update();
}

// === DATA CALCULATION FUNCTIONS ===
function calculateDailyTrips(data) {
    const dailyCounts = {};
    
    data.forEach(trip => {
        const date = new Date(trip.pickupTime).toLocaleDateString();
        dailyCounts[date] = (dailyCounts[date] || 0) + 1;
    });
    
    const sortedDates = Object.keys(dailyCounts).sort((a, b) => new Date(a) - new Date(b));
    
    return {
        labels: sortedDates,
        values: sortedDates.map(date => dailyCounts[date])
    };
}

function calculateRevenueByBorough(data) {
    const boroughRevenue = {};
    
    data.forEach(trip => {
        boroughRevenue[trip.borough] = (boroughRevenue[trip.borough] || 0) + parseFloat(trip.total);
    });
    
    return {
        labels: Object.keys(boroughRevenue),
        values: Object.values(boroughRevenue).map(val => val.toFixed(0))
    };
}

function calculateTripDistribution(data) {
    const boroughCounts = {};
    
    data.forEach(trip => {
        boroughCounts[trip.borough] = (boroughCounts[trip.borough] || 0) + 1;
    });
    
    return {
        labels: Object.keys(boroughCounts),
        values: Object.values(boroughCounts)
    };
}

function calculateFareByHour(data) {
    const hourlyFares = {};
    const hourlyCounts = {};
    
    data.forEach(trip => {
        const hour = trip.hour;
        hourlyFares[hour] = (hourlyFares[hour] || 0) + trip.fare;
        hourlyCounts[hour] = (hourlyCounts[hour] || 0) + 1;
    });
    
    const hours = Array.from({length: 24}, (_, i) => i);
    const avgFares = hours.map(hour => 
        hourlyCounts[hour] ? (hourlyFares[hour] / hourlyCounts[hour]).toFixed(2) : 0
    );
    
    return {
        labels: hours.map(h => `${String(h).padStart(2, '0')}:00`),
        values: avgFares
    };
}

function calculateDistanceDistribution(data) {
    const ranges = ['0-2 mi', '2-5 mi', '5-10 mi', '10-20 mi', '20+ mi'];
    const counts = [0, 0, 0, 0, 0];
    
    data.forEach(trip => {
        const dist = trip.distance;
        if (dist < 2) counts[0]++;
        else if (dist < 5) counts[1]++;
        else if (dist < 10) counts[2]++;
        else if (dist < 20) counts[3]++;
        else counts[4]++;
    });
    
    return {
        labels: ranges,
        values: counts
    };
}

function calculatePaymentMethods(data) {
    const paymentCounts = {};
    
    data.forEach(trip => {
        paymentCounts[trip.payment] = (paymentCounts[trip.payment] || 0) + 1;
    });
    
    return {
        labels: Object.keys(paymentCounts),
        values: Object.values(paymentCounts)
    };
}

console.log('App.js loaded successfully');
