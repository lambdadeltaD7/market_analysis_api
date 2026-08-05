import {
    handleErr,
    higlightInputErr,
    showErr,
    showToast
} from "./utils.js"



const base_url = "/api/v1";

const n_clusters = document.getElementById('n_clusters');
const cluster_btn = document.getElementById('cluster_btn');
const centroids_clean_btn = document.getElementById('centroids_clean_btn');
const centroids_reload_btn = document.getElementById('centroids_reload_btn');
const centroids_table_body = document.getElementById('centroids_table_body');

const users_count = document.getElementById('users_count');
const users_offset = document.getElementById('users_offset');
const cluster_ix = document.getElementById('cluster_ix');
const cluster_load_btn = document.getElementById('cluster_load_btn');
const cluster_users_clean_btn = document.getElementById('cluster_users_clean_btn');
const cluster_size_box = document.getElementById('cluster_size_box');
const cluster_users_table_body = document.getElementById('cluster_users_table_body');


// so user can only input 0-9 inside numeric fields
for(const num_input_field of [n_clusters, cluster_ix]){
    num_input_field.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace('/\D/g',"");
    });
}


async function load_centroids(){
    const result = await fetch(base_url + "/users/clusters/centroids");
    
    if(!result.ok){
        await handleErr(result);
    }

    const data = await result.json();

    return data;
}

async function render_centroids(centroids){
    centroids_table_body.innerHTML='';

    for(const c of centroids){
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td>${c.cluster}</td>
            <td>${c.cluster_size}</td>
            <td>${c.cnt_sales}</td>
            <td>${c.avg_price}</td>
            <td>${c.med_price}</td>
            <td>${c.user_age}</td>
            <td class="${c.bought_premium ? 'premium' : 'no-premium'}">${c.bought_premium}</td>
            <td>${c.mode_category}</td>
        `;

        centroids_table_body.appendChild(tr);
    }
}

centroids_reload_btn.addEventListener('click', async () => {
    try{
        const centroids = await load_centroids();
        await render_centroids(centroids);
    }
    catch(err){
        const txt = `Failed to reload centroids: ${err.status}(${err.message})`;
        showErr(txt);
        console.error(txt);
    }
});

cluster_btn.addEventListener('click', async () => {
    try{
        const params = new URLSearchParams({n_clusters: Number(n_clusters.value)});

        const result = await fetch(
            base_url + `/users/cluster_users?${params}`,
            {method: 'POST'}
        );

        if(!result.ok){
            await handleErr(result);
        }

        const centroids = await result.json();

        await render_centroids(centroids);

        showToast(`clustered users into ${centroids.length} clusters`)
    }
    catch(err){
        const txt = `Failed to cluster users: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('n_clusters');
    }
});

centroids_clean_btn.addEventListener('click', () => {
    centroids_table_body.innerHTML = '';
});

cluster_users_clean_btn.addEventListener('click', () => {
    cluster_users_table_body.innerHTML = '';
});

cluster_load_btn.addEventListener('click', async () => {
    try{
        const cix = Number(cluster_ix.value);

        const params = new URLSearchParams({
            "count": Number(users_count.value),
            "offset": Number(users_offset.value)
        });

        const result = await fetch(
            base_url + `/users/clusters/${cix}?${params}`,
        );

        if(!result.ok){
            await handleErr(result,
                {
                    "count" : "users_count",
                    "offset" : "users_offset"
                }
            );
        }

        const data = await result.json();

        cluster_users_table_body.innerHTML='';

        for(const u of data.users){
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${u.user_id}</td>
                <td>${u.cnt_sales}</td>
                <td>${u.avg_price}</td>
                <td>${u.med_price}</td>
                <td>${u.user_age}</td>
                <td class="${u.bought_premium ? 'premium' : 'no-premium'}">${u.bought_premium}</td>
                <td>${u.mode_category}</td>
            `;

            cluster_users_table_body.appendChild(tr);
        }


    }
    catch(err){
        const txt = `Failed to load cluster: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
    }
});
