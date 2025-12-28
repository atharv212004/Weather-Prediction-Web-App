document.addEventListener('DOMContentLoaded', function(){
  const themeToggle = document.getElementById('themeToggle');
  function setTheme(isDark){
    if(isDark) document.body.classList.add('dark');
    else document.body.classList.remove('dark');
    if(themeToggle) {
      const icon = themeToggle.querySelector('i');
      if(icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
      }
    }
    localStorage.setItem('isDark', isDark ? '1' : '0');
  }
  const saved = localStorage.getItem('isDark') === '1';
  setTheme(saved);
  if(themeToggle) themeToggle.addEventListener('click', ()=> setTheme(!document.body.classList.contains('dark')));

  // Toast notification helper
  function showToast(message, type = 'info'){
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;min-width:300px;border-radius:10px;';
    toast.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(toast);
    setTimeout(()=>{ 
      toast.style.transition = 'opacity 0.3s ease';
      toast.style.opacity = '0';
      setTimeout(()=>toast.remove(), 300);
    }, 4000);
  }

  // Location autocomplete: when user types a place, fetch lat/lon from Nominatim
  const locationInput = document.getElementById('location');
  if(locationInput){
    let autocompleteTimeout;
    locationInput.addEventListener('input', ()=>{
      clearTimeout(autocompleteTimeout);
      const query = locationInput.value.trim();
      if(query.length < 2) return; // wait for at least 2 chars
      
      autocompleteTimeout = setTimeout(async ()=>{
        try{
          const resp = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1&timeout=5`, {
            headers: {
              'User-Agent': 'WeatherML-App/1.0'
            }
          });
          
          if(!resp.ok) {
            console.log('Nominatim API error:', resp.status);
            return;
          }
          
          const results = await resp.json();
          if(results && results.length > 0){
            const result = results[0];
            const lat = parseFloat(result.lat);
            const lon = parseFloat(result.lon);
            
            // Validate coordinates
            if(lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180) {
              document.getElementById('lat').value = lat.toFixed(4);
              document.getElementById('lon').value = lon.toFixed(4);
              showToast(`✅ Location detected: ${result.display_name.split(',')[0]}`, 'success');
            }
          } else {
            // No results found - user can still type or use Detect button
            showToast(`⚠️ Location not found. Try another city name or use Detect button`, 'warning');
          }
        }catch(e){
          console.log('Geolocation fetch error:', e.message);
          // Silent fail - user can still submit or use Detect button
        }
      }, 1000); // wait 1000ms after user stops typing
    });
  }

  // Use my location button - browser geolocation API
  const detectLocationBtn = document.getElementById('detectLocationBtn');
  if(detectLocationBtn){
    detectLocationBtn.addEventListener('click', ()=>{
      if(!navigator.geolocation){
        showToast('❌ Geolocation is not supported by your browser', 'danger');
        return;
      }
      
      detectLocationBtn.disabled = true;
      const originalHTML = detectLocationBtn.innerHTML;
      detectLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Detecting...';
      
      // Set a timeout to reset button if geolocation takes too long
      const resetTimeout = setTimeout(() => {
        detectLocationBtn.disabled = false;
        detectLocationBtn.innerHTML = originalHTML;
        showToast('⏱️ Location detection is taking longer than expected. Please try again.', 'warning');
      }, 30000); // 30 second fallback timeout
      
      navigator.geolocation.getCurrentPosition(
        async (position)=>{
          clearTimeout(resetTimeout);
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          
          // Set coordinates immediately
          document.getElementById('lat').value = lat.toFixed(4);
          document.getElementById('lon').value = lon.toFixed(4);
          
          // Update button to show we're getting city name
          detectLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting city name...';
          
          // Reverse geocode to get city name (with timeout)
          const geocodeTimeout = setTimeout(() => {
            // If reverse geocoding takes too long, just use coordinates
            document.getElementById('location').value = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
            showToast(`✅ Location detected: ${lat.toFixed(4)}, ${lon.toFixed(4)}`, 'success');
            detectLocationBtn.disabled = false;
            detectLocationBtn.innerHTML = originalHTML;
          }, 5000); // 5 second timeout for reverse geocoding
          
          try{
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            const resp = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1`, {
              headers: {
                'User-Agent': 'WeatherML-App/1.0'
              },
              signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            clearTimeout(geocodeTimeout);
            
            if(resp.ok){
              const data = await resp.json();
              const cityName = data.address.city || data.address.town || data.address.village || data.address.county || data.address.municipality || data.display_name.split(',')[0];
              document.getElementById('location').value = cityName;
              showToast(`✅ Location detected: ${cityName}`, 'success');
            } else {
              clearTimeout(geocodeTimeout);
              document.getElementById('location').value = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
              showToast(`✅ Location detected: ${lat.toFixed(4)}, ${lon.toFixed(4)}`, 'success');
            }
          } catch(e){
            clearTimeout(geocodeTimeout);
            if(e.name !== 'AbortError'){
              console.log('Reverse geocoding error:', e.message);
            }
            document.getElementById('location').value = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
            showToast(`✅ Location detected: ${lat.toFixed(4)}, ${lon.toFixed(4)}`, 'success');
          }
          
          detectLocationBtn.disabled = false;
          detectLocationBtn.innerHTML = originalHTML;
        },
        (error)=>{
          clearTimeout(resetTimeout);
          detectLocationBtn.disabled = false;
          detectLocationBtn.innerHTML = originalHTML;
          
          let errorMsg = '❌ Failed to get location';
          if(error.code === 1){
            errorMsg = '❌ Location access denied. Please enable location permissions in your browser settings.';
          } else if(error.code === 2){
            errorMsg = '❌ Location unavailable. Please check your GPS/network connection and try again.';
          } else if(error.code === 3){
            errorMsg = '⏱️ Location request timed out. Please try again or enter location manually.';
          }
          showToast(errorMsg, 'danger');
        },
        {
          enableHighAccuracy: false, // Changed to false for faster response
          timeout: 20000, // Increased to 20 seconds
          maximumAge: 60000 // Accept cached location up to 1 minute old
        }
      );
    });
  }

  // Form validation - extends to 10 years
  const form = document.getElementById('predictForm');
  const dateInput = document.getElementById('date');
  if(dateInput){
    // Set max date to allow future predictions (up to 10 years = 3650 days ahead)
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 3650);
    dateInput.max = maxDate.toISOString().split('T')[0];
    // Set min date to historical data
    dateInput.min = '1980-01-01';
  }

  if(form){
    form.addEventListener('submit', (e)=>{
      const date = document.getElementById('date').value.trim();
      const loc = document.getElementById('location').value.trim();
      const lat = document.getElementById('lat').value.trim();
      const lon = document.getElementById('lon').value.trim();
      
      // Validation checks
      if(!date){
        e.preventDefault(); 
        showToast('📅 Please select a date', 'warning'); 
        return;
      }
      
      // Location is REQUIRED
      if(!loc){
        e.preventDefault(); 
        showToast('📍 Please enter a location or use the "Detect" button', 'warning'); 
        return;
      }
      
      // Both lat and lon must be set
      if(!lat || !lon){
        e.preventDefault(); 
        showToast('🗺️ Location coordinates not found. Try a different city name or use "Detect" button', 'warning'); 
        return;
      }
      
      // Latitude range check
      if(lat){
        const lf = parseFloat(lat);
        if(isNaN(lf)){ 
          e.preventDefault(); 
          showToast('❌ Latitude must be a valid number', 'danger'); 
          return; 
        }
        if(lf < -90 || lf > 90){ 
          e.preventDefault(); 
          showToast('❌ Latitude must be between -90 and 90', 'danger'); 
          return; 
        }
      }
      
      // Longitude range check
      if(lon){
        const lof = parseFloat(lon);
        if(isNaN(lof)){ 
          e.preventDefault(); 
          showToast('❌ Longitude must be a valid number', 'danger'); 
          return; 
        }
        if(lof < -180 || lof > 180){ 
          e.preventDefault(); 
          showToast('❌ Longitude must be between -180 and 180', 'danger'); 
          return; 
        }
      }
    });
  }

  // Quick date buttons and clear
  const todayBtn = document.getElementById('todayBtn');
  const tomorrowBtn = document.getElementById('tomorrowBtn');
  const next7Btn = document.getElementById('next7Btn');
  const yesterdayBtn = document.getElementById('yesterdayBtn');
  const clearBtn = document.getElementById('clearBtn');
  
  function setDateValue(daysOffset){
    const d = new Date();
    d.setDate(d.getDate() + daysOffset);
    document.getElementById('date').valueAsDate = d;
  }

  if(todayBtn){
    todayBtn.addEventListener('click', ()=>{ setDateValue(0); });
  }
  if(tomorrowBtn){
    tomorrowBtn.addEventListener('click', ()=>{ setDateValue(1); });
  }
  if(next7Btn){
    next7Btn.addEventListener('click', ()=>{ setDateValue(7); });
  }
  if(yesterdayBtn){
    yesterdayBtn.addEventListener('click', ()=>{ setDateValue(-1); });
  }
  if(clearBtn){
    clearBtn.addEventListener('click', ()=>{
      document.getElementById('location').value = '';
      document.getElementById('lat').value = '';
      document.getElementById('lon').value = '';
      document.getElementById('date').value = '';
    });
  }
});
