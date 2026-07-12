// DOM elements
const leadsBody = document.getElementById('leads-body');
const totalLeads = document.getElementById('total-leads');
const scanBtn = document.getElementById('scan-btn');
const keywordInput = document.getElementById('keyword-input');
const statusArea = document.getElementById('status-area');
const statusText = document.getElementById('status-text');

// Fetch leads
async function fetchLeads() {
    try {
        const response = await fetch('/api/leads');
        const data = await response.json();
        
        if (data.status === 'success' || data.data) {
            const leads = data.data || data;
            totalLeads.textContent = leads.length;
            
            leadsBody.innerHTML = leads.map(lead => `
                <tr>
                    <td>${lead.id}</td>
                    <td>${lead.company_name || '-'}</td>
                    <td>${lead.contact_email || '-'}</td>
                    <td>${lead.website_url ? `<a href="${lead.website_url}" target="_blank">${lead.website_url}</a>` : '-'}</td>
                    <td>${lead.scraped_at ? new Date(lead.scraped_at).toLocaleString() : '-'}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Scan leads
async function scanLeads() {
    const keyword = keywordInput.value.trim();
    if (!keyword) return;

    scanBtn.disabled = true;
    statusArea.classList.remove('hidden');

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ keyword })
        });
        
        const data = await response.json();
        
        if (data.status === 'success' || response.ok) {
            const savedCount = data.saved_count !== undefined ? data.saved_count : (data.leads ? data.leads.length : 0);
            alert(`Scan complete. Saved ${savedCount} leads.`);
            keywordInput.value = '';
            fetchLeads();
        } else {
            alert('Scan failed: ' + (data.message || data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Scan error:', error);
        alert('An error occurred during scan.');
    } finally {
        scanBtn.disabled = false;
        statusArea.classList.add('hidden');
    }
}

// Event listeners
scanBtn.addEventListener('click', scanLeads);
keywordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') scanLeads();
});

// Init
fetchLeads();