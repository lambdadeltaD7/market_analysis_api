const gifs = ['200.gif', '201.gif', 'AMA4d7I.gif',
     'anime-anime-girl.gif', 'giphy.gif', 'shigure-ui.gif'];

const one_card = document.getElementById('users-summary');
const main_clr = one_card.style.borderColor;

const loc_users_a = document.getElementById('loc_users');
const loc_things_a = document.getElementById('loc_things');
const loc_sales_a = document.getElementById('loc_sales');



// todo: make this more compact
loc_things_a.addEventListener('mousemove', () => {
    loc_things_a.classList.remove('other_page');
    loc_things_a.classList.add('current_page');
});

loc_things_a.addEventListener('mouseleave', () => {
    loc_things_a.classList.remove('current_page');
    loc_things_a.classList.add('other_page');
});

loc_users_a.addEventListener('mousemove', () => {
    loc_users_a.classList.remove('other_page');
    loc_users_a.classList.add('current_page');
});

loc_users_a.addEventListener('mouseleave', () => {
    loc_users_a.classList.remove('current_page');
    loc_users_a.classList.add('other_page');
});

loc_sales_a.addEventListener('mousemove', () => {
    loc_sales_a.classList.remove('other_page');
    loc_sales_a.classList.add('current_page');
});

loc_sales_a.addEventListener('mouseleave', () => {
    loc_sales_a.classList.remove('current_page');
    loc_sales_a.classList.add('other_page');
});



function pickRandomGif() {
    const idx = Math.floor(Math.random() * gifs.length);
    document.getElementById('random-gif').src = '../img/' + gifs[idx];
}

function kvTable(rows) {
    let html = '<table>';
    rows.forEach(([k, v]) => {
        html += '<tr><th>' + k + '</th><td>' + (v !== null && v !== undefined ? v : '—') + '</td></tr>';
    });
    return html + '</table>';
}

function arrayTable(arr, headers) {
    if (!arr || arr.length === 0) return '<p><em>empty</em></p>';
    let html = '<table><tr>';
    headers.forEach(h => { html += '<th>' + h + '</th>'; });
    html += '</tr>';
    arr.forEach(row => {
        html += '<tr>';
        headers.forEach(h => { html += '<td>' + (row[h] !== undefined ? row[h] : '—') + '</td>'; });
        html += '</tr>';
    });
    return html + '</table>';
}

function renderUsers(d) {
    let html = '<h3>Main</h3>';
    html += kvTable([
        ['cnt_users', d.cnt_users],
        ['cnt_premium_users', d.cnt_premium_users],
        ['frac_premium_users', d.frac_premium_users]
    ]);
    if (d['quartiles(age)']) {
        const q = d['quartiles(age)'];
        html += '<h3>Quartiles (age)</h3>';
        html += kvTable([
            ['25%', q['0.25']],
            ['50%', q['0.5']],
            ['75%', q['0.75']]
        ]);
    }
    return html;
}

function renderThings(d) {
    let html = '<h3 style="font-size: 30px;">Total</h3>';
    html += kvTable([['cnt_things', d.cnt_things]]);
    const cats = Object.keys(d).filter(k => k !== 'cnt_things');
    cats.forEach(cat => {
        const c = d[cat];
        html += '<h3>' + cat + '</h3>';
        html += '<p>Stats</p>';
        html += kvTable([
            ['cnt_things', c.cnt_things],
            ['frac_things', c.frac_things]
        ]);
        if (c.price_quartiles) {
            const q = c.price_quartiles;
            html += '<p>Quartiles (price)</p>';
            html += kvTable([
                ['25%', q['0.25']],
                ['50%', q['0.5']],
                ['75%', q['0.75']]
            ]);
        }
    });
    return html;
}

function renderSales(d) {
    let html = '<h3>Overview</h3>';
    html += kvTable([
        ['cnt_sales', d.cnt_sales],
        ['avg_sales_per_user', d.avg_sales_per_user],
        ['avg_sales_per_day', d.avg_sales_per_day],
        ['avg_sales_per_hour', d.avg_sales_per_hour],
        ['most_active_hour', d.most_active_hour],
        ['most_active_date', d.most_active_date],
        ['earliest_sale_time', d.earliest_sale_time],
        ['latest_sale_time', d.latest_sale_time]
    ]);
    html += '<h3>Most Active Users</h3>';
    html += arrayTable(d.most_active_users, ['user_id', 'cnt_sales']);
    html += '<h3>Most Popular Things</h3>';
    html += arrayTable(d.most_popular_things, ['thing_id', 'cnt_sales']);
    if (d.cnt_per_category) {
        html += '<h3>Category Breakdown</h3>';
        const rows = Object.entries(d.cnt_per_category).map(([cat, cnt]) => [
            cat, cnt, d.frac_per_category ? d.frac_per_category[cat] : '—'
        ]);
        let t = '<table><tr><th>category</th><th>count</th><th>fraction</th></tr>';
        rows.forEach(([cat, cnt, frac]) => {
            t += '<tr><td>' + cat + '</td><td>' + cnt + '</td><td>' + frac + '</td></tr>';
        });
        html += t + '</table>';
    }
    if (d.cnt_payment_type) {
        html += '<h3>Payment Type</h3>';
        const rows = Object.entries(d.cnt_payment_type).map(([pt, cnt]) => [
            pt, cnt, d.frac_payment_type ? d.frac_payment_type[pt] : '—'
        ]);
        let t = '<table><tr><th>type</th><th>count</th><th>fraction</th></tr>';
        rows.forEach(([pt, cnt, frac]) => {
            t += '<tr><td>' + pt + '</td><td>' + cnt + '</td><td>' + frac + '</td></tr>';
        });
        html += t + '</table>';
    }
    return html;
}

const renderers = {
    'users-summary': { url: '/api/v1/users/summary', fn: renderUsers },
    'things-summary': { url: '/api/v1/things/summary', fn: renderThings },
    'sales-summary':  { url: '/api/v1/sales/summary',  fn: renderSales }
};

function loadSummary(cardId) {
    const { url, fn } = renderers[cardId];
    const card = document.getElementById(cardId);

    const h2 = card.querySelector('h2');
    while (h2.nextSibling) {
        h2.nextSibling.remove();
    }

    const placeholder = document.createElement('p');
    placeholder.textContent = 'Loading...';
    card.appendChild(placeholder);

    
    
    fetch(url)
        .then(async (r) => {
            if (!r.ok) {
                const err_body = await r.json().catch(() => ({}));
                const err = new Error(err_body.detail || 'Unknown server error'); 
                err.status = r.status;
                throw err;
            } 
            return r.json();     
        })
        .then(data => {
            placeholder.remove();
            card.insertAdjacentHTML('beforeend', fn(data));
            card.style.borderColor = "rgb(20, 235, 16)";
            setTimeout(()=>{card.style.borderColor = main_clr;}, 3000);
        })
        .catch( (err) => {
            setTimeout(()=>{card.style.borderColor = main_clr;}, 3000);
            placeholder.textContent = `Failed to load: ${err.status}(${err.message})`;
            card.style.borderColor = "rgb(241, 63, 63)";
        });
}

function loadAllSummaries() {
    Object.keys(renderers).forEach(loadSummary);
}

document.addEventListener('DOMContentLoaded', () => {
    pickRandomGif();
    loadAllSummaries();
});

document.getElementById('random-gif').addEventListener('click', pickRandomGif);

setInterval(pickRandomGif, 10000);